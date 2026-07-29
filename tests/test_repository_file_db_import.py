from __future__ import annotations

import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
import subprocess
import sys

from tools.import_repository_file_db import convert_many


def add_file(bundle: tarfile.TarFile, name: str, content: str) -> None:
    data = content.encode()
    entry = tarfile.TarInfo(name)
    entry.size = len(data)
    bundle.addfile(entry, io.BytesIO(data))


class RepositoryFileDatabaseImportTests(unittest.TestCase):
    def test_converts_file_database_to_uninstalled_artifact_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, output = root / "msys.files", root / "output"
            with tarfile.open(archive, "w") as bundle:
                add_file(bundle, "sample-1/desc", "%NAME%\nsample\n\n")
                add_file(bundle, "sample-1/files", "%FILES%\nusr/\nusr/bin/sample.exe\nusr/include/sample.h\n\n")
            self.assertEqual(convert_many([archive], ["msys"], output), {"artifacts": 2, "packages": 1})
            artifacts = [json.loads(line) for line in (output / "artifacts.jsonl").read_text().splitlines()]
        self.assertEqual([item["path"] for item in artifacts], ["/usr/bin/sample.exe", "/usr/include/sample.h"])
        self.assertTrue(all(item["present"] is False for item in artifacts))

    def test_command_line_entry_point_runs_outside_package_import_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, output = root / "msys.files", root / "output"
            with tarfile.open(archive, "w") as bundle:
                add_file(bundle, "sample-1/desc", "%NAME%\nsample\n\n")
                add_file(bundle, "sample-1/files", "%FILES%\nusr/bin/sample.exe\n\n")
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parents[1] / "tools" / "import_repository_file_db.py"),
                 str(archive), "--repository", "msys", "--output", str(output)],
                capture_output=True, text=True, check=True,
            )
        self.assertIn("Converted artifacts=1, packages=1", result.stdout)


if __name__ == "__main__":
    unittest.main()
