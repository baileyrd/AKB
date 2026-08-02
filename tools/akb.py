#!/usr/bin/env python3
"""Validate and generate foundational MSYS2 AKB views."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model" / "graph.json"
CATALOG = ROOT / "model" / "catalog" / "current.json"
INVENTORY = ROOT / "model" / "inventory" / "current.json"
RUNTIME = ROOT / "model" / "runtime" / "current.json"
RECIPES = ROOT / "model" / "recipes" / "current.json"
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
    for projection_path in (CATALOG, RECIPES, INVENTORY, RUNTIME):
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


DOCS = ROOT / "docs"
SOURCE_REGISTRY = ROOT / "evidence" / "source-registry.json"

REQUIRED_FRONTMATTER = ("id", "title", "volume", "status", "last_verified")
ALLOWED_DOC_STATUS = {"planned", "partial", "verified"}
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SCALAR_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)$")
GENERATED_MARKERS = (
    "<!-- BEGIN GENERATED dependency-subgraph -->",
    "<!-- END GENERATED dependency-subgraph -->",
)


def parse_frontmatter(text: str) -> dict[str, Any] | None:
    """Parse the leading YAML block.

    Deliberately minimal rather than a YAML dependency: it reads the scalar
    keys and the two list forms this project's pages actually use. Anything
    it cannot read is reported as an error rather than silently skipped.
    """
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields: dict[str, Any] = {}
    key: str | None = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            stripped = line.strip()
            if stripped.startswith("- ") and key:
                fields.setdefault(key, []).append(stripped[2:].strip())
            continue
        scalar = SCALAR_KEY.match(line)
        if not scalar:
            continue
        key, value = scalar.group(1), scalar.group(2).strip()
        if value in ("[]", "{}"):
            fields[key] = []
        elif value:
            fields[key] = value
        else:
            fields[key] = []
    return fields


def known_source_ids() -> set[str]:
    if not SOURCE_REGISTRY.is_file():
        return set()
    registry = load_json(SOURCE_REGISTRY)
    entries = registry if isinstance(registry, list) else registry.get("sources", [])
    return {entry["id"] for entry in entries if isinstance(entry, dict) and "id" in entry}


def validate_docs() -> dict[str, int]:
    """Validate authored documentation pages against the documentation standard.

    `validate()` operates only on the composed JSON graph and never opens a
    Markdown file, so a page could reference an entity that does not exist,
    omit its status, or carry an unbalanced generated block without any check
    noticing. This closes that gap.
    """
    graph = load_composed_graph()
    known_entities = {item["id"] for item in graph["entities"]}
    # A page may cite either a graph evidence record or a registered source.
    known_evidence = {item["id"] for item in graph.get("evidence", [])} | known_source_ids()

    errors: list[str] = []
    pages = sorted(DOCS.glob("*.md"))
    for path in pages:
        name = path.name
        text = path.read_text(encoding="utf-8")

        fields = parse_frontmatter(text)
        if fields is None:
            errors.append(f"{name}: no YAML frontmatter block")
            continue

        for key in REQUIRED_FRONTMATTER:
            if key not in fields:
                errors.append(f"{name}: missing required frontmatter key {key!r}")

        volume = fields.get("volume")
        if volume is not None:
            try:
                number = int(str(volume))
            except ValueError:
                errors.append(f"{name}: volume {volume!r} is not an integer")
            else:
                if not 1 <= number <= 20:
                    errors.append(f"{name}: volume {number} outside the twenty-volume range")

        status = fields.get("status")
        if status is not None and str(status) not in ALLOWED_DOC_STATUS:
            errors.append(
                f"{name}: status {status!r} not one of {sorted(ALLOWED_DOC_STATUS)}"
            )

        for ref in fields.get("model_refs", []) or []:
            if ref not in known_entities:
                errors.append(f"{name}: model_ref does not resolve: {ref}")
        for ref in fields.get("evidence_refs", []) or []:
            if ref not in known_evidence:
                errors.append(f"{name}: evidence_ref does not resolve: {ref}")

        begin, end = (text.count(marker) for marker in GENERATED_MARKERS)
        if begin != end:
            errors.append(f"{name}: unbalanced generated-block markers ({begin} begin, {end} end)")
        if begin > 1:
            errors.append(f"{name}: {begin} generated blocks, expected at most one")

    if errors:
        raise ValidationError("\n".join(errors))

    return {"pages": len(pages)}


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

    claim_lines = [
        "# Generated Claim Evidence Index",
        "",
        "> Generated from the composed model; do not edit manually.",
        "",
        "| Claim | Subject | Classification | Confidence | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for claim in sorted(graph["claims"], key=lambda item: item["id"]):
        claim_lines.append(
            "| {id} | {subject} | {classification} | {confidence} | {evidence} |".format(
                id=escape_cell(claim["id"]), subject=escape_cell(claim["subject"]),
                classification=escape_cell(claim["classification"]),
                confidence=escape_cell(claim["confidence"]),
                evidence=escape_cell(", ".join(claim.get("evidence_refs", []))),
            )
        )
    if not graph["claims"]:
        claim_lines.append("| _No claims recorded_ |  |  |  |  |")

    status_counts = Counter(item["status"] for item in graph["entities"])
    evidenced_entities = sum(bool(item.get("evidence_refs")) for item in graph["entities"])
    coverage_lines = [
        "# Generated Coverage Report", "",
        "> Generated from the composed model; do not edit manually.", "",
        f"- Entities: **{len(graph['entities'])}**",
        f"- Entities with evidence: **{evidenced_entities}**",
        f"- Claims: **{len(graph['claims'])}**",
        f"- Evidence records: **{len(graph['evidence'])}**", "",
        "| Entity status | Count |", "| --- | ---: |",
    ]
    coverage_lines.extend(f"| {status} | {count} |" for status, count in sorted(status_counts.items()))

    dossier_lines = [
        "# Generated Object Dossiers", "",
        "> Generated from the composed model; each heading is a stable object documentation anchor.",
    ]
    for entity in sorted(graph["entities"], key=lambda item: item["id"]):
        identifier = entity["id"]
        dossier_lines.extend([
            "", f"## `{identifier}`", "",
            f"- Name: {escape_cell(entity['name'])}",
            f"- Kind: `{escape_cell(entity['kind'])}`",
            f"- Status: `{escape_cell(entity['status'])}`",
            f"- Evidence: {escape_cell(', '.join(entity.get('evidence_refs', [])) or 'none recorded')}",
            f"- Outgoing relationships: {len(by_source[identifier])}",
            f"- Incoming relationships: {len(by_target[identifier])}",
        ])

    outputs = [
        GENERATED / "entity-index.md",
        GENERATED / "relationship-index.md",
        GENERATED / "claim-evidence-index.md",
        GENERATED / "coverage-report.md",
        GENERATED / "object-dossiers.md",
    ]
    outputs[0].write_text("\n".join(entity_lines) + "\n", encoding="utf-8")
    outputs[1].write_text(
        "\n".join(relationship_lines) + "\n", encoding="utf-8"
    )
    outputs[2].write_text("\n".join(claim_lines) + "\n", encoding="utf-8")
    outputs[3].write_text("\n".join(coverage_lines) + "\n", encoding="utf-8")
    outputs[4].write_text("\n".join(dossier_lines) + "\n", encoding="utf-8")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("validate", "validate-docs", "generate", "all")
    )
    args = parser.parse_args()

    try:
        if args.command in {"validate", "all"}:
            counts = validate()
            print(
                "Validated "
                + ", ".join(f"{value} {key}" for key, value in counts.items())
            )
        if args.command in {"validate-docs", "all"}:
            counts = validate_docs()
            print(f"Validated {counts['pages']} documentation pages")
        if args.command in {"generate", "all"}:
            for output in generate():
                print(f"Generated {output.relative_to(ROOT)}")
    except (OSError, KeyError, TypeError, ValueError, ValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
