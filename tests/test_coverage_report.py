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
class CoverageReportTests(unittest.TestCase):
    def test_generate_coverage_report(self):
        original = AKB.GENERATED
        try:
            with tempfile.TemporaryDirectory() as directory:
                AKB.GENERATED = Path(directory); AKB.generate()
                report = (AKB.GENERATED / "coverage-report.md").read_text()
        finally: AKB.GENERATED = original
        self.assertIn("Entities with evidence", report)
if __name__ == "__main__": unittest.main()
