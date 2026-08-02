#!/usr/bin/env python3
"""Import catalog-msys2-packages.ps1 output into the MSYS2 AKB."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "model" / "catalog" / "current.json"
SNAPSHOTS = ROOT / "evidence" / "snapshots"
GENERATED = ROOT / "generated"
REQUIRED_PACKAGE_FIELDS = {
    "repository",
    "name",
    "version",
    "installed",
    "architecture",
    "classification",
    "description",
}
REPOSITORY_ENVIRONMENTS = {
    "msys": "environment:msys2:msys",
    "ucrt64": "environment:msys2:ucrt64",
    "clang64": "environment:msys2:clang64",
    "clangarm64": "environment:msys2:clangarm64",
    "mingw64": "environment:msys2:mingw64",
    "mingw32": "environment:msys2:mingw32",
}


class CatalogError(Exception):
    """Raised for invalid or internally inconsistent catalog input."""


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8-sig") as stream:
        return json.load(stream)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def slug(value: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789._/+@-")
    return "".join(char if char in allowed else "-" for char in value.lower())


def package_id(name: str) -> str:
    return f"package:msys2:{slug(name)}"


def repository_id(name: str) -> str:
    return f"repository:msys2:{slug(name)}"


def relationship_id(prefix: str, *parts: str) -> str:
    key = "\0".join(parts).encode()
    return f"relationship:catalog:{prefix}-{hashlib.sha256(key).hexdigest()[:20]}"


def verify_input(directory: Path) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]]]:
    manifest_path = directory / "catalog-manifest.json"
    package_path = directory / "all-packages.csv"
    edge_path = directory / "dependency-edges.csv"
    for path in (manifest_path, package_path, edge_path):
        if not path.is_file():
            raise CatalogError(f"required input is missing: {path}")

    manifest = read_json(manifest_path)
    for filename, expected in manifest.get("sha256", {}).items():
        path = directory / filename
        if not path.is_file():
            raise CatalogError(f"manifest file is missing: {path}")
        actual = sha256(path)
        if actual.lower() != str(expected).lower():
            raise CatalogError(f"SHA-256 mismatch for {filename}")

    packages = read_csv(package_path)
    edges = read_csv(edge_path)
    if not packages:
        raise CatalogError("all-packages.csv contains no packages")
    missing = REQUIRED_PACKAGE_FIELDS - set(packages[0])
    if missing:
        raise CatalogError(f"all-packages.csv is missing fields: {sorted(missing)}")
    if len(packages) != int(manifest.get("package_count", -1)):
        raise CatalogError("package count does not match catalog-manifest.json")
    return manifest, packages, edges


def make_entity(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id": package_id(row["name"]),
        "kind": "package",
        "name": row["name"],
        "summary": row.get("description", ""),
        "status": "verified",
        "confidence": "verified",
        "authority": "MSYS2",
        "aliases": [],
        "tags": ["generated", "package", row.get("classification", "unclassified")],
        "applicability": {"repository": row["repository"]},
        "properties": {
            key: value
            for key, value in row.items()
            if key not in {"name", "description", "repository"} and value != ""
        },
        "evidence_refs": ["evidence:catalog:current"],
    }


def build_catalog(
    manifest: dict[str, Any],
    packages: list[dict[str, str]],
    edges: list[dict[str, str]],
    snapshot_id: str,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    repositories = sorted({row["repository"] for row in packages})
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    unresolved: list[dict[str, str]] = []
    package_names = {row["name"] for row in packages}

    for repository in repositories:
        entities.append(
            {
                "id": repository_id(repository),
                "kind": "repository",
                "name": repository,
                "status": "verified",
                "confidence": "verified",
                "authority": "MSYS2",
                "aliases": [],
                "tags": ["generated", "package-repository"],
                "applicability": {},
                "properties": {},
                "evidence_refs": ["evidence:catalog:current"],
            }
        )

    for row in sorted(packages, key=lambda item: item["name"]):
        source = package_id(row["name"])
        repo = row["repository"]
        entities.append(make_entity(row))
        relationships.append(
            {
                "id": relationship_id("published", row["name"], repo),
                "type": "published-in",
                "source": source,
                "target": repository_id(repo),
                "status": "verified",
                "confidence": "verified",
                "scope": "package-catalog",
                "condition": "",
                "properties": {},
                "evidence_refs": ["evidence:catalog:current"],
            }
        )
        if repo in REPOSITORY_ENVIRONMENTS:
            relationships.append(
                {
                    "id": relationship_id("environment", row["name"], repo),
                    "type": "belongs-to-environment",
                    "source": source,
                    "target": REPOSITORY_ENVIRONMENTS[repo],
                    "status": "verified",
                    "confidence": "verified",
                    "scope": "package-catalog",
                    "condition": "",
                    "properties": {},
                    "evidence_refs": ["evidence:catalog:current"],
                }
            )

    for edge in edges:
        source_name = edge.get("source_package", "")
        target_name = edge.get("target_package", "")
        relation = edge.get("relationship", "")
        if (
            source_name not in package_names
            or target_name not in package_names
            or relation not in {
                "runtime-depends-on",
                "optional-depends-on",
                "build-depends-on",
                "check-depends-on",
            }
        ):
            unresolved.append(edge)
            continue
        relationships.append(
            {
                "id": relationship_id(relation, source_name, target_name),
                "type": relation,
                "source": package_id(source_name),
                "target": package_id(target_name),
                "status": "verified",
                "confidence": "verified",
                "scope": "package-catalog",
                "condition": edge.get("constraint", ""),
                "properties": {
                    "source_repository": edge.get("source_repository", "")
                },
                "evidence_refs": ["evidence:catalog:current"],
            }
        )

    catalog = {
        "schema_version": "0.1.0",
        "snapshot": {
            "id": snapshot_id,
            "observed_at": manifest["generated_at"],
            "description": "Generated projection of the MSYS2 package catalog.",
            "upstream_versions": {"pacman": manifest.get("pacman_version", "")},
        },
        "entities": entities,
        "relationships": relationships,
        "claims": [],
        "evidence": [
            {
                "id": "evidence:catalog:current",
                "class": "observed",
                "title": "MSYS2 pacman package catalog",
                "locator": f"evidence/snapshots/{snapshot_id}/catalog-manifest.json",
                "retrieved_at": manifest["generated_at"],
                "upstream_version": manifest.get("pacman_version"),
                "integrity": manifest["sha256"].get("all-packages.csv"),
                "notes": "Collected by tools/catalog-msys2-packages.ps1.",
            }
        ],
    }
    return catalog, unresolved


def entity_versions(catalog: dict[str, Any] | None) -> dict[str, str]:
    if not catalog:
        return {}
    return {
        item["id"]: str(item.get("properties", {}).get("version", ""))
        for item in catalog.get("entities", [])
        if item.get("kind") == "package"
    }


def make_changes(
    previous: dict[str, Any] | None, current: dict[str, Any]
) -> dict[str, Any]:
    old = entity_versions(previous)
    new = entity_versions(current)
    return {
        "previous_snapshot": previous["snapshot"]["id"] if previous else None,
        "current_snapshot": current["snapshot"]["id"],
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "updated": [
            {"id": item, "from": old[item], "to": new[item]}
            for item in sorted(set(old) & set(new))
            if old[item] != new[item]
        ],
        "unchanged_count": sum(
            old[item] == new[item] for item in set(old) & set(new)
        ),
    }


def write_reports(
    catalog: dict[str, Any],
    changes: dict[str, Any],
    unresolved: list[dict[str, str]],
) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    packages = [item for item in catalog["entities"] if item["kind"] == "package"]
    repositories = [
        item for item in catalog["entities"] if item["kind"] == "repository"
    ]
    lines = [
        "# Generated Package Catalog",
        "",
        "> Generated from a verified pacman catalog snapshot; do not edit manually.",
        "",
        f"- Snapshot: `{catalog['snapshot']['id']}`",
        f"- Packages: **{len(packages)}**",
        f"- Repositories: **{len(repositories)}**",
        f"- Relationships: **{len(catalog['relationships'])}**",
        f"- Unresolved dependency references: **{len(unresolved)}**",
        "",
        "| Repository | Package | Version | Installed | Classification |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in sorted(
        packages,
        key=lambda entry: (
            entry["applicability"]["repository"],
            entry["name"],
        ),
    ):
        props = item["properties"]
        lines.append(
            f"| {item['applicability']['repository']} | {item['name']} | "
            f"{props.get('version', '')} | {props.get('installed', '')} | "
            f"{props.get('classification', '')} |"
        )
    (GENERATED / "package-catalog.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    change_lines = [
        "# Package Catalog Change Report",
        "",
        f"- Previous snapshot: `{changes['previous_snapshot'] or 'none'}`",
        f"- Current snapshot: `{changes['current_snapshot']}`",
        f"- Added packages: **{len(changes['added'])}**",
        f"- Removed packages: **{len(changes['removed'])}**",
        f"- Updated packages: **{len(changes['updated'])}**",
        f"- Unchanged packages: **{changes['unchanged_count']}**",
        "",
    ]
    for heading, values in (
        ("Added", changes["added"]),
        ("Removed", changes["removed"]),
    ):
        change_lines.extend([f"## {heading}", ""])
        change_lines.extend(f"- `{value}`" for value in values)
        if not values:
            change_lines.append("- None")
        change_lines.append("")
    change_lines.extend(["## Updated", ""])
    change_lines.extend(
        f"- `{item['id']}`: `{item['from']}` → `{item['to']}`"
        for item in changes["updated"]
    )
    if not changes["updated"]:
        change_lines.append("- None")
    (GENERATED / "catalog-change-report.md").write_text(
        "\n".join(change_lines) + "\n", encoding="utf-8"
    )
    write_json(GENERATED / "catalog-changes.json", changes)
    write_json(GENERATED / "unresolved-dependencies.json", unresolved)


def import_catalog(directory: Path) -> dict[str, Any]:
    manifest, packages, edges = verify_input(directory)
    content_key = hashlib.sha256(
        (
            manifest["sha256"]["all-packages.csv"]
            + manifest["sha256"]["dependency-edges.csv"]
        ).encode()
    ).hexdigest()[:12]
    generated_at = datetime.fromisoformat(
        manifest["generated_at"].replace("Z", "+00:00")
    ).astimezone(timezone.utc)
    snapshot_id = generated_at.strftime("%Y%m%dT%H%M%SZ") + "-" + content_key
    previous = read_json(CURRENT) if CURRENT.is_file() else None
    catalog, unresolved = build_catalog(
        manifest, packages, edges, snapshot_id
    )
    changes = make_changes(previous, catalog)

    snapshot_dir = SNAPSHOTS / snapshot_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    for path in directory.iterdir():
        if path.is_file():
            shutil.copy2(path, snapshot_dir / path.name)
    write_json(snapshot_dir / "architecture-catalog.json", catalog)
    write_json(snapshot_dir / "changes.json", changes)
    write_json(CURRENT, catalog)
    write_reports(catalog, changes, unresolved)
    return {
        "snapshot": snapshot_id,
        "packages": len(packages),
        "relationships": len(catalog["relationships"]),
        "unresolved": len(unresolved),
        "added": len(changes["added"]),
        "removed": len(changes["removed"]),
        "updated": len(changes["updated"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog_directory", type=Path)
    args = parser.parse_args()
    try:
        result = import_catalog(args.catalog_directory.resolve())
    except (CatalogError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Imported " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
