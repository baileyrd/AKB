#!/usr/bin/env python3
"""Collect and analyze MSYS2 package artifacts without third-party modules."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator


SCHEMA_VERSION = "1.0.0"
COLLECTOR_VERSION = "0.3.0"
PE_MACHINE = {0x014C: "i686", 0x8664: "x86_64", 0xAA64: "aarch64"}
PE_SUBSYSTEM = {
    1: "native",
    2: "windows-gui",
    3: "windows-console",
    7: "posix-console",
    10: "efi-application",
}
ARTIFACT_SUFFIXES = {
    ".exe": "executable",
    ".dll": "dll",
    ".a": "static-library",
    ".lib": "static-library",
    ".h": "header",
    ".hh": "header",
    ".hpp": "header",
    ".hxx": "header",
    ".pc": "pkg-config-module",
}


class InventoryError(Exception):
    """Raised when collection input or a required external command is invalid."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify_path(value: str) -> str:
    path = PurePosixPath(value.lower())
    name = path.name
    if name.endswith(".dll.a"):
        return "import-library"
    if name.endswith((".cmake", "config.cmake", "targets.cmake")):
        return "cmake-module"
    return ARTIFACT_SUFFIXES.get(path.suffix, "file")


def msys_path(root: Path, value: str) -> Path:
    """Map an MSYS absolute package path to its Windows installation root."""
    normalized = value.replace("\\", "/")
    package_path = PurePosixPath(normalized)
    if not normalized.startswith("/") or ".." in package_path.parts:
        raise InventoryError(f"unsafe package path: {value}")
    return root.joinpath(*package_path.parts[1:])


def _cstring(data: bytes, offset: int, limit: int | None = None) -> str:
    if offset < 0 or offset >= len(data):
        return ""
    end = data.find(b"\0", offset, limit)
    if end < 0:
        end = len(data) if limit is None else min(limit, len(data))
    return data[offset:end].decode("ascii", errors="replace")


def parse_pe(path: Path) -> dict[str, Any]:
    """Read PE/COFF headers, imported DLLs, exports, and debug-directory presence."""
    data = path.read_bytes()
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise InventoryError(f"not a PE file: {path}")
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_offset + 24 > len(data) or data[pe_offset : pe_offset + 4] != b"PE\0\0":
        raise InventoryError(f"invalid PE signature: {path}")
    coff = pe_offset + 4
    machine, sections, timestamp, _, _, optional_size, characteristics = (
        struct.unpack_from("<HHIIIHH", data, coff)
    )
    optional = coff + 20
    if optional + optional_size > len(data):
        raise InventoryError(f"truncated optional header: {path}")
    magic = struct.unpack_from("<H", data, optional)[0]
    if magic == 0x10B:
        bitness, image_base_offset, directory_offset = 32, 28, 96
        thunk_size, ordinal_flag = 4, 0x80000000
    elif magic == 0x20B:
        bitness, image_base_offset, directory_offset = 64, 24, 112
        thunk_size, ordinal_flag = 8, 0x8000000000000000
    else:
        raise InventoryError(f"unsupported PE optional-header magic 0x{magic:x}")
    subsystem = struct.unpack_from("<H", data, optional + 68)[0]
    image_base_format = "<I" if bitness == 32 else "<Q"
    image_base = struct.unpack_from(
        image_base_format, data, optional + image_base_offset
    )[0]
    section_table = optional + optional_size
    section_rows: list[tuple[int, int, int, int]] = []
    for index in range(sections):
        offset = section_table + index * 40
        if offset + 40 > len(data):
            raise InventoryError(f"truncated section table: {path}")
        virtual_size, virtual_address, raw_size, raw_offset = struct.unpack_from(
            "<IIII", data, offset + 8
        )
        section_rows.append(
            (virtual_address, max(virtual_size, raw_size), raw_offset, raw_size)
        )

    def rva_to_offset(rva: int) -> int | None:
        for virtual, size, raw, raw_size in section_rows:
            if virtual <= rva < virtual + size:
                delta = rva - virtual
                return raw + delta if delta < raw_size else None
        return rva if 0 <= rva < len(data) else None

    number_of_directories = struct.unpack_from(
        "<I", data, optional + directory_offset - 4
    )[0]

    def directory(index: int) -> tuple[int, int]:
        if index >= number_of_directories:
            return 0, 0
        offset = optional + directory_offset + index * 8
        if offset + 8 > optional + optional_size:
            return 0, 0
        return struct.unpack_from("<II", data, offset)

    imports: list[dict[str, Any]] = []
    import_rva, _ = directory(1)
    descriptor_offset = rva_to_offset(import_rva) if import_rva else None
    if descriptor_offset is not None:
        for descriptor_index in range(65536):
            offset = descriptor_offset + descriptor_index * 20
            if offset + 20 > len(data):
                break
            original_thunk, _, _, name_rva, first_thunk = struct.unpack_from(
                "<IIIII", data, offset
            )
            if not any((original_thunk, name_rva, first_thunk)):
                break
            name_offset = rva_to_offset(name_rva)
            dll = _cstring(data, name_offset) if name_offset is not None else ""
            symbols: list[str] = []
            ordinals: list[int] = []
            thunk_offset = rva_to_offset(original_thunk or first_thunk)
            if thunk_offset is not None:
                unpack = "<I" if thunk_size == 4 else "<Q"
                for thunk_index in range(100000):
                    entry_offset = thunk_offset + thunk_index * thunk_size
                    if entry_offset + thunk_size > len(data):
                        break
                    value = struct.unpack_from(unpack, data, entry_offset)[0]
                    if value == 0:
                        break
                    if value & ordinal_flag:
                        ordinals.append(value & 0xFFFF)
                    else:
                        hint_name = rva_to_offset(value)
                        if hint_name is not None:
                            symbols.append(_cstring(data, hint_name + 2))
            imports.append(
                {
                    "dll": dll.lower(),
                    "symbols": sorted(item for item in symbols if item),
                    "ordinals": sorted(ordinals),
                }
            )

    exports: list[dict[str, Any]] = []
    export_rva, _ = directory(0)
    export_offset = rva_to_offset(export_rva) if export_rva else None
    if export_offset is not None and export_offset + 40 <= len(data):
        (
            _,
            _,
            _,
            _,
            _,
            ordinal_base,
            function_count,
            name_count,
            functions_rva,
            names_rva,
            ordinals_rva,
        ) = struct.unpack_from("<IIHHIIIIIII", data, export_offset)
        functions_offset = rva_to_offset(functions_rva)
        names_offset = rva_to_offset(names_rva)
        ordinals_offset = rva_to_offset(ordinals_rva)
        named_ordinals: set[int] = set()
        if names_offset is not None and ordinals_offset is not None:
            for index in range(min(name_count, 1_000_000)):
                if names_offset + index * 4 + 4 > len(data):
                    break
                name_rva = struct.unpack_from("<I", data, names_offset + index * 4)[0]
                name_offset = rva_to_offset(name_rva)
                if name_offset is None or ordinals_offset + index * 2 + 2 > len(data):
                    continue
                ordinal_index = struct.unpack_from(
                    "<H", data, ordinals_offset + index * 2
                )[0]
                named_ordinals.add(ordinal_index)
                exports.append(
                    {
                        "name": _cstring(data, name_offset),
                        "ordinal": ordinal_base + ordinal_index,
                    }
                )
        if functions_offset is not None:
            for ordinal_index in range(min(function_count, 1_000_000)):
                if ordinal_index in named_ordinals:
                    continue
                if functions_offset + ordinal_index * 4 + 4 > len(data):
                    break
                function_rva = struct.unpack_from(
                    "<I", data, functions_offset + ordinal_index * 4
                )[0]
                if function_rva:
                    exports.append(
                        {"name": "", "ordinal": ordinal_base + ordinal_index}
                    )

    debug_rva, debug_size = directory(6)
    return {
        "format": "PE32+" if bitness == 64 else "PE32",
        "architecture": PE_MACHINE.get(machine, f"machine-0x{machine:04x}"),
        "machine": f"0x{machine:04x}",
        "timestamp": timestamp,
        "subsystem": PE_SUBSYSTEM.get(subsystem, f"subsystem-{subsystem}"),
        "image_base": image_base,
        "characteristics": f"0x{characteristics:04x}",
        "section_count": sections,
        "has_debug_directory": bool(debug_rva and debug_size),
        "imports": sorted(imports, key=lambda item: item["dll"]),
        "exports": sorted(exports, key=lambda item: (item["ordinal"], item["name"])),
    }


def parse_ar(path: Path) -> list[dict[str, Any]]:
    """Parse common GNU/BSD ar member headers, including GNU long names."""
    data = path.read_bytes()
    if not data.startswith(b"!<arch>\n"):
        raise InventoryError(f"not an ar archive: {path}")
    offset = 8
    string_table = b""
    members: list[dict[str, Any]] = []
    while offset + 60 <= len(data):
        header = data[offset : offset + 60]
        if header[58:60] != b"`\n":
            raise InventoryError(f"invalid ar member header at {offset}: {path}")
        raw_name = header[:16].decode("ascii", errors="replace").strip()
        try:
            size = int(header[48:58].decode("ascii").strip())
        except ValueError as exc:
            raise InventoryError(f"invalid ar member size at {offset}: {path}") from exc
        payload = offset + 60
        name = raw_name.rstrip("/")
        data_offset, data_size = payload, size
        if raw_name == "//":
            string_table = data[payload : payload + size]
            name = "//"
        elif raw_name.startswith("/") and raw_name[1:].isdigit() and string_table:
            start = int(raw_name[1:])
            end = string_table.find(b"/\n", start)
            if end < 0:
                end = len(string_table)
            name = string_table[start:end].decode("utf-8", errors="replace")
        elif raw_name.startswith("#1/"):
            name_size = int(raw_name[3:])
            name = data[payload : payload + name_size].decode(
                "utf-8", errors="replace"
            )
            data_offset += name_size
            data_size -= name_size
        if name not in {"", "/", "//", "__.SYMDEF", "__.SYMDEF SORTED"}:
            members.append(
                {
                    "name": name,
                    "size": max(data_size, 0),
                    "offset": data_offset,
                }
            )
        offset = payload + size + (size % 2)
    return members


def _logical_lines(text: str) -> list[str]:
    lines: list[str] = []
    pending = ""
    for raw in text.splitlines():
        stripped = raw.rstrip()
        pending += stripped[:-1] if stripped.endswith("\\") else stripped
        if not stripped.endswith("\\"):
            lines.append(pending)
            pending = ""
    if pending:
        lines.append(pending)
    return lines


def parse_pkg_config(path: Path) -> dict[str, Any]:
    variables: dict[str, str] = {}
    fields: dict[str, str] = {}
    for raw in _logical_lines(path.read_text(encoding="utf-8", errors="replace")):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line and (":" not in line or line.index("=") < line.index(":")):
            key, value = line.split("=", 1)
            variables[key.strip()] = value.strip()
        elif ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    variable_pattern = re.compile(r"\$\{([^}]+)\}")

    def expand(value: str) -> str:
        for _ in range(20):
            updated = variable_pattern.sub(
                lambda match: variables.get(match.group(1), match.group(0)), value
            )
            if updated == value:
                return value
            value = updated
        return value

    expanded = {key: expand(value) for key, value in fields.items()}
    requires: list[dict[str, str]] = []
    for field in ("Requires", "Requires.private"):
        for token in re.split(r"\s*,\s*|\s+(?=[A-Za-z0-9_.+-]+\s*(?:[<>=]|$))", expanded.get(field, "")):
            match = re.match(r"^([A-Za-z0-9_.+-]+)\s*(.*)$", token.strip())
            if match:
                requires.append(
                    {
                        "name": match.group(1),
                        "constraint": match.group(2).strip(),
                        "private": str(field.endswith(".private")).lower(),
                    }
                )
    return {
        "name": expanded.get("Name", path.stem),
        "version": expanded.get("Version", ""),
        "description": expanded.get("Description", ""),
        "url": expanded.get("URL", ""),
        "requires": requires,
        "libs": expanded.get("Libs", "").split(),
        "libs_private": expanded.get("Libs.private", "").split(),
        "cflags": expanded.get("Cflags", "").split(),
        "variables": variables,
    }


def parse_cmake(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    dependencies = re.findall(
        r"(?im)\bfind_(?:dependency|package)\s*\(\s*([A-Za-z0-9_.+-]+)", text
    )
    targets = re.findall(
        r"(?im)\badd_library\s*\(\s*([A-Za-z0-9_.:+-]+)\s+IMPORTED\b", text
    )
    locations = re.findall(
        r"(?im)\bIMPORTED_(?:IMPLIB|LOCATION)(?:_[A-Z0-9_]+)?\s+\"?([^\"\s)]+)",
        text,
    )
    return {
        "dependencies": sorted(set(dependencies)),
        "imported_targets": sorted(set(targets)),
        "imported_locations": sorted(set(locations)),
    }


def _shell_array(text: str, name: str) -> list[str]:
    match = re.search(
        rf"(?ms)^\s*{re.escape(name)}\s*=\s*\((.*?)\)", text
    )
    if not match:
        scalar = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*(['\"]?)(.*?)\1\s*$", text)
        return [scalar.group(2)] if scalar and scalar.group(2) else []
    return re.findall(r"(?:'([^']*)'|\"([^\"]*)\"|([^\s#]+))", match.group(1))


def parse_pkgbuild(path: Path) -> dict[str, Any]:
    """Statically extract declarative PKGBUILD fields without executing shell code."""
    text = path.read_text(encoding="utf-8", errors="replace")

    def values(name: str) -> list[str]:
        raw = _shell_array(text, name)
        parsed = [
            next((value for value in item if value), "") if isinstance(item, tuple) else item
            for item in raw
        ]
        return [value for value in parsed if value]

    def scalar(name: str) -> str:
        match = re.search(
            rf"(?m)^\s*{re.escape(name)}\s*=\s*(['\"]?)(.*?)\1\s*(?:#.*)?$", text
        )
        return match.group(2).strip() if match else ""

    functions = sorted(
        set(re.findall(r"(?m)^\s*(prepare|pkgver|build|check|package(?:_[A-Za-z0-9_+-]+)?)\s*\(\s*\)", text))
    )
    return {
        "pkgbase": scalar("pkgbase"),
        "pkgname": values("pkgname") or ([scalar("pkgname")] if scalar("pkgname") else []),
        "pkgver": scalar("pkgver"),
        "pkgrel": scalar("pkgrel"),
        "arch": values("arch"),
        "url": scalar("url"),
        "license": values("license"),
        "depends": values("depends"),
        "makedepends": values("makedepends"),
        "checkdepends": values("checkdepends"),
        "optdepends": values("optdepends"),
        "provides": values("provides"),
        "conflicts": values("conflicts"),
        "replaces": values("replaces"),
        "source": values("source"),
        "sha256sums": values("sha256sums"),
        "functions": functions,
        "dynamic_fields": sorted(set(re.findall(r"\$\([^)]+\)|\$\{?[\w@#?-]+\}?", text))),
    }


def run(command: list[str]) -> list[str]:
    result = subprocess.run(
        command, check=False, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, "LANG": "C", "LC_ALL": "C"},
    )
    if result.returncode:
        raise InventoryError(
            f"{' '.join(command)} failed ({result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout.splitlines()


def package_files(pacman: Path, scope: str) -> Iterator[tuple[str, str]]:
    if scope == "repositories":
        for line in run([str(pacman), "-Fl"]):
            parts = line.split(None, 2)
            if len(parts) == 3 and not parts[2].endswith("/"):
                yield parts[1], "/" + parts[2].lstrip("/")
    else:
        for line in run([str(pacman), "-Ql"]):
            parts = line.split(None, 1)
            if len(parts) == 2 and not parts[1].endswith("/"):
                yield parts[0], parts[1]


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> int:
    values = list(records)
    path.write_text(
        "".join(json.dumps(value, sort_keys=True) + "\n" for value in values),
        encoding="utf-8",
    )
    return len(values)


def collect(
    root: Path, output: Path, scope: str = "installed", recipes: Path | None = None
) -> dict[str, Any]:
    pacman = root / "usr" / "bin" / ("pacman.exe" if os.name == "nt" else "pacman")
    if not pacman.is_file():
        raise InventoryError(f"pacman was not found at {pacman}")
    output.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any]] = []
    pe_imports: list[dict[str, Any]] = []
    pe_exports: list[dict[str, Any]] = []
    archive_members: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for package, package_path in package_files(pacman, scope):
        key = (package, package_path)
        if key in seen:
            continue
        seen.add(key)
        try:
            local = msys_path(root, package_path)
        except InventoryError as exc:
            warnings.append({"path": package_path, "message": str(exc)})
            continue
        kind = classify_path(package_path)
        record: dict[str, Any] = {
            "package": package,
            "path": package_path,
            "kind": kind,
            "present": local.is_file(),
        }
        if local.is_file():
            try:
                local.resolve().relative_to(root.resolve())
            except ValueError:
                warnings.append(
                    {
                        "path": package_path,
                        "message": "resolved path escapes the MSYS2 root",
                    }
                )
                artifacts.append(record)
                continue
            stat = local.stat()
            record.update({"size": stat.st_size, "sha256": sha256(local)})
            try:
                if kind in {"executable", "dll"}:
                    pe = parse_pe(local)
                    record["pe"] = {key: value for key, value in pe.items() if key not in {"imports", "exports"}}
                    for item in pe["imports"]:
                        pe_imports.append({"package": package, "path": package_path, **item})
                    for item in pe["exports"]:
                        pe_exports.append({"package": package, "path": package_path, **item})
                elif kind in {"static-library", "import-library"}:
                    for member in parse_ar(local):
                        archive_members.append({"package": package, "path": package_path, **member})
                elif kind == "pkg-config-module":
                    metadata.append({"package": package, "path": package_path, "format": "pkg-config", **parse_pkg_config(local)})
                elif kind == "cmake-module":
                    metadata.append({"package": package, "path": package_path, "format": "cmake", **parse_cmake(local)})
            except (InventoryError, OSError, ValueError, struct.error) as exc:
                warnings.append({"path": package_path, "message": str(exc)})
        artifacts.append(record)

    recipe_records: list[dict[str, Any]] = []
    if recipes and recipes.is_dir():
        for path in sorted(recipes.rglob("PKGBUILD")):
            try:
                recipe_records.append(
                    {"path": path.relative_to(recipes).as_posix(), **parse_pkgbuild(path)}
                )
            except OSError as exc:
                warnings.append({"path": str(path), "message": str(exc)})

    files = {
        "artifacts.jsonl": artifacts,
        "pe-imports.jsonl": pe_imports,
        "pe-exports.jsonl": pe_exports,
        "archive-members.jsonl": archive_members,
        "development-metadata.jsonl": metadata,
        "recipes.jsonl": recipe_records,
        "warnings.jsonl": warnings,
    }
    counts = {name: write_jsonl(output / name, values) for name, values in files.items()}
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "collector_version": COLLECTOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collector": "tools/deep_inventory.py",
        "msys2_root": str(root),
        "scope": scope,
        "counts": counts,
        "sha256": {name: sha256(output / name) for name in files},
    }
    (output / "inventory-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--msys2-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scope", choices=("installed", "repositories"), default="installed")
    parser.add_argument("--recipes", type=Path)
    args = parser.parse_args()
    try:
        manifest = collect(
            args.msys2_root.resolve(),
            args.output.resolve(),
            args.scope,
            args.recipes.resolve() if args.recipes else None,
        )
    except (InventoryError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Collected " + ", ".join(f"{key}={value}" for key, value in manifest["counts"].items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
