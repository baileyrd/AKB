#!/usr/bin/env python3
"""Safely analyze and accumulate a directory of uninstalled pacman archives."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from tools.analyze_package_archive import PackageArchiveError, analyze
from tools.import_deep_inventory import InventoryImportError, import_inventory


def package_archives(directory: Path) -> list[Path]:
    """Return supported archive files in deterministic order."""
    return sorted(
        path for path in directory.rglob("*.pkg.tar*")
        if path.is_file() and path.name.endswith((".pkg.tar", ".pkg.tar.zst", ".pkg.tar.xz", ".pkg.tar.gz"))
    )


def import_archives(directory: Path) -> list[dict[str, object]]:
    """Analyze each archive independently and retain each verified snapshot."""
    archives = package_archives(directory)
    if not archives:
        raise PackageArchiveError(f"no supported package archives in {directory}")
    results: list[dict[str, object]] = []
    for archive in archives:
        with tempfile.TemporaryDirectory(prefix="akb-package-") as temporary:
            manifest = analyze(archive, None, Path(temporary))
            result = import_inventory(Path(temporary), accumulate=True)
        results.append({"archive": archive.name, "package": manifest["package"], **result})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_directory", type=Path)
    args = parser.parse_args()
    try:
        results = import_archives(args.archive_directory.resolve())
    except (PackageArchiveError, InventoryImportError, OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    for result in results:
        print("Imported " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
