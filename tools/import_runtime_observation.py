#!/usr/bin/env python3
"""Validate, project, and compare a runtime observation without altering authored entities."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "model" / "runtime" / "current.json"
GENERATED = ROOT / "generated"
REQUIRED = {"schema_version", "collector_version", "observed_at", "environment", "host", "environment_variables", "tools"}
SUPPORTED_SCHEMA_VERSIONS = {"1.0.0", "1.1.0"}
CURRENT_SCHEMA_VERSION = "1.1.0"


class RuntimeObservationError(Exception):
    pass


def migrate_to_current_schema(value: dict[str, Any]) -> dict[str, Any]:
    """Forward-migrate a 1.0.0 observation to the 1.1.0 shape without loss.

    1.1.0 formally declares the ``probes`` field collect_runtime_observation.py
    has always emitted; 1.0.0 documents may or may not carry it (undeclared
    in the 1.0.0 schema). Every original field is preserved; only a default
    ``probes: {}`` is added when absent.
    """
    if value["schema_version"] == CURRENT_SCHEMA_VERSION:
        return value
    migrated = dict(value)
    migrated["schema_version"] = CURRENT_SCHEMA_VERSION
    migrated.setdefault("probes", {})
    return migrated


def load_observation(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not REQUIRED.issubset(value):
        raise RuntimeObservationError("runtime observation is missing required fields")
    if value["schema_version"] not in SUPPORTED_SCHEMA_VERSIONS:
        raise RuntimeObservationError("unsupported runtime observation schema")
    if value["environment"] not in {"msys", "ucrt64", "clang64", "clangarm64", "mingw64", "mingw32"}:
        raise RuntimeObservationError("unknown MSYS2 environment")
    return migrate_to_current_schema(value)


def projection(observation: dict[str, Any]) -> dict[str, Any]:
    environment = observation["environment"]
    digest = hashlib.sha256(json.dumps(observation, sort_keys=True).encode()).hexdigest()
    identifier = f"configuration:msys2:runtime-observation-{environment}"
    return {
        "snapshot": {"id": f"runtime-{environment}-{digest[:12]}", "observed_at": observation["observed_at"], "description": "Generated runtime observation."},
        "entities": [{"id": identifier, "kind": "configuration", "name": f"{environment.upper()} runtime observation", "status": "verified", "confidence": "verified", "authority": "local-observation", "aliases": [], "tags": ["generated", "runtime-observation"], "applicability": {"environment_ids": [f"environment:msys2:{environment}"]}, "properties": observation, "evidence_refs": []}],
        "relationships": [{"id": f"relationship:runtime-observation:{environment}", "type": "belongs-to-environment", "source": identifier, "target": f"environment:msys2:{environment}", "status": "verified", "confidence": "verified", "scope": "runtime-observation", "condition": "", "properties": {"observed_at": observation["observed_at"]}, "evidence_refs": []}],
        "claims": [], "evidence": []
    }


def render_report(observation: dict[str, Any]) -> str:
    rows = ["# Generated Runtime Environment Report", "", "> Generated from a bounded local observation; do not edit manually.", "", f"- Environment: `{observation['environment']}`", f"- Observed: `{observation['observed_at']}`", f"- Host: `{observation['host']['system']} {observation['host']['machine']}`", "", "| Tool | Found | Version |", "| --- | --- | --- |"]
    for name, value in sorted(observation["tools"].items()):
        version = str(value.get("version", "")).replace("|", "\\|")
        rows.append(f"| `{name}` | {value.get('found', False)} | {version} |")
    return "\n".join(rows) + "\n"


def merge_projection(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    """Retain the latest bounded observation independently for each environment."""
    environment = current["entities"][0]["applicability"]["environment_ids"][0]
    entity_id = current["entities"][0]["id"]
    entities = [item for item in previous.get("entities", []) if item.get("id") != entity_id]
    relationships = [
        item for item in previous.get("relationships", [])
        if item.get("source") != entity_id
    ]
    entities.extend(current["entities"])
    relationships.extend(current["relationships"])
    return {"snapshot": current["snapshot"], "entities": sorted(entities, key=lambda item: item["id"]), "relationships": sorted(relationships, key=lambda item: item["id"]), "claims": [], "evidence": []}


def import_observation(path: Path) -> dict[str, Any]:
    observation = load_observation(path)
    value = projection(observation)
    if CURRENT.is_file():
        value = merge_projection(json.loads(CURRENT.read_text(encoding="utf-8")), value)
    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    GENERATED.mkdir(parents=True, exist_ok=True)
    (GENERATED / "runtime-environment-report.md").write_text(render_report(observation), encoding="utf-8")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observation", type=Path)
    args = parser.parse_args()
    try:
        result = import_observation(args.observation)
        print(f"Imported {result['snapshot']['id']}")
    except (OSError, ValueError, RuntimeObservationError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
