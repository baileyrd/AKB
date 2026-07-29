import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"


class DiagramTests(unittest.TestCase):
    def test_linked_diagrams_are_well_formed_and_have_explorer_routes(self):
        diagrams = sorted((ROOT / "diagrams").glob("*.svg"))
        self.assertGreaterEqual(len(diagrams), 3)
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


if __name__ == "__main__":
    unittest.main()
