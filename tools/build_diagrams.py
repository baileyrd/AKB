#!/usr/bin/env python3
"""Generate the Level 0-7 diagram ladder from the composed AKB graph.

The charter requires a drill-down ladder in which every diagram hyperlinks to
related diagrams, and requires diagrams to be generated from the model rather
than hand-drawn. The levels follow the charter ladder:

    L0 ecosystem -> L1 layered architecture -> L2 subsystem -> L3 component
    -> L4 package -> L5 library -> L6 executable and DLL -> L7 source unit

Each level emits three artifacts from the same selection: an SVG carrying
object deep links plus parent/child/sibling navigation, a PlantUML source,
and a Graphviz source.

Selection is deterministic: nodes are ranked by graph degree and broken by
identifier, so a rebuild against an unchanged snapshot is byte-identical.
Where a level is capped, the cap is stated in the diagram itself rather than
silently truncating.
"""

from __future__ import annotations

import html
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "diagrams"
EXPLORER = "../generated/explorer/index.html"

# Levels are (number, slug, title, doc page, node cap, kinds in rank order).
# Rank order also drives vertical placement: earlier kinds sit in higher rows.
LEVELS = [
    (
        0,
        "Ecosystem context",
        "ECOSYSTEM-CONTEXT.md",
        None,
        ["ecosystem", "platform", "runtime", "layer"],
        "The whole ecosystem in one frame: the distribution, the host platform, the POSIX runtime, and the eight architecture layers.",
    ),
    (
        1,
        "Layered architecture",
        "EIGHT-LAYER-ARCHITECTURE.md",
        None,
        ["ecosystem", "layer"],
        "The eight-layer navigation framework. Layering gives navigation; it does not license replacing typed dependency analysis with adjacent-layer assumptions.",
    ),
    (
        2,
        "Subsystems",
        "RUNTIME-ENVIRONMENTS.md",
        None,
        ["platform", "runtime", "environment", "repository"],
        "The major subsystems: the POSIX runtime, the six execution environments, and the six package repositories that serve them.",
    ),
    (
        3,
        "Components",
        "GNU-USERLAND-ROLE-MODEL.md",
        18,
        ["component"],
        "Modelled components ranked by graph degree.",
    ),
    (
        4,
        "Packages",
        "REPOSITORY-PACKAGE-INVENTORY.md",
        18,
        ["package"],
        "Catalog packages ranked by graph degree.",
    ),
    (
        5,
        "Libraries",
        "LIBRARIES-ARCHITECTURE.md",
        18,
        ["library"],
        "Modelled libraries ranked by graph degree.",
    ),
    (
        6,
        "Executables and DLLs",
        "BINARY-DLL-DEPENDENCY-GRAPH.md",
        18,
        ["executable", "dll", "import-library", "static-library"],
        "Binary artifacts recovered by the deep-inventory pipeline.",
    ),
    (
        7,
        "Source and development artifacts",
        "HEADER-AND-METADATA-INDEXES.md",
        18,
        ["header", "pkg-config-module", "filesystem-path"],
        "Source-adjacent development artifacts: headers, pkg-config modules, and owned filesystem paths.",
    ),
]

NODE_W, NODE_H, GAP_X, GAP_Y = 196, 46, 26, 74
MARGIN_X, HEADER_H, FOOTER_H = 28, 96, 62
PER_ROW = 4


def load_graph() -> dict:
    sys.path.insert(0, str(ROOT / "tools"))
    import akb  # pylint: disable=import-outside-toplevel

    return akb.load_composed_graph()


def route_for(identifier: str) -> str:
    return EXPLORER + "#/object/" + quote(identifier, safe="")


def slug(number: int) -> str:
    return f"level-{number}"


def degrees(graph: dict) -> Counter:
    counter: Counter = Counter()
    for edge in graph["relationships"]:
        counter[edge["source"]] += 1
        counter[edge["target"]] += 1
    return counter


def ordinal(entity: dict) -> int:
    """Return a semantic sort position when the model carries one.

    Layers have a documented order that degree ranking would scramble, so an
    explicit ordinal wins over degree wherever the model states it.
    """
    raw = (entity.get("properties") or {}).get("layer_number")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


def select(graph: dict, kinds: list[str], cap: int | None, degree: Counter):
    """Return (nodes, total_available).

    Deterministic: kind order, then any semantic ordinal, then degree
    descending, then identifier. A rebuild against an unchanged snapshot is
    byte-identical.
    """
    pool = [e for e in graph["entities"] if e["kind"] in kinds]
    order = {kind: index for index, kind in enumerate(kinds)}
    pool.sort(key=lambda e: (order[e["kind"]], ordinal(e), -degree[e["id"]], e["id"]))
    if cap is None:
        return pool, len(pool)
    return pool[:cap], len(pool)


def layout(nodes, kinds):
    """Place nodes in rows grouped by kind. Returns positions and canvas size."""
    rows: dict[str, list] = defaultdict(list)
    for node in nodes:
        rows[node["kind"]].append(node)

    positions, row_index = {}, 0
    row_labels = []
    for kind in kinds:
        members = rows.get(kind)
        if not members:
            continue
        for chunk_start in range(0, len(members), PER_ROW):
            chunk = members[chunk_start : chunk_start + PER_ROW]
            for column, node in enumerate(chunk):
                x = MARGIN_X + column * (NODE_W + GAP_X)
                y = HEADER_H + row_index * GAP_Y
                positions[node["id"]] = (x, y)
            row_labels.append((kind if chunk_start == 0 else "", HEADER_H + row_index * GAP_Y))
            row_index += 1

    width = MARGIN_X * 2 + PER_ROW * NODE_W + (PER_ROW - 1) * GAP_X
    height = HEADER_H + max(row_index, 1) * GAP_Y + FOOTER_H
    return positions, row_labels, width, height


def edges_within(graph: dict, positions) -> list[dict]:
    present = set(positions)
    seen, kept = set(), []
    for edge in graph["relationships"]:
        if edge["source"] in present and edge["target"] in present:
            key = (edge["source"], edge["target"], edge["type"])
            if key not in seen:
                seen.add(key)
                kept.append(edge)
    return kept


def anchor(source, target) -> str:
    """Attach an edge to the facing sides of two boxes.

    Anchoring every edge bottom-to-top misroutes edges that run upward or
    sideways, drawing them back through the boxes they came from.
    """
    sx, sy = source
    tx, ty = target
    if ty > sy:  # target below: leave the bottom, arrive at the top
        return f'x1="{sx + NODE_W // 2}" y1="{sy + NODE_H}" x2="{tx + NODE_W // 2}" y2="{ty}"'
    if ty < sy:  # target above: leave the top, arrive at the bottom
        return f'x1="{sx + NODE_W // 2}" y1="{sy}" x2="{tx + NODE_W // 2}" y2="{ty + NODE_H}"'
    if tx >= sx:  # same row, to the right
        return f'x1="{sx + NODE_W}" y1="{sy + NODE_H // 2}" x2="{tx}" y2="{ty + NODE_H // 2}"'
    return f'x1="{sx}" y1="{sy + NODE_H // 2}" x2="{tx + NODE_W}" y2="{ty + NODE_H // 2}"'


def nav_links(number: int) -> list[tuple[str, str]]:
    links = []
    if number > 0:
        links.append((f"Up to L{number - 1}", f"{slug(number - 1)}.svg"))
    if number < len(LEVELS) - 1:
        links.append((f"Down to L{number + 1}", f"{slug(number + 1)}.svg"))
    return links


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_svg(number, title, doc, note, nodes, total, graph, kinds) -> str:
    positions, row_labels, width, height = layout(nodes, kinds)
    drawn = edges_within(graph, positions)
    capped = total > len(nodes)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
        f'<title id="title">Level {number}: {html.escape(title)}</title>',
        f'<desc id="description">{html.escape(note)} '
        f'{len(nodes)} of {total} objects shown, with {len(drawn)} relationships between them. '
        f'Every node links to its object page in the architecture explorer, and the diagram links '
        f'to the levels above and below it. Generated from the composed model by tools/build_diagrams.py.</desc>',
        "<style>"
        ".edge{stroke:#8896ab;stroke-width:1;fill:none}"
        ".node{fill:#eef4ff;stroke:#0645ad;stroke-width:1}"
        ".label{font:12px system-ui,sans-serif;fill:#111}"
        ".kindlabel{font:11px system-ui,sans-serif;fill:#5a6478}"
        ".h1{font:bold 17px system-ui,sans-serif;fill:#111}"
        ".meta{font:12px system-ui,sans-serif;fill:#41485a}"
        ".nav{font:12px system-ui,sans-serif;fill:#0645ad}"
        "</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text class="h1" x="{MARGIN_X}" y="30">Level {number} — {html.escape(title)}</text>',
        f'<text class="meta" x="{MARGIN_X}" y="50">{html.escape(truncate(note, 118))}</text>',
    ]

    offset = MARGIN_X
    for text, target in nav_links(number):
        out.append(
            f'<a href="{target}"><text class="nav" x="{offset}" y="72">{html.escape(text)}</text></a>'
        )
        offset += 11 + 7 * len(text)
    if doc:
        out.append(
            f'<a href="../docs/{doc}"><text class="nav" x="{offset}" y="72">Read {html.escape(doc)}</text></a>'
        )

    for edge in drawn:
        out.append(
            f'<line class="edge" {anchor(positions[edge["source"]], positions[edge["target"]])}>'
            f'<title>{html.escape(edge["type"])}</title></line>'
        )

    for text, y in row_labels:
        if text:
            out.append(f'<text class="kindlabel" x="{MARGIN_X}" y="{y - 6}">{html.escape(text)}</text>')

    for node in nodes:
        x, y = positions[node["id"]]
        name = html.escape(node["name"])
        identifier = html.escape(node["id"])
        out.extend([
            f'<a href="{route_for(node["id"])}" aria-label="{name} ({identifier})">',
            f'<rect class="node" x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="5" tabindex="0">'
            f"<title>{name}: {identifier}</title></rect>",
            f'<text class="label" x="{x + NODE_W // 2}" y="{y + 28}" text-anchor="middle">'
            f"{html.escape(truncate(node['name'], 27))}</text>",
            "</a>",
        ])

    footer = (
        f"{len(nodes)} of {total} objects shown, ranked by graph degree"
        if capped
        else f"All {total} objects of this level shown"
    )
    out.append(f'<text class="meta" x="{MARGIN_X}" y="{height - 32}">{html.escape(footer)}.</text>')
    out.append(
        f'<text class="meta" x="{MARGIN_X}" y="{height - 14}">'
        "Generated from the composed model by tools/build_diagrams.py — do not edit by hand.</text>"
    )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def render_puml(number, title, note, nodes, total, graph, positions_ids) -> str:
    drawn = edges_within(graph, {i: None for i in positions_ids})
    alias = {node["id"]: f"n{index}" for index, node in enumerate(nodes)}
    lines = [
        f"@startuml level-{number}",
        "' Generated from the composed model by tools/build_diagrams.py - do not edit by hand.",
        f"title Level {number} - {title}",
        f"header {len(nodes)} of {total} objects, ranked by graph degree",
        "skinparam componentStyle rectangle",
        "skinparam defaultFontName sans-serif",
    ]
    for node in nodes:
        lines.append(
            f'rectangle "{node["name"]}" as {alias[node["id"]]} <<{node["kind"]}>>'
        )
    for edge in drawn:
        lines.append(
            f'{alias[edge["source"]]} --> {alias[edge["target"]]} : {edge["type"]}'
        )
    if number > 0:
        lines.append(f"note bottom : Parent level-{number - 1}")
    if number < len(LEVELS) - 1:
        lines.append(f"note bottom : Child level-{number + 1}")
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def render_dot(number, title, nodes, total, graph, positions_ids) -> str:
    drawn = edges_within(graph, {i: None for i in positions_ids})
    alias = {node["id"]: f"n{index}" for index, node in enumerate(nodes)}
    lines = [
        f"// Generated from the composed model by tools/build_diagrams.py - do not edit by hand.",
        f"digraph level_{number} {{",
        "  rankdir=TB;",
        '  node [shape=box style=rounded fontname="sans-serif" fontsize=10];',
        '  edge [fontname="sans-serif" fontsize=8 color="#8896ab"];',
        f'  label="Level {number} - {title} ({len(nodes)} of {total} objects, ranked by graph degree)";',
        "  labelloc=t;",
    ]
    for node in nodes:
        escaped = node["name"].replace('"', '\\"')
        lines.append(
            f'  {alias[node["id"]]} [label="{escaped}" tooltip="{node["id"]}" '
            f'URL="{route_for(node["id"])}"];'
        )
    for edge in drawn:
        lines.append(
            f'  {alias[edge["source"]]} -> {alias[edge["target"]]} [label="{edge["type"]}"];'
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def build(graph: dict, output: Path = OUTPUT) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    degree = degrees(graph)
    written = []
    for number, title, doc, cap, kinds, note in LEVELS:
        nodes, total = select(graph, kinds, cap, degree)
        ids = [node["id"] for node in nodes]
        artifacts = {
            f"{slug(number)}.svg": render_svg(number, title, doc, note, nodes, total, graph, kinds),
            f"{slug(number)}.puml": render_puml(number, title, note, nodes, total, graph, ids),
            f"{slug(number)}.dot": render_dot(number, title, nodes, total, graph, ids),
        }
        for name, body in artifacts.items():
            path = output / name
            path.write_text(body, encoding="utf-8")
            written.append(path)
    return written


if __name__ == "__main__":
    for path in build(load_graph()):
        print(path.relative_to(ROOT))
