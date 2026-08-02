import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"


class DiagramTests(unittest.TestCase):
    def test_linked_diagrams_are_well_formed_and_have_explorer_routes(self):
        diagrams = sorted((ROOT / "diagrams").glob("*.svg"))
        self.assertGreaterEqual(len(diagrams), 8)
        for path in diagrams:
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, SVG + "svg")
            links = root.findall(".//" + SVG + "a")
            self.assertTrue(links, path.name)
            for link in links:
                href = link.get("href") or link.get(XLINK)
                self.assertIn("generated/explorer/index.html#/", href or "")

    def test_level_two_diagram_covers_runtime_and_package_routes(self):
        diagram = (ROOT / "diagrams" / "level-2-runtime-package-flow.svg").read_text(encoding="utf-8")
        for route in ("#/view/repositories", "#/view/artifacts", "environment%3Amsys2%3Aucrt64"):
            self.assertIn(route, diagram)

    def test_level_three_diagram_distinguishes_msys_and_native_routes(self):
        diagram = (ROOT / "diagrams" / "level-3-msys-runtime-boundary.svg").read_text(encoding="utf-8")
        for route in ("runtime%3Amsys2%3Amsys-2.0.dll", "environment%3Amsys2%3Amsys", "#/view/runtimes"):
            self.assertIn(route, diagram)

    def test_level_four_diagram_links_all_environment_objects(self):
        diagram = (ROOT / "diagrams" / "level-4-environment-matrix.svg").read_text(encoding="utf-8")
        for environment in ("msys", "ucrt64", "clang64", "clangarm64", "mingw64", "mingw32"):
            self.assertIn(f"environment%3Amsys2%3A{environment}", diagram)

    def test_level_five_diagram_links_evidence_and_artifact_views(self):
        diagram = (ROOT / "diagrams" / "level-5-package-artifact-evidence.svg").read_text(encoding="utf-8")
        for route in ("#/view/repositories", "#/view/artifacts", "#/view/evidenced"):
            self.assertIn(route, diagram)

    def test_level_six_diagram_links_toolchain_and_artifact_views(self):
        diagram = (ROOT / "diagrams" / "level-6-toolchain-build-flow.svg").read_text(encoding="utf-8")
        for route in ("#/view/toolchains", "#/view/artifacts", "#/view/evidenced"):
            self.assertIn(route, diagram)

    def test_level_seven_diagram_links_userland_and_runtime_views(self):
        diagram = (ROOT / "diagrams" / "level-7-userland-applications.svg").read_text(encoding="utf-8")
        for route in ("environment%3Amsys2%3Amsys", "#/view/packages", "#/view/runtimes"):
            self.assertIn(route, diagram)

    def test_every_view_a_diagram_links_to_resolves_to_objects(self):
        """A shipped hyperlink must not land on an empty projection.

        Asserting only that a link is present lets a diagram ship pointing at
        a view that renders nothing; the toolchains view shipped that way
        because it projected by an entity kind the graph never emits.
        """
        import sys

        sys.path.insert(0, str(ROOT / "tools"))
        sys.path.insert(0, str(ROOT / "tests"))
        import akb
        from test_roadmap_claims import EXPLORER_VIEWS, view_members

        graph = akb.load_composed_graph()
        linked = set()
        for path in sorted((ROOT / "diagrams").glob("*.svg")):
            for match in re.finditer(r"#/view/([a-z-]+)", path.read_text(encoding="utf-8")):
                linked.add((path.name, match.group(1)))
        self.assertTrue(linked, "no diagram links to any view")

        empty = []
        for diagram, view in sorted(linked):
            if view == "evidenced":
                members = [e for e in graph["entities"] if e.get("evidence_refs")]
            else:
                self.assertIn(view, EXPLORER_VIEWS, f"{diagram} links to unknown view '{view}'")
                members = view_members(graph, view)
            if not members:
                empty.append(f"{diagram} -> #/view/{view}")
        self.assertEqual(
            empty,
            [],
            "diagrams link to views that render no objects:\n  " + "\n  ".join(empty),
        )


if __name__ == "__main__":
    unittest.main()
