#!/usr/bin/env python3
"""Inject a generated facts block into each object page.

The companion objective requires repetitive per-object content to be
generated from the model rather than hand-authored. Object pages currently
restate their subject's kind, authority, packaged version, license, and
evidence in prose, by hand, once per page. Three hundred pages of hand-copied
catalog fields drift the moment the catalog is refreshed, and nothing catches
it: `validate_docs` checks that a `model_ref` resolves, not that the prose
beside it still matches what it resolves to.

This tool writes those fields from the composed model into a marker-delimited
block placed after the page's H1 and before its first authored section, so the
authored prose is untouched and the mechanical fields are correct by
construction.

It deliberately does *not* generate prose. Purpose, boundaries, and analysis
stay hand-authored; only the fields that have one right answer in the model
are generated.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

BEGIN = "<!-- BEGIN GENERATED object-facts -->"
END = "<!-- END GENERATED object-facts -->"

MODEL_REFS = re.compile(r"^model_refs:\s*\n((?:[ \t]+-[ \t]+.*\n)+)", re.M)

# A page may opt out with `object_facts: skip` in its frontmatter. That is for
# pages which reference objects *illustratively* rather than being about one:
# a page about a constraint may cite two example packages without either being
# its subject, and a facts table headed with the first of them would mislead.
OPT_OUT = re.compile(r"^object_facts:\s*skip\s*$", re.M)

# Catalog properties worth surfacing, in the order they are shown.
PACKAGE_FIELDS = (
    ("version", "Version"),
    ("licenses", "License"),
    ("architecture", "Architecture"),
    ("installed_size", "Installed size"),
)

# Kinds whose pages are about a modelled object rather than a topic. A page
# whose first resolving ref is an environment or ecosystem is a narrative
# page, and a facts table on it would be noise.
OBJECT_KINDS = {
    "library",
    "component",
    "package",
    "runtime",
    "subsystem",
    "package-manager",
    "distribution",
    "toolchain",
}


def load_graph() -> dict:
    sys.path.insert(0, str(ROOT / "tools"))
    import akb  # pylint: disable=import-outside-toplevel

    return akb.load_composed_graph()


def primary_ref(text: str, entities: dict) -> str | None:
    match = MODEL_REFS.search(text)
    if not match:
        return None
    for line in match.group(1).splitlines():
        ref = line.strip().lstrip("-").strip()
        if ref in entities:
            return ref
    return None


def humanise_size(raw: str) -> str:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return str(raw)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:,} B" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return str(raw)


def cell(value) -> str:
    """Escape a value for a Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def facts(subject: str, entities: dict, evidence: dict, claims: list) -> str | None:
    entity = entities[subject]
    if entity.get("kind") not in OBJECT_KINDS:
        return None

    rows = [
        ("Object", f"`{subject}`"),
        ("Kind", f"`{entity['kind']}`"),
        ("Status", f"`{entity.get('status', 'unknown')}`"),
        ("Confidence", f"`{entity.get('confidence', 'unknown')}`"),
    ]
    if entity.get("authority"):
        rows.append(("Authority", cell(entity["authority"])))

    environments = (entity.get("applicability") or {}).get("environment_ids") or []
    if environments:
        rows.append(
            ("Environments", ", ".join(f"`{e.split(':')[-1]}`" for e in sorted(environments)))
        )

    properties = entity.get("properties") or {}
    if properties.get("upstream_project"):
        rows.append(("Upstream", f"<{properties['upstream_project']}>"))

    packaged = properties.get("packaged_as")
    if packaged:
        rows.append(("Packaged as", f"`{packaged}`"))
        package = entities.get(packaged)
        if package:
            observed = package.get("properties") or {}
            for key, title in PACKAGE_FIELDS:
                value = observed.get(key)
                if not value:
                    continue
                shown = humanise_size(value) if key == "installed_size" else cell(value)
                rows.append((f"{title} (observed)", shown))

    lines = [
        BEGIN,
        "",
        "| Model fact | Value |",
        "| --- | --- |",
    ]
    lines += [f"| {name} | {value} |" for name, value in rows]

    refs = sorted(entity.get("evidence_refs") or [])
    if refs:
        lines += ["", "**Evidence on this object**", ""]
        for ref in refs:
            record = evidence.get(ref)
            if not record:
                lines.append(f"- `{ref}` — *not resolvable in the composed model*")
                continue
            retrieved = (record.get("retrieved_at") or "")[:10]
            lines.append(
                f"- `{ref}` — {cell(record.get('title', ''))}"
                f" (`{record.get('class', 'unknown')}`"
                + (f", retrieved {retrieved}" if retrieved else "")
                + ")"
            )

    about = [c for c in claims if c.get("subject") == subject]
    if about:
        lines += ["", "**Claims about this object**", ""]
        for claim in sorted(about, key=lambda c: c["id"]):
            lines.append(
                f"- `{claim['id']}` (`{claim.get('classification', '?')}`,"
                f" `{claim.get('confidence', '?')}`) — {cell(claim['statement'])}"
            )

    lines += [
        "",
        "Generated from the composed model by `tools/build_object_facts.py`."
        " Observed values come from the catalog snapshot and change when it"
        " is refreshed.",
        "Edits between the surrounding markers are overwritten on the next"
        " build.",
        "",
        END,
    ]
    return "\n".join(lines)


def splice(text: str, block: str) -> str:
    """Place the block after the H1 and before the first authored section."""
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        finish = text.index(END) + len(END)
        return text[:start] + block + text[finish:]

    heading = re.search(r"^# .*$", text, re.M)
    if not heading:
        return text
    at = heading.end()
    return text[:at] + "\n\n" + block + "\n" + text[at:]


def strip(text: str) -> str:
    start, finish = text.index(BEGIN), text.index(END) + len(END)
    joined = text[:start].rstrip("\n") + "\n\n" + text[finish:].lstrip("\n")
    return joined.rstrip("\n") + "\n"


def build(graph: dict, docs: Path = DOCS, write: bool = True) -> list[Path]:
    """Return the pages whose facts block is out of date."""
    entities = {entity["id"]: entity for entity in graph["entities"]}
    evidence = {record["id"]: record for record in graph.get("evidence", [])}
    claims = graph.get("claims", [])

    written = []
    for path in sorted(docs.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        subject = None if OPT_OUT.search(text) else primary_ref(text, entities)
        block = facts(subject, entities, evidence, claims) if subject else None
        if block is None:
            if BEGIN in text and END in text:
                updated = strip(text)
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
