from __future__ import annotations
import importlib.util, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("toolchain_build", ROOT / "tools" / "collect_toolchain_build_observation.py")
assert spec and spec.loader
COLLECTOR = importlib.util.module_from_spec(spec); spec.loader.exec_module(COLLECTOR)
class ToolchainBuildObservationTests(unittest.TestCase):
    def test_missing_compiler_is_recorded(self) -> None:
        self.assertEqual(COLLECTOR.collect("C:/missing/compiler.exe", "ucrt64")["compile"], {"found": False})
    def test_pe_summary_rejects_non_pe_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not-pe"; path.write_text("not a PE", encoding="utf-8")
            self.assertEqual(COLLECTOR.pe_summary(path), {"recognized": False})
if __name__ == "__main__": unittest.main()
