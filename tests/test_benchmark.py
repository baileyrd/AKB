from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("benchmark", ROOT / "tools" / "benchmark_akb.py")
assert spec and spec.loader
BENCHMARK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BENCHMARK)


class BenchmarkTests(unittest.TestCase):
    def test_report_has_all_hot_paths(self) -> None:
        report = BENCHMARK.benchmark(repetitions=1)
        self.assertEqual(report["schema_version"], "1.0.0")
        self.assertEqual(
            [item["operation"] for item in report["results"]],
            ["validate", "generate-indexes", "build-explorer"],
        )
        self.assertTrue(all(item["minimum_ms"] >= 0 for item in report["results"]))
