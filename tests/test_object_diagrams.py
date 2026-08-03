"""Guard the generated per-object dependency subgraphs.

These blocks are written into hand-authored pages, so the tests that matter
are the ones proving the tool owns only what is between its markers and that
a rebuild is a no-op.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_object_diagrams as bod  # noqa: E402

DOCS = sorted((ROOT / "docs").glob("*.md"))
BLOCK = re.compile(
    re.escape(bod.BEGIN) + r"(.*?)" + re.escape(bod.END), re.S
)


def pages_with_block():
    return [p for p in DOCS if bod.BEGIN in p.read_text(encoding="utf-8")]


class ObjectDiagramTests(unittest.TestCase):
    def test_charter_diagram_coverage(self):
        """The charter wants diagrams on object pages, not on a token few."""
        self.assertGreaterEqual(len(pages_with_block()), 100)

    def test_markers_are_balanced_and_unique(self):
        for path in DOCS:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(
                text.count(bod.BEGIN), text.count(bod.END), f"unbalanced markers in {path.name}"
            )
            self.assertLessEqual(text.count(bod.BEGIN), 1, f"duplicate block in {path.name}")

    def test_blocks_are_well_formed_mermaid(self):
        for path in pages_with_block():
            body = BLOCK.search(path.read_text(encoding="utf-8")).group(1)
            self.assertIn("```mermaid", body, path.name)
            self.assertIn("flowchart LR", body, path.name)
            self.assertEqual(body.count("```"), 2, f"unbalanced fence in {path.name}")

            declared = set(re.findall(r"^\s+(\w+)\[", body, re.M))
            self.assertIn("subject", declared, path.name)
            for node in re.findall(r"^\s+(\w+) -->", body, re.M):
                self.assertIn(node, declared, f"{path.name}: edge from undeclared {node}")
            for node in re.findall(r"--> (\w+)$", body, re.M):
                self.assertIn(node, declared, f"{path.name}: edge to undeclared {node}")

    def test_labels_avoid_mermaid_breaking_characters(self):
        for path in pages_with_block():
            body = BLOCK.search(path.read_text(encoding="utf-8")).group(1)
            for label in re.findall(r'\w+\["([^"]*)"\]', body):
                for char in '"#`{}<>':
                    self.assertNotIn(char, label, f"{path.name}: {char!r} in {label!r}")

    def test_truncation_is_disclosed(self):
        """A capped subgraph must say so; silence reads as completeness."""
        for path in pages_with_block():
            body = BLOCK.search(path.read_text(encoding="utf-8")).group(1)
            rendered = len(re.findall(r"^\s+[ud]\d+\[", body, re.M))
            claimed = re.search(r"(\d+) dependents? and (\d+) dependenc", body)
            self.assertIsNotNone(claimed, path.name)
            total = int(claimed.group(1)) + int(claimed.group(2))
            if total > rendered:
                self.assertIn("omitted here for legibility", body, path.name)

    def test_rebuild_is_a_no_op(self):
        """CI regenerates before `git diff --exit-code`."""
        before = {p: p.read_text(encoding="utf-8") for p in DOCS}
        changed = bod.build(bod.load_graph(), write=False)
        self.assertEqual(
            [p.name for p in changed], [], "regeneration is not idempotent"
        )
        for path, text in before.items():
            self.assertEqual(path.read_text(encoding="utf-8"), text, path.name)

    def test_authored_prose_is_outside_the_markers(self):
        """The tool must not have swallowed a page's Related Objects section."""
        for path in pages_with_block():
            text = path.read_text(encoding="utf-8")
            if "## Related Objects" in text:
                body = BLOCK.search(text).group(1)
                self.assertNotIn("## Related Objects", body, path.name)


if __name__ == "__main__":
    unittest.main()
