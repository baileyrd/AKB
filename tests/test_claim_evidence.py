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
    def test_generate_includes_empty_claim_index(self) -> None:
        original = AKB.GENERATED
        try:
            with tempfile.TemporaryDirectory() as directory:
                AKB.GENERATED = Path(directory)
                AKB.generate()
                report = (AKB.GENERATED / "claim-evidence-index.md").read_text()
        finally:
            AKB.GENERATED = original
        self.assertIn("No claims recorded", report)


if __name__ == "__main__":
    unittest.main()
