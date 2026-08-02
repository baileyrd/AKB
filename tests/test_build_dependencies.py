"""Cover repository-database parsing of build-time and check-time dependencies.

The catalog projection carried four relationship types and none of them was a
build-time edge, because `import_repository_db.py` read `%DEPENDS%` and
`%OPTDEPENDS%` from each `desc` record and dropped `%MAKEDEPENDS%` and
`%CHECKDEPENDS%`. A test framework is a `checkdepends` and never a runtime
dependency, so ten of them recorded one dependent between them and every
dependency ranking in this knowledge base was blind to half the graph.

`tools/import_repository_db.py` now reads both fields, and these tests hold
that. The *projection* built from them has since been superseded: reading the
PKGBUILDs directly resolves virtual provides such as `${MINGW_PACKAGE_PREFIX}-cc`,
which the database importer had to drop, so no package had a build edge to its
own compiler. See `tests/test_recipe_dependencies.py` and
`model/recipe-dependencies/README.md`. The database path is kept for hosts
without the recipe trees, so its parsing stays covered here.
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


if __name__ == "__main__":
    unittest.main()
