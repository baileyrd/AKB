#!/usr/bin/env python3
"""Measure AKB validation and generated-view hot paths reproducibly."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import akb  # pylint: disable=wrong-import-position
import build_explorer  # pylint: disable=wrong-import-position


def timings(label: str, action: Callable[[], object], repetitions: int) -> dict:
    """Run an action repeatedly and return milliseconds without masking errors."""
    samples: list[float] = []
    for _ in range(repetitions):
        started = time.perf_counter()
        action()
        samples.append((time.perf_counter() - started) * 1000)
    return {
        "operation": label,
        "repetitions": repetitions,
        "minimum_ms": round(min(samples), 3),
        "median_ms": round(statistics.median(samples), 3),
    }


def benchmark(repetitions: int = 5) -> dict:
    """Benchmark validation, indexes, and explorer generation on one graph."""
    graph = akb.load_composed_graph()
    with tempfile.TemporaryDirectory() as directory:
        destination = Path(directory) / "explorer"
        results = [
            timings("validate", akb.validate, repetitions),
            timings("generate-indexes", akb.generate, repetitions),
            timings("build-explorer", lambda: build_explorer.build(graph, destination), repetitions),
        ]
    return {
        "schema_version": "1.0.0",
        "graph": {
            "entities": len(graph["entities"]),
            "relationships": len(graph["relationships"]),
            "claims": len(graph["claims"]),
            "evidence": len(graph["evidence"]),
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.repetitions < 1:
        parser.error("--repetitions must be positive")
    report = benchmark(args.repetitions)
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
