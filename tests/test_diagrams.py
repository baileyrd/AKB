import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"


class DiagramTests(unittest.TestCase):
    def test_linked_diagrams_are_well_formed_and_have_explorer_routes(self):
        diagrams = sorted((ROOT / "diagrams").glob("*.svg"))
        self.assertGreaterEqual(len(diagrams), 2)
        for path in diagrams:
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, SVG + "svg")
            links = root.findall(".//" + SVG + "a")
            self.assertTrue(links, path.name)
            for link in links:
                href = link.get("href") or link.get(XLINK)
                self.assertIn("generated/explorer/index.html#/", href or "")


if __name__ == "__main__":
    unittest.main()
