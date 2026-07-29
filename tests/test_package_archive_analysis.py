from __future__ import annotations

import io
import json
import struct
import tarfile
import tempfile
import unittest
from pathlib import Path

from tools.analyze_package_archive import (
    PackageArchiveError, analyze, safe_external_member_path, safe_link_target,
)


def minimal_pe() -> bytes:
    data = bytearray(0x200)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3C, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 0x84, 0x8664, 0, 1, 0, 0, 240, 0x2022)
    struct.pack_into("<H", data, 0x98, 0x20B)
    struct.pack_into("<H", data, 0x98 + 68, 3)
    struct.pack_into("<I", data, 0x98 + 108, 16)
    return bytes(data)


def add_file(bundle: tarfile.TarFile, name: str, data: bytes) -> None:
    entry = tarfile.TarInfo(name)
    entry.size = len(data)
    bundle.addfile(entry, io.BytesIO(data))


class PackageArchiveAnalysisTests(unittest.TestCase):
    def test_analyzes_uninstalled_binary_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, output = root / "sample.pkg.tar", root / "output"
            with tarfile.open(archive, "w") as bundle:
                add_file(bundle, "ucrt64/bin/sample.exe", minimal_pe())
                add_file(bundle, "ucrt64/lib/pkgconfig/sample.pc", b"Name: Sample\nVersion: 1\n")
            manifest = analyze(archive, "sample", output)
            artifacts = [json.loads(line) for line in (output / "artifacts.jsonl").read_text().splitlines()]
            self.assertEqual(manifest["scope"], "package-archive")
            self.assertEqual(manifest["counts"]["artifacts.jsonl"], 2)
            self.assertEqual(artifacts[0]["path"], "/ucrt64/bin/sample.exe")
            self.assertEqual(artifacts[0]["pe"]["architecture"], "x86_64")

    def test_rejects_traversal_member(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "unsafe.pkg.tar"
            with tarfile.open(archive, "w") as bundle:
                add_file(bundle, "../outside.dll", b"x")
            with self.assertRaisesRegex(PackageArchiveError, "unsafe archive member"):
                analyze(archive, "sample", Path(directory) / "output")

    def test_derives_package_name_from_pkginfo(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, output = root / "sample.pkg.tar", root / "output"
            with tarfile.open(archive, "w") as bundle:
                add_file(bundle, ".PKGINFO", b"pkgname = derived-sample\n")
                add_file(bundle, "usr/bin/sample.exe", minimal_pe())
            manifest = analyze(archive, None, output)
        self.assertEqual(manifest["package"], "derived-sample")

    def test_rejects_unsafe_external_tar_name(self):
        with self.assertRaisesRegex(PackageArchiveError, "unsafe archive member"):
            safe_external_member_path("../outside.dll")

    def test_records_safe_symbolic_link_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, output = root / "sample.pkg.tar", root / "output"
            with tarfile.open(archive, "w") as bundle:
                add_file(bundle, "usr/lib/libsample.dll", b"payload")
                link = tarfile.TarInfo("usr/lib/libsample-current.dll")
                link.type, link.linkname = tarfile.SYMTYPE, "libsample.dll"
                bundle.addfile(link)
            analyze(archive, "sample", output)
            artifacts = [json.loads(line) for line in (output / "artifacts.jsonl").read_text().splitlines()]
            link_record = next(item for item in artifacts if item["kind"] == "symlink")
            self.assertEqual(link_record["target"], "/usr/lib/libsample.dll")

    def test_rejects_escape_link_target(self):
        link = tarfile.TarInfo("usr/lib/sample.dll")
        link.linkname = "../../../outside.dll"
        with self.assertRaisesRegex(PackageArchiveError, "unsafe archive link target"):
            safe_link_target(link)


if __name__ == "__main__":
    unittest.main()
