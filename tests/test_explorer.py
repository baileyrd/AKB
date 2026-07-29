from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("explorer", ROOT / "tools" / "build_explorer.py")
assert spec and spec.loader
EXPLORER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(EXPLORER)


class ExplorerTests(unittest.TestCase):
    def test_routes_are_url_safe_and_stable(self) -> None:
        self.assertEqual(EXPLORER.route_for("runtime:msys2:msys-2.0.dll"), "#/object/runtime%3Amsys2%3Amsys-2.0.dll")

    def test_build_includes_all_entity_routes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            graph = EXPLORER.load_graph()
            [path] = EXPLORER.build(graph, Path(directory))
            rendered = path.read_text(encoding="utf-8")
        for item in graph["entities"]:
            self.assertIn(EXPLORER.route_for(item["id"]), rendered)
        self.assertIn('id="search"', rendered)
        self.assertIn('aria-label="Breadcrumb"', rendered)


if __name__ == "__main__":
    unittest.main()
