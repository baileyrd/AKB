#!/usr/bin/env python3
"""A dependency-free JSON Schema checker for this repository's own schemas.

`model/schema/*.schema.json` existed from the first commit and were never
executed: `jsonschema` is imported nowhere, so the constraints they express
were documentation rather than enforcement.

This repository has no dependency manifest and CI installs nothing, which is
a deliberate property rather than an oversight — see
`charter/adr/0002-dependency-free-schema-checking.md`. So rather than adding
a runtime dependency to run three schemas, this implements the closed subset
of JSON Schema those three actually use:

    type, properties, required, additionalProperties, items, $ref,
    enum, const, pattern, minLength, minimum, minItems, uniqueItems, format

It is **not** a general JSON Schema implementation. Constructs outside that
list — `oneOf`, `allOf`, `not`, `patternProperties`, external `$ref` — are
rejected loudly by `assert_supported()` rather than silently ignored, so a
schema that grows past this subset fails the build instead of quietly
becoming unenforced again.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "model" / "schema"

SUPPORTED = {
    "type", "properties", "required", "additionalProperties", "items", "$ref",
    "enum", "const", "pattern", "minLength", "minimum", "minItems",
    "uniqueItems", "format",
    # Annotations, carried but not enforced.
    "$schema", "$id", "$defs", "title", "description", "default", "examples",
}

TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "null": type(None),
}

DATE_TIME = re.compile(
    r"\A\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})\Z"
)


class SchemaError(Exception):
    """Raised when a schema uses a construct this checker does not implement."""


def assert_supported(schema, where="#"):
    """Fail loudly on any construct outside the implemented subset."""
    if isinstance(schema, dict):
        for key, value in schema.items():
            if key not in SUPPORTED:
                raise SchemaError(f"{where}: unsupported schema keyword {key!r}")
            if key == "$ref" and not str(value).startswith("#/$defs/"):
                raise SchemaError(f"{where}: only #/$defs/ refs are supported, got {value!r}")
            if key in ("properties", "$defs"):
                for name, sub in value.items():
                    assert_supported(sub, f"{where}/{key}/{name}")
            elif key == "items":
                assert_supported(value, f"{where}/items")
            elif key == "additionalProperties" and isinstance(value, dict):
                assert_supported(value, f"{where}/additionalProperties")


def matches_type(value, expected) -> bool:
    names = expected if isinstance(expected, list) else [expected]
    for name in names:
        if name == "integer":
            if isinstance(value, int) and not isinstance(value, bool):
                return True
        elif name == "number":
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return True
        elif name in TYPES and isinstance(value, TYPES[name]):
            # bool is a subclass of int; keep "string"/"object" honest anyway.
            if name != "boolean" and isinstance(value, bool):
                continue
            return True
    return False


def check(instance, schema, root, path="$") -> list[str]:
    """Return a list of human-readable violations."""
    if "$ref" in schema:
        target = schema["$ref"].split("/")[-1]
        resolved = root.get("$defs", {}).get(target)
        if resolved is None:
            return [f"{path}: unresolvable $ref {schema['$ref']}"]
        return check(instance, resolved, root, path)

    errors: list[str] = []

    if "type" in schema and not matches_type(instance, schema["type"]):
        return [f"{path}: expected type {schema['type']}, got {type(instance).__name__}"]

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match pattern {schema['pattern']!r}")
        if schema.get("format") == "date-time" and not DATE_TIME.match(instance):
            errors.append(f"{path}: {instance!r} is not an RFC 3339 date-time")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} below minimum {schema['minimum']}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                errors += check(value, properties[key], root, f"{path}.{key}")
            elif extra is False:
                errors.append(f"{path}: additional property {key!r} is not allowed")
            elif isinstance(extra, dict):
                errors += check(value, extra, root, f"{path}.{key}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if schema.get("uniqueItems") and len(instance) != len({json.dumps(i, sort_keys=True) for i in instance}):
            errors.append(f"{path}: items are not unique")
        if "items" in schema:
            for index, item in enumerate(instance):
                errors += check(item, schema["items"], root, f"{path}[{index}]")

    return errors


def load_schema(name: str) -> dict:
    schema = json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))
    assert_supported(schema, f"{name}.schema.json")
    return schema


def check_file(instance_path: Path, schema_name: str) -> list[str]:
    schema = load_schema(schema_name)
    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    return check(instance, schema, schema, instance_path.name)


# Instance files paired with the schema each must satisfy.
PAIRS = [
    (ROOT / "model" / "graph.json", "architecture-graph"),
    (ROOT / "model" / "catalog" / "current.json", "architecture-graph"),
    (ROOT / "model" / "inventory" / "current.json", "deep-inventory"),
    (ROOT / "model" / "runtime" / "current.json", "runtime-observation"),
]


def main() -> int:
    failures = 0
    for path, schema_name in PAIRS:
        if not path.is_file():
            print(f"skip  {path.relative_to(ROOT)} (not present)")
            continue
        errors = check_file(path, schema_name)
        if errors:
            failures += 1
            print(f"FAIL  {path.relative_to(ROOT)} against {schema_name}", file=sys.stderr)
            for error in errors[:25]:
                print(f"        {error}", file=sys.stderr)
            if len(errors) > 25:
                print(f"        ... and {len(errors) - 25} more", file=sys.stderr)
        else:
            print(f"ok    {path.relative_to(ROOT)} against {schema_name}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
