"""Cover the build-time and check-time dependency projection.

The catalog projection carried four relationship types and none of them was a
build-time edge, because `import_repository_db.py` read `%DEPENDS%` and
`%OPTDEPENDS%` from each `desc` record and dropped `%MAKEDEPENDS%` and
`%CHECKDEPENDS%`. A test framework is a `checkdepends` and never a runtime
dependency, so ten of them recorded one dependent between them and every
dependency ranking in this knowledge base was blind to half the graph.

These tests hold the properties that keep the fix honest:

- the two fields are actually parsed out of a `desc` record;
- the projection is *additive* -- relationships only, no entities, no versions,
  so it cannot silently restate the catalog's observations at a second date;
- an edge whose endpoint is absent from the catalog is dropped and counted
  rather than minting an entity;
- the drop is disclosed in the evidence record rather than buried.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import import_build_dependencies as ibd  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "repository_db", ROOT / "tools" / "import_repository_db.py"
)
assert spec and spec.loader
REPO_DB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(REPO_DB)

DESC = b"""%NAME%
example

%VERSION%
1.0-1

%ARCH%
any

%DEPENDS%
zlib
libfoo>=2.0

%OPTDEPENDS%
bar: for bar support

%MAKEDEPENDS%
cmake
ninja>=1.11

%CHECKDEPENDS%
gtest
"""


class DescParsingTests(unittest.TestCase):
    def test_repository_db_now_reads_both_dropped_fields(self):
        fields = REPO_DB.parse_desc(DESC)
        self.assertEqual(fields["MAKEDEPENDS"], ["cmake", "ninja>=1.11"])
        self.assertEqual(fields["CHECKDEPENDS"], ["gtest"])

    def test_repository_db_emits_build_and_check_edges(self):
        _, edges = REPO_DB.package_rows(REPO_DB.parse_desc(DESC), "msys")
        by_type = {}
        for edge in edges:
            by_type.setdefault(edge["relationship"], []).append(edge["target_package"])
        self.assertEqual(sorted(by_type["build-depends-on"]), ["cmake", "ninja"])
        self.assertEqual(by_type["check-depends-on"], ["gtest"])
        # The pre-existing behaviour must be unchanged.
        self.assertEqual(sorted(by_type["runtime-depends-on"]), ["libfoo", "zlib"])

    def test_repository_db_carries_the_fields_into_the_package_row(self):
        package, _ = REPO_DB.package_rows(REPO_DB.parse_desc(DESC), "msys")
        self.assertEqual(package["build_dependencies"], "cmake;ninja>=1.11")
        self.assertEqual(package["check_dependencies"], "gtest")

    def test_catalog_importer_accepts_the_new_relations(self):
        source = (ROOT / "tools" / "import_package_catalog.py").read_text(encoding="utf-8")
        self.assertIn('"build-depends-on"', source)
        self.assertIn('"check-depends-on"', source)

    def test_version_constraints_are_split_off_the_name(self):
        self.assertEqual(ibd.dependency_name("ninja>=1.11"), ("ninja", ">=1.11"))
        self.assertEqual(ibd.dependency_name("bar: for bar support"), ("bar", ""))
        self.assertEqual(ibd.dependency_name("plain"), ("plain", ""))


class ProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projection = json.loads(ibd.OUTPUT.read_text(encoding="utf-8"))

    def test_the_projection_is_additive(self):
        """Relationships only. Entities or claims here would restate the
        catalog's observations at a different date."""
        self.assertEqual(self.projection["entities"], [])
        self.assertEqual(self.projection["claims"], [])
        self.assertEqual(len(self.projection["evidence"]), 1)

    def test_it_contributes_only_build_and_check_edges(self):
        types = {edge["type"] for edge in self.projection["relationships"]}
        self.assertEqual(types, {"build-depends-on", "check-depends-on"})

    def test_every_endpoint_exists_in_the_catalog(self):
        catalog = ibd.catalog_package_ids()
        for edge in self.projection["relationships"]:
            self.assertIn(edge["source"], catalog, edge["id"])
            self.assertIn(edge["target"], catalog, edge["id"])

    def test_relationship_ids_are_unique(self):
        identifiers = [edge["id"] for edge in self.projection["relationships"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_the_drop_is_disclosed_in_the_evidence_record(self):
        notes = self.projection["evidence"][0]["notes"]
        self.assertIn("dropped", notes)
        self.assertIn("absent from the catalog", notes)
        self.assertIn("later than, the package catalog", notes)

    def test_it_reaches_the_composed_graph(self):
        import akb  # pylint: disable=import-outside-toplevel

        graph = akb.load_composed_graph()
        types = {edge["type"] for edge in graph["relationships"]}
        self.assertIn("build-depends-on", types)
        self.assertIn("check-depends-on", types)

    def test_the_defect_it_fixes_is_actually_fixed(self):
        """Test frameworks were invisible. They must not be again."""
        import akb  # pylint: disable=import-outside-toplevel

        graph = akb.load_composed_graph()
        gtest = "package:msys2:mingw-w64-ucrt-x86_64-gtest"
        dependents = [
            edge for edge in graph["relationships"]
            if edge["target"] == gtest and edge["type"] in
            {"build-depends-on", "check-depends-on"}
        ]
        self.assertGreater(
            len(dependents), 0,
            "gtest has no build-time dependents; the projection is not composed",
        )


if __name__ == "__main__":
    unittest.main()
