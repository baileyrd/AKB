from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from tools.import_package_archives import package_archives


class PackageArchiveBatchTests(unittest.TestCase):
    def test_discovers_supported_archives_in_stable_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            for name in ("z.pkg.tar.zst", "a.pkg.tar", "ignored.tar"):
                path = root / "nested" / name
                path.write_bytes(b"")
            self.assertEqual(
                [path.name for path in package_archives(root)],
                ["a.pkg.tar", "z.pkg.tar.zst"],
            )


if __name__ == "__main__":
    unittest.main()
