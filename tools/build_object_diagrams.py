#!/usr/bin/env python3
"""Inject a generated Mermaid dependency subgraph into each object page.

The charter requires diagrams on object pages and requires repetitive
per-object content to be generated from the model rather than hand-authored.
This writes one subgraph per documentation page whose primary `model_refs`
entry resolves to an entity carrying dependency edges.

The block is delimited by markers and rewritten in place on every run, so it
is safe to regenerate and safe to hand-edit around. Everything between the
markers is owned by this tool; everything outside it is not touched.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

BEGIN = "<!-- BEGIN GENERATED dependency-subgraph -->"
END = "<!-- END GENERATED dependency-subgraph -->"

# Edge types that express "A needs B" in some form. Containment, packaging,
# and provenance edges are deliberately excluded: they make the subgraph a
# taxonomy rather than a dependency view.
DEPENDENCY_TYPES = {
    "requires",
    "runtime-depends-on",
    "build-depends-on",
    "check-depends-on",
    "optional-depends-on",
    "imports-dll",
    "links-dynamically",
    "links-statically",
    "uses-runtime",
}

SIDE_LIMIT = 8
MODEL_REFS = re.compile(r"^model_refs:\s*\n((?:[ \t]+-[ \t]+.*\n)+)", re.M)


def load_graph() -> dict:
    sys.path.insert(0, str(ROOT / "tools"))
    import akb  # pylint: disable=import-outside-toplevel

    return akb.load_composed_graph()


def label(name: str) -> str:
    """Make an entity name safe inside a Mermaid quoted label."""
    cleaned = name.replace('"', "'").replace("\n", " ").strip()
    cleaned = cleaned.replace("#", "＃").replace("`", "'")
    return cleaned if len(cleaned) <= 34 else cleaned[:33] + "…"


def primary_ref(text: str, entities: dict) -> str | None:
    """Return the page's subject: its first model_ref that resolves."""
    match = MODEL_REFS.search(text)
    if not match:
        return None
    for line in match.group(1).splitlines():
        ref = line.strip().lstrip("-").strip()
        if ref in entities:
            return ref
    return None


def subgraph(subject: str, entities: dict, out_edges, in_edges) -> str | None:
    """Render the Mermaid block for one subject, or None if it has no edges."""
    dependencies, seen = [], set()
    for edge in out_edges.get(subject, []):
        if edge["target"] in entities and edge["target"] not in seen:
            seen.add(edge["target"])
            dependencies.append(edge)
    dependents, seen = [], set()
    for edge in in_edges.get(subject, []):
        if edge["source"] in entities and edge["source"] not in seen:
            seen.add(edge["source"])
            dependents.append(edge)

    if not dependencies and not dependents:
        return None

    dependencies.sort(key=lambda e: (e["target"], e["type"]))
    dependents.sort(key=lambda e: (e["source"], e["type"]))
    shown_deps, shown_dependents = dependencies[:SIDE_LIMIT], dependents[:SIDE_LIMIT]

    lines = ["```mermaid", "flowchart LR"]
    lines.append(f'    subject["{label(entities[subject]["name"])}"]')

    for index, edge in enumerate(shown_dependents):
        node = f"u{index}"
        lines.append(f'    {node}["{label(entities[edge["source"]]["name"])}"]')
        lines.append(f'    {node} -->|{edge["type"]}| subject')
    for index, edge in enumerate(shown_deps):
        node = f"d{index}"
        lines.append(f'    {node}["{label(entities[edge["target"]]["name"])}"]')
        lines.append(f'    subject -->|{edge["type"]}| {node}')

    lines.append("    style subject stroke-width:3px")
    lines.append("```")

    caption = (
        f"Dependencies and dependents of `{subject}` in the composed graph: "
        f"{len(dependents)} dependent{'' if len(dependents) == 1 else 's'} "
        f"and {len(dependencies)} dependenc{'y' if len(dependencies) == 1 else 'ies'}"
    )
    hidden = (len(dependencies) - len(shown_deps)) + (len(dependents) - len(shown_dependents))
    caption += f", of which {hidden} are omitted here for legibility." if hidden else "."

    return "\n".join(
        [
            BEGIN,
            "",
            "## Dependency Diagram",
            "",
            *lines,
            "",
            caption,
            "",
            "Generated from the composed model by `tools/build_object_diagrams.py`.",
            "Edits between the surrounding markers are overwritten on the next build.",
            "",
            END,
        ]
    )


def splice(text: str, block: str) -> str:
    """Insert or replace the generated block, leaving authored prose alone."""
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        finish = text.index(END) + len(END)
        return text[:start] + block + text[finish:]

    anchor = "\n## Related Objects"
    if anchor in text:
        at = text.index(anchor)
        return text[:at] + "\n" + block + "\n" + text[at:]
    return text.rstrip("\n") + "\n\n" + block + "\n"


def build(graph: dict, docs: Path = DOCS, write: bool = True) -> list[Path]:
    """Return the pages whose generated block is out of date.

    With ``write=False`` nothing is written, so a caller can ask "would this
    change anything?" without changing anything. The idempotence test needs
    that: a checking test that repairs what it is checking passes on its own
    second run and hides the failure it just reported.
    """
    entities = {entity["id"]: entity for entity in graph["entities"]}
    out_edges, in_edges = defaultdict(list), defaultdict(list)
    for edge in graph["relationships"]:
        if edge["type"] in DEPENDENCY_TYPES:
            out_edges[edge["source"]].append(edge)
            in_edges[edge["target"]].append(edge)

    written = []
    for path in sorted(docs.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        subject = primary_ref(text, entities)
        block = subgraph(subject, entities, out_edges, in_edges) if subject else None
        if block is None:
            # No subject or no dependency edges: remove a stale block if one
            # was written by an earlier snapshot, otherwise leave the page be.
            if BEGIN in text and END in text:
                start, finish = text.index(BEGIN), text.index(END) + len(END)
                updated = (text[:start].rstrip("\n") + "\n\n" + text[finish:].lstrip("\n")).rstrip("\n") + "\n"
                if updated != text:
                    if write:
                        path.write_text(updated, encoding="utf-8")
                    written.append(path)
            continue
        updated = splice(text, block)
        if updated != text:
            if write:
                path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


if __name__ == "__main__":
    changed = build(load_graph())
    for path in changed:
        print(path.relative_to(ROOT))
    print(f"{len(changed)} pages updated")
