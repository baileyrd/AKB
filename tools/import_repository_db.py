#!/usr/bin/env python3
"""Convert a pacman repository database archive into catalog importer input."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
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
                version = fields.get("VERSION", [""])[0]
                if not name or not version or name in seen:
                    raise RepositoryDatabaseError(f"invalid or duplicate package record: {member.name}")
                seen.add(name)
                values = lambda key: fields.get(key, [])
                package = {
                    "repository": repository,
                    "name": name,
                    "version": version,
                    "installed": "False",
                    "installed_version": "",
                    "architecture": values("ARCH")[0] if values("ARCH") else "",
                    "classification": classify(repository, name),
                    "description": values("DESC")[0] if values("DESC") else "",
                    "groups": ";".join(values("GROUPS")),
                    "licenses": ";".join(values("LICENSE")),
                    "project_url": values("URL")[0] if values("URL") else "",
                    "required_dependencies": ";".join(values("DEPENDS")),
                    "optional_dependencies": ";".join(values("OPTDEPENDS")),
                    "provides": ";".join(values("PROVIDES")),
                    "conflicts": ";".join(values("CONFLICTS")),
                    "replaces": ";".join(values("REPLACES")),
                    "download_size": values("CSIZE")[0] if values("CSIZE") else "",
                    "installed_size": values("ISIZE")[0] if values("ISIZE") else "",
                    "build_date": values("BUILDDATE")[0] if values("BUILDDATE") else "",
                }
                packages.append(package)
                for relation, field in (("runtime-depends-on", "DEPENDS"), ("optional-depends-on", "OPTDEPENDS")):
                    for dependency in values(field):
                        target, constraint = dependency_name(dependency.split(":", 1)[0])
                        if target:
                            edges.append({"source_repository": repository, "source_package": name, "relationship": relation, "target_package": target, "constraint": constraint})
    except (OSError, tarfile.TarError, UnicodeDecodeError) as exc:
        raise RepositoryDatabaseError(f"cannot read repository database: {exc}") from exc
    return sorted(packages, key=lambda item: item["name"]), sorted(edges, key=lambda item: (item["source_package"], item["relationship"], item["target_package"]))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def convert(archive: Path, repository: str, output: Path) -> dict[str, int]:
    if not archive.is_file():
        raise RepositoryDatabaseError(f"archive is missing: {archive}")
    if not repository or repository != repository.lower() or not repository.replace("-", "").isalnum():
        raise RepositoryDatabaseError("repository must be a lowercase pacman repository name")
    packages, edges = archive_records(archive, repository)
    output.mkdir(parents=True, exist_ok=True)
    package_path, edge_path = output / "all-packages.csv", output / "dependency-edges.csv"
    package_fields = list(packages[0])
    edge_fields = ["source_repository", "source_package", "relationship", "target_package", "constraint"]
    write_csv(package_path, packages, package_fields)
    write_csv(edge_path, edges, edge_fields)
    observed_at = datetime.fromtimestamp(archive.stat().st_mtime, timezone.utc).isoformat().replace("+00:00", "Z")
    manifest: dict[str, Any] = {
        "schema_version": "1.0.0", "generated_at": observed_at,
        "collector": "tools/import_repository_db.py", "pacman_version": "",
        "repositories": [repository], "package_count": len(packages),
        "installed_count": 0, "dependency_edge_count": len(edges),
        "source_archive": {"name": archive.name, "sha256": sha256(archive)},
        "sha256": {"all-packages.csv": sha256(package_path), "dependency-edges.csv": sha256(edge_path)},
    }
    (output / "catalog-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"packages": len(packages), "edges": len(edges)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = convert(args.archive.resolve(), args.repository, args.output.resolve())
    except (RepositoryDatabaseError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Converted " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
