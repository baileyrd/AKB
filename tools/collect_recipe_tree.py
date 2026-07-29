#!/usr/bin/env python3
"""Collect declarative PKGBUILD evidence from a checked-out recipe tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.deep_inventory import InventoryError, parse_pkgbuild, sha256
except ModuleNotFoundError:  # Permit direct execution from tools/.
    from deep_inventory import InventoryError, parse_pkgbuild, sha256  # type: ignore[no-redef]


FILES = (
    "artifacts.jsonl", "pe-imports.jsonl", "pe-exports.jsonl",
    "archive-members.jsonl", "development-metadata.jsonl", "recipes.jsonl",
    "warnings.jsonl",
)


class RecipeTreeError(Exception):
    """Raised when a recipe tree cannot be collected safely."""


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> int:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    return len(records)


def revision(root: Path) -> str:
    """Return a checked-out Git revision, or an empty value for a plain tree."""
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def collect(recipe_root: Path, output: Path) -> dict[str, Any]:
    if not recipe_root.is_dir():
        raise RecipeTreeError(f"recipe root is missing: {recipe_root}")
    root = recipe_root.resolve()
    recipes: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    for path in sorted(recipe_root.rglob("PKGBUILD")):
        if not path.is_file():
            continue
        try:
            resolved = path.resolve()
            relative = resolved.relative_to(root).as_posix()
        except ValueError:
            warnings.append({"path": str(path), "message": "recipe path escapes source root"})
            continue
        try:
            recipes.append({
                "path": relative,
                "recipe_sha256": sha256(resolved),
                **parse_pkgbuild(resolved),
            })
        except (InventoryError, OSError, ValueError) as exc:
            warnings.append({"path": relative, "message": str(exc)})
    if not recipes:
        raise RecipeTreeError(f"no PKGBUILD files found in {recipe_root}")
    output.mkdir(parents=True, exist_ok=True)
    records: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    records["recipes.jsonl"] = recipes
    records["warnings.jsonl"] = warnings
    counts = {name: write_jsonl(output / name, values) for name, values in records.items()}
    manifest = {
        "schema_version": "1.0.0",
        "collector_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collector": "tools/collect_recipe_tree.py",
        "scope": "recipe-source-tree",
        "source_revision": revision(root),
        "recipe_count": len(recipes),
        "counts": counts,
        "sha256": {name: sha256(output / name) for name in FILES},
    }
    (output / "inventory-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipe_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = collect(args.recipe_root.resolve(), args.output.resolve())
    except (RecipeTreeError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Collected recipes={manifest['recipe_count']}, warnings={manifest['counts']['warnings.jsonl']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
