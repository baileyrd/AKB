"""Cover the zoomable graph view in the explorer page.

The explorer had stable routes, filters, progressive expansion, and an
accessible SVG overview, but no interactive rendering: the overview was a
fixed-size static picture of the first eighty objects and there was no way to
look at one object's neighbourhood at any magnification.

Three properties are worth holding, and they are what these tests check.

1. **Zero dependencies.** The repository has no dependency manifest and CI has
   no install step (ADR 0002). A graph view that pulls in a layout library
   would break that, so the viewBox is the entire zoom model.
2. **Pointer gestures are not an interface.** Wheel-and-drag alone excludes
   keyboard and assistive-technology users, so buttons and key handlers are
   required, not optional.
3. **The textual equivalent stays complete.** The figure is bounded for
   legibility; the list below it is not, and the caption discloses the
   difference.
"""

from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "explorer_graph", ROOT / "tools" / "build_explorer.py"
)
assert spec and spec.loader
EXPLORER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(EXPLORER)

SMALL = {
    "entities": [
        {"id": "library:test:subject", "kind": "library", "name": "Subject",
         "status": "partial", "aliases": [], "tags": [], "summary": ""},
        {"id": "library:test:dep", "kind": "library", "name": "Dependency",
         "status": "partial", "aliases": [], "tags": [], "summary": ""},
        {"id": "library:test:user", "kind": "library", "name": "Dependent",
         "status": "partial", "aliases": [], "tags": [], "summary": ""},
    ],
    "relationships": [
        {"id": "relationship:test:a", "type": "runtime-depends-on",
         "source": "library:test:subject", "target": "library:test:dep"},
        {"id": "relationship:test:b", "type": "runtime-depends-on",
         "source": "library:test:user", "target": "library:test:subject"},
    ],
}


def rendered(graph=SMALL) -> str:
    with tempfile.TemporaryDirectory() as directory:
        index, _, _ = EXPLORER.build(graph, Path(directory))
        return index.read_text(encoding="utf-8")


class GraphViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = rendered()

    def test_the_route_exists_and_object_pages_link_to_it(self):
        self.assertIn("'#/graph/'", self.page)
        self.assertIn("hash.startsWith('#/graph/')", self.page)
        self.assertIn("View this object's dependency graph", self.page)

    def test_zoom_is_viewbox_arithmetic_with_no_library(self):
        """A dependency here would break the zero-dependency posture."""
        self.assertIn("setAttribute('viewBox'", self.page)
        for forbidden in ("<script src", "cdn.", "import(", "require("):
            self.assertNotIn(forbidden, self.page, forbidden)

    def test_pointer_gestures_have_keyboard_and_button_equivalents(self):
        for control in ("zoom-in", "zoom-out", "zoom-reset"):
            self.assertIn(f'id="{control}"', self.page, control)
        self.assertIn("role=\"group\" aria-label=\"Zoom controls\"", self.page)
        for key in ("ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"):
            self.assertIn(key, self.page, key)
        self.assertIn("addEventListener('keydown'", self.page)

    def test_the_figure_is_labelled_and_focusable(self):
        for fragment in ('id="graph"', 'aria-labelledby="gtitle gdesc"',
                         '<desc id="gdesc">', '<title id="gtitle">',
                         'role="img" tabindex="0"'):
            self.assertTrue(fragment in self.page, f"missing: {fragment}")

    def test_the_textual_equivalent_is_present_and_named(self):
        self.assertIn("Textual equivalent", self.page)
        self.assertIn("accessible fallback", self.page)

    def test_the_figure_is_bounded_and_the_bound_is_disclosed(self):
        self.assertIn("GRAPH_LIMIT", self.page)
        limit = re.search(r"const GRAPH_LIMIT = (\d+)", self.page)
        self.assertIsNotNone(limit)
        self.assertLessEqual(int(limit.group(1)), 40)
        self.assertIn("omitted from the figure for legibility", self.page)

    def test_layout_is_deterministic(self):
        """The same graph must produce the same page, byte for byte."""
        self.assertEqual(rendered(), rendered())

    def test_neighbourhood_ordering_is_stated_as_sorted(self):
        """An unsorted neighbourhood would redraw differently each build."""
        self.assertIn(".sort(", self.page)

    def test_zoom_is_clamped(self):
        """Unbounded zoom lets a user lose the figure entirely."""
        self.assertIn("Math.min(base[2] * 4", self.page)
        self.assertIn("Math.max(base[2] / 8", self.page)

    def test_the_static_overview_and_fallback_survive(self):
        """The new view is additional, not a replacement."""
        with tempfile.TemporaryDirectory() as directory:
            _, svg, text = EXPLORER.build(SMALL, Path(directory))
            self.assertIn('role="img"', svg.read_text(encoding="utf-8"))
            self.assertIn("Relationships", text.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
