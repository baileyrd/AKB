from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.collect_recipe_tree import RecipeTreeError, collect
from tools.import_deep_inventory import build_projection, verify_input


class RecipeTreeCollectionTests(unittest.TestCase):
    def test_collects_hashed_recipes_in_inventory_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = root / "sample" / "PKGBUILD"
            recipe.parent.mkdir()
            recipe.write_text(
                "pkgname=sample\npkgver=1\npkgrel=1\n"
                "source=('https://example.invalid/sample.tar.gz')\n"
                "sha256sums=('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')\n",
                encoding="utf-8",
            )
            output = root / "output"
            manifest = collect(root, output)
            verified, records = verify_input(output)
            projection, unresolved = build_projection(
                verified, records, "fixture", {"package:msys2:sample"}
            )
        self.assertEqual(manifest["scope"], "recipe-source-tree")
        self.assertEqual(verified["recipe_count"], 1)
        self.assertEqual(len(records["recipes.jsonl"]), 1)
        self.assertEqual(records["recipes.jsonl"][0]["path"], "sample/PKGBUILD")
        self.assertEqual(len(records["recipes.jsonl"][0]["recipe_sha256"]), 64)
        self.assertEqual(unresolved, [])
        self.assertIn("packaged-by", {item["type"] for item in projection["relationships"]})

    def test_requires_recipe_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RecipeTreeError, "no PKGBUILD"):
                collect(root, root / "output")


if __name__ == "__main__":
    unittest.main()
