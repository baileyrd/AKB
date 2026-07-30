from __future__ import annotations

import hashlib
import importlib.util
import json
import struct
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


ANALYZER = load_module("deep_inventory", ROOT / "tools" / "deep_inventory.py")
IMPORTER = load_module(
    "import_deep_inventory", ROOT / "tools" / "import_deep_inventory.py"
)


def make_minimal_pe(path: Path) -> None:
    data = bytearray(0x200)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3C, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into(
        "<HHIIIHH", data, 0x84,
        0x8664, 0, 123456789, 0, 0, 240, 0x2022,
    )
    optional = 0x98
    struct.pack_into("<H", data, optional, 0x20B)
    struct.pack_into("<Q", data, optional + 24, 0x140000000)
    struct.pack_into("<H", data, optional + 68, 3)
    struct.pack_into("<I", data, optional + 108, 16)
    path.write_bytes(data)


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(value, sort_keys=True) + "\n" for value in values),
        encoding="utf-8",
    )


class AnalyzerTests(unittest.TestCase):
    def test_license_lib_suffix_is_not_an_archive(self) -> None:
        self.assertEqual(
            ANALYZER.classify_path("/ucrt64/share/licenses/gcc/COPYING.LIB"),
            "file",
        )

    def test_msys_path_rejects_traversal(self) -> None:
        with self.assertRaises(ANALYZER.InventoryError):
            ANALYZER.msys_path(Path("C:/msys64"), "/usr/../../outside")

    def test_parse_minimal_pe_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.exe"
            make_minimal_pe(path)
            result = ANALYZER.parse_pe(path)
        self.assertEqual(result["format"], "PE32+")
        self.assertEqual(result["architecture"], "x86_64")
        self.assertEqual(result["subsystem"], "windows-console")
        self.assertEqual(result["imports"], [])
        self.assertEqual(result["exports"], [])

    def test_parse_gnu_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "libsample.a"
            payload = b"object"
            header = (
                b"sample.o/       "
                b"0           "
                b"0     "
                b"0     "
                b"100644  "
                + f"{len(payload):<10}".encode()
                + b"`\n"
            )
            path.write_bytes(b"!<arch>\n" + header + payload)
            members = ANALYZER.parse_ar(path)
        self.assertEqual(members[0]["name"], "sample.o")
        self.assertEqual(members[0]["size"], len(payload))

    def test_parse_development_metadata_and_recipe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pc = root / "sample.pc"
            pc.write_text(
                "prefix=/ucrt64\nlibdir=${prefix}/lib\n"
                "Name: Sample\nVersion: 1.2\nRequires: zlib >= 1.3, libpng >= 1.6\n"
                "Libs: -L${libdir} -lsample\nCflags: -I${prefix}/include\n",
                encoding="utf-8",
            )
            recipe = root / "PKGBUILD"
            recipe.write_text(
                "pkgbase=sample\npkgname=('sample' 'sample-tools')\n"
                "pkgver=1.2\npkgrel=1\n"
                "depends=('zlib>=1.3')\nmakedepends=('cmake' 'ninja')\n"
                "source=('https://example.invalid/sample.tar.zst')\n"
                "build() { :; }\npackage_sample() { :; }\n",
                encoding="utf-8",
            )
            pc_result = ANALYZER.parse_pkg_config(pc)
            recipe_result = ANALYZER.parse_pkgbuild(recipe)
        self.assertEqual(pc_result["version"], "1.2")
        self.assertEqual(pc_result["requires"][0]["name"], "zlib")
        self.assertEqual(pc_result["requires"][0]["constraint"], ">= 1.3")
        self.assertEqual(pc_result["requires"][1]["name"], "libpng")
        self.assertIn("-L/ucrt64/lib", pc_result["libs"])
        self.assertEqual(recipe_result["pkgname"], ["sample", "sample-tools"])
        self.assertEqual(recipe_result["makedepends"], ["cmake", "ninja"])
        self.assertIn("build", recipe_result["functions"])

    def test_parse_recipe_allows_empty_arrays(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            recipe = Path(directory) / "PKGBUILD"
            recipe.write_text(
                "pkgname=sample\npkgver=1\npkgrel=1\ndepends=()\nsource=()\n",
                encoding="utf-8",
            )
            result = ANALYZER.parse_pkgbuild(recipe)
        self.assertEqual(result["depends"], [])
        self.assertEqual(result["source"], [])


class ImporterTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> dict:
        records = {
            "artifacts.jsonl": [
                {
                    "package": "sample",
                    "path": "/ucrt64/bin/sample.exe",
                    "kind": "executable",
                    "present": True,
                    "size": 100,
                    "sha256": "a" * 64,
                    "pe": {"architecture": "x86_64"},
                },
                {
                    "package": "sample",
                    "path": "/ucrt64/bin/sample.dll",
                    "kind": "dll",
                    "present": True,
                    "size": 200,
                    "sha256": "b" * 64,
                    "pe": {"architecture": "x86_64"},
                },
            ],
            "pe-imports.jsonl": [
                {
                    "package": "sample",
                    "path": "/ucrt64/bin/sample.exe",
                    "dll": "sample.dll",
                    "symbols": ["sample_start"],
                    "ordinals": [],
                }
            ],
            "pe-exports.jsonl": [
                {
                    "package": "sample",
                    "path": "/ucrt64/bin/sample.dll",
                    "name": "sample_start",
                    "ordinal": 1,
                }
            ],
            "archive-members.jsonl": [],
            "development-metadata.jsonl": [],
            "recipes.jsonl": [
                {
                    "path": "sample/PKGBUILD",
                    "pkgbase": "sample",
                    "pkgname": ["sample"],
                    "pkgver": "1",
                    "pkgrel": "1",
                    "depends": [],
                    "makedepends": [],
                    "checkdepends": [],
                }
            ],
            "warnings.jsonl": [],
        }
        counts: dict[str, int] = {}
        hashes: dict[str, str] = {}
        for name, values in records.items():
            path = root / name
            write_jsonl(path, values)
            counts[name] = len(values)
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest = {
            "schema_version": "1.0.0",
            "collector_version": "0.3.0",
            "generated_at": "2026-07-28T21:00:00Z",
            "collector": "fixture",
            "scope": "installed",
            "counts": counts,
            "sha256": hashes,
        }
        (root / "inventory-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        return manifest

    def test_verify_and_project_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            manifest, records = IMPORTER.verify_input(root)
            projection, unresolved = IMPORTER.build_projection(
                manifest,
                records,
                "fixture",
                {"package:msys2:sample"},
            )
        self.assertEqual(unresolved, [])
        kinds = {item["kind"] for item in projection["entities"]}
        self.assertGreaterEqual(kinds, {"executable", "dll", "build-recipe"})
        types = {item["type"] for item in projection["relationships"]}
        self.assertGreaterEqual(types, {"installs", "imports-dll", "packaged-by"})
        dll = next(item for item in projection["entities"] if item["kind"] == "dll")
        self.assertEqual(dll["properties"]["exports"][0]["name"], "sample_start")

    def test_projection_uses_snapshot_qualified_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            manifest, records = IMPORTER.verify_input(root)
            projection, _ = IMPORTER.build_projection(
                manifest, records, "fixture", {"package:msys2:sample"}
            )
        evidence_id = "evidence:inventory:fixture"
        self.assertEqual(projection["evidence"][0]["id"], evidence_id)
        self.assertTrue(
            all(evidence_id in item["evidence_refs"] for item in projection["entities"])
        )

    def test_identical_dll_candidates_are_resolved_by_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            artifacts = [json.loads(line) for line in (root / "artifacts.jsonl").read_text(encoding="utf-8").splitlines()]
            duplicate = dict(artifacts[1])
            duplicate["path"] = "/ucrt64/lib/sample.dll"
            artifacts.append(duplicate)
            write_jsonl(root / "artifacts.jsonl", artifacts)
            manifest = json.loads((root / "inventory-manifest.json").read_text(encoding="utf-8"))
            manifest["counts"]["artifacts.jsonl"] = len(artifacts)
            manifest["sha256"]["artifacts.jsonl"] = hashlib.sha256((root / "artifacts.jsonl").read_bytes()).hexdigest()
            (root / "inventory-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            manifest, records = IMPORTER.verify_input(root)
            projection, unresolved = IMPORTER.build_projection(manifest, records, "fixture", {"package:msys2:sample"})
        self.assertEqual(unresolved, [])
        self.assertEqual(len([edge for edge in projection["relationships"] if edge["type"] == "imports-dll"]), 1)

    def test_recipe_paths_prevent_dynamic_package_name_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            manifest, records = IMPORTER.verify_input(root)
            first = records["recipes.jsonl"][0]
            second = {**first, "path": "other/PKGBUILD", "pkgbase": "${MINGW_PACKAGE_PREFIX}-sample"}
            first["pkgbase"] = "${MINGW_PACKAGE_PREFIX}-sample"
            records["recipes.jsonl"].append(second)
            projection, _ = IMPORTER.build_projection(
                manifest, records, "fixture", {"package:msys2:sample"}
            )
        recipes = [item for item in projection["entities"] if item["kind"] == "build-recipe"]
        self.assertEqual(len(recipes), 2)

    def test_projects_archive_link_to_observed_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            manifest, records = IMPORTER.verify_input(root)
            records["artifacts.jsonl"].append(
                {
                    "package": "sample",
                    "path": "/ucrt64/bin/sample-current.dll",
                    "kind": "symlink",
                    "present": True,
                    "link_type": "symbolic",
                    "target": "/ucrt64/bin/sample.dll",
                }
            )
            projection, unresolved = IMPORTER.build_projection(
                manifest, records, "fixture", {"package:msys2:sample"}
            )
        self.assertEqual(unresolved, [])
        links = [item for item in projection["relationships"] if item["type"] == "links-to"]
        self.assertEqual(len(links), 1)
        self.assertTrue(links[0]["target"].endswith("/ucrt64/bin/sample.dll"))

    def test_inventory_change_detection(self) -> None:
        previous = {
            "snapshot": {"id": "old"},
            "entities": [{"id": "dll:msys2:/a.dll", "properties": {"sha256": "1"}}],
        }
        current = {
            "snapshot": {"id": "new"},
            "entities": [
                {"id": "dll:msys2:/a.dll", "properties": {"sha256": "2"}},
                {"id": "dll:msys2:/b.dll", "properties": {"sha256": "3"}},
            ],
        }
        changes = IMPORTER.make_changes(previous, current)
        self.assertEqual(changes["added"], ["dll:msys2:/b.dll"])
        self.assertEqual(changes["changed"], ["dll:msys2:/a.dll"])

    def test_accumulated_projection_retains_prior_observations(self) -> None:
        previous = {
            "entities": [{"id": "dll:msys2:/curl.dll", "name": "curl.dll"}],
            "relationships": [{"id": "relationship:inventory:curl", "type": "installs"}],
            "evidence": [{"id": "evidence:inventory:curl"}],
        }
        current = {
            "entities": [{"id": "dll:msys2:/zlib1.dll", "name": "zlib1.dll"}],
            "relationships": [{"id": "relationship:inventory:zlib", "type": "installs"}],
            "evidence": [{"id": "evidence:inventory:zlib"}],
            "claims": ["discarded"],
        }
        merged = IMPORTER.merge_projection(previous, current)
        self.assertEqual([item["id"] for item in merged["entities"]], ["dll:msys2:/curl.dll", "dll:msys2:/zlib1.dll"])
        self.assertEqual(len(merged["relationships"]), 2)
        self.assertEqual(len(merged["evidence"]), 2)
        self.assertEqual(merged["claims"], [])

    def test_accumulation_retains_evidence_for_overlapping_objects(self) -> None:
        previous = {
            "entities": [{"id": "dll:msys2:/curl.dll", "evidence_refs": ["evidence:inventory:old"]}],
            "relationships": [{"id": "relationship:inventory:curl", "evidence_refs": ["evidence:inventory:old"]}],
            "evidence": [{"id": "evidence:inventory:old"}],
        }
        current = {
            "entities": [{"id": "dll:msys2:/curl.dll", "evidence_refs": ["evidence:inventory:new"], "properties": {"sha256": "new"}}],
            "relationships": [{"id": "relationship:inventory:curl", "evidence_refs": ["evidence:inventory:new"]}],
            "evidence": [{"id": "evidence:inventory:new"}],
        }
        merged = IMPORTER.merge_projection(previous, current)
        self.assertEqual(
            merged["entities"][0]["evidence_refs"],
            ["evidence:inventory:new", "evidence:inventory:old"],
        )
        self.assertEqual(
            merged["relationships"][0]["evidence_refs"],
            ["evidence:inventory:new", "evidence:inventory:old"],
        )

    def test_end_to_end_import_writes_snapshot_and_reports(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            self.make_fixture(source)
            original = (
                IMPORTER.CURRENT,
                IMPORTER.CATALOG,
                IMPORTER.SNAPSHOTS,
                IMPORTER.GENERATED,
            )
            try:
                IMPORTER.CURRENT = root / "model" / "current.json"
                IMPORTER.CATALOG = root / "model" / "catalog.json"
                IMPORTER.SNAPSHOTS = root / "snapshots"
                IMPORTER.GENERATED = root / "generated"
                IMPORTER.CATALOG.parent.mkdir(parents=True)
                IMPORTER.CATALOG.write_text(
                    json.dumps(
                        {
                            "entities": [
                                {
                                    "id": "package:msys2:sample",
                                    "kind": "package",
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                result = IMPORTER.import_inventory(source)
            finally:
                (
                    IMPORTER.CURRENT,
                    IMPORTER.CATALOG,
                    IMPORTER.SNAPSHOTS,
                    IMPORTER.GENERATED,
                ) = original
            self.assertEqual(result["unresolved"], 0)
            self.assertTrue((root / "model" / "current.json").is_file())
            self.assertTrue((root / "generated" / "deep-inventory-report.md").is_file())
            self.assertTrue(
                (root / "snapshots" / result["snapshot"] / "architecture-inventory.json").is_file()
            )

    def test_verify_only_validates_without_current_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            result = IMPORTER.verify_inventory(root)
        self.assertEqual(result["collector"], "fixture")
        self.assertEqual(result["records"], 5)
        self.assertEqual(result["warnings"], 0)

    def test_standalone_projection_does_not_use_current_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            output = root / "projection.json"
            result = IMPORTER.project_inventory(root, output)
            projection = json.loads(output.read_text(encoding="utf-8"))
        self.assertTrue(output.name)
        self.assertEqual(result["unresolved"], 3)
        self.assertEqual(projection["snapshot"]["id"], result["snapshot"])


if __name__ == "__main__":
    unittest.main()
