import json
import tempfile
import unittest
from pathlib import Path

from tools.build_catalog_views import build


class CatalogViewTests(unittest.TestCase):
    def test_library_candidates_are_snapshot_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = {"snapshot": {"id": "fixture"}, "entities": [
                {"id": "package:test:libalpha", "kind": "package", "name": "libalpha", "applicability": {"repository": "msys"}, "properties": {"version": "1"}},
                {"id": "package:test:app", "kind": "package", "name": "app", "applicability": {"repository": "msys"}, "properties": {"version": "1"}},
            ], "relationships": [{"type": "runtime-depends-on", "source": "package:test:app", "target": "package:test:libalpha"}]}
            source = root / "catalog.json"; source.write_text(json.dumps(catalog))
            self.assertEqual(build(source, root)["candidates"], 1)
            view = json.loads((root / "library-candidates.json").read_text())
            self.assertEqual(view["candidates"][0]["declared_runtime_dependents"], 1)
            impact = json.loads((root / "reverse-dependency-impact.json").read_text())
            self.assertEqual(impact["packages"][0]["name"], "libalpha")


if __name__ == "__main__":
    unittest.main()
