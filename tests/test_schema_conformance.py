"""Cover `tools/schema_check.py` and hold the model to its own schemas.

The schemas sat unexecuted from the first commit, so these tests do two
jobs: prove the checker actually rejects what it claims to reject, and hold
the shipped model files against the schemas that describe them.

See `charter/adr/0002-dependency-free-schema-checking.md` for why this is a
subset implementation rather than the `jsonschema` package.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import schema_check as sc  # noqa: E402


def errs(instance, schema, root=None):
    return sc.check(instance, schema, root if root is not None else schema)


class CheckerBehaviourTests(unittest.TestCase):
    """A validator that never fails is worse than none, so prove it fails."""

    def test_type_mismatch(self):
        self.assertTrue(errs(5, {"type": "string"}))
        self.assertFalse(errs("five", {"type": "string"}))

    def test_boolean_is_not_an_integer(self):
        """bool subclasses int in Python; the schema meaning must not."""
        self.assertTrue(errs(True, {"type": "integer"}))
        self.assertFalse(errs(3, {"type": "integer"}))

    def test_required_and_additional_properties(self):
        schema = {
            "type": "object",
            "required": ["a"],
            "additionalProperties": False,
            "properties": {"a": {"type": "string"}},
        }
        self.assertTrue(errs({}, schema))
        self.assertTrue(errs({"a": "x", "b": 1}, schema))
        self.assertFalse(errs({"a": "x"}, schema))

    def test_enum_const_pattern_and_min_length(self):
        self.assertTrue(errs("d", {"enum": ["a", "b"]}))
        self.assertTrue(errs("x", {"const": "y"}))
        self.assertTrue(errs("A!", {"pattern": "^[a-z]+$"}))
        self.assertTrue(errs("", {"minLength": 1}))

    def test_date_time_format(self):
        self.assertFalse(errs("2026-08-02T00:00:00Z", {"type": "string", "format": "date-time"}))
        self.assertTrue(errs("2026-08-02", {"type": "string", "format": "date-time"}))

    def test_array_constraints(self):
        self.assertTrue(errs([], {"type": "array", "minItems": 1}))
        self.assertTrue(errs([1, 1], {"type": "array", "uniqueItems": True}))
        self.assertTrue(errs([1, "x"], {"type": "array", "items": {"type": "integer"}}))

    def test_internal_ref_resolution(self):
        root = {"$defs": {"name": {"type": "string", "minLength": 2}}}
        self.assertTrue(errs("a", {"$ref": "#/$defs/name"}, root))
        self.assertFalse(errs("ab", {"$ref": "#/$defs/name"}, root))

    def test_nested_errors_carry_a_path(self):
        schema = {"type": "object", "properties": {"a": {"type": "object", "properties": {"b": {"type": "integer"}}}}}
        (message,) = errs({"a": {"b": "no"}}, schema)
        self.assertIn("$.a.b", message)


class UnsupportedConstructTests(unittest.TestCase):
    """Silent under-checking is the failure mode this guards against."""

    def test_unknown_keyword_is_rejected(self):
        for keyword in ("oneOf", "allOf", "not", "patternProperties"):
            with self.assertRaises(sc.SchemaError, msg=keyword):
                sc.assert_supported({keyword: {}})

    def test_external_ref_is_rejected(self):
        with self.assertRaises(sc.SchemaError):
            sc.assert_supported({"$ref": "https://example.com/other.schema.json"})

    def test_shipped_schemas_stay_inside_the_subset(self):
        for name in ("architecture-graph", "deep-inventory", "runtime-observation"):
            sc.load_schema(name)


class ModelConformanceTests(unittest.TestCase):
    def test_every_shipped_model_file_conforms(self):
        failures = []
        for path, schema_name in sc.PAIRS:
            if not path.is_file():
                continue
            for error in sc.check_file(path, schema_name):
                failures.append(f"{path.name} vs {schema_name}: {error}")
        self.assertEqual(failures[:20], [], f"{len(failures)} schema violations")

    def test_identifier_valued_properties_resolve(self):
        """packaged_as sits in free-form properties and is otherwise unchecked."""
        sys.path.insert(0, str(ROOT / "tools"))
        import akb

        graph = akb.load_composed_graph()
        known = {entity["id"] for entity in graph["entities"]}
        unresolved = [
            f"{entity['id']} -> {entity['properties']['packaged_as']}"
            for entity in graph["entities"]
            if (entity.get("properties") or {}).get("packaged_as")
            and entity["properties"]["packaged_as"] not in known
        ]
        self.assertEqual(unresolved, [])


if __name__ == "__main__":
    unittest.main()
