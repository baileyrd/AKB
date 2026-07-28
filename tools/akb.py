#!/usr/bin/env python3
"""Validate and generate foundational MSYS2 AKB views."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model" / "graph.json"
CATALOG = ROOT / "model" / "catalog" / "current.json"
INVENTORY = ROOT / "model" / "inventory" / "current.json"
RUNTIME = ROOT / "model" / "runtime" / "current.json"
KINDS = ROOT / "model" / "vocabularies" / "entity-kinds.json"
REL_TYPES = ROOT / "model" / "vocabularies" / "relationship-types.json"
GENERATED = ROOT / "generated"


class ValidationError(Exception):
    """Raised when canonical model invariants are violated."""


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def load_composed_graph() -> dict[str, Any]:
    """Compose reviewed architecture with the current generated catalog."""
    graph = load_json(MODEL)
    composed = {
        "entities": list(graph.get("entities", [])),
        "relationships": list(graph.get("relationships", [])),
        "claims": list(graph.get("claims", [])),
        "evidence": list(graph.get("evidence", [])),
    }
    for projection_path in (CATALOG, INVENTORY, RUNTIME):
        if projection_path.is_file():
            projection = load_json(projection_path)
            for key in composed:
                composed[key].extend(projection.get(key, []))
    return composed


def validate() -> dict[str, int]:
    graph = load_composed_graph()
    allowed_kinds = set(load_json(KINDS)["kinds"])
    allowed_relationships = set(load_json(REL_TYPES)["types"])

    entities = graph.get("entities", [])
    relationships = graph.get("relationships", [])
    entity_ids = [item["id"] for item in entities]
    relationship_ids = [item["id"] for item in relationships]
    claim_ids = [item["id"] for item in graph.get("claims", [])]
    evidence_ids = [item["id"] for item in graph.get("evidence", [])]
    errors: list[str] = []

    duplicates = [item for item, count in Counter(entity_ids).items() if count > 1]
    errors.extend(f"duplicate entity ID: {item}" for item in duplicates)
    duplicates = [
        item for item, count in Counter(relationship_ids).items() if count > 1
    ]
    errors.extend(f"duplicate relationship ID: {item}" for item in duplicates)
    duplicates = [item for item, count in Counter(claim_ids).items() if count > 1]
    errors.extend(f"duplicate claim ID: {item}" for item in duplicates)
    duplicates = [
        item for item, count in Counter(evidence_ids).items() if count > 1
    ]
    errors.extend(f"duplicate evidence ID: {item}" for item in duplicates)

    known_entities = set(entity_ids)
    for entity in entities:
        if entity["kind"] not in allowed_kinds:
            errors.append(
                f"{entity['id']}: unknown entity kind {entity['kind']!r}"
            )

    for relationship in relationships:
        if relationship["type"] not in allowed_relationships:
            errors.append(
                f"{relationship['id']}: unknown relationship type "
                f"{relationship['type']!r}"
            )
        if relationship["source"] not in known_entities:
            errors.append(
                f"{relationship['id']}: unknown source {relationship['source']}"
            )
        if relationship["target"] not in known_entities:
            errors.append(
                f"{relationship['id']}: unknown target {relationship['target']}"
            )

    known_evidence = set(evidence_ids)
    for item in entities + relationships + graph.get("claims", []):
        for evidence_ref in item.get("evidence_refs", []):
            if evidence_ref not in known_evidence:
                errors.append(f"{item['id']}: unknown evidence {evidence_ref}")

    for claim in graph.get("claims", []):
        if claim["subject"] not in known_entities:
            errors.append(f"{claim['id']}: unknown subject {claim['subject']}")

    if errors:
        raise ValidationError("\n".join(errors))

    return {
        "entities": len(entities),
        "relationships": len(relationships),
        "claims": len(graph.get("claims", [])),
        "evidence": len(graph.get("evidence", [])),
    }


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def generate() -> list[Path]:
    graph = load_composed_graph()
    GENERATED.mkdir(parents=True, exist_ok=True)
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relationship in graph["relationships"]:
        by_source[relationship["source"]].append(relationship)
        by_target[relationship["target"]].append(relationship)

    entity_lines = [
        "# Generated Entity Index",
        "",
        "> Generated from the composed authored and current catalog models; do not edit manually.",
        "",
        "| ID | Kind | Name | Status | Out | In |",
        "| --- | --- | --- | --- | ---: | ---: |",
    ]
    for entity in sorted(graph["entities"], key=lambda item: item["id"]):
        entity_lines.append(
            "| {id} | {kind} | {name} | {status} | {out} | {in_} |".format(
                id=escape_cell(entity["id"]),
                kind=escape_cell(entity["kind"]),
                name=escape_cell(entity["name"]),
                status=escape_cell(entity["status"]),
                out=len(by_source[entity["id"]]),
                in_=len(by_target[entity["id"]]),
            )
        )

    relationship_lines = [
        "# Generated Relationship Index",
        "",
        "> Generated from the composed authored and current catalog models; do not edit manually.",
        "",
        "| ID | Type | Source | Target | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in sorted(graph["relationships"], key=lambda edge: edge["id"]):
        relationship_lines.append(
            "| {id} | {type} | {source} | {target} | {status} |".format(
                **{key: escape_cell(value) for key, value in item.items()}
            )
        )

    outputs = [
        GENERATED / "entity-index.md",
        GENERATED / "relationship-index.md",
    ]
    outputs[0].write_text("\n".join(entity_lines) + "\n", encoding="utf-8")
    outputs[1].write_text(
        "\n".join(relationship_lines) + "\n", encoding="utf-8"
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "generate", "all"))
    args = parser.parse_args()

    try:
        if args.command in {"validate", "all"}:
            counts = validate()
            print(
                "Validated "
                + ", ".join(f"{value} {key}" for key, value in counts.items())
            )
        if args.command in {"generate", "all"}:
            for output in generate():
                print(f"Generated {output.relative_to(ROOT)}")
    except (OSError, KeyError, TypeError, ValueError, ValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
