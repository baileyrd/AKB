#!/usr/bin/env python3
"""Collect a bounded, self-cleaning compiler build observation."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path

SOURCE = b"int main(void) { return 0; }\n"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pe_summary(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    if data[:2] != b"MZ" or len(data) < 0x40:
        return {"recognized": False}
    offset = int.from_bytes(data[0x3C:0x40], "little")
    if data[offset:offset + 4] != b"PE\0\0":
        return {"recognized": False}
    machine = int.from_bytes(data[offset + 4:offset + 6], "little")
    return {"recognized": True, "machine": {0x14C: "x86", 0x8664: "x86_64", 0xAA64: "aarch64"}.get(machine, hex(machine))}

def collect(compiler: str, environment: str, execute: bool = False) -> dict[str, object]:
    compiler_path = Path(compiler).resolve()
    result: dict[str, object] = {"schema_version": "1.0.0", "collector_version": "0.1.0", "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "environment": environment, "compiler": str(compiler_path), "source_sha256": hashlib.sha256(SOURCE).hexdigest()}
    if not compiler_path.is_file():
        result["compile"] = {"found": False}; return result
    with tempfile.TemporaryDirectory(prefix="akb-toolchain-") as directory:
        root = Path(directory); source, output = root / "probe.c", root / "probe.exe"; source.write_bytes(SOURCE)
        try:
            completed = subprocess.run([str(compiler_path), str(source), "-o", str(output)], capture_output=True, text=True, timeout=30, check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            result["compile"] = {"found": True, "executed": False, "error": type(exc).__name__}; return result
        probe: dict[str, object] = {"found": True, "executed": True, "returncode": completed.returncode, "stderr": completed.stderr[:4000]}
        if completed.returncode == 0 and output.is_file():
            probe["artifact"] = {"size": output.stat().st_size, "sha256": sha256(output), "pe": pe_summary(output)}
            if execute:
                try:
                    run = subprocess.run([str(output)], capture_output=True, text=True, timeout=10, check=False); probe["execution"] = {"executed": True, "returncode": run.returncode}
                except (OSError, subprocess.SubprocessError) as exc:
                    probe["execution"] = {"executed": False, "error": type(exc).__name__}
        result["compile"] = probe
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--compiler", required=True); parser.add_argument("--environment", required=True); parser.add_argument("--execute", action="store_true"); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(collect(args.compiler, args.environment, args.execute), indent=2, sort_keys=True) + "\n", encoding="utf-8"); return 0
if __name__ == "__main__": raise SystemExit(main())
