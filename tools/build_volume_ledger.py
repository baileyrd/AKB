#!/usr/bin/env python3
"""Generate the per-volume metrics block in the coverage ledger.

The ledger's coverage column read "Partial" for all twenty volumes, which
carried no information: a volume with 164 pages and one with 596 words across
two stubs were reported identically. The charter asks coverage reports to
distinguish eight states, and it asks for gaps to be *measured* rather than
described.

This tool measures. Page counts, second-level heading counts, word counts, and
distinct evidence and model references are computed from the pages themselves.
The coverage state is not computed - it is a judgment, authored in
`model/volume-coverage.json` so that a change to it appears in a diff with its
rationale beside it.

Generated content lives between markers inside the hand-authored ledger, so
the per-volume narrative rows around it are untouched.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LEDGER = DOCS / "VOLUME-COVERAGE-LEDGER.md"
COVERAGE = ROOT / "model" / "volume-coverage.json"

BEGIN = "<!-- BEGIN GENERATED volume-metrics -->"
END = "<!-- END GENERATED volume-metrics -->"

# Other tools' generated blocks must not be counted as authored prose.
GENERATED_BLOCK = re.compile(r"<!-- BEGIN GENERATED .*?<!-- END GENERATED [^>]*-->", re.S)

VOLUME_TITLES = {
    1: "Executive Architecture",
    2: "Windows Platform",
    3: "MSYS Runtime",
    4: "Runtime Environments",
    5: "GNU Userland",
    6: "Libraries",
    7: "Package Management",
    8: "Toolchains",
    9: "Git for Windows",
    10: "Interactive Architecture Explorer",
    11: "Package Catalog",
    12: "Source Code Organization",
    13: "Dependency Analysis",
    14: "Build Systems",
    15: "Extension and Plugin Architecture",
    16: "Security",
    17: "Performance",
    18: "Developer Guide",
    19: "Operations Guide",
    20: "Reference Appendices",
}


def measure(docs: Path = DOCS) -> dict[int, dict]:
    sys.path.insert(0, str(ROOT / "tools"))
    import akb  # pylint: disable=import-outside-toplevel

    volumes: dict[int, dict] = {}
    for path in sorted(docs.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fields = akb.parse_frontmatter(text) or {}
        raw = fields.get("volume")
        if not raw or not str(raw).isdigit():
            continue
        row = volumes.setdefault(
            int(raw),
            {"pages": 0, "headings": 0, "words": 0, "evidence": set(), "refs": set()},
        )
        body = GENERATED_BLOCK.sub("", text.split("---", 2)[-1])
        row["pages"] += 1
        row["headings"] += len(re.findall(r"^## ", body, re.M))
        row["words"] += len(body.split())
        row["evidence"].update(fields.get("evidence_refs") or [])
        row["refs"].update(fields.get("model_refs") or [])
    return volumes


def render(volumes: dict[int, dict], coverage: dict) -> str:
    states = coverage["states"]
    authored = coverage["volumes"]
    total_pages = sum(row["pages"] for row in volumes.values())
    total_words = sum(row["words"] for row in volumes.values())

    lines = [
        BEGIN,
        "",
        "## Measured Coverage",
        "",
        "Page, heading, word, and reference counts are measured from the pages"
        " themselves by `tools/build_volume_ledger.py`. Generated blocks are"
        " excluded from the prose counts, so a volume cannot inflate its word"
        " count by carrying more diagrams.",
        "",
        "The coverage state is a judgment, not a measurement. It is authored in"
        " [`model/volume-coverage.json`](../model/volume-coverage.json) with a"
        " rationale per volume, so changing it shows up in a diff.",
        "",
        "| Vol | Title | State | Pages | `##` | Words | Words/page | Evidence | Model refs |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for number in sorted(VOLUME_TITLES):
        row = volumes.get(number, {"pages": 0, "headings": 0, "words": 0, "evidence": set(), "refs": set()})
        state = authored.get(str(number), {}).get("state", "unknown")
        per_page = round(row["words"] / row["pages"]) if row["pages"] else 0
        lines.append(
            f"| {number} | {VOLUME_TITLES[number]} | `{state}` | {row['pages']} | "
            f"{row['headings']} | {row['words']:,} | {per_page:,} | "
            f"{len(row['evidence'])} | {len(row['refs'])} |"
        )
    lines.append(
        f"| | **Total** | | **{total_pages}** | "
        f"**{sum(r['headings'] for r in volumes.values()):,}** | "
        f"**{total_words:,}** | | | |"
    )

    lines += ["", "### What the numbers say", ""]

    ranked = sorted(volumes.items(), key=lambda kv: kv[1]["words"], reverse=True)
    top, top_row = ranked[0]
    share = round(100 * top_row["words"] / total_words, 1)
    lines.append(
        f"- Volume {top} ({VOLUME_TITLES[top]}) holds {top_row['pages']} of"
        f" {total_pages} pages and {share}% of all prose."
    )

    no_evidence = [n for n in sorted(VOLUME_TITLES) if not volumes.get(n, {}).get("evidence")]
    if no_evidence:
        lines.append(
            f"- {len(no_evidence)} volumes cite no evidence record on any page:"
            f" {', '.join(str(n) for n in no_evidence)}. Their claims are"
            " authored rather than sourced."
        )

    thinnest = min(
        (kv for kv in volumes.items() if kv[1]["pages"]),
        key=lambda kv: kv[1]["words"] / kv[1]["pages"],
    )
    lines.append(
        f"- Volume {thinnest[0]} ({VOLUME_TITLES[thinnest[0]]}) has the lowest"
        f" prose density at {round(thinnest[1]['words'] / thinnest[1]['pages']):,}"
        " words per page."
    )

    used = {authored.get(str(n), {}).get("state") for n in VOLUME_TITLES}
    unused = [s for s in states if s not in used]
    lines.append(
        f"- {len(used)} of the charter's {len(states)} coverage states are in use."
        f" Unused: {', '.join(f'`{s}`' for s in unused)}."
        if unused
        else f"- All {len(states)} charter coverage states are in use."
    )

    lines += [
        "",
        "### Coverage states",
        "",
        "| State | Meaning |",
        "| --- | --- |",
    ]
    for name, meaning in states.items():
        lines.append(f"| `{name}` | {meaning} |")

    lines += [
        "",
        "### Why each volume carries the state it does",
        "",
    ]
    for number in sorted(VOLUME_TITLES):
        entry = authored.get(str(number))
        if not entry:
            continue
        lines.append(
            f"**{number} {VOLUME_TITLES[number]} — `{entry['state']}`.**"
            f" {entry['rationale']}"
        )
        lines.append("")

    lines += [
        "Generated from the pages and `model/volume-coverage.json` by"
        " `tools/build_volume_ledger.py`.",
        "Edits between the surrounding markers are overwritten on the next build.",
        "",
        END,
    ]
    return "\n".join(lines)


def splice(text: str, block: str) -> str:
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        finish = text.index(END) + len(END)
        return text[:start] + block + text[finish:]
    return text.rstrip("\n") + "\n\n" + block + "\n"


def build(write: bool = True) -> bool:
    """Return True if the ledger's generated block is out of date."""
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    text = LEDGER.read_text(encoding="utf-8")
    updated = splice(text, render(measure(), coverage))
    if updated == text:
        return False
    if write:
        LEDGER.write_text(updated, encoding="utf-8")
    return True


if __name__ == "__main__":
    print("ledger updated" if build() else "ledger already current")
