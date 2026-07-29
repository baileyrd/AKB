from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COLLECTOR = load_module("runtime_collector", ROOT / "tools" / "collect_runtime_observation.py")
IMPORTER = load_module("runtime_importer", ROOT / "tools" / "import_runtime_observation.py")


class RuntimeObservationTests(unittest.TestCase):
    def fixture(self) -> dict:
        return {
            "schema_version": "1.0.0", "collector_version": "0.4.0",
            "observed_at": "2026-07-28T22:00:00Z", "environment": "ucrt64",
            "host": {"system": "Windows", "machine": "AMD64", "release": "11"},
            "environment_variables": {"MSYSTEM": "UCRT64"},
            "tools": {"gcc": {"found": True, "path": "/ucrt64/bin/gcc.exe", "version": "gcc 14"}},
            "notes": []
        }

    def test_collector_uses_allowlist(self) -> None:
        result = COLLECTOR.collect("ucrt64")
        self.assertEqual(result["environment"], "ucrt64")
        self.assertNotIn("PATH", result["environment_variables"])
        self.assertEqual(set(result["tools"]), set(COLLECTOR.TOOLS))

    def test_projection_preserves_environment_as_target(self) -> None:
        result = IMPORTER.projection(self.fixture())
        self.assertEqual(result["entities"][0]["kind"], "configuration")
        self.assertEqual(result["relationships"][0]["target"], "environment:msys2:ucrt64")

    def test_import_writes_current_projection_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "observation.json"
            source.write_text(json.dumps(self.fixture()), encoding="utf-8")
            original = (IMPORTER.CURRENT, IMPORTER.GENERATED)
            try:
                IMPORTER.CURRENT = root / "model" / "runtime.json"
                IMPORTER.GENERATED = root / "generated"
                result = IMPORTER.import_observation(source)
            finally:
                IMPORTER.CURRENT, IMPORTER.GENERATED = original
            self.assertTrue(result["snapshot"]["id"].startswith("runtime-ucrt64-"))
            self.assertTrue((root / "generated" / "runtime-environment-report.md").is_file())

    def test_invalid_environment_is_rejected(self) -> None:
        value = self.fixture()
        value["environment"] = "unknown"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(IMPORTER.RuntimeObservationError):
                IMPORTER.load_observation(path)

    def test_merge_retains_distinct_environment_observations(self) -> None:
        first = IMPORTER.projection(self.fixture())
        second_value = self.fixture(); second_value["environment"] = "msys"
        second = IMPORTER.projection(second_value)
        merged = IMPORTER.merge_projection(first, second)
        self.assertEqual(len(merged["entities"]), 2)
        self.assertEqual(len(merged["relationships"]), 2)


if __name__ == "__main__":
    unittest.main()
