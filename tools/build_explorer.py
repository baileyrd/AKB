#!/usr/bin/env python3
"""Build a static, deep-linkable explorer from the composed AKB graph."""

from __future__ import annotations

import html
import json
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "generated" / "explorer"


def load_graph() -> dict:
    """Load the validated composed graph through the canonical generator."""
    sys.path.insert(0, str(ROOT / "tools"))
    import akb  # pylint: disable=import-outside-toplevel

    akb.validate()
    return akb.load_composed_graph()


def route_for(identifier: str) -> str:
    """Return the canonical hash route for an immutable object identifier."""
    return "#/object/" + quote(identifier, safe="")


def build(graph: dict, output: Path = OUTPUT) -> list[Path]:
    """Write a no-dependency static explorer and an accessible object index."""
    output.mkdir(parents=True, exist_ok=True)
    entities = sorted(graph["entities"], key=lambda item: item["id"])
    outgoing: dict[str, list[dict]] = defaultdict(list)
    incoming: dict[str, list[dict]] = defaultdict(list)
    for edge in graph["relationships"]:
        outgoing[edge["source"]].append(edge)
        incoming[edge["target"]].append(edge)
    data = {"entities": entities, "relationships": graph["relationships"]}
    rows = "\n".join(
        f'<li><a href="{route_for(item["id"])}">{html.escape(item["name"])}</a> '
        f'<code>{html.escape(item["id"])}</code></li>'
        for item in entities
    )
    script = """
const data = __DATA__;
const byId = Object.fromEntries(data.entities.map(item => [item.id, item]));
const esc = value => String(value).replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));
const route = id => '#/object/' + encodeURIComponent(id);
function render() {
  const id = decodeURIComponent(location.hash.replace(/^#\\/object\\//, ''));
  const item = byId[id];
  const root = document.querySelector('main');
  if (!item) { root.innerHTML = '<h1>Architecture Explorer</h1><p>Select an object from the <a href="#/">text index</a>.</p>'; return; }
  const out = data.relationships.filter(edge => edge.source === id);
  const inc = data.relationships.filter(edge => edge.target === id);
  const links = edges => edges.length ? '<ul>' + edges.map(edge => { const other = edge.source === id ? edge.target : edge.source; return `<li><code>${esc(edge.type)}</code> <a href="${route(other)}">${esc(byId[other]?.name || other)}</a></li>`; }).join('') + '</ul>' : '<p>None.</p>';
  root.innerHTML = `<p><a href="#/">Text index</a></p><h1>${esc(item.name)}</h1><dl><dt>ID</dt><dd><code>${esc(item.id)}</code></dd><dt>Kind</dt><dd>${esc(item.kind)}</dd><dt>Status</dt><dd>${esc(item.status)}</dd></dl>${item.summary ? `<p>${esc(item.summary)}</p>` : ''}<h2>Outgoing relationships</h2>${links(out)}<h2>Incoming relationships</h2>${links(inc)}`;
}
addEventListener('hashchange', render); render();
""".replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AKB Explorer</title>
<style>body{{font:16px system-ui,sans-serif;max-width:70rem;margin:auto;padding:1rem}}code{{overflow-wrap:anywhere}}a{{color:#0645ad}}dt{{font-weight:bold}}dd{{margin:0 0 1rem}}</style></head>
<body><main><h1>Architecture Explorer</h1><p>Use stable object links or the textual index.</p><ul>{rows}</ul></main><script>{script}</script></body></html>"""
    index = output / "index.html"
    index.write_text(page, encoding="utf-8")
    return [index]


if __name__ == "__main__":
    for path in build(load_graph()):
        print(path.relative_to(ROOT))
