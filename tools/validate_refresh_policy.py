#!/usr/bin/env python3
"""Validate the multi-source refresh policy against the source registry."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "source-registry.json"
POLICY = ROOT / "evidence" / "refresh-policy.json"
CADENCES = {"daily", "weekly", "on-demand"}
PRIORITIES = {"high", "normal", "low"}


class ValidationError(Exception):
    """Raised when the refresh policy cannot safely drive a refresh."""


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def validate(registry_path: Path = REGISTRY, policy_path: Path = POLICY) -> dict[str, int]:
    registry = load_json(registry_path)
    policy = load_json(policy_path)
    errors: list[str] = []
    if policy.get("schema_version") != "1.0.0":
        errors.append("unsupported refresh policy schema_version")

    known_sources = {item["id"] for item in registry.get("sources", [])}
    configured_sources = [item.get("source_id") for item in policy.get("sources", [])]
    duplicate_sources = sorted(
        source for source, count in Counter(configured_sources).items() if count > 1
    )
    if duplicate_sources:
        errors.append("duplicate source policy: " + ", ".join(duplicate_sources))
    missing_sources = sorted(known_sources - set(configured_sources))
    unknown_sources = sorted(set(configured_sources) - known_sources)
    if missing_sources:
        errors.append("missing source policy: " + ", ".join(missing_sources))
    if unknown_sources:
        errors.append("unknown source policy: " + ", ".join(unknown_sources))

    for item in policy.get("sources", []):
        source_id = item.get("source_id", "<missing>")
        if item.get("cadence") not in CADENCES:
            errors.append(f"{source_id}: invalid cadence")
        if item.get("priority") not in PRIORITIES:
            errors.append(f"{source_id}: invalid priority")
        if not isinstance(item.get("adapter"), str) or not item["adapter"]:
            errors.append(f"{source_id}: missing adapter")

    for section, fields in {
        "successful_snapshots": ("minimum_count", "minimum_days"),
        "failed_runs": ("minimum_count", "minimum_days"),
    }.items():
        values = policy.get("retention", {}).get(section, {})
        for field in fields:
            if not isinstance(values.get(field), int) or values[field] < 1:
                errors.append(f"retention.{section}.{field} must be a positive integer")
    for field in (
        "source_failure_consecutive",
        "snapshot_validation_failure_consecutive",
        "unresolved_dependency_growth_percent",
    ):
        value = policy.get("alerts", {}).get(field)
        if not isinstance(value, int) or value < 1:
            errors.append(f"alerts.{field} must be a positive integer")

    if errors:
        raise ValidationError("\n".join(errors))
    return {"sources": len(configured_sources)}


def main() -> int:
    try:
        counts = validate()
    except (OSError, KeyError, TypeError, ValueError, ValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Validated refresh policy for {counts['sources']} sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
