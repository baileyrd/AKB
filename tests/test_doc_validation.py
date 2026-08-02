"""Cover `akb.validate_docs`, which is the only check that opens a page.

`akb.validate()` operates purely on the composed JSON graph, so before this
existed a page could cite a non-existent entity, omit its status, or carry a
half-spliced generated block and nothing would notice.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import akb  # noqa: E402

GOOD = """---
id: doc:volume-6:example
title: Example
volume: 6
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs: []
last_verified: 2026-08-02
---

# Example
"""


class FrontmatterParsingTests(unittest.TestCase):
    def test_parses_scalars_and_lists(self):
        fields = akb.parse_frontmatter(GOOD)
        self.assertEqual(fields["volume"], "6")
        self.assertEqual(fields["status"], "partial")
        self.assertEqual(fields["model_refs"], ["ecosystem:msys2:msys2"])
        self.assertEqual(fields["evidence_refs"], [])

    def test_missing_block_is_none_not_empty(self):
        """A page with no frontmatter must be distinguishable from an empty one."""
        self.assertIsNone(akb.parse_frontmatter("# No frontmatter\n"))

    def test_body_text_is_not_mistaken_for_frontmatter(self):
        """Prose containing 'volume:' must not be read as a key.

        Two pages have body text a naive line scan misreads this way, which is
        how a page could appear to declare a volume it does not have.
        """
        text = GOOD + "\nSee volume: 3 for the runtime model.\n"
        self.assertEqual(akb.parse_frontmatter(text)["volume"], "6")


class ValidateDocsTests(unittest.TestCase):
    def test_repository_passes(self):
        counts = akb.validate_docs()
        self.assertGreater(counts["pages"], 200)

    def test_every_page_has_frontmatter(self):
        bare = [
            path.name
            for path in sorted((ROOT / "docs").glob("*.md"))
            if akb.parse_frontmatter(path.read_text(encoding="utf-8")) is None
        ]
        self.assertEqual(bare, [], "pages missing the required frontmatter block")

    def test_every_model_ref_resolves(self):
        known = {item["id"] for item in akb.load_composed_graph()["entities"]}
        unresolved = []
        for path in sorted((ROOT / "docs").glob("*.md")):
            fields = akb.parse_frontmatter(path.read_text(encoding="utf-8")) or {}
            unresolved += [
                f"{path.name}: {ref}"
                for ref in fields.get("model_refs", []) or []
                if ref not in known
            ]
        self.assertEqual(unresolved, [])

    def test_every_evidence_ref_resolves(self):
        graph = akb.load_composed_graph()
        known = {item["id"] for item in graph["evidence"]} | akb.known_source_ids()
        unresolved = []
        for path in sorted((ROOT / "docs").glob("*.md")):
            fields = akb.parse_frontmatter(path.read_text(encoding="utf-8")) or {}
            unresolved += [
                f"{path.name}: {ref}"
                for ref in fields.get("evidence_refs", []) or []
                if ref not in known
            ]
        self.assertEqual(unresolved, [])

    def test_status_vocabulary_is_respected(self):
        for path in sorted((ROOT / "docs").glob("*.md")):
            fields = akb.parse_frontmatter(path.read_text(encoding="utf-8")) or {}
            if "status" in fields:
                self.assertIn(str(fields["status"]), akb.ALLOWED_DOC_STATUS, path.name)

    def test_volumes_are_in_range(self):
        for path in sorted((ROOT / "docs").glob("*.md")):
            fields = akb.parse_frontmatter(path.read_text(encoding="utf-8")) or {}
            if "volume" in fields:
                self.assertIn(int(str(fields["volume"])), range(1, 21), path.name)


if __name__ == "__main__":
    unittest.main()
