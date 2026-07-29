#!/usr/bin/env python3
"""Report evidence-backed AKB coverage and explicit remaining gaps."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    graph = json.loads((ROOT / "model" / "catalog" / "current.json").read_text(encoding="utf-8"))
    inventory_path = ROOT / "model" / "inventory" / "current.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8")) if inventory_path.is_file() else {}
    docs = list((ROOT / "docs").glob("*.md"))
    entities = graph["entities"]
    package_count = sum(item["kind"] == "package" for item in entities)
    observed_packages = sorted({
        edge["source"] for edge in inventory.get("relationships", [])
        if edge.get("type") == "installs" and edge.get("source", "").startswith("package:")
    })
    by_kind = Counter(item["kind"] for item in entities)
    status = Counter(item.get("status", "unknown") for item in entities)
    report = {
        "snapshot": graph["snapshot"]["id"], "entities": len(entities),
        "relationships": len(graph["relationships"]), "entity_kinds": dict(sorted(by_kind.items())),
        "entity_status": dict(sorted(status.items())), "authored_documents": len(docs),
        "diagram_files": len(list((ROOT / "diagrams").glob("*.svg"))),
        "package_payload_coverage": {
            "catalog_packages": package_count,
            "observed_packages": len(observed_packages),
            "percent": round((100 * len(observed_packages) / package_count), 3) if package_count else 0,
        },
        "gaps": [
            "Repository catalog evidence does not prove installed file, binary, header, export, or source-unit coverage.",
            "Package-name library candidates are not logical library identities or ABI evidence.",
            "The Level 0–7 linked SVG hierarchy and generated per-object dossiers are navigable, but they do not replace substantive per-object evidence.",
        ],
    }
    output = ROOT / "generated" / "coverage-assessment.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    payload = report["package_payload_coverage"]
    lines = ["# Generated AKB Coverage Assessment", "", f"- Snapshot: `{report['snapshot']}`", f"- Entities: **{report['entities']}**", f"- Relationships: **{report['relationships']}**", f"- Authored documents: **{report['authored_documents']}**", f"- Linked SVG diagrams: **{report['diagram_files']}**", "", "## Package payload coverage", "", f"- Catalog packages: **{payload['catalog_packages']}**", f"- Packages with retained payload observations: **{payload['observed_packages']}**", f"- Observed package coverage: **{payload['percent']}%**", "", "## Explicit gaps", ""]
    lines.extend(f"- {gap}" for gap in report["gaps"])
    (ROOT / "generated" / "coverage-assessment.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__": main()
