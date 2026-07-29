#!/usr/bin/env python3
"""Convert pacman `.files` databases into deep-inventory collector input."""

from __future__ import annotations

import argparse
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from tools.deep_inventory import classify_path
from tools.import_repository_db import RepositoryDatabaseError, parse_desc, sha256


STREAMS = (
    "artifacts.jsonl", "pe-imports.jsonl", "pe-exports.jsonl",
    "archive-members.jsonl", "development-metadata.jsonl", "recipes.jsonl",
    "warnings.jsonl",
)


def safe_package_path(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if not value or value.startswith("/") or ".." in path.parts:
        raise RepositoryDatabaseError(f"unsafe repository file path: {value!r}")
    return "/" + path.as_posix()


def records(archive: Path) -> list[dict[str, str]]:
    """Extract package-owned paths from a `.files` archive without unpacking it."""
    artifacts: list[dict[str, str]] = []
    try:
        with tarfile.open(archive, "r:*") as bundle:
            members = {member.name: member for member in bundle.getmembers() if member.isfile()}
            descriptions = sorted(name for name in members if name.endswith("/desc"))
            if not descriptions:
                raise RepositoryDatabaseError("archive has no package desc records")
            for description_name in descriptions:
                prefix = description_name.removesuffix("/desc")
                files_member = members.get(f"{prefix}/files")
                if files_member is None:
                    continue
                description = bundle.extractfile(members[description_name])
                file_list = bundle.extractfile(files_member)
                if description is None or file_list is None:
                    raise RepositoryDatabaseError(f"cannot read package file records: {prefix}")
                package = parse_desc(description.read()).get("NAME", [""])[0]
                if not package:
                    raise RepositoryDatabaseError(f"package description lacks NAME: {prefix}")
                values = parse_desc(file_list.read()).get("FILES", [])
                for value in values:
                    if value.endswith("/"):
                        continue
                    path = safe_package_path(value)
                    artifacts.append({"package": package, "path": path, "kind": classify_path(path), "present": False})
    except tarfile.ReadError as exc:
        raise RepositoryDatabaseError("cannot read repository file database; provide a tar-readable .files archive") from exc
    except (OSError, tarfile.TarError, UnicodeDecodeError) as exc:
        raise RepositoryDatabaseError(f"cannot read repository file database: {exc}") from exc
    if not artifacts:
        raise RepositoryDatabaseError("archive has no package file records")
    return sorted(artifacts, key=lambda item: (item["package"], item["path"]))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def convert_many(archives: list[Path], repositories: list[str], output: Path) -> dict[str, int]:
    if not archives or len(archives) != len(repositories):
        raise RepositoryDatabaseError("each file database requires exactly one repository")
    artifacts: list[dict[str, str]] = []
    sources: list[dict[str, str]] = []
    for archive, repository in zip(archives, repositories):
        if not archive.is_file():
            raise RepositoryDatabaseError(f"archive is missing: {archive}")
        if not repository or repository != repository.lower() or not repository.replace("-", "").isalnum():
            raise RepositoryDatabaseError("repository must be a lowercase pacman repository name")
        artifacts.extend(records(archive))
        sources.append({"repository": repository, "name": archive.name, "sha256": sha256(archive)})
    output.mkdir(parents=True, exist_ok=True)
    rows: dict[str, list[dict[str, Any]]] = {stream: [] for stream in STREAMS}
    rows["artifacts.jsonl"] = artifacts
    for stream, values in rows.items():
        write_jsonl(output / stream, values)
    manifest = {
        "schema_version": "1.0.0", "collector_version": "0.5.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collector": "tools/import_repository_file_db.py", "scope": "repository-file-database",
        "repositories": sorted(repositories), "source_archives": sources,
        "counts": {stream: len(values) for stream, values in rows.items()},
        "sha256": {stream: sha256(output / stream) for stream in STREAMS},
    }
    (output / "inventory-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"artifacts": len(artifacts), "packages": len({row["package"] for row in artifacts})}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, nargs="+")
    parser.add_argument("--repository", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = convert_many([path.resolve() for path in args.archive], args.repository, args.output.resolve())
    except (RepositoryDatabaseError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print("Converted " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
