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


class ArrayParsingTests(unittest.TestCase):
    """Four defects that between them dropped 2,033 declarations."""

    def parse(self, text):
        path = Path(self.enterContext(__import__("tempfile").TemporaryDirectory()))
        recipe = path / "PKGBUILD"
        recipe.write_text(text, encoding="utf-8")
        return deep_inventory.parse_pkgbuild(recipe)

    def test_elements_after_a_command_substitution_survive(self):
        """The worst of the four: a non-greedy scan to the first `)` truncated
        the array, silently losing every element after it."""
        parsed = self.parse(
            'makedepends=(a b $([[ ${CARCH} == aarch64 ]] || echo c) d e)\n'
        )
        self.assertEqual(parsed["makedepends"], ["a", "b", "d", "e"])

    def test_the_conditional_itself_is_dropped_and_counted(self):
        """Its dependency is real but conditional; recording it
        unconditionally would assert something false on the other arch."""
        parsed = self.parse('makedepends=(a $([[ x ]] || echo nasm) b)\n')
        self.assertNotIn("nasm", parsed["makedepends"])
        self.assertEqual(parsed["conditional_spans_dropped"], 1)

    def test_comments_inside_an_array_are_not_dependencies(self):
        parsed = self.parse(
            'makedepends=(\n  "one"\n'
            '  # Note: the following are carried from vtk\n'
            '  "two"\n)\n'
        )
        self.assertEqual(parsed["makedepends"], ["one", "two"])

    def test_an_apostrophe_in_a_comment_does_not_swallow_the_array(self):
        """`#"...-ruby" unable to find ruby's pkgconfig file` opened a phantom
        single quote that ate the closing paren, so the whole array was lost."""
        parsed = self.parse(
            'makedepends=("one"\n'
            "             #\"two\" unable to find ruby's pkgconfig file\n"
            '             "three")\n'
        )
        self.assertEqual(parsed["makedepends"], ["one", "three"])

    def test_recipe_local_arrays_are_captured_for_splicing(self):
        parsed = self.parse('_extra=(alpha beta)\nmakedepends=(cc "${_extra[@]}")\n')
        self.assertEqual(parsed["local_arrays"]["_extra"], ["alpha", "beta"])

    def test_shell_keywords_never_become_dependencies(self):
        parsed = self.parse("makedepends=(real && echo || fi [[ ]])\n")
        self.assertEqual(parsed["makedepends"], ["real"])

    def test_an_unterminated_array_reports_nothing(self):
        """Better to record none than to guess where it ended."""
        parsed = self.parse('makedepends=("one" "two"\n')
        self.assertNotIn("two", parsed["makedepends"])


class SpliceAndBraceTests(unittest.TestCase):
    def test_array_splice_resolves_against_the_recipe(self):
        recipe = {
            "pkgname": ["p"], "checkdepends": ["boost"],
            "makedepends": ["cc", "${checkdepends[@]}"], "variables": {},
        }
        packages = {"p": "package:msys2:p", "cc": "package:msys2:cc",
                    "boost": "package:msys2:boost"}
        projection, stats, _ = self._project(recipe, packages)
        targets = {e["target"] for e in projection["relationships"]}
        self.assertIn("package:msys2:boost", targets)
        self.assertEqual(stats["array_splices_resolved"], 1)

    def test_brace_expansion_becomes_several_dependencies(self):
        self.assertEqual(
            sorted(ird.expand_braces("p-{build,installer}")),
            ["p-build", "p-installer"],
        )
        self.assertEqual(ird.expand_braces("plain"), ["plain"])

    def _project(self, recipe, packages):
        original = ird.catalog_index
        ird.catalog_index = lambda: (packages, {})
        try:
            return ird.project([recipe])
        finally:
            ird.catalog_index = original


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

    def test_unresolved_endpoints_never_reach_the_composed_graph(self):
        """The catalog refreshes independently of this projection and can
        retire a package an edge still names -- upstream trimming
        mingw-w64-i686-* out of the mingw32 repository is the first observed
        case. `akb.load_composed_graph` re-checks the invariant
        `import_recipe_dependencies.py` enforces at generation time and
        drops any edge that no longer resolves, so nothing dangling should
        ever leak into validation, generation, or the explorer.
        """
        import akb  # pylint: disable=import-outside-toplevel

        packages, _ = ird.catalog_index()
        known = set(packages.values())
        composed_ids = {edge["id"] for edge in akb.load_composed_graph()["relationships"]}
        leaked = [
            edge for edge in self.edges
            if (edge["source"] not in known or edge["target"] not in known)
            and edge["id"] in composed_ids
        ]
        self.assertEqual(leaked, [])

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
