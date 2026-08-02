from __future__ import annotations

import importlib.util
import tempfile
import time
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
            index, d3_file, svg, text = EXPLORER.build(graph, Path(directory))
            rendered = index.read_text(encoding="utf-8")
            rendered_svg = svg.read_text(encoding="utf-8")
            rendered_text = text.read_text(encoding="utf-8")
            d3_file_exists = d3_file.is_file()
        for item in graph["entities"]:
            self.assertIn(EXPLORER.route_for(item["id"]), rendered)
            self.assertIn(item["id"], rendered_text)
        self.assertIn('id="search"', rendered)
        self.assertIn('aria-label="Breadcrumb"', rendered)
        self.assertIn('class="expand"', rendered)
        self.assertIn('Collapse relationships', rendered)
        self.assertIn('Dependencies', rendered)
        self.assertIn('Dependents', rendered)
        self.assertIn('isDependency', rendered)
        self.assertIn("const viewRoute", rendered)
        for name in ("layers", "packages", "artifacts", "libraries", "runtimes", "toolchains", "repositories", "evidenced"):
            self.assertIn(f"{name}:", rendered)
        self.assertIn("Observed properties", rendered)
        self.assertIn("Evidence", rendered)
        self.assertIn("objectDetails", rendered)
        self.assertIn('role="img"', rendered_svg)
        self.assertIn('<desc id="description">', rendered_svg)
        self.assertIn('tabindex="0"', rendered_svg)
        self.assertTrue(d3_file_exists)
        self.assertIn('<script src="d3.v7.min.js"></script>', rendered)
        self.assertIn("d3.forceSimulation", rendered)
        self.assertIn("function renderGraph", rendered)
        self.assertIn("graphNodeRoute", rendered)
        self.assertIn("graphViewRoute", rendered)
        self.assertIn("View in graph", rendered)
        self.assertIn("__all__", rendered)
        self.assertIn("GRAPH_NODE_CAP", rendered)

    def test_large_graph_build_is_bounded_and_complete(self) -> None:
        entities = [
            {"id": f"package:test:node-{number:04d}", "kind": "package",
             "name": f"Node {number:04d}", "status": "partial",
             "aliases": [], "tags": [], "summary": ""}
            for number in range(2000)
        ]
        relationships = [
            {"id": f"relationship:test:{number:04d}", "type": "runtime-depends-on",
             "source": entities[number % len(entities)]["id"],
             "target": entities[(number + 1) % len(entities)]["id"]}
            for number in range(4000)
        ]
        started = time.perf_counter()
        with tempfile.TemporaryDirectory() as directory:
            index, d3_file, svg, text = EXPLORER.build(
                {"entities": entities, "relationships": relationships}, Path(directory)
            )
            rendered = index.read_text(encoding="utf-8")
            fallback = text.read_text(encoding="utf-8")
            svg_text = svg.read_text(encoding="utf-8")
            d3_file_exists = d3_file.is_file()
        self.assertLess(time.perf_counter() - started, 10.0)
        self.assertIn(EXPLORER.route_for(entities[-1]["id"]), rendered)
        self.assertIn(entities[-1]["id"], fallback)
        self.assertLess(svg_text.count('<rect '), 81)
        self.assertTrue(d3_file_exists)

    def test_vendor_d3_source_file_exists_and_is_named_correctly(self) -> None:
        self.assertTrue(EXPLORER.VENDOR_D3.is_file())
        first_line = EXPLORER.VENDOR_D3.read_text(encoding="utf-8").split("\n", 1)[0]
        self.assertIn("d3js.org", first_line)

    def test_vendor_d3_is_copied_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            graph = EXPLORER.load_graph()
            _, d3_file, _, _ = EXPLORER.build(graph, Path(directory))
            self.assertEqual(d3_file.read_bytes(), EXPLORER.VENDOR_D3.read_bytes())


if __name__ == "__main__":
    unittest.main()
