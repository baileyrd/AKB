"""Cover the recipe-derived build and check dependency projection.

The repository-database projection that preceded this one could not see a
package's compiler: recipes name `${MINGW_PACKAGE_PREFIX}-cc`, no package is
called that, and the database importer dropped every edge it could not resolve
to a package name. Under that projection not one package in the ecosystem had
a build edge to gcc or clang.

Reading the PKGBUILDs directly fixes that, at the cost of two problems the
database did not have -- shell interpolation in package names, and virtual
provides -- so these tests hold the handling of both, and hold the boundary
that keeps the projection additive.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import import_recipe_dependencies as ird  # noqa: E402
import deep_inventory  # noqa: E402

PKGBUILD = """# comment
pkgbase=guile
_realname=sample
pkgname=("${pkgbase}" "lib${pkgbase}" "${MINGW_PACKAGE_PREFIX}-python-${_realname}")
pkgver=1.0
makedepends=('autotools' "${MINGW_PACKAGE_PREFIX}-cc" 'gcc>=13')
checkdepends=("${MINGW_PACKAGE_PREFIX}-python-pytest")
depends=('zlib')
"""


class ParserTests(unittest.TestCase):
    def test_recipe_local_scalars_are_captured(self):
        """Without these, a package name interpolating them resolves to nothing."""
        path = Path(self.enterContext(__import__("tempfile").TemporaryDirectory()))
        recipe = path / "PKGBUILD"
        recipe.write_text(PKGBUILD, encoding="utf-8")
        parsed = deep_inventory.parse_pkgbuild(recipe)
        self.assertEqual(parsed["variables"]["_realname"], "sample")
        self.assertEqual(parsed["pkgbase"], "guile")

    def test_command_substitutions_are_not_captured_as_values(self):
        """A `_x=$(...)` is shell to execute, not a value to substitute."""
        path = Path(self.enterContext(__import__("tempfile").TemporaryDirectory()))
        recipe = path / "PKGBUILD"
        recipe.write_text("_bad=$(uname -m)\n_good=plain\n", encoding="utf-8")
        parsed = deep_inventory.parse_pkgbuild(recipe)
        self.assertNotIn("_bad", parsed["variables"])
        self.assertEqual(parsed["variables"]["_good"], "plain")


class ExpansionTests(unittest.TestCase):
    def test_prefix_and_locals_expand(self):
        variables = {"_realname": "pytest", "pkgbase": "guile"}
        self.assertEqual(
            ird.expand("${MINGW_PACKAGE_PREFIX}-python-${_realname}",
                       "mingw-w64-ucrt-x86_64", variables),
            "mingw-w64-ucrt-x86_64-python-pytest",
        )
        self.assertEqual(ird.expand("lib${pkgbase}", None, variables), "libguile")

    def test_unknown_variables_are_left_visible(self):
        """They must stay detectable so they can be dropped and counted."""
        self.assertIn("$", ird.expand("${_unknown}-thing", None, {}))

    def test_constraints_and_descriptions_are_stripped(self):
        self.assertEqual(ird.clean("gcc>=13"), "gcc")
        self.assertEqual(ird.clean("ed: for patch -e"), "ed")

    def test_shell_fragments_are_recognised(self):
        """Conditional arrays defeat static parsing; the debris must not
        become dependency names."""
        for fragment in ("]]", "||", "echo", "\\", "$([["):
            self.assertTrue(ird.SHELL_NOISE.match(fragment) or "$" in fragment, fragment)


class ProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projection = json.loads(ird.OUTPUT.read_text(encoding="utf-8"))
        cls.edges = cls.projection["relationships"]

    def test_the_projection_is_additive(self):
        self.assertEqual(self.projection["entities"], [])
        self.assertEqual(self.projection["claims"], [])
        self.assertEqual(len(self.projection["evidence"]), 1)

    def test_only_build_and_check_edges(self):
        self.assertEqual(
            {edge["type"] for edge in self.edges},
            {"build-depends-on", "check-depends-on"},
        )

    def test_every_endpoint_resolves_in_the_catalog(self):
        packages, _ = ird.catalog_index()
        known = set(packages.values())
        for edge in self.edges:
            self.assertIn(edge["source"], known, edge["id"])
            self.assertIn(edge["target"], known, edge["id"])

    def test_provides_resolution_is_disclosed_per_edge(self):
        """A reader must be able to discount virtual resolution."""
        routes = {edge["properties"]["resolved_via"] for edge in self.edges}
        self.assertTrue(routes <= {"name", "provides"}, routes)
        self.assertIn("provides", routes)

    def test_the_compiler_edge_the_database_could_not_see(self):
        """The defect that motivated reading recipes at all."""
        compilers = [
            edge for edge in self.edges
            if edge["target"].endswith((":gcc", ":clang"))
            or "-gcc" in edge["target"] or "-clang" in edge["target"]
        ]
        self.assertGreater(len(compilers), 1000, "compiler build edges are missing")

    def test_prefix_pairing_never_crosses_environments(self):
        """A UCRT64 package must not build-depend on a CLANG64 one."""
        marks = ("ucrt-x86_64", "clang-x86_64", "clang-aarch64")

        def env(identifier):
            return next((m for m in marks if m in identifier), None)

        crossed = [
            edge for edge in self.edges
            if env(edge["source"]) and env(edge["target"])
            and env(edge["source"]) != env(edge["target"])
        ]
        self.assertEqual(crossed[:3], [], f"{len(crossed)} cross-environment edges")

    def test_ids_are_unique(self):
        identifiers = [edge["id"] for edge in self.edges]
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_drops_are_disclosed_in_the_evidence_record(self):
        notes = self.projection["evidence"][0]["notes"]
        for phrase in ("Dropped and counted", "virtual provide", "without\nexecuting"):
            self.assertIn(phrase.replace("\n", " "), notes.replace("\n", " "), phrase)

    def test_it_reaches_the_composed_graph(self):
        import akb  # pylint: disable=import-outside-toplevel

        types = {edge["type"] for edge in akb.load_composed_graph()["relationships"]}
        self.assertIn("build-depends-on", types)
        self.assertIn("check-depends-on", types)

    def test_only_one_build_dependency_projection_is_composed(self):
        """Composing both sources would double-count their shared edges."""
        import akb  # pylint: disable=import-outside-toplevel

        self.assertFalse(
            (ROOT / "model" / "build-dependencies" / "current.json").exists(),
            "both build-dependency projections are present; they overlap",
        )
        self.assertTrue(akb.RECIPE_DEPENDENCIES.is_file())


if __name__ == "__main__":
    unittest.main()
