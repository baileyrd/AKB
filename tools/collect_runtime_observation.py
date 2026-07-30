#!/usr/bin/env python3
"""Collect a bounded, non-secret runtime observation from the active environment."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ENVIRONMENTS = ("msys", "ucrt64", "clang64", "clangarm64", "mingw64", "mingw32")
SAFE_VARIABLES = ("MSYSTEM", "MSYSTEM_PREFIX", "MSYS2_PATH_TYPE", "CHERE_INVOKING", "OSTYPE")
TOOLS = ("sh", "bash", "gcc", "clang", "ld", "cmake", "make", "ninja", "pacman")
PROBES = {
    "uname": ("uname", "-srm"),
    "posix_to_windows_path": ("cygpath", "-w", "/usr/bin"),
    "windows_to_posix_path": ("cygpath", "-u", "C:/Windows"),
    "mount_table": ("mount",),
    "proc_self_executable": ("readlink", "/proc/self/exe"),
}
BEHAVIOR_PROBES = {
    # Every command is self-contained. The symlink probe uses and removes a
    # fresh temporary directory; no existing file or configuration is changed.
    "process_lifecycle": 'sleep 1 & child=$!; kill -0 "$child"; wait "$child"; printf "child-exited=%s" "$?"',
    "exec_replacement": 'exec printf "exec-ok"',
    "signal_delivery": "trap 'printf signal=USR1' USR1; kill -USR1 $$",
    "filesystem_symlink": 'd=$(mktemp -d) || exit 1; trap \'rm -rf "$d"\' EXIT; printf payload > "$d/target"; ln -s target "$d/link"; made=$?; test -L "$d/link"; is_link=$?; content=$(cat "$d/link" 2>&1); read_status=$?; test "$content" = payload; matches=$?; printf "made=%s is-link=%s read=%s matches=%s" "$made" "$is_link" "$read_status" "$matches"; test "$made" -eq 0 && test "$is_link" -eq 0 && test "$read_status" -eq 0 && test "$matches" -eq 0',
    "terminal_device_namespace": 'test -d /dev && test -e /dev/tty && printf dev-tty=present',
}


def tool_observation(name: str) -> dict[str, object]:
    path = shutil.which(name)
    result: dict[str, object] = {"found": bool(path)}
    if not path:
        return result
    result["path"] = path
    try:
        completed = subprocess.run(
            [path, "--version"], capture_output=True, text=True, timeout=3, check=False
        )
        result["executed"] = True
        result["returncode"] = completed.returncode
        first_line = (completed.stdout or completed.stderr).splitlines()
        if first_line:
            result["version"] = first_line[0][:500]
    except (OSError, subprocess.SubprocessError) as exc:
        result["executed"] = False
        result["error"] = type(exc).__name__
    return result


def probe_observation(command: tuple[str, ...]) -> dict[str, object]:
    """Capture a short, read-only shell/runtime probe without environment data."""
    executable = shutil.which(command[0])
    if not executable:
        return {"found": False}
    try:
        completed = subprocess.run(
            [executable, *command[1:]], capture_output=True, text=True,
            timeout=3, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return {"found": True, "executed": False}
    output = (completed.stdout or completed.stderr).strip()
    return {
        "found": True,
        "executed": True,
        "returncode": completed.returncode,
        "output": output[:8000],
    }


def behavior_probe_observation(script: str) -> dict[str, object]:
    """Run one bounded MSYS-shell behavior probe without retaining secrets."""
    shell = shutil.which("sh")
    if not shell:
        return {"found": False}
    try:
        completed = subprocess.run(
            [shell, "-c", script], capture_output=True, text=True,
            timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"found": True, "executed": False, "error": type(exc).__name__}
    output = (completed.stdout or completed.stderr).strip()
    return {
        "found": True,
        "executed": True,
        "returncode": completed.returncode,
        "output": output[:8000],
    }


def collect(environment: str, behavior: bool = False) -> dict[str, object]:
    """Capture only explicit allow-listed variables and tool identity metadata."""
    result: dict[str, object] = {
        "schema_version": "1.0.0",
        "collector_version": "0.4.0",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "environment": environment,
        "host": {"system": platform.system(), "machine": platform.machine(), "release": platform.release()},
        "environment_variables": {key: os.environ[key] for key in SAFE_VARIABLES if key in os.environ},
        "tools": {name: tool_observation(name) for name in TOOLS},
        "probes": {name: probe_observation(command) for name, command in PROBES.items()},
        "notes": [
            "PATH and all variables outside the explicit allow-list are intentionally excluded.",
            "Path and mount probes describe the MSYS shell/runtime that executed the collector; they do not establish native tool runtime behavior.",
        ],
    }
    if behavior:
        result["behavior_probes"] = {
            name: behavior_probe_observation(script)
            for name, script in BEHAVIOR_PROBES.items()
        }
        result["notes"].append(
            "Behavior probes run through the selected MSYS shell; the symlink probe creates and removes only a fresh temporary directory."
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True, choices=ENVIRONMENTS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--behavior", action="store_true",
        help="include bounded process, exec, signal, symlink, and terminal-device probes",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(collect(args.environment, args.behavior), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
