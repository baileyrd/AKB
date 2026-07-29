from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("akb", ROOT / "tools" / "akb.py")
assert spec and spec.loader
AKB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AKB)


class ClaimEvidenceTests(unittest.TestCase):
    def test_generate_includes_evidenced_claim_index(self) -> None:
        original = AKB.GENERATED
        try:
            with tempfile.TemporaryDirectory() as directory:
                AKB.GENERATED = Path(directory)
                AKB.generate()
                report = (AKB.GENERATED / "claim-evidence-index.md").read_text()
        finally:
            AKB.GENERATED = original
        self.assertIn("claim:environment:ucrt64:default", report)
        self.assertIn("evidence:msys2:environments-2026-07-28", report)

    def test_generate_dossiers_cover_every_composed_entity(self) -> None:
        original = AKB.GENERATED
        try:
            with tempfile.TemporaryDirectory() as directory:
                AKB.GENERATED = Path(directory)
                AKB.generate()
                dossiers = (AKB.GENERATED / "object-dossiers.md").read_text()
                graph = AKB.load_composed_graph()
        finally:
            AKB.GENERATED = original
        self.assertIn("# Generated Object Dossiers", dossiers)
        for entity in graph["entities"]:
            self.assertIn(f"## `{entity['id']}`", dossiers)
        self.assertIn("- Evidence:", dossiers)
        self.assertIn("- Outgoing relationships:", dossiers)
        self.assertIn("- Incoming relationships:", dossiers)


if __name__ == "__main__":
    unittest.main()
