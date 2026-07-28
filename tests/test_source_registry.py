import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SourceRegistryTests(unittest.TestCase):
    def test_primary_sources_are_unique_and_https(self):
        registry = json.loads((ROOT / "evidence" / "source-registry.json").read_text())
        sources = registry["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertEqual(len({item["id"] for item in sources}), len(sources))
        self.assertTrue(all(item["class"] == "primary" and item["locator"].startswith("https://") for item in sources))

if __name__ == "__main__":
    unittest.main()
