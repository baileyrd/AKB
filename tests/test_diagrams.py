import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
LEVELS = range(8)

sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))


def diagram(number):
    return (ROOT / "diagrams" / f"level-{number}.svg").read_text(encoding="utf-8")


def hrefs(number):
    root = ET.parse(ROOT / "diagrams" / f"level-{number}.svg").getroot()
    return [
        link.get("href") or link.get(XLINK) or ""
        for link in root.findall(".//" + SVG + "a")
    ]


class DiagramTests(unittest.TestCase):
    def test_every_level_emits_svg_puml_and_dot(self):
        """The charter asks for reusable Graphviz and PlantUML, not only SVG."""
        for number in LEVELS:
            for suffix in ("svg", "puml", "dot"):
                path = ROOT / "diagrams" / f"level-{number}.{suffix}"
                self.assertTrue(path.exists(), f"missing {path.name}")
                self.assertTrue(path.read_text(encoding="utf-8").strip(), f"empty {path.name}")

    def test_diagrams_are_well_formed_and_accessible(self):
        for number in LEVELS:
            root = ET.parse(ROOT / "diagrams" / f"level-{number}.svg").getroot()
            self.assertEqual(root.tag, SVG + "svg")
            self.assertEqual(root.get("role"), "img")
            self.assertTrue(root.findall(".//" + SVG + "title"))
            self.assertTrue(root.findall(".//" + SVG + "desc"))

    def test_drill_down_chain_links_parent_and_child(self):
        """The charter requires every diagram to hyperlink to related diagrams.

        The retired hand-authored set had zero diagram-to-diagram links, so the
        L0-L7 ladder existed only as filenames.
        """
        for number in LEVELS:
            links = hrefs(number)
            if number > 0:
                self.assertIn(
                    f"level-{number - 1}.svg", links, f"level-{number} does not link up"
                )
            if number < 7:
                self.assertIn(
                    f"level-{number + 1}.svg", links, f"level-{number} does not link down"
                )

    def test_every_diagram_links_to_its_canonical_page(self):
        for number in LEVELS:
            self.assertTrue(
                any(href.startswith("../docs/") for href in hrefs(number)),
                f"level-{number} does not link to a documentation page",
            )

    def test_object_nodes_use_stable_explorer_routes(self):
        for number in LEVELS:
            routes = [h for h in hrefs(number) if "explorer/index.html#/" in h]
            self.assertTrue(routes, f"level-{number} has no object routes")

    def test_capped_diagrams_disclose_the_cap(self):
        """Silent truncation reads as complete coverage."""
        for number in LEVELS:
            body = diagram(number)
            self.assertTrue(
                "objects shown" in body or "objects of this level shown" in body,
                f"level-{number} does not state its selection",
            )

    def test_diagrams_are_generated_not_hand_edited(self):
        for number in LEVELS:
            self.assertIn("tools/build_diagrams.py", diagram(number))

    def test_rebuild_is_byte_identical(self):
        """CI regenerates before `git diff --exit-code`, so output must be stable."""
        import build_diagrams

        before = {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "diagrams").glob("level-*"))
        }
        build_diagrams.build(build_diagrams.load_graph())
        after = {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "diagrams").glob("level-*"))
        }
        self.assertEqual(sorted(before), sorted(after))
        changed = [name for name in before if before[name] != after[name]]
        self.assertEqual(changed, [], f"non-deterministic output: {changed}")

    def test_every_view_a_diagram_links_to_resolves_to_objects(self):
        """A shipped hyperlink must not land on an empty projection.

        Asserting only that a link is present lets a diagram ship pointing at
        a view that renders nothing; the toolchains view shipped that way
        because it projected by an entity kind the graph never emits.
        """
        import akb
        from test_roadmap_claims import EXPLORER_VIEWS, view_members

        graph = akb.load_composed_graph()
        linked = set()
        for path in sorted((ROOT / "diagrams").glob("*.svg")):
            for match in re.finditer(r"#/view/([a-z-]+)", path.read_text(encoding="utf-8")):
                linked.add((path.name, match.group(1)))

        empty = []
        for name, view in sorted(linked):
            if view == "evidenced":
                members = [e for e in graph["entities"] if e.get("evidence_refs")]
            else:
                self.assertIn(view, EXPLORER_VIEWS, f"{name} links to unknown view '{view}'")
                members = view_members(graph, view)
            if not members:
                empty.append(f"{name} -> #/view/{view}")
        self.assertEqual(
            empty,
            [],
            "diagrams link to views that render no objects:\n  " + "\n  ".join(empty),
        )


if __name__ == "__main__":
    unittest.main()
