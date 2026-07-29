#!/usr/bin/env python3
"""Project a verified local recipe-source collection without loading artifact inventory."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    from tools.import_deep_inventory import (
        InventoryImportError, build_projection, merge_projection, sha_manifest, verify_input,
    )
except ModuleNotFoundError:  # Permit direct execution from tools/.
    from import_deep_inventory import (  # type: ignore[no-redef]
        InventoryImportError, build_projection, merge_projection, sha_manifest, verify_input,
    )

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "model" / "recipes" / "current.json"
SNAPSHOTS = ROOT / "evidence" / "recipe-snapshots"


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def import_recipe_tree(source: Path, accumulate: bool = True) -> dict[str, int | str]:
    manifest, records = verify_input(source)
    if manifest.get("scope") != "recipe-source-tree":
        raise InventoryImportError("recipe importer requires recipe-source-tree scope")
    snapshot_id = manifest["generated_at"].replace(":", "").replace("-", "").replace("+00:00", "Z")[:16] + "-" + sha_manifest(manifest)[:12]
    projection, unresolved = build_projection(manifest, records, snapshot_id)
    projection["snapshot"]["description"] = "Generated MSYS2 recipe-source projection."
    projection["evidence"][0]["notes"] = "Collected by tools/collect_recipe_tree.py."
    if accumulate and CURRENT.is_file():
        projection = merge_projection(json.loads(CURRENT.read_text(encoding="utf-8")), projection)
    destination = SNAPSHOTS / snapshot_id
    if destination.exists():
        raise InventoryImportError(f"recipe snapshot already exists: {snapshot_id}")
    destination.mkdir(parents=True)
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, destination / item.name)
    write(destination / "projection.json", projection)
    write(destination / "unresolved.json", unresolved)
    write(CURRENT, projection)
    return {"snapshot": snapshot_id, "recipes": len(records["recipes.jsonl"]), "unresolved": len(unresolved)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    try:
        print("Imported " + ", ".join(f"{k}={v}" for k, v in import_recipe_tree(args.source.resolve(), not args.replace).items()))
    except (InventoryImportError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
