#!/usr/bin/env python3
"""Convert a pacman repository database archive into catalog importer input."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


class RepositoryDatabaseError(Exception):
    """Raised when a repository database archive is unsafe or malformed."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(repository: str, name: str) -> str:
    if name.endswith("-toolchain"):
        return "toolchain-group"
    if name.startswith(("mingw-w64-", "mingw-w64-clang-")):
        return "mingw-package"
    if name in {"filesystem", "bash", "pacman"} or name.startswith("msys2-runtime"):
        return "system-package"
    return "msys-package" if repository == "msys" else "native-package"


def parse_desc(data: bytes) -> dict[str, list[str]]:
    lines = data.decode("utf-8").splitlines()
    fields: dict[str, list[str]] = {}
    index = 0
    while index < len(lines):
        marker = lines[index]
        if not marker:
            index += 1
            continue
        if not (marker.startswith("%") and marker.endswith("%")):
            raise RepositoryDatabaseError(f"unexpected desc line: {marker!r}")
        key = marker[1:-1]
        index += 1
        values: list[str] = []
        while index < len(lines) and lines[index]:
            values.append(lines[index])
            index += 1
        fields[key] = values
        index += 1
    return fields


def dependency_name(value: str) -> tuple[str, str]:
    for index, char in enumerate(value):
        if char in "<=>":
            return value[:index], value[index:]
    return value, ""


def package_rows(fields: dict[str, list[str]], repository: str) -> tuple[dict[str, str], list[dict[str, str]]]:
    name = fields.get("NAME", [""])[0]
    version = fields.get("VERSION", [""])[0]
    if not name or not version:
        raise RepositoryDatabaseError("package description lacks NAME or VERSION")
    values = lambda key: fields.get(key, [])
    package = {
        "repository": repository, "name": name, "version": version, "installed": "False", "installed_version": "",
        "architecture": values("ARCH")[0] if values("ARCH") else "", "classification": classify(repository, name),
        "description": values("DESC")[0] if values("DESC") else "", "groups": ";".join(values("GROUPS")),
        "licenses": ";".join(values("LICENSE")), "project_url": values("URL")[0] if values("URL") else "",
        "required_dependencies": ";".join(values("DEPENDS")), "optional_dependencies": ";".join(values("OPTDEPENDS")),
        "provides": ";".join(values("PROVIDES")), "conflicts": ";".join(values("CONFLICTS")),
        "replaces": ";".join(values("REPLACES")), "download_size": values("CSIZE")[0] if values("CSIZE") else "",
        "installed_size": values("ISIZE")[0] if values("ISIZE") else "", "build_date": values("BUILDDATE")[0] if values("BUILDDATE") else "",
    }
    edges: list[dict[str, str]] = []
    for relation, field in (("runtime-depends-on", "DEPENDS"), ("optional-depends-on", "OPTDEPENDS")):
        for dependency in values(field):
            target, constraint = dependency_name(dependency.split(":", 1)[0])
            if target:
                edges.append({"source_repository": repository, "source_package": name, "relationship": relation, "target_package": target, "constraint": constraint})
    return package, edges


def archive_records_with_bsdtar(archive: Path, repository: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Use Windows bsdtar only for Zstandard archives unsupported by tarfile."""
    listed = subprocess.run(["tar", "-tf", str(archive)], text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if listed.returncode:
        raise RepositoryDatabaseError(f"cannot list repository database: {listed.stderr.strip()}")
    names = [line for line in listed.stdout.splitlines() if line]
    if any(name.startswith("/") or ".." in PurePosixPath(name).parts for name in names):
        raise RepositoryDatabaseError("archive contains an unsafe member path")
    with tempfile.TemporaryDirectory() as directory:
        destination = Path(directory)
        extracted = subprocess.run(["tar", "-xf", str(archive), "-C", str(destination)], text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if extracted.returncode:
            raise RepositoryDatabaseError(f"cannot extract repository descriptions: {extracted.stderr.strip()}")
        packages: list[dict[str, str]] = []
        edges: list[dict[str, str]] = []
        for path in sorted(destination.rglob("desc")):
            if not path.is_file() or path.resolve().is_relative_to(destination.resolve()) is False:
                continue
            package, package_edges = package_rows(parse_desc(path.read_bytes()), repository)
            packages.append(package)
            edges.extend(package_edges)
    if not packages:
        raise RepositoryDatabaseError("archive has no package desc records")
    names = [package["name"] for package in packages]
    if len(names) != len(set(names)):
        raise RepositoryDatabaseError("archive contains duplicate package records")
    return sorted(packages, key=lambda item: item["name"]), sorted(edges, key=lambda item: (item["source_package"], item["relationship"], item["target_package"]))


def archive_records(archive: Path, repository: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    packages: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    seen: set[str] = set()
    try:
        with tarfile.open(archive, "r:*") as bundle:
            members = sorted(
                (member for member in bundle.getmembers() if member.isfile() and member.name.endswith("/desc")),
                key=lambda member: member.name,
            )
            if not members:
                raise RepositoryDatabaseError("archive has no package desc records")
            for member in members:
                if member.name.startswith("/") or ".." in Path(member.name).parts:
                    raise RepositoryDatabaseError(f"unsafe archive member: {member.name}")
                stream = bundle.extractfile(member)
                if stream is None:
                    raise RepositoryDatabaseError(f"cannot read archive member: {member.name}")
                fields = parse_desc(stream.read())
                name = fields.get("NAME", [""])[0]
                if not name or name in seen:
                    raise RepositoryDatabaseError(f"invalid or duplicate package record: {member.name}")
                seen.add(name)
                package, package_edges = package_rows(fields, repository)
                packages.append(package)
                edges.extend(package_edges)
    except tarfile.ReadError:
        return archive_records_with_bsdtar(archive, repository)
    except (OSError, tarfile.TarError, UnicodeDecodeError) as exc:
        raise RepositoryDatabaseError(f"cannot read repository database: {exc}") from exc
    return sorted(packages, key=lambda item: item["name"]), sorted(edges, key=lambda item: (item["source_package"], item["relationship"], item["target_package"]))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def convert_many(
    archives: list[Path], repositories: list[str], output: Path
) -> dict[str, int]:
    if not archives or len(archives) != len(repositories):
        raise RepositoryDatabaseError("each archive requires exactly one repository")
    packages: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    source_archives: list[dict[str, str]] = []
    for archive, repository in zip(archives, repositories):
        if not archive.is_file():
            raise RepositoryDatabaseError(f"archive is missing: {archive}")
        if not repository or repository != repository.lower() or not repository.replace("-", "").isalnum():
            raise RepositoryDatabaseError("repository must be a lowercase pacman repository name")
        current_packages, current_edges = archive_records(archive, repository)
        packages.extend(current_packages)
        edges.extend(current_edges)
        source_archives.append({"repository": repository, "name": archive.name, "sha256": sha256(archive)})
    output.mkdir(parents=True, exist_ok=True)
    package_path, edge_path = output / "all-packages.csv", output / "dependency-edges.csv"
    package_fields = list(packages[0])
    edge_fields = ["source_repository", "source_package", "relationship", "target_package", "constraint"]
    write_csv(package_path, packages, package_fields)
    write_csv(edge_path, edges, edge_fields)
    observed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    manifest: dict[str, Any] = {
        "schema_version": "1.0.0", "generated_at": observed_at,
        "collector": "tools/import_repository_db.py", "pacman_version": "",
        "repositories": sorted(repositories), "package_count": len(packages),
        "installed_count": 0, "dependency_edge_count": len(edges),
        "source_archives": source_archives,
        "sha256": {"all-packages.csv": sha256(package_path), "dependency-edges.csv": sha256(edge_path)},
    }
    if len(source_archives) == 1:
        manifest["source_archive"] = source_archives[0]
    (output / "catalog-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"packages": len(packages), "edges": len(edges)}


def convert(archive: Path, repository: str, output: Path) -> dict[str, int]:
    """Convert one archive; retained for API and command-line compatibility."""
    return convert_many([archive], [repository], output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, nargs="+")
    parser.add_argument("--repository", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = convert_many(
            [archive.resolve() for archive in args.archive],
            args.repository,
            args.output.resolve(),
        )
    except (RepositoryDatabaseError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Converted " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
