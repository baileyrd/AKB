from __future__ import annotations

import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from tools.import_repository_db import RepositoryDatabaseError, convert, convert_many


def add_desc(bundle: tarfile.TarFile, name: str, content: str) -> None:
    data = content.encode()
    entry = tarfile.TarInfo(f"{name}/desc")
    entry.size = len(data)
    bundle.addfile(entry, io.BytesIO(data))


class RepositoryDatabaseImportTests(unittest.TestCase):
    def test_converts_pacman_desc_records_to_catalog_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, output = root / "core.db", root / "output"
            with tarfile.open(archive, "w") as bundle:
                add_desc(bundle, "bash-5.2-1", "%NAME%\nbash\n\n%VERSION%\n5.2-1\n\n%ARCH%\nx86_64\n\n%DESC%\nShell\n\n%DEPENDS%\nreadline>=8\n\n%LICENSE%\nGPL\n\n")
                add_desc(bundle, "readline-8.2-1", "%NAME%\nreadline\n\n%VERSION%\n8.2-1\n\n%ARCH%\nx86_64\n\n%DESC%\nLibrary\n\n")
            self.assertEqual(convert(archive, "msys", output), {"packages": 2, "edges": 1})
            manifest = json.loads((output / "catalog-manifest.json").read_text())
            self.assertEqual(manifest["source_archive"]["name"], "core.db")
            rows = (output / "all-packages.csv").read_text()
            self.assertIn("bash,5.2-1,False", rows)
            edges = (output / "dependency-edges.csv").read_text()
            self.assertIn("bash,runtime-depends-on,readline,>=8", edges)

    def test_rejects_archive_without_desc_records(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "empty.db"
            with tarfile.open(archive, "w") as bundle:
                entry = tarfile.TarInfo("nothing")
                entry.size = 0
                bundle.addfile(entry, io.BytesIO())
            with self.assertRaisesRegex(RepositoryDatabaseError, "no package desc"):
                convert(archive, "msys", Path(directory) / "output")

    def test_combines_multiple_repositories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archives = []
            for repository in ("msys", "ucrt64"):
                archive = root / f"{repository}.db"
                with tarfile.open(archive, "w") as bundle:
                    add_desc(bundle, f"{repository}-sample-1", f"%NAME%\n{repository}-sample\n\n%VERSION%\n1-1\n\n")
                archives.append(archive)
            output = root / "output"
            result = convert_many(archives, ["msys", "ucrt64"], output)
            manifest = json.loads((output / "catalog-manifest.json").read_text())
            self.assertEqual(result["packages"], 2)
            self.assertEqual(manifest["repositories"], ["msys", "ucrt64"])
            self.assertEqual(len(manifest["source_archives"]), 2)


if __name__ == "__main__":
    unittest.main()
