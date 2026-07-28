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
        first_line = (completed.stdout or completed.stderr).splitlines()
        if first_line:
            result["version"] = first_line[0][:500]
    except (OSError, subprocess.SubprocessError):
        pass
    return result


def collect(environment: str) -> dict[str, object]:
    """Capture only explicit allow-listed variables and tool identity metadata."""
    return {
        "schema_version": "1.0.0",
        "collector_version": "0.4.0",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "environment": environment,
        "host": {"system": platform.system(), "machine": platform.machine(), "release": platform.release()},
        "environment_variables": {key: os.environ[key] for key in SAFE_VARIABLES if key in os.environ},
        "tools": {name: tool_observation(name) for name in TOOLS},
        "notes": ["PATH and all variables outside the explicit allow-list are intentionally excluded."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True, choices=ENVIRONMENTS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(collect(args.environment), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
