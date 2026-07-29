from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CoverageAssessmentTests(unittest.TestCase):
    def test_reports_completed_diagram_hierarchy_without_overclaiming_object_coverage(self):
        subprocess.run([sys.executable, str(ROOT / "tools" / "assess_akb_coverage.py")], check=True)
        report = json.loads((ROOT / "generated" / "coverage-assessment.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(report["diagram_files"], 8)
        self.assertIn("package_payload_coverage", report)
        self.assertLess(
            report["package_payload_coverage"]["observed_packages"],
            report["package_payload_coverage"]["catalog_packages"],
        )
        self.assertTrue(any("Level 0–7" in gap for gap in report["gaps"]))
        self.assertTrue(any("per-object" in gap for gap in report["gaps"]))


if __name__ == "__main__":
    unittest.main()
