#!/usr/bin/env python3
"""Statically analyze an uninstalled pacman package archive into inventory JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from tools.deep_inventory import (
        InventoryError, classify_path, parse_ar, parse_cmake, parse_pe,
        parse_pkg_config, sha256,
    )
except ModuleNotFoundError:  # Running this file directly adds tools/ to sys.path.
    from deep_inventory import (  # type: ignore[no-redef]
        InventoryError, classify_path, parse_ar, parse_cmake, parse_pe,
        parse_pkg_config, sha256,
    )


class PackageArchiveError(Exception):
    """Raised when an archive cannot be safely analyzed."""


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> int:
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    return len(records)


def safe_member_path(member: tarfile.TarInfo) -> str:
    value = member.name.replace("\\", "/")
    path = PurePosixPath(value)
    if value.startswith("/") or ".." in path.parts or not value:
        raise PackageArchiveError(f"unsafe archive member: {member.name}")
    return "/" + path.as_posix()


def safe_external_member_path(value: str) -> None:
    """Reject names that would be unsafe for the platform tar extractor."""
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if normalized.startswith("/") or ".." in path.parts or not normalized:
        raise PackageArchiveError(f"unsafe archive member: {value}")


def unpack_zstandard_archive(archive: Path, extracted: Path) -> None:
    """Safely expand a `.tar.zst` using the host tar implementation."""
    listing = subprocess.run(
        ["tar", "-tf", str(archive)], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if listing.returncode:
        raise PackageArchiveError(f"cannot list Zstandard package archive: {listing.stderr.strip()}")
    for name in listing.stdout.splitlines():
        safe_external_member_path(name)
    result = subprocess.run(
        ["tar", "-xf", str(archive), "-C", str(extracted)], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise PackageArchiveError(f"cannot extract Zstandard package archive: {result.stderr.strip()}")


def analyze(archive: Path, package: str, output: Path, source_archive: Path | None = None) -> dict[str, Any]:
    if not archive.is_file():
        raise PackageArchiveError(f"archive is missing: {archive}")
    if not package or any(char.isspace() for char in package):
        raise PackageArchiveError("package must be a non-empty pacman package name")
    source_archive = source_archive or archive
    if archive.suffix == ".zst":
        with tempfile.TemporaryDirectory() as directory:
            extracted = Path(directory) / "extracted"
            extracted.mkdir()
            unpack_zstandard_archive(archive, extracted)
            bundle = Path(directory) / "payload.tar"
            with tarfile.open(bundle, "w") as target:
                for path in extracted.rglob("*"):
                    if path.is_file() and path.resolve().is_relative_to(extracted.resolve()):
                        target.add(path, arcname=path.relative_to(extracted).as_posix())
            return analyze(bundle, package, output, source_archive)
    output.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any]] = []
    imports: list[dict[str, Any]] = []
    exports: list[dict[str, Any]] = []
    members: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    try:
        with tarfile.open(archive, "r:*") as bundle, tempfile.TemporaryDirectory() as scratch:
            scratch_path = Path(scratch)
            for index, item in enumerate(sorted(bundle.getmembers(), key=lambda value: value.name)):
                if not item.isfile():
                    continue
                path = safe_member_path(item)
                kind = classify_path(path)
                stream = bundle.extractfile(item)
                if stream is None:
                    raise PackageArchiveError(f"cannot read archive member: {item.name}")
                payload = stream.read()
                record: dict[str, Any] = {"package": package, "path": path, "kind": kind, "present": True, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "archive": source_archive.name}
                temporary = scratch_path / f"member-{index}{Path(path).suffix}"
                temporary.write_bytes(payload)
                try:
                    if kind in {"executable", "dll"}:
                        pe = parse_pe(temporary)
                        record["pe"] = {key: value for key, value in pe.items() if key not in {"imports", "exports"}}
                        imports.extend({"package": package, "path": path, **value} for value in pe["imports"])
                        exports.extend({"package": package, "path": path, **value} for value in pe["exports"])
                    elif kind in {"static-library", "import-library"}:
                        members.extend({"package": package, "path": path, **value} for value in parse_ar(temporary))
                    elif kind == "pkg-config-module":
                        metadata.append({"package": package, "path": path, "format": "pkg-config", **parse_pkg_config(temporary)})
                    elif kind == "cmake-module":
                        metadata.append({"package": package, "path": path, "format": "cmake", **parse_cmake(temporary)})
                except (InventoryError, OSError, ValueError) as exc:
                    warnings.append({"path": path, "message": str(exc)})
                artifacts.append(record)
    except (OSError, tarfile.TarError) as exc:
        raise PackageArchiveError(f"cannot read package archive: {exc}") from exc
    files = {
        "artifacts.jsonl": artifacts, "pe-imports.jsonl": imports,
        "pe-exports.jsonl": exports, "archive-members.jsonl": members,
        "development-metadata.jsonl": metadata, "recipes.jsonl": [],
        "warnings.jsonl": warnings,
    }
    counts = {name: write_jsonl(output / name, values) for name, values in files.items()}
    manifest = {
        "schema_version": "1.0.0", "collector_version": "0.4.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collector": "tools/analyze_package_archive.py", "scope": "package-archive",
        "package": package, "source_archive": {"name": source_archive.name, "sha256": sha256(source_archive)},
        "counts": counts, "sha256": {name: sha256(output / name) for name in files},
    }
    (output / "inventory-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = analyze(args.archive.resolve(), args.package, args.output.resolve())
    except (PackageArchiveError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Analyzed " + ", ".join(f"{key}={value}" for key, value in manifest["counts"].items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
