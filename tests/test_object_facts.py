"""Cover the generated object-facts block.

The companion objective asks for repetitive per-object content to be generated
rather than hand-authored. Before this, every object page restated its
subject's kind, authority, packaged version, and license in prose by hand, and
nothing checked that the prose still matched the model: `validate_docs`
verifies a `model_ref` resolves, not that the sentence beside it is still true
after a catalog refresh.

These tests hold three properties: the block is generated from the model and
not typed, it never swallows authored prose, and regenerating is a no-op.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_object_facts as bof  # noqa: E402

DOCS = sorted((ROOT / "docs").glob("*.md"))
BLOCK = re.compile(re.escape(bof.BEGIN) + r"(.*?)" + re.escape(bof.END), re.S)


def pages_with_block():
    return [p for p in DOCS if bof.BEGIN in p.read_text(encoding="utf-8")]


class ObjectFactsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = bof.load_graph()
        cls.entities = {e["id"]: e for e in cls.graph["entities"]}

    def test_the_block_reaches_most_object_pages(self):
        self.assertGreaterEqual(len(pages_with_block()), 200)

    def test_markers_are_balanced_and_unique(self):
        for path in DOCS:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count(bof.BEGIN), text.count(bof.END), path.name)
            self.assertLessEqual(text.count(bof.BEGIN), 1, path.name)

    def test_block_sits_after_the_h1_and_before_the_first_section(self):
        """Authored prose must stay below it, not be split by it."""
        for path in pages_with_block():
            text = path.read_text(encoding="utf-8")
            h1 = re.search(r"^# .*$", text, re.M)
            self.assertIsNotNone(h1, path.name)
            self.assertLess(h1.start(), text.index(bof.BEGIN), path.name)
            first_section = re.search(r"^## ", text, re.M)
            if first_section:
                self.assertLess(
                    text.index(bof.END), first_section.start(), path.name
                )

    def test_no_authored_heading_is_inside_the_block(self):
        for path in pages_with_block():
            body = BLOCK.search(path.read_text(encoding="utf-8")).group(1)
            self.assertNotIn("\n## ", body, path.name)

    def test_values_come_from_the_model(self):
        """Spot-check: the stated object id must be the page's first live ref."""
        for path in pages_with_block():
            text = path.read_text(encoding="utf-8")
            subject = bof.primary_ref(text, self.entities)
            self.assertIsNotNone(subject, path.name)
            body = BLOCK.search(text).group(1)
            self.assertIn(f"`{subject}`", body, path.name)

    def test_only_object_kinds_get_a_block(self):
        for path in pages_with_block():
            subject = bof.primary_ref(path.read_text(encoding="utf-8"), self.entities)
            self.assertIn(
                self.entities[subject]["kind"], bof.OBJECT_KINDS, path.name
            )

    def test_table_cells_cannot_break_the_table(self):
        """A pipe in an authority or license would split a row."""
        self.assertEqual(bof.cell("a|b"), "a\\|b")
        self.assertEqual(bof.cell("a\nb"), "a b")

    def test_a_page_can_opt_out(self):
        """A page that cites objects illustratively must be able to decline.

        DEEP-INVENTORY-BLOCKER.md is about a constraint and cites two example
        packages; a facts table headed with the first of them would announce
        the wrong subject.
        """
        page = ROOT / "docs" / "DEEP-INVENTORY-BLOCKER.md"
        text = page.read_text(encoding="utf-8")
        self.assertIsNotNone(bof.OPT_OUT.search(text), "opt-out key removed")
        self.assertNotIn(bof.BEGIN, text, "opt-out did not take effect")

    def test_rebuild_is_a_no_op(self):
        """CI regenerates before `git diff --exit-code`."""
        changed = bof.build(self.graph, write=False)
        self.assertEqual(
            [p.name for p in changed], [], "regeneration is not idempotent"
        )


if __name__ == "__main__":
    unittest.main()
