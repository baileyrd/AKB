#!/usr/bin/env python3
"""Build a static, deep-linkable explorer from the composed AKB graph."""

from __future__ import annotations

import html
import json
import math
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
const isDependency = edge => edge.type.includes('depends-on') || edge.type === 'requires' || edge.type === 'imports-dll';
// A view projects the graph by entity kind, by tag, or by both. Toolchain
// tools are modelled as components carrying a toolchain/build-system tag
// rather than as a dedicated kind, so a kind-only projection renders that
// view empty while the objects exist. Keep in sync with EXPLORER_VIEWS in
// tests/test_roadmap_claims.py.
const views = {layers:{kinds:['layer']}, packages:{kinds:['package','package-artifact']}, artifacts:{kinds:['dll','executable','import-library','static-library','filesystem-path']}, libraries:{kinds:['library','dll','import-library','static-library']}, runtimes:{kinds:['runtime','environment','crt','abi']}, toolchains:{kinds:['toolchain','compiler','linker','debugger','build-system'], tags:['toolchain','compiler','linker','debugger','build-system']}, repositories:{kinds:['repository','mirror','source-repository']}, evidenced:{}};
const inView = (entry, spec) => (spec.kinds || []).includes(entry.kind) || (spec.tags || []).some(tag => (entry.tags || []).includes(tag));
const viewRoute = name => '#/view/' + name;
const viewLinks = () => `<nav aria-label="Explorer views"><strong>Views:</strong> ${Object.keys(views).map(name => `<a href="${viewRoute(name)}">${esc(name)}</a>`).join(' · ')}</nav>`;
const compactValue = value => { if (Array.isArray(value)) return `${value.length} item${value.length === 1 ? '' : 's'}${value.length ? `: ${value.slice(0, 8).map(item => typeof item === 'object' ? (item.name || item.dll || JSON.stringify(item)) : item).join(', ')}` : ''}`; if (value && typeof value === 'object') return Object.entries(value).map(([key, item]) => `${key}=${item}`).join(', '); return String(value); };
const objectDetails = item => { const properties = Object.entries(item.properties || {}); const evidence = item.evidence_refs || []; return `${properties.length ? `<section aria-labelledby="properties"><h2 id="properties">Observed properties</h2><dl>${properties.map(([key, value]) => `<dt>${esc(key)}</dt><dd>${esc(compactValue(value))}</dd>`).join('')}</dl></section>` : ''}${evidence.length ? `<section aria-labelledby="evidence"><h2 id="evidence">Evidence</h2><ul>${evidence.map(reference => `<li><code>${esc(reference)}</code></li>`).join('')}</ul></section>` : '<section aria-labelledby="evidence"><h2 id="evidence">Evidence</h2><p>No evidence reference is attached to this object.</p></section>'}`; };
const index = () => {
  const kinds = [...new Set(data.entities.map(item => item.kind))].sort();
  const statuses = [...new Set(data.entities.map(item => item.status))].sort();
  return `${viewLinks()}<h1>Architecture Explorer</h1><p>Search the composed graph or narrow the textual index.</p><label>Search <input id="search" type="search" autofocus></label> <label>Kind <select id="kind"><option value="">All</option>${kinds.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label> <label>Status <select id="status"><option value="">All</option>${statuses.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label><p id="count"></p><ul id="results"></ul>`;
};
function bindIndex() {
  const search = document.querySelector('#search'), kind = document.querySelector('#kind'), status = document.querySelector('#status'), results = document.querySelector('#results'), count = document.querySelector('#count');
  const update = () => { const term = search.value.toLowerCase(); const found = data.entities.filter(item => (!term || [item.id,item.name,...(item.aliases||[]),...(item.tags||[])].join(' ').toLowerCase().includes(term)) && (!kind.value || item.kind === kind.value) && (!status.value || item.status === status.value)); count.textContent = `${found.length} objects`; results.innerHTML = found.map(item => `<li><a href="${route(item.id)}">${esc(item.name)}</a> <code>${esc(item.id)}</code> — ${esc(item.kind)}, ${esc(item.status)}</li>`).join(''); }; [search,kind,status].forEach(control => control.addEventListener('input', update)); update();
}
// Zoomable neighbourhood rendering. No library: the SVG viewBox is the whole
// zoom model, so pan and zoom are arithmetic on four numbers. Layout is
// deterministic - dependencies fan right, dependents fan left, both ordered by
// id - so the same object always draws the same picture and the accessible
// list below the figure always matches what is on screen.
const GRAPH_LIMIT = 14;
const graphRoute = id => '#/graph/' + encodeURIComponent(id);
function neighbourhood(id) {
  const pick = edges => [...new Map(edges.map(e => [e.source === id ? e.target : e.source, e])).values()]
    .filter(e => byId[e.source === id ? e.target : e.source])
    .sort((a, b) => ((a.source === id ? a.target : a.source) < (b.source === id ? b.target : b.source) ? -1 : 1));
  const deps = pick(data.relationships.filter(e => e.source === id && isDependency(e)));
  const dependents = pick(data.relationships.filter(e => e.target === id && isDependency(e)));
  return {deps, dependents};
}
function graphFigure(id) {
  const item = byId[id];
  const {deps, dependents} = neighbourhood(id);
  const right = deps.slice(0, GRAPH_LIMIT), left = dependents.slice(0, GRAPH_LIMIT);
  const hidden = (deps.length - right.length) + (dependents.length - left.length);
  const span = Math.max(right.length, left.length, 1);
  const H = 120 + span * 54, mid = H / 2;
  const place = (list, x) => list.map((edge, i) => ({
    edge, other: edge.source === id ? edge.target : edge.source,
    x, y: mid + (i - (list.length - 1) / 2) * 54
  }));
  const nodes = [...place(left, 130), ...place(right, 770)];
  const node = n => {
    const name = esc((byId[n.other].name || n.other).slice(0, 18));
    return `<a href="${route(n.other)}" aria-label="${esc(byId[n.other].name || n.other)} (${esc(n.other)})">`
      + `<rect class="gnode" x="${n.x - 82}" y="${n.y - 17}" width="164" height="34" rx="5" tabindex="0">`
      + `<title>${esc(n.other)}</title></rect>`
      + `<text class="glabel" x="${n.x}" y="${n.y + 5}" text-anchor="middle">${name}</text></a>`;
  };
  const edge = n => `<line class="gedge" x1="${n.x < 450 ? n.x + 82 : 450 - 92}" y1="${n.x < 450 ? n.y : mid}"`
    + ` x2="${n.x < 450 ? 450 - 92 : n.x - 82}" y2="${n.x < 450 ? mid : n.y}">`
    + `<title>${esc(n.edge.type)}</title></line>`;
  return {
    height: H,
    svg: `<svg id="graph" viewBox="0 0 900 ${H}" width="100%" height="${Math.min(H, 620)}" role="img" tabindex="0"`
      + ` aria-labelledby="gtitle gdesc" xmlns="http://www.w3.org/2000/svg">`
      + `<title id="gtitle">Dependency neighbourhood of ${esc(item.name)}</title>`
      + `<desc id="gdesc">${left.length} dependents on the left and ${right.length} dependencies on the right,`
      + ` drawn around ${esc(item.name)}. Every node is a keyboard-focusable link. The same information is`
      + ` listed as text below this figure.</desc>`
      + nodes.map(edge).join('') + nodes.map(node).join('')
      + `<rect class="gsubject" x="358" y="${mid - 22}" width="184" height="44" rx="6"/>`
      + `<text class="glabel gsubjectlabel" x="450" y="${mid + 5}" text-anchor="middle">${esc((item.name || id).slice(0, 20))}</text>`
      + `</svg>`,
    hidden, deps, dependents
  };
}
function bindZoom() {
  const svg = document.querySelector('#graph');
  if (!svg) return;
  const base = svg.getAttribute('viewBox').split(' ').map(Number);
  let box = base.slice();
  const apply = () => svg.setAttribute('viewBox', box.join(' '));
  const zoom = (factor, cx, cy) => {
    const w = Math.min(base[2] * 4, Math.max(base[2] / 8, box[2] * factor));
    const scale = w / box[2];
    box = [cx - (cx - box[0]) * scale, cy - (cy - box[1]) * scale, w, box[3] * scale];
    apply();
  };
  const centre = () => [box[0] + box[2] / 2, box[1] + box[3] / 2];
  const point = event => {
    const rect = svg.getBoundingClientRect();
    return [box[0] + (event.clientX - rect.left) / rect.width * box[2],
            box[1] + (event.clientY - rect.top) / rect.height * box[3]];
  };
  svg.addEventListener('wheel', event => { event.preventDefault(); const [x, y] = point(event); zoom(event.deltaY > 0 ? 1.2 : 1 / 1.2, x, y); }, {passive: false});
  let dragging = null;
  svg.addEventListener('pointerdown', event => { dragging = point(event); svg.setPointerCapture(event.pointerId); });
  svg.addEventListener('pointerup', event => { dragging = null; svg.releasePointerCapture(event.pointerId); });
  svg.addEventListener('pointermove', event => {
    if (!dragging) return;
    const [x, y] = point(event);
    box = [box[0] + dragging[0] - x, box[1] + dragging[1] - y, box[2], box[3]];
    apply();
  });
  // Keyboard equivalents, because pointer gestures are not an interface.
  svg.addEventListener('keydown', event => {
    const step = box[2] / 10;
    const moves = {ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, -step], ArrowDown: [0, step]};
    if (moves[event.key]) { box = [box[0] + moves[event.key][0], box[1] + moves[event.key][1], box[2], box[3]]; apply(); event.preventDefault(); return; }
    if (event.key === '+' || event.key === '=') { zoom(1 / 1.4, ...centre()); event.preventDefault(); }
    if (event.key === '-') { zoom(1.4, ...centre()); event.preventDefault(); }
    if (event.key === '0') { box = base.slice(); apply(); event.preventDefault(); }
  });
  const on = (selector, handler) => { const button = document.querySelector(selector); if (button) button.addEventListener('click', handler); };
  on('#zoom-in', () => zoom(1 / 1.4, ...centre()));
  on('#zoom-out', () => zoom(1.4, ...centre()));
  on('#zoom-reset', () => { box = base.slice(); apply(); });
}
function graphView(id) {
  const item = byId[id];
  const root = document.querySelector('main');
  if (!item) { root.innerHTML = `${viewLinks()}<h1>Unknown object</h1><p><a href="#/">Return to the explorer index.</a></p>`; return; }
  const figure = graphFigure(id);
  const list = (edges, heading) => `<h3>${heading} (${edges.length})</h3>` + (edges.length
    ? `<ul>${edges.map(e => { const other = e.source === id ? e.target : e.source; return `<li><code>${esc(e.type)}</code> <a href="${route(other)}">${esc(byId[other].name || other)}</a></li>`; }).join('')}</ul>`
    : '<p>None.</p>');
  root.innerHTML = `<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <a href="${route(id)}">${esc(item.name)}</a> / <span aria-current="page">graph</span></nav>`
    + `<h1>${esc(item.name)} — dependency graph</h1>`
    + `<div role="group" aria-label="Zoom controls"><button type="button" id="zoom-in">Zoom in</button> <button type="button" id="zoom-out">Zoom out</button> <button type="button" id="zoom-reset">Reset view</button></div>`
    + `<p>Scroll or use the buttons to zoom, drag to pan. With the figure focused: arrow keys pan, <kbd>+</kbd> and <kbd>-</kbd> zoom, <kbd>0</kbd> resets.</p>`
    + `<figure>${figure.svg}<figcaption>${figure.hidden ? `${figure.hidden} neighbour${figure.hidden === 1 ? '' : 's'} omitted from the figure for legibility; all of them are listed below.` : 'All neighbours are shown.'}</figcaption></figure>`
    + `<section aria-labelledby="textual"><h2 id="textual">Textual equivalent</h2>`
    + `<p>Everything in the figure, as text. This is the accessible fallback and it is complete where the figure is bounded.</p>`
    + list(figure.dependents, 'Dependents') + list(figure.deps, 'Dependencies') + '</section>';
  bindZoom();
}
function render() {
  const hash = location.hash || '#/';
  const view = decodeURIComponent(hash.replace(/^#\\/view\\//, ''));
  const id = decodeURIComponent(hash.replace(/^#\\/object\\//, ''));
  if (hash.startsWith('#/graph/')) { graphView(decodeURIComponent(hash.replace(/^#\\/graph\\//, ''))); return; }
  const item = byId[id];
  const root = document.querySelector('main');
  if (hash.startsWith('#/view/')) { const spec = views[view]; if (!spec) { root.innerHTML = `${viewLinks()}<h1>Unknown view</h1><p><a href="#/">Return to the explorer index.</a></p>`; return; } const members = view === 'evidenced' ? data.entities.filter(entry => (entry.evidence_refs || []).length) : data.entities.filter(entry => inView(entry, spec)); root.innerHTML = `${viewLinks()}<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <span aria-current="page">${esc(view)}</span></nav><h1>${esc(view)} view</h1><p>${members.length} ${view === 'evidenced' ? 'objects with attached evidence' : 'typed objects'}.</p><ul>${members.map(entry => `<li><a href="${route(entry.id)}">${esc(entry.name)}</a> <code>${esc(entry.kind)}</code></li>`).join('') || '<li>No objects in the current projection.</li>'}</ul>`; return; }
  if (!item) { root.innerHTML = index(); bindIndex(); return; }
  const out = data.relationships.filter(edge => edge.source === id);
  const inc = data.relationships.filter(edge => edge.target === id);
  const dependencies = out.filter(isDependency);
  const dependents = inc.filter(isDependency);
  const links = (edges, direction) => { const limit = 25; if (!edges.length) return '<p>None.</p>'; const rows = edges.map((edge, index) => { const other = edge.source === id ? edge.target : edge.source; return `<li${index >= limit ? ' hidden' : ''}><code>${esc(edge.type)}</code> <a href="${route(other)}">${esc(byId[other]?.name || other)}</a></li>`; }).join(''); const control = edges.length > limit ? `<button type="button" class="expand" data-direction="${direction}" aria-expanded="false">Show ${edges.length - limit} more</button>` : ''; return `<ul data-direction="${direction}">${rows}</ul>${control}`; };
  root.innerHTML = `<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <span>${esc(item.kind)}</span> / <span aria-current="page">${esc(item.name)}</span></nav><h1>${esc(item.name)}</h1><p><a href="${graphRoute(item.id)}">View this object's dependency graph</a> — zoomable, with a textual equivalent.</p><dl><dt>ID</dt><dd><code>${esc(item.id)}</code></dd><dt>Kind</dt><dd>${esc(item.kind)}</dd><dt>Status</dt><dd>${esc(item.status)}</dd></dl>${item.summary ? `<p>${esc(item.summary)}</p>` : ''}${objectDetails(item)}<section aria-labelledby="dependencies"><h2 id="dependencies">Dependencies</h2>${links(dependencies, 'dependencies')}</section><section aria-labelledby="dependents"><h2 id="dependents">Dependents</h2>${links(dependents, 'dependents')}</section><h2>Outgoing relationships</h2>${links(out, 'outgoing')}<h2>Incoming relationships</h2>${links(inc, 'incoming')}`;
  root.querySelectorAll('.expand').forEach(button => button.addEventListener('click', () => { const list = root.querySelector(`ul[data-direction="${button.dataset.direction}"]`); const expanded = button.getAttribute('aria-expanded') === 'true'; list.querySelectorAll('li[hidden]').forEach(row => row.hidden = expanded); button.setAttribute('aria-expanded', String(!expanded)); button.textContent = expanded ? `Show ${list.querySelectorAll('li[hidden]').length} more` : 'Collapse relationships'; }));
}
addEventListener('hashchange', render); render();
""".replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AKB Explorer</title>
<style>body{{font:16px system-ui,sans-serif;max-width:70rem;margin:auto;padding:1rem}}code{{overflow-wrap:anywhere}}a{{color:#0645ad}}dt{{font-weight:bold}}dd{{margin:0 0 1rem}}
figure{{margin:1rem 0;border:1px solid #d0d5dd;border-radius:6px;padding:.5rem;overflow:hidden}}
figcaption{{font-size:.875rem;color:#475467;padding-top:.5rem}}
#graph{{display:block;touch-action:none;cursor:grab;background:#fcfcfd}}
#graph:active{{cursor:grabbing}}
#graph:focus-visible{{outline:3px solid #0645ad;outline-offset:2px}}
.gedge{{stroke:#98a2b3;stroke-width:1.5}}
.gnode{{fill:#eef4ff;stroke:#0645ad}}
.gnode:focus-visible{{outline:3px solid #b42318}}
.gsubject{{fill:#0645ad;stroke:#03306b}}
.glabel{{font:12px system-ui,sans-serif;fill:#101828;pointer-events:none}}
.gsubjectlabel{{fill:#fff;font-weight:600}}
kbd{{font:inherit;border:1px solid #d0d5dd;border-radius:3px;padding:0 .25rem;background:#f9fafb}}</style></head>
<body><main><h1>Architecture Explorer</h1><p>Use stable object links or the textual index.</p><ul>{rows}</ul></main><script>{script}</script></body></html>"""
    index = output / "index.html"
    index.write_text(page, encoding="utf-8")
    visible = entities[:80]
    positions = {
        item["id"]: (70 + (number % 8) * 100, 70 + (number // 8) * 80)
        for number, item in enumerate(visible)
    }
    height = max(140, 100 + math.ceil(len(visible) / 8) * 80)
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{height}" viewBox="0 0 860 {height}" role="img" aria-labelledby="title description">',
        '<title id="title">AKB architecture graph overview</title>',
        '<desc id="description">A bounded overview of the composed architecture graph. Each labeled node is a keyboard-focusable link to its object detail. Use overview.txt for a complete textual relationship list.</desc>',
        '<style>.edge{stroke:#667085;stroke-width:1}.node{fill:#eef4ff;stroke:#0645ad}.label{font:11px system-ui,sans-serif;fill:#111}</style>',
    ]
    for edge in graph["relationships"]:
        if edge["source"] in positions and edge["target"] in positions:
            x1, y1 = positions[edge["source"]]
            x2, y2 = positions[edge["target"]]
            svg_lines.append(f'<line class="edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><title>{html.escape(edge["type"])}</title></line>')
    for item in visible:
        x, y = positions[item["id"]]
        label = html.escape(item["name"])
        identifier = html.escape(item["id"])
        svg_lines.extend([
            f'<a href="index.html{route_for(item["id"])}" aria-label="{label} ({identifier})">',
            f'<rect class="node" x="{x - 42}" y="{y - 16}" width="84" height="32" rx="4" tabindex="0"><title>{label}: {identifier}</title></rect>',
            f'<text class="label" x="{x}" y="{y + 4}" text-anchor="middle">{label[:13]}</text>',
            '</a>',
        ])
    svg_lines.append('</svg>')
    svg = output / "overview.svg"
    svg.write_text("\n".join(svg_lines) + "\n", encoding="utf-8")
    text = output / "overview.txt"
    text.write_text(
        "AKB architecture graph overview\n\nObjects\n" + "\n".join(
            f"- {item['id']} ({item['kind']}): {item['name']}" for item in entities
        ) + "\n\nRelationships\n" + "\n".join(
            f"- {edge['source']} --{edge['type']}--> {edge['target']}"
            for edge in graph["relationships"]
        ) + "\n",
        encoding="utf-8",
    )
    return [index, svg, text]


if __name__ == "__main__":
    for path in build(load_graph()):
        print(path.relative_to(ROOT))
