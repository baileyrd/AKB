#!/usr/bin/env python3
"""Report evidence-backed AKB coverage and explicit remaining gaps."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    graph = json.loads((ROOT / "model" / "catalog" / "current.json").read_text(encoding="utf-8"))
    docs = list((ROOT / "docs").glob("*.md"))
    entities = graph["entities"]
    by_kind = Counter(item["kind"] for item in entities)
    status = Counter(item.get("status", "unknown") for item in entities)
    report = {
        "snapshot": graph["snapshot"]["id"], "entities": len(entities),
        "relationships": len(graph["relationships"]), "entity_kinds": dict(sorted(by_kind.items())),
        "entity_status": dict(sorted(status.items())), "authored_documents": len(docs),
        "diagram_files": len(list((ROOT / "diagrams").glob("*.svg"))),
        "gaps": [
            "Repository catalog evidence does not prove installed file, binary, header, export, or source-unit coverage.",
            "Package-name library candidates are not logical library identities or ABI evidence.",
            "Per-object documentation and Level 1–7 linked diagrams remain incomplete.",
        ],
    }
    output = ROOT / "generated" / "coverage-assessment.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Generated AKB Coverage Assessment", "", f"- Snapshot: `{report['snapshot']}`", f"- Entities: **{report['entities']}**", f"- Relationships: **{report['relationships']}**", f"- Authored documents: **{report['authored_documents']}**", f"- Linked SVG diagrams: **{report['diagram_files']}**", "", "## Explicit gaps", ""]
    lines.extend(f"- {gap}" for gap in report["gaps"])
    (ROOT / "generated" / "coverage-assessment.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__": main()
