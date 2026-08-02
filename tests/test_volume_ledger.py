"""Cover the per-volume coverage ledger generator.

The ledger reported "Partial" for all twenty volumes, which meant a volume of
164 pages and a volume of 596 words across two stubs were indistinguishable.
These tests hold the replacement honest: every volume has a state, every state
is one the charter names, every state has a rationale, and the measured half
of the table is actually measured rather than typed.
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_volume_ledger as bvl  # noqa: E402

CHARTER = ROOT / "charter" / "PROJECT-CHARTER.md"


class CoverageStateTests(unittest.TestCase):
    def setUp(self):
        self.coverage = json.loads(bvl.COVERAGE.read_text(encoding="utf-8"))

    def test_every_volume_has_a_state_and_a_rationale(self):
        for number in bvl.VOLUME_TITLES:
            entry = self.coverage["volumes"].get(str(number))
            self.assertIsNotNone(entry, f"volume {number} has no coverage entry")
            self.assertIn("state", entry, f"volume {number} has no state")
            self.assertTrue(
                len(entry.get("rationale", "")) >= 40,
                f"volume {number} needs a rationale, not a label",
            )

    def test_states_are_the_charter_vocabulary(self):
        """The eight states are the charter's, not this file's invention."""
        charter = CHARTER.read_text(encoding="utf-8")
        match = re.search(
            r"Coverage reports distinguish (.*?)\s*states\.", charter, re.S
        )
        self.assertIsNotNone(match, "charter no longer states the coverage vocabulary")
        named = {
            word.strip().strip(",").replace(" ", "-")
            for word in match.group(1).replace("and ", "").replace("\n", " ").split(",")
        }
        declared = set(self.coverage["states"])
        self.assertEqual(
            declared,
            named,
            "model/volume-coverage.json states have drifted from the charter's",
        )

    def test_no_volume_uses_an_undeclared_state(self):
        declared = set(self.coverage["states"])
        for number, entry in self.coverage["volumes"].items():
            self.assertIn(entry["state"], declared, f"volume {number}")

    def test_the_uniform_partial_is_gone(self):
        """The defect this replaced: every volume reading the same."""
        used = {e["state"] for e in self.coverage["volumes"].values()}
        self.assertGreater(
            len(used), 1, "all twenty volumes carry one state again"
        )


class LedgerGenerationTests(unittest.TestCase):
    def test_rebuild_is_a_no_op(self):
        """CI regenerates before `git diff --exit-code`."""
        self.assertFalse(bvl.build(write=False), "regeneration is not idempotent")

    def test_metrics_are_measured_not_typed(self):
        """A page added to a volume must move that volume's numbers."""
        measured = bvl.measure()
        self.assertGreater(measured[6]["pages"], 100, "Volume 6 page count")
        self.assertEqual(
            measured[6]["pages"],
            len([p for p in bvl.DOCS.glob("*.md")
                 if re.search(r"^volume: 6$", p.read_text(encoding="utf-8"), re.M)]),
        )

    def test_generated_blocks_are_excluded_from_prose_counts(self):
        """Otherwise a volume inflates its word count by carrying diagrams."""
        sample = (
            "---\nvolume: 6\n---\n\nwords here\n\n"
            "<!-- BEGIN GENERATED dependency-subgraph -->\n"
            "lots of generated words indeed\n"
            "<!-- END GENERATED dependency-subgraph -->\n"
        )
        self.assertNotIn("generated", bvl.GENERATED_BLOCK.sub("", sample))

    def test_the_block_is_present_and_balanced_in_the_ledger(self):
        text = bvl.LEDGER.read_text(encoding="utf-8")
        self.assertEqual(text.count(bvl.BEGIN), 1)
        self.assertEqual(text.count(bvl.END), 1)
        self.assertLess(text.index(bvl.BEGIN), text.index(bvl.END))


if __name__ == "__main__":
    unittest.main()
