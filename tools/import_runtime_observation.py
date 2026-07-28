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


class RuntimeObservationError(Exception):
    pass


def load_observation(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not REQUIRED.issubset(value):
        raise RuntimeObservationError("runtime observation is missing required fields")
    if value["schema_version"] != "1.0.0":
        raise RuntimeObservationError("unsupported runtime observation schema")
    if value["environment"] not in {"msys", "ucrt64", "clang64", "clangarm64", "mingw64", "mingw32"}:
        raise RuntimeObservationError("unknown MSYS2 environment")
    return value


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


def import_observation(path: Path) -> dict[str, Any]:
    observation = load_observation(path)
    value = projection(observation)
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
