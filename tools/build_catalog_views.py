#!/usr/bin/env python3
"""Build snapshot-bound package and library-candidate navigation views."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "model" / "catalog" / "current.json"
GENERATED = ROOT / "generated"


def is_library_candidate(name: str) -> bool:
    lowered = name.lower()
    stem = lowered.rsplit("-", 1)[-1]
    return stem.startswith("lib") or "-devel" in lowered or "-dev" in lowered


def build(catalog_path: Path = CATALOG, output: Path = GENERATED) -> dict[str, int]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    packages = [item for item in catalog["entities"] if item["kind"] == "package"]
    inbound: dict[str, int] = Counter(
        edge["target"] for edge in catalog["relationships"]
        if edge["type"] == "runtime-depends-on"
    )
    candidates = []
    by_repository: dict[str, int] = Counter()
    for package in packages:
        if not is_library_candidate(package["name"]):
            continue
        repository = package["applicability"]["repository"]
        candidates.append({
            "id": package["id"], "name": package["name"], "repository": repository,
            "version": package["properties"].get("version", ""),
            "declared_runtime_dependents": inbound[package["id"]],
        })
        by_repository[repository] += 1
    candidates.sort(key=lambda item: (-item["declared_runtime_dependents"], item["name"]))
    output.mkdir(parents=True, exist_ok=True)
    (output / "library-candidates.json").write_text(json.dumps({"snapshot": catalog["snapshot"]["id"], "classification": "package-name candidate; not a logical library identity", "candidates": candidates}, indent=2) + "\n", encoding="utf-8")
    lines = ["# Generated Library Package Candidates", "", "> Snapshot-bound package-name candidates. They are not proof of DLLs, headers, or logical API identity.", "", f"- Snapshot: `{catalog['snapshot']['id']}`", f"- Candidates: **{len(candidates)}**", "", "| Package | Repository | Version | Declared runtime dependents |", "| --- | --- | --- | ---: |"]
    lines.extend(f"| `{item['name']}` | {item['repository']} | {item['version']} | {item['declared_runtime_dependents']} |" for item in candidates)
    (output / "library-candidates.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    names = {package["id"]: package["name"] for package in packages}
    consumers: dict[str, list[str]] = defaultdict(list)
    for edge in catalog["relationships"]:
        if edge.get("type") == "runtime-depends-on" and edge.get("source") and edge.get("target"):
            source = edge["source"]
            consumers[edge["target"]].append(names.get(source, source))
    impact = [
        {"id": target, "name": names.get(target, target), "declared_consumers": sorted(values), "count": len(values)}
        for target, values in consumers.items()
    ]
    impact.sort(key=lambda item: (-item["count"], item["name"]))
    (output / "reverse-dependency-impact.json").write_text(json.dumps({"snapshot": catalog["snapshot"]["id"], "scope": "declared runtime package dependencies only", "packages": impact}, indent=2) + "\n", encoding="utf-8")
    impact_lines = ["# Generated Reverse Dependency Impact", "", "> Declared package dependencies, not binary/DLL loader evidence.", "", f"- Snapshot: `{catalog['snapshot']['id']}`", "", "| Package | Declared consumers |", "| --- | ---: |"]
    impact_lines.extend(f"| `{item['name']}` | {item['count']} |" for item in impact)
    (output / "reverse-dependency-impact.md").write_text("\n".join(impact_lines) + "\n", encoding="utf-8")
    return {"packages": len(packages), "candidates": len(candidates), "repositories": len(by_repository)}


if __name__ == "__main__":
    print("Built " + ", ".join(f"{key}={value}" for key, value in build().items()))
