from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "import_package_catalog.py"
SPEC = importlib.util.spec_from_file_location("catalog_import", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CatalogImportTests(unittest.TestCase):
    def test_input_integrity_and_count(self) -> None:
        fixture = ROOT / "tests" / "fixtures" / "catalog"
        manifest, packages, edges = MODULE.verify_input(fixture)
        self.assertEqual(manifest["package_count"], 4)
        self.assertEqual(len(packages), 4)
        self.assertEqual(len(edges), 5)

    def test_build_catalog_resolves_and_reports_dependencies(self) -> None:
        fixture = ROOT / "tests" / "fixtures" / "catalog"
        manifest, packages, edges = MODULE.verify_input(fixture)
        catalog, unresolved = MODULE.build_catalog(
            manifest, packages, edges, "fixture-snapshot"
        )

        self.assertEqual(
            len([x for x in catalog["entities"] if x["kind"] == "package"]), 4
        )
        self.assertEqual(
            len([x for x in catalog["entities"] if x["kind"] == "repository"]), 2
        )
        self.assertEqual(len(unresolved), 2)
        self.assertGreaterEqual(
            {edge["type"] for edge in catalog["relationships"]},
            {"published-in", "belongs-to-environment", "runtime-depends-on"},
        )

    def test_change_detection(self) -> None:
        previous = {
            "snapshot": {"id": "old"},
            "entities": [
                {
                    "id": "package:msys2:a",
                    "kind": "package",
                    "properties": {"version": "1"},
                },
                {
                    "id": "package:msys2:b",
                    "kind": "package",
                    "properties": {"version": "1"},
                },
            ],
        }
        current = {
            "snapshot": {"id": "new"},
            "entities": [
                {
                    "id": "package:msys2:b",
                    "kind": "package",
                    "properties": {"version": "2"},
                },
                {
                    "id": "package:msys2:c",
                    "kind": "package",
                    "properties": {"version": "1"},
                },
            ],
        }
        changes = MODULE.make_changes(previous, current)
        self.assertEqual(changes["added"], ["package:msys2:c"])
        self.assertEqual(changes["removed"], ["package:msys2:a"])
        self.assertEqual(
            changes["updated"],
            [{"id": "package:msys2:b", "from": "1", "to": "2"}],
        )


if __name__ == "__main__":
    unittest.main()
