#!/usr/bin/env python3
"""Validate and import deep MSYS2 artifact observations into the AKB."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "model" / "inventory" / "current.json"
CATALOG = ROOT / "model" / "catalog" / "current.json"
SNAPSHOTS = ROOT / "evidence" / "inventory-snapshots"
GENERATED = ROOT / "generated"
FILES = (
    "artifacts.jsonl",
    "pe-imports.jsonl",
    "pe-exports.jsonl",
    "archive-members.jsonl",
    "development-metadata.jsonl",
    "recipes.jsonl",
    "warnings.jsonl",
)
KIND_MAP = {
    "executable": "executable",
    "dll": "dll",
    "static-library": "static-library",
    "import-library": "import-library",
    "header": "header",
    "pkg-config-module": "pkg-config-module",
    "cmake-module": "cmake-module",
    "symlink": "filesystem-path",
    "file": "filesystem-path",
}


class InventoryImportError(Exception):
    """Raised when deep-inventory evidence is invalid."""


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8-sig") as stream:
        return json.load(stream)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    with path.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise InventoryImportError(f"{path.name}:{number}: {exc}") from exc
                if not isinstance(value, dict):
                    raise InventoryImportError(f"{path.name}:{number}: expected object")
                values.append(value)
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def slug(value: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789._/+@-")
    return "".join(char if char in allowed else "-" for char in value.lower())


def artifact_id(kind: str, path: str) -> str:
    return f"{KIND_MAP[kind]}:msys2:{slug(path)}"


def package_id(name: str) -> str:
    return f"package:msys2:{slug(name)}"


def recipe_id(name: str) -> str:
    return f"build-recipe:msys2:{slug(name)}"


def relationship_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\0".join(parts).encode()).hexdigest()[:20]
    return f"relationship:inventory:{prefix}-{digest}"


def verify_input(directory: Path) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    manifest_path = directory / "inventory-manifest.json"
    if not manifest_path.is_file():
        raise InventoryImportError(f"required input is missing: {manifest_path}")
    manifest = read_json(manifest_path)
    if manifest.get("schema_version") != "1.0.0":
        raise InventoryImportError("unsupported inventory schema version")
    records: dict[str, list[dict[str, Any]]] = {}
    for name in FILES:
        path = directory / name
        if not path.is_file():
            raise InventoryImportError(f"required input is missing: {path}")
        expected_hash = manifest.get("sha256", {}).get(name)
        if not expected_hash or sha256(path).lower() != str(expected_hash).lower():
            raise InventoryImportError(f"SHA-256 mismatch for {name}")
        records[name] = read_jsonl(path)
        if len(records[name]) != int(manifest.get("counts", {}).get(name, -1)):
            raise InventoryImportError(f"record count mismatch for {name}")
    for index, item in enumerate(records["artifacts.jsonl"], 1):
        missing = {"package", "path", "kind", "present"} - set(item)
        if missing:
            raise InventoryImportError(
                f"artifacts.jsonl:{index}: missing fields {sorted(missing)}"
            )
        if item["kind"] not in KIND_MAP:
            raise InventoryImportError(
                f"artifacts.jsonl:{index}: unknown kind {item['kind']!r}"
            )
        if not str(item["path"]).startswith("/") or ".." in Path(
            str(item["path"])
        ).parts:
            raise InventoryImportError(
                f"artifacts.jsonl:{index}: unsafe package path"
            )
        if not isinstance(item["present"], bool):
            raise InventoryImportError(
                f"artifacts.jsonl:{index}: present must be boolean"
            )
    return manifest, records


def known_package_ids() -> set[str]:
    if not CATALOG.is_file():
        return set()
    return {
        item["id"]
        for item in read_json(CATALOG).get("entities", [])
        if item.get("kind") == "package"
    }


def _entity(
    identifier: str,
    kind: str,
    name: str,
    properties: dict[str, Any],
    evidence: str,
) -> dict[str, Any]:
    return {
        "id": identifier,
        "kind": kind,
        "name": name,
        "status": "verified",
        "confidence": "verified",
        "authority": "MSYS2",
        "aliases": [],
        "tags": ["generated", "deep-inventory"],
        "applicability": {},
        "properties": properties,
        "evidence_refs": [evidence],
    }


def _edge(
    edge_type: str,
    source: str,
    target: str,
    evidence: str,
    **properties: Any,
) -> dict[str, Any]:
    return {
        "id": relationship_id(edge_type, source, target, json.dumps(properties, sort_keys=True)),
        "type": edge_type,
        "source": source,
        "target": target,
        "status": "verified",
        "confidence": "verified",
        "scope": "deep-inventory",
        "condition": "",
        "properties": properties,
        "evidence_refs": [evidence],
    }


def build_projection(
    manifest: dict[str, Any],
    records: dict[str, list[dict[str, Any]]],
    snapshot_id: str,
    packages: set[str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    # Snapshot-qualified evidence remains distinct when projections accumulate.
    # A generic "current" identifier would make retained entities appear to be
    # supported by the latest import rather than their observed archive.
    evidence = f"evidence:inventory:{snapshot_id}"
    package_ids = known_package_ids() if packages is None else packages
    entities: dict[str, dict[str, Any]] = {}
    relationships: dict[str, dict[str, Any]] = {}
    unresolved: list[dict[str, Any]] = []
    path_ids: dict[str, str] = {}
    for row in records["artifacts.jsonl"]:
        try:
            identifier = artifact_id(row["kind"], row["path"])
        except KeyError:
            unresolved.append({"category": "artifact", "record": row, "reason": "invalid-kind"})
            continue
        path_ids[row["path"]] = identifier
        properties = {
            key: value for key, value in row.items()
            if key not in {"package", "path", "kind"}
        }
        entities[identifier] = _entity(
            identifier, KIND_MAP[row["kind"]], row["path"], properties, evidence
        )
        owner = package_id(row["package"])
        if owner in package_ids:
            edge = _edge("installs", owner, identifier, evidence)
            relationships[edge["id"]] = edge
        else:
            unresolved.append(
                {
                    "category": "artifact-owner",
                    "record": {"package": row["package"], "path": row["path"]},
                    "reason": "package-not-in-catalog",
                }
            )

    for row in records["artifacts.jsonl"]:
        if row.get("kind") != "symlink":
            continue
        source = path_ids.get(row["path"])
        target_path = row.get("target")
        target = path_ids.get(target_path) if isinstance(target_path, str) else None
        if not source or not target:
            unresolved.append({
                "category": "symlink", "record": row,
                "reason": "missing-source-or-target",
            })
            continue
        edge = _edge("links-to", source, target, evidence, link_type=row.get("link_type", ""))
        relationships[edge["id"]] = edge

    for row in records["pe-imports.jsonl"]:
        source = path_ids.get(row.get("path", ""))
        dll_name = str(row.get("dll", "")).lower()
        if not source or not dll_name:
            unresolved.append({"category": "pe-import", "record": row, "reason": "missing-source-or-dll"})
            continue
        candidates = [
            identifier
            for path, identifier in path_ids.items()
            if path.lower().endswith("/" + dll_name)
        ]
        target = candidates[0] if len(candidates) == 1 else f"dll:windows:{slug(dll_name)}"
        if not candidates:
            entities.setdefault(
                target,
                _entity(target, "dll", dll_name, {"external": True}, evidence),
            )
        elif len(candidates) > 1:
            unresolved.append(
                {"category": "pe-import", "record": row, "reason": "ambiguous-dll", "candidates": candidates}
            )
            continue
        edge = _edge(
            "imports-dll", source, target, evidence,
            symbols=row.get("symbols", []), ordinals=row.get("ordinals", []),
        )
        relationships[edge["id"]] = edge

    exports_by_path: dict[str, list[dict[str, Any]]] = {}
    for row in records["pe-exports.jsonl"]:
        exports_by_path.setdefault(row.get("path", ""), []).append(
            {"name": row.get("name", ""), "ordinal": row.get("ordinal")}
        )
    for path, exports in exports_by_path.items():
        if path in path_ids:
            entities[path_ids[path]]["properties"]["exports"] = sorted(
                exports, key=lambda item: (item["ordinal"] or 0, item["name"])
            )

    members_by_path: dict[str, list[dict[str, Any]]] = {}
    for row in records["archive-members.jsonl"]:
        members_by_path.setdefault(row.get("path", ""), []).append(
            {key: row.get(key) for key in ("name", "size", "offset")}
        )
    for path, members in members_by_path.items():
        if path in path_ids:
            entities[path_ids[path]]["properties"]["members"] = members

    module_index: dict[str, str] = {}
    metadata_rows: list[tuple[dict[str, Any], str]] = []
    for row in records["development-metadata.jsonl"]:
        source = path_ids.get(row.get("path", ""))
        if not source:
            unresolved.append({"category": "metadata", "record": row, "reason": "missing-source"})
            continue
        metadata_rows.append((row, source))
        entities[source]["properties"]["parsed_metadata"] = {
            key: value for key, value in row.items()
            if key not in {"package", "path", "format"}
        }
        path_stem = Path(str(row.get("path", ""))).stem.lower()
        module_index[path_stem] = source
        if row.get("format") == "pkg-config":
            module_index[str(row.get("name", path_stem)).lower()] = source

    for row, source in metadata_rows:
        if row.get("format") == "pkg-config":
            for requirement in row.get("requires", []):
                target = module_index.get(str(requirement["name"]).lower())
                if not target:
                    unresolved.append(
                        {"category": "pkg-config-requirement", "source": source, **requirement}
                    )
                    continue
                edge = _edge("requires", source, target, evidence, constraint=requirement.get("constraint", ""))
                relationships[edge["id"]] = edge
        elif row.get("format") == "cmake":
            for dependency in row.get("dependencies", []):
                target = module_index.get(str(dependency).lower())
                if not target:
                    unresolved.append(
                        {
                            "category": "cmake-dependency",
                            "source": source,
                            "dependency": dependency,
                        }
                    )
                    continue
                edge = _edge("requires", source, target, evidence)
                relationships[edge["id"]] = edge

    for row in records["recipes.jsonl"]:
        names = row.get("pkgname", [])
        canonical = row.get("pkgbase") or (names[0] if names else row.get("path", "unknown"))
        identifier = recipe_id(canonical)
        entities[identifier] = _entity(
            identifier, "build-recipe", canonical,
            {key: value for key, value in row.items() if key not in {"pkgname"}},
            evidence,
        )
        for name in names:
            target = package_id(name)
            if target not in package_ids and target not in entities:
                unresolved.append({"category": "recipe-package", "source": identifier, "package": name})
                continue
            edge = _edge("packaged-by", target, identifier, evidence)
            relationships[edge["id"]] = edge
        for dependency_type, edge_type in (
            ("depends", "runtime-depends-on"),
            ("makedepends", "build-depends-on"),
            ("checkdepends", "check-depends-on"),
        ):
            for dependency in row.get(dependency_type, []):
                name = re_dependency_name(str(dependency))
                target = package_id(name)
                if target not in package_ids and target not in entities:
                    unresolved.append({"category": dependency_type, "source": identifier, "package": name})
                    continue
                edge = _edge(edge_type, identifier, target, evidence, declared=str(dependency))
                relationships[edge["id"]] = edge

    projection = {
        "schema_version": "0.2.0",
        "snapshot": {
            "id": snapshot_id,
            "observed_at": manifest["generated_at"],
            "description": "Generated MSYS2 package artifact and build-evidence projection.",
            "upstream_versions": {"collector": manifest.get("collector_version", "")},
        },
        "entities": sorted(entities.values(), key=lambda item: item["id"]),
        "relationships": sorted(relationships.values(), key=lambda item: item["id"]),
        "claims": [],
        "evidence": [{
            "id": evidence,
            "class": "observed",
            "title": "MSYS2 deep package inventory",
            "locator": f"evidence/inventory-snapshots/{snapshot_id}/inventory-manifest.json",
            "retrieved_at": manifest["generated_at"],
            "upstream_version": manifest.get("collector_version"),
            "integrity": sha_manifest(manifest),
            "notes": "Collected by tools/deep_inventory.py.",
        }],
    }
    return projection, unresolved


def re_dependency_name(value: str) -> str:
    return value.split(":", 1)[0].split("<", 1)[0].split(">", 1)[0].split("=", 1)[0].strip()


def sha_manifest(manifest: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(manifest.get("sha256", {}), sort_keys=True).encode()
    ).hexdigest()


def fingerprints(projection: dict[str, Any] | None) -> dict[str, str]:
    if not projection:
        return {}
    return {
        item["id"]: hashlib.sha256(
            json.dumps(item.get("properties", {}), sort_keys=True).encode()
        ).hexdigest()
        for item in projection.get("entities", [])
    }


def make_changes(
    previous: dict[str, Any] | None, current: dict[str, Any]
) -> dict[str, Any]:
    old, new = fingerprints(previous), fingerprints(current)
    return {
        "previous_snapshot": previous["snapshot"]["id"] if previous else None,
        "current_snapshot": current["snapshot"]["id"],
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": sorted(item for item in set(old) & set(new) if old[item] != new[item]),
        "unchanged_count": sum(old[item] == new[item] for item in set(old) & set(new)),
    }


def write_reports(
    projection: dict[str, Any],
    changes: dict[str, Any],
    unresolved: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    counts = Counter(item["kind"] for item in projection["entities"])
    lines = [
        "# Deep Inventory Report", "",
        "> Generated from verified artifact observations; do not edit manually.", "",
        f"- Snapshot: `{projection['snapshot']['id']}`",
        f"- Entities: **{len(projection['entities'])}**",
        f"- Relationships: **{len(projection['relationships'])}**",
        f"- Unresolved references: **{len(unresolved)}**",
        f"- Collector warnings: **{len(warnings)}**", "",
        "| Entity kind | Count |", "| --- | ---: |",
    ]
    lines.extend(f"| {kind} | {count} |" for kind, count in sorted(counts.items()))
    lines.extend([
        "", "## Change summary", "",
        f"- Added: **{len(changes['added'])}**",
        f"- Removed: **{len(changes['removed'])}**",
        f"- Changed: **{len(changes['changed'])}**",
        f"- Unchanged: **{changes['unchanged_count']}**",
    ])
    (GENERATED / "deep-inventory-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    entity_names = {
        item["id"]: item["name"] for item in projection["entities"]
    }
    binary_edges = [
        item
        for item in projection["relationships"]
        if item["type"] == "imports-dll"
    ]
    reverse_counts = Counter(item["target"] for item in binary_edges)
    binary_lines = [
        "# Binary Dependency Report",
        "",
        "> Generated from PE import tables; reverse counts are derived, not stored.",
        "",
        f"- Binary import relationships: **{len(binary_edges)}**",
        f"- Imported DLL identities: **{len(reverse_counts)}**",
        "",
        "| Importing binary | Imported DLL | Named symbols | Ordinals | Reverse importers |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for edge in sorted(
        binary_edges,
        key=lambda item: (item["target"], item["source"]),
    ):
        properties = edge.get("properties", {})
        binary_lines.append(
            f"| `{entity_names.get(edge['source'], edge['source'])}` | "
            f"`{entity_names.get(edge['target'], edge['target'])}` | "
            f"{len(properties.get('symbols', []))} | "
            f"{len(properties.get('ordinals', []))} | "
            f"{reverse_counts[edge['target']]} |"
        )
    (GENERATED / "binary-dependency-report.md").write_text(
        "\n".join(binary_lines) + "\n", encoding="utf-8"
    )
    write_json(
        GENERATED / "binary-dependency-graph.json",
        {
            "snapshot": projection["snapshot"]["id"],
            "edges": binary_edges,
            "reverse_importer_counts": dict(sorted(reverse_counts.items())),
        },
    )

    development_kinds = {
        "header",
        "import-library",
        "static-library",
        "pkg-config-module",
        "cmake-module",
    }
    development = [
        item for item in projection["entities"] if item["kind"] in development_kinds
    ]
    development_lines = [
        "# Development Artifact Catalog",
        "",
        "> Generated from package-owned development files; do not edit manually.",
        "",
        "| Kind | Artifact | SHA-256 |",
        "| --- | --- | --- |",
    ]
    for item in sorted(development, key=lambda value: (value["kind"], value["name"])):
        development_lines.append(
            f"| {item['kind']} | `{item['name']}` | "
            f"`{item.get('properties', {}).get('sha256', '')}` |"
        )
    (GENERATED / "development-artifact-catalog.md").write_text(
        "\n".join(development_lines) + "\n", encoding="utf-8"
    )

    write_json(GENERATED / "deep-inventory-changes.json", changes)
    write_json(GENERATED / "unresolved-inventory-references.json", unresolved)
    write_json(GENERATED / "deep-inventory-warnings.json", warnings)


def merge_projection(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    """Accumulate independently verified inventory snapshots by stable IDs."""
    if not previous:
        return current
    for key in ("entities", "relationships", "evidence"):
        merged = {item["id"]: item for item in previous.get(key, [])}
        merged.update({item["id"]: item for item in current.get(key, [])})
        current[key] = sorted(merged.values(), key=lambda item: item["id"])
    current["claims"] = []
    return current


def import_inventory(directory: Path, accumulate: bool = False) -> dict[str, Any]:
    manifest, records = verify_input(directory)
    generated_at = datetime.fromisoformat(
        manifest["generated_at"].replace("Z", "+00:00")
    ).astimezone(timezone.utc)
    snapshot_id = generated_at.strftime("%Y%m%dT%H%M%SZ") + "-" + sha_manifest(manifest)[:12]
    previous = read_json(CURRENT) if CURRENT.is_file() else None
    projection, unresolved = build_projection(manifest, records, snapshot_id)
    if accumulate:
        projection = merge_projection(previous, projection)
    changes = make_changes(previous, projection)
    snapshot_dir = SNAPSHOTS / snapshot_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    for path in directory.iterdir():
        if path.is_file():
            shutil.copy2(path, snapshot_dir / path.name)
    write_json(snapshot_dir / "architecture-inventory.json", projection)
    write_json(snapshot_dir / "changes.json", changes)
    write_json(snapshot_dir / "unresolved.json", unresolved)
    write_json(CURRENT, projection)
    write_reports(projection, changes, unresolved, records["warnings.jsonl"])
    return {
        "snapshot": snapshot_id,
        "entities": len(projection["entities"]),
        "relationships": len(projection["relationships"]),
        "unresolved": len(unresolved),
        "warnings": len(records["warnings.jsonl"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory_directory", type=Path)
    parser.add_argument("--accumulate", action="store_true", help="retain prior verified inventory observations")
    args = parser.parse_args()
    try:
        result = import_inventory(args.inventory_directory.resolve(), args.accumulate)
    except (InventoryImportError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Imported " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
