#!/usr/bin/env python3
"""Build a static, deep-linkable explorer from the composed AKB graph."""

from __future__ import annotations

import html
import json
import math
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "generated" / "explorer"
VENDOR_D3 = ROOT / "tools" / "vendor" / "d3.v7.min.js"

# Fields the rendered page actually reads. `confidence`, `authority`, and
# `applicability` are modelled on every entity and displayed by none of the
# views, so embedding them cost megabytes and rendered nothing. Anything a
# view starts reading has to be added here as well as used in the script.
ENTITY_FIELDS = (
    "id",
    "kind",
    "name",
    "status",
    "summary",
    "tags",
    "aliases",
    "properties",
    "evidence_refs",
)

# Ceiling for the embedded page, enforced by tests/test_explorer.py. The
# page is a single tracked file regenerated on every build, so unbounded
# growth shows up in every diff and every clone. GitHub warns above 50 MB;
# this leaves room for the graph to roughly double before the ceiling
# forces a decision rather than letting the file quietly pass 50 MB.
MAX_INDEX_BYTES = 32 * 1024 * 1024


def load_graph() -> dict:
    """Load the validated composed graph through the canonical generator."""
    sys.path.insert(0, str(ROOT / "tools"))
    import akb  # pylint: disable=import-outside-toplevel

    akb.validate()
    return akb.load_composed_graph()


def route_for(identifier: str) -> str:
    """Return the canonical hash route for an immutable object identifier."""
    return "#/object/" + quote(identifier, safe="")


def pack(entities: list[dict], relationships: list[dict]) -> dict:
    """Return the compact wire form the page decodes back into graph shape.

    Every relationship carried ten fields, seven of which no view read, and
    repeated both endpoint identifiers in full — so `source` and `target`
    alone outweighed the entities they pointed at. Endpoints become indexes
    into the entity array and the type becomes an index into a table of the
    19 distinct values, which is what makes the payload bounded by the graph
    rather than by the length of its identifiers.

    An edge whose endpoint is not a composed entity is dropped: the page can
    neither render nor navigate it, and `akb.validate` rejects the graph
    before this runs, so a nonzero drop count means the caller bypassed it.
    """
    index = {entity["id"]: number for number, entity in enumerate(entities)}
    types = sorted({edge["type"] for edge in relationships})
    type_index = {name: number for number, name in enumerate(types)}
    slim = [
        {
            field: entity[field]
            for field in ENTITY_FIELDS
            if entity.get(field) not in (None, "", [], {})
        }
        for entity in entities
    ]
    edges = [
        [index[edge["source"]], index[edge["target"]], type_index[edge["type"]]]
        for edge in relationships
        if edge["source"] in index and edge["target"] in index
    ]
    return {"e": slim, "t": types, "r": edges}


def build(graph: dict, output: Path = OUTPUT) -> list[Path]:
    """Write a no-dependency static explorer and an accessible object index."""
    output.mkdir(parents=True, exist_ok=True)
    entities = sorted(graph["entities"], key=lambda item: item["id"])
    outgoing: dict[str, list[dict]] = defaultdict(list)
    incoming: dict[str, list[dict]] = defaultdict(list)
    for edge in graph["relationships"]:
        outgoing[edge["source"]].append(edge)
        incoming[edge["target"]].append(edge)
    data = pack(entities, graph["relationships"])
    rows = "\n".join(
        f'<li><a href="{route_for(item["id"])}">{html.escape(item["name"])}</a> '
        f'<code>{html.escape(item["id"])}</code></li>'
        for item in entities
    )
    script = """
// The payload arrives packed: entities carry only the fields the views read,
// and each edge is [sourceIndex, targetIndex, typeIndex] against the entity
// array and a table of the distinct type names. Decoding here restores the
// {source, target, type} shape every view below already expects, so the
// wire format stays an encoding concern rather than leaking into rendering.
const packed = __DATA__;
const data = {
  entities: packed.e,
  relationships: packed.r.map(([source, target, type]) => ({
    source: packed.e[source].id,
    target: packed.e[target].id,
    type: packed.t[type],
  })),
};
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
const graphViewRoute = name => '#/graph/' + name;
const graphNodeRoute = id => '#/graph-node/' + encodeURIComponent(id);
const viewLinks = () => `<nav aria-label="Explorer views"><strong>Views:</strong> ${Object.keys(views).map(name => `<a href="${viewRoute(name)}">${esc(name)}</a>`).join(' · ')}</nav><nav aria-label="Graph views"><strong>Graph:</strong> ${Object.keys(views).map(name => `<a href="${graphViewRoute(name)}">${esc(name)}</a>`).join(' · ')} · <a href="${graphViewRoute('__all__')}">all objects (large)</a></nav>`;
const compactValue = value => { if (Array.isArray(value)) return `${value.length} item${value.length === 1 ? '' : 's'}${value.length ? `: ${value.slice(0, 8).map(item => typeof item === 'object' ? (item.name || item.dll || JSON.stringify(item)) : item).join(', ')}` : ''}`; if (value && typeof value === 'object') return Object.entries(value).map(([key, item]) => `${key}=${item}`).join(', '); return String(value); };
const objectDetails = item => { const properties = Object.entries(item.properties || {}); const evidence = item.evidence_refs || []; return `${properties.length ? `<section aria-labelledby="properties"><h2 id="properties">Observed properties</h2><dl>${properties.map(([key, value]) => `<dt>${esc(key)}</dt><dd>${esc(compactValue(value))}</dd>`).join('')}</dl></section>` : ''}${evidence.length ? `<section aria-labelledby="evidence"><h2 id="evidence">Evidence</h2><ul>${evidence.map(reference => `<li><code>${esc(reference)}</code></li>`).join('')}</ul></section>` : '<section aria-labelledby="evidence"><h2 id="evidence">Evidence</h2><p>No evidence reference is attached to this object.</p></section>'}`; };
const index = () => {
  const kinds = [...new Set(data.entities.map(item => item.kind))].sort();
  const statuses = [...new Set(data.entities.map(item => item.status))].sort();
  return `${viewLinks()}<h1>Architecture Explorer</h1><p>Search the composed graph or narrow the textual index.</p><label>Search <input id="search" type="search" autofocus></label> <label>Kind <select id="kind"><option value="">All</option>${kinds.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label> <label>Status <select id="status"><option value="">All</option>${statuses.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label><p id="count"></p><ul id="results"></ul>`;
};
function bindIndex() {
  const search = document.querySelector('#search'), kind = document.querySelector('#kind'), status = document.querySelector('#status'), results = document.querySelector('#results'), count = document.querySelector('#count');
  const update = () => { const term = search.value.toLowerCase(); const found = data.entities.filter(item => (!term || [item.id,item.name,...(item.aliases||[]),...(item.tags||[])].join(' ').toLowerCase().includes(term)) && (!kind.value || item.kind === kind.value) && (!status.value || item.status === status.value)); count.textContent = `${found.length} objects`; results.innerHTML = found.map(item => `<li><a href="${route(item.id)}">${esc(item.name)}</a> <code>${esc(item.id)}</code> <span class="badge">${esc(item.kind)}</span> <span class="badge" data-status="${esc(item.status)}">${esc(item.status)}</span></li>`).join(''); }; [search,kind,status].forEach(control => control.addEventListener('input', update)); update();
}
// --- Graph view: real force-directed rendering (D3 v7, canvas) ---
const KIND_COLOR = d3.scaleOrdinal(d3.schemeTableau10);
const GRAPH_NODE_CAP = 800;
function neighborsOf(id) {
  const found = [];
  for (const edge of data.relationships) {
    if (edge.source === id && byId[edge.target]) found.push(edge.target);
    else if (edge.target === id && byId[edge.source]) found.push(edge.source);
  }
  return [...new Set(found)];
}
function edgesAmong(idSet) {
  return data.relationships.filter(edge => idSet.has(edge.source) && idSet.has(edge.target));
}
function renderGraph(root, seedIds, title, opts) {
  opts = opts || {};
  let nodeIds = [...new Set(seedIds)].filter(id => byId[id]);
  root.innerHTML = `${viewLinks()}<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <span aria-current="page">Graph: ${esc(title)}</span></nav><h1>Graph: ${esc(title)}</h1><p id="graph-status"></p><div id="graph-toolbar"><button type="button" id="graph-open" disabled>Open selected</button> <button type="button" id="graph-expand" disabled>Expand selected</button> <span id="graph-selected"></span></div><canvas id="graph-canvas" width="900" height="600" role="img" aria-label="Force-directed graph, ${nodeIds.length} nodes" style="border:1px solid #98a2b3;max-width:100%;touch-action:none;cursor:grab"></canvas><p>Drag a node to move it, drag the background to pan, scroll/pinch to zoom, click a node to select it.</p>`;
  const canvas = root.querySelector('#graph-canvas');
  const status = root.querySelector('#graph-status');
  const ctx = canvas.getContext('2d');
  const width = canvas.width, height = canvas.height;
  const themeStyle = getComputedStyle(document.documentElement);
  const themeColor = (name, fallback) => (themeStyle.getPropertyValue(name) || '').trim() || fallback;
  const edgeColor = themeColor('--border-strong', '#c1c7d0');
  const labelColor = themeColor('--fg', '#111');
  const selectedColor = themeColor('--accent', '#111');
  const idSet = new Set(nodeIds);
  const nodes = nodeIds.map(id => Object.assign({}, byId[id], {id}));
  const nodeById = new Map(nodes.map(node => [node.id, node]));
  const links = edgesAmong(idSet).map(edge => ({type: edge.type, source: nodeById.get(edge.source), target: nodeById.get(edge.target)}));
  status.textContent = `${nodes.length} nodes, ${links.length} edges.`;
  let transform = d3.zoomIdentity;
  let selected = null;
  let hovered = null;
  const openButton = root.querySelector('#graph-open'), expandButton = root.querySelector('#graph-expand'), selectedLabel = root.querySelector('#graph-selected');
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(node => node.id).distance(50).strength(0.25))
    .force('charge', d3.forceManyBody().strength(-90))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collide', d3.forceCollide(13))
    .on('tick', draw);
  function draw() {
    ctx.save();
    ctx.clearRect(0, 0, width, height);
    ctx.translate(transform.x, transform.y);
    ctx.scale(transform.k, transform.k);
    ctx.strokeStyle = edgeColor;
    ctx.lineWidth = 1 / transform.k;
    for (const link of links) { ctx.beginPath(); ctx.moveTo(link.source.x, link.source.y); ctx.lineTo(link.target.x, link.target.y); ctx.stroke(); }
    for (const node of nodes) {
      ctx.beginPath();
      ctx.fillStyle = KIND_COLOR(node.kind);
      ctx.arc(node.x, node.y, node === selected ? 8 : 5, 0, 2 * Math.PI);
      ctx.fill();
      if (node === selected) { ctx.lineWidth = 2 / transform.k; ctx.strokeStyle = selectedColor; ctx.stroke(); }
      if (node === selected || node === hovered || transform.k > 1.8) { ctx.fillStyle = labelColor; ctx.font = `${11 / transform.k}px system-ui`; ctx.fillText(node.name, node.x + 8, node.y + 3); }
    }
    ctx.restore();
  }
  function nodeAtScreenPoint(px, py) {
    const [x, y] = transform.invert([px, py]);
    let closest = null, closestDistance = 9 / transform.k;
    for (const node of nodes) { const distance = Math.hypot(node.x - x, node.y - y); if (distance < closestDistance) { closest = node; closestDistance = distance; } }
    return closest;
  }
  function selectNode(node) {
    selected = node;
    openButton.disabled = !node;
    expandButton.disabled = !node;
    selectedLabel.textContent = node ? `Selected: ${node.name} (${node.kind})` : '';
    draw();
  }
  d3.select(canvas).call(
    d3.drag()
      .subject(event => nodeAtScreenPoint(event.x, event.y))
      .on('start', event => { if (event.subject) { if (!event.active) simulation.alphaTarget(0.3).restart(); event.subject.fx = event.subject.x; event.subject.fy = event.subject.y; } })
      .on('drag', event => { if (event.subject) { const [x, y] = transform.invert([event.x, event.y]); event.subject.fx = x; event.subject.fy = y; } })
      .on('end', event => { if (event.subject) { if (!event.active) simulation.alphaTarget(0); event.subject.fx = null; event.subject.fy = null; } })
  );
  d3.select(canvas).call(
    d3.zoom().scaleExtent([0.15, 8]).filter(event => event.type !== 'mousedown' || !nodeAtScreenPoint(event.offsetX, event.offsetY)).on('zoom', event => { transform = event.transform; draw(); })
  );
  canvas.addEventListener('click', event => {
    const rect = canvas.getBoundingClientRect();
    selectNode(nodeAtScreenPoint(event.clientX - rect.left, event.clientY - rect.top));
  });
  canvas.addEventListener('mousemove', event => {
    const rect = canvas.getBoundingClientRect();
    const next = nodeAtScreenPoint(event.clientX - rect.left, event.clientY - rect.top);
    canvas.style.cursor = next ? 'pointer' : 'grab';
    if (next !== hovered) { hovered = next; draw(); }
  });
  canvas.addEventListener('mouseleave', () => { if (hovered) { hovered = null; draw(); } canvas.style.cursor = 'grab'; });
  openButton.addEventListener('click', () => { if (selected) location.hash = route(selected.id); });
  expandButton.addEventListener('click', () => {
    if (!selected) return;
    const additions = neighborsOf(selected.id).filter(id => !idSet.has(id));
    if (!additions.length) { status.textContent = `${nodes.length} nodes, ${links.length} edges. Selected node has no unexplored neighbors.`; return; }
    const room = GRAPH_NODE_CAP - nodeIds.length;
    if (room <= 0) { status.textContent = `${nodes.length} nodes, ${links.length} edges. Node cap (${GRAPH_NODE_CAP}) reached; open a narrower view to explore further.`; return; }
    renderGraph(root, [...nodeIds, ...additions.slice(0, room)], title, opts);
  });
  draw();
}
function graphViewMembers(name) {
  if (name === '__all__') return data.entities.map(entry => entry.id);
  const spec = views[name];
  if (!spec) return null;
  return (name === 'evidenced' ? data.entities.filter(entry => (entry.evidence_refs || []).length) : data.entities.filter(entry => inView(entry, spec))).map(entry => entry.id);
}
function render() {
  const hash = location.hash || '#/';
  const view = decodeURIComponent(hash.replace(/^#\\/view\\//, ''));
  const id = decodeURIComponent(hash.replace(/^#\\/object\\//, ''));
  const root = document.querySelector('main');
  if (hash.startsWith('#/graph-node/')) {
    const seedId = decodeURIComponent(hash.replace(/^#\\/graph-node\\//, ''));
    if (!byId[seedId]) { root.innerHTML = `${viewLinks()}<h1>Unknown object</h1><p><a href="#/">Return to the explorer index.</a></p>`; return; }
    renderGraph(root, [seedId, ...neighborsOf(seedId)], byId[seedId].name, {seedId});
    return;
  }
  if (hash.startsWith('#/graph/')) {
    const name = decodeURIComponent(hash.replace(/^#\\/graph\\//, ''));
    const members = graphViewMembers(name);
    if (!members) { root.innerHTML = `${viewLinks()}<h1>Unknown graph view</h1><p><a href="#/">Return to the explorer index.</a></p>`; return; }
    if (members.length > GRAPH_NODE_CAP) {
      root.innerHTML = `${viewLinks()}<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <span aria-current="page">Graph: ${esc(name)}</span></nav><h1>Graph: ${esc(name)}</h1><p>${members.length} objects — above the ${GRAPH_NODE_CAP}-node interactive rendering cap, which would be slow and unreadable as one force-directed layout.</p><p><button type="button" id="graph-render-anyway">Render anyway (may be slow)</button> or pick a narrower <a href="#/">view</a>.</p>`;
      root.querySelector('#graph-render-anyway').addEventListener('click', () => renderGraph(root, members.slice(0, 4000), name, {}));
      return;
    }
    renderGraph(root, members, name, {});
    return;
  }
  if (hash.startsWith('#/view/')) { const spec = views[view]; if (!spec) { root.innerHTML = `${viewLinks()}<h1>Unknown view</h1><p><a href="#/">Return to the explorer index.</a></p>`; return; } const members = view === 'evidenced' ? data.entities.filter(entry => (entry.evidence_refs || []).length) : data.entities.filter(entry => inView(entry, spec)); root.innerHTML = `${viewLinks()}<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <span aria-current="page">${esc(view)}</span></nav><h1>${esc(view)} view <a class="graph-link" href="${graphViewRoute(view)}">View as graph</a></h1><p>${members.length} ${view === 'evidenced' ? 'objects with attached evidence' : 'typed objects'}.</p><ul>${members.map(entry => `<li><a href="${route(entry.id)}">${esc(entry.name)}</a> <code>${esc(entry.kind)}</code></li>`).join('') || '<li>No objects in the current projection.</li>'}</ul>`; return; }
  const item = byId[id];
  if (!item) { root.innerHTML = index(); bindIndex(); return; }
  renderObject(item, id, root);
}
function renderObject(item, id, root) {
  const out = data.relationships.filter(edge => edge.source === id);
  const inc = data.relationships.filter(edge => edge.target === id);
  const dependencies = out.filter(isDependency);
  const dependents = inc.filter(isDependency);
  const links = (edges, direction) => { const limit = 25; if (!edges.length) return '<p>None.</p>'; const rows = edges.map((edge, index) => { const other = edge.source === id ? edge.target : edge.source; return `<li${index >= limit ? ' hidden' : ''}><code>${esc(edge.type)}</code> <a href="${route(other)}">${esc(byId[other]?.name || other)}</a></li>`; }).join(''); const control = edges.length > limit ? `<button type="button" class="expand" data-direction="${direction}" aria-expanded="false">Show ${edges.length - limit} more</button>` : ''; return `<ul data-direction="${direction}">${rows}</ul>${control}`; };
  root.innerHTML = `<nav aria-label="Breadcrumb"><a href="#/">Explorer</a> / <span>${esc(item.kind)}</span> / <span aria-current="page">${esc(item.name)}</span></nav><h1>${esc(item.name)} <a class="graph-link" href="${graphNodeRoute(id)}">View in graph</a></h1><dl><dt>ID</dt><dd><code>${esc(item.id)}</code></dd><dt>Kind</dt><dd><span class="badge">${esc(item.kind)}</span></dd><dt>Status</dt><dd><span class="badge" data-status="${esc(item.status)}">${esc(item.status)}</span></dd></dl>${item.summary ? `<p>${esc(item.summary)}</p>` : ''}${objectDetails(item)}<section aria-labelledby="dependencies"><h2 id="dependencies">Dependencies</h2>${links(dependencies, 'dependencies')}</section><section aria-labelledby="dependents"><h2 id="dependents">Dependents</h2>${links(dependents, 'dependents')}</section><h2>Outgoing relationships</h2>${links(out, 'outgoing')}<h2>Incoming relationships</h2>${links(inc, 'incoming')}`;
  root.querySelectorAll('.expand').forEach(button => button.addEventListener('click', () => { const list = root.querySelector(`ul[data-direction="${button.dataset.direction}"]`); const expanded = button.getAttribute('aria-expanded') === 'true'; list.querySelectorAll('li[hidden]').forEach(row => row.hidden = expanded); button.setAttribute('aria-expanded', String(!expanded)); button.textContent = expanded ? `Show ${list.querySelectorAll('li[hidden]').length} more` : 'Collapse relationships'; }));
}
addEventListener('hashchange', render); render();
""".replace(
        "__DATA__",
        json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"),
    )
    style = """
:root{
  --bg:#f7f8fa;--bg-elevated:#ffffff;--bg-muted:#eef0f3;
  --fg:#1a1d21;--fg-muted:#5b6472;--fg-subtle:#656d79;
  --border:#dde1e7;--border-strong:#c3c9d3;
  --accent:#2f5fd6;--accent-fg:#ffffff;--accent-muted:#e7edfb;
  --radius-sm:6px;--radius-md:10px;--radius-lg:14px;
  --shadow-sm:0 1px 2px rgba(20,22,30,.06);
  --shadow-md:0 6px 20px -4px rgba(20,22,30,.14),0 2px 6px -2px rgba(20,22,30,.08);
  --font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,Roboto,sans-serif;
  --font-mono:ui-monospace,"Cascadia Code","SFMono-Regular",Consolas,"Liberation Mono",monospace;
  --space-1:4px;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:24px;--space-6:32px;--space-7:48px;
  --status-verified:#1c7c44;--status-verified-bg:#e5f6ec;
  --status-partial:#916108;--status-partial-bg:#fbf1de;
  --status-planned:#656d79;--status-planned-bg:#eef0f3;
  --status-inferred:#7550c9;--status-inferred-bg:#f1ecfb;
  --status-deprecated:#c23b3b;--status-deprecated-bg:#fbeaea;
  --status-superseded:#656d79;--status-superseded-bg:#eef0f3;
  --status-unknown:#656d79;--status-unknown-bg:#eef0f3;
  color-scheme:light dark;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#0f1216;--bg-elevated:#171b21;--bg-muted:#1d222a;
    --fg:#e7e9ec;--fg-muted:#9aa3b2;--fg-subtle:#7a818f;
    --border:#2a3038;--border-strong:#3a414c;
    --accent:#7aa2f7;--accent-fg:#0f1216;--accent-muted:#1c2b4d;
    --shadow-sm:0 1px 2px rgba(0,0,0,.4);
    --shadow-md:0 10px 30px -8px rgba(0,0,0,.6),0 4px 10px -4px rgba(0,0,0,.5);
    --status-verified:#3ecb7e;--status-verified-bg:#123322;
    --status-partial:#e0ab3d;--status-partial-bg:#3a2c0d;
    --status-planned:#9aa3b2;--status-planned-bg:#232a34;
    --status-inferred:#a98bf0;--status-inferred-bg:#2a2140;
    --status-deprecated:#f0716e;--status-deprecated-bg:#3a1414;
    --status-superseded:#9aa3b2;--status-superseded-bg:#232a34;
    --status-unknown:#9aa3b2;--status-unknown-bg:#232a34;
  }
}
*{box-sizing:border-box}
body{margin:0;font:400 15px/1.55 var(--font-sans);color:var(--fg);background:var(--bg);-webkit-font-smoothing:antialiased}
main{max-width:76rem;margin:0 auto;padding:var(--space-6) var(--space-5) var(--space-7)}
header{margin-bottom:var(--space-2)}
h1{font-size:1.75rem;font-weight:650;letter-spacing:-.02em;line-height:1.2;margin:var(--space-2) 0;display:flex;align-items:center;gap:var(--space-3);flex-wrap:wrap}
h2{font-size:1.05rem;font-weight:600;letter-spacing:-.01em;margin:var(--space-6) 0 var(--space-3);padding-top:var(--space-4);border-top:1px solid var(--border)}
h2:first-of-type{border-top:none;padding-top:0}
p{color:var(--fg-muted);margin:0 0 var(--space-4);max-width:65ch}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
code{font:400 .85em/1.4 var(--font-mono);background:var(--bg-muted);border:1px solid var(--border);padding:.1em .4em;border-radius:5px;overflow-wrap:anywhere;color:var(--fg)}
nav[aria-label="Explorer views"],nav[aria-label="Graph views"]{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-2);font-size:.82rem;color:var(--fg-subtle);padding:var(--space-2) 0}
nav[aria-label="Explorer views"] strong,nav[aria-label="Graph views"] strong{color:var(--fg-muted);font-weight:600;margin-right:var(--space-1)}
nav[aria-label="Explorer views"] a,nav[aria-label="Graph views"] a{padding:3px 10px;border-radius:999px;color:var(--fg-muted);background:var(--bg-elevated);border:1px solid var(--border);transition:background .15s ease,color .15s ease,border-color .15s ease}
nav[aria-label="Explorer views"] a:hover,nav[aria-label="Graph views"] a:hover{color:var(--accent);border-color:var(--accent);text-decoration:none}
nav[aria-label="Breadcrumb"]{font-size:.85rem;color:var(--fg-subtle);margin-bottom:var(--space-2)}
nav[aria-label="Breadcrumb"] [aria-current="page"]{color:var(--fg);font-weight:600}
label{display:inline-flex;flex-direction:column;gap:4px;font-size:.78rem;color:var(--fg-muted);font-weight:600;margin:0 var(--space-4) var(--space-3) 0;text-transform:uppercase;letter-spacing:.03em}
input,select{font:400 .95rem/1.3 var(--font-sans);color:var(--fg);background:var(--bg-elevated);border:1px solid var(--border-strong);border-radius:var(--radius-sm);padding:7px 10px}
input[type=search]{min-width:16rem}
#count{color:var(--fg-subtle);font-size:.82rem;font-variant-numeric:tabular-nums;margin:var(--space-3) 0}
main>ul,ul[data-direction]{list-style:none;margin:0;padding:0;border:1px solid var(--border);border-radius:var(--radius-md);overflow:hidden;background:var(--bg-elevated)}
main>ul li,ul[data-direction] li{display:flex;align-items:center;gap:var(--space-3);flex-wrap:wrap;padding:9px var(--space-4);border-top:1px solid var(--border);transition:background .15s ease}
main>ul li:first-child,ul[data-direction] li:first-child{border-top:none}
main>ul li:hover,ul[data-direction] li:hover{background:var(--bg-muted)}
.badge{display:inline-flex;align-items:center;font:600 .72rem/1 var(--font-sans);text-transform:uppercase;letter-spacing:.04em;padding:4px 8px;border-radius:5px;color:var(--fg-muted);background:var(--bg-muted)}
.badge[data-status=verified]{color:var(--status-verified);background:var(--status-verified-bg)}
.badge[data-status=partial]{color:var(--status-partial);background:var(--status-partial-bg)}
.badge[data-status=planned]{color:var(--status-planned);background:var(--status-planned-bg)}
.badge[data-status=inferred]{color:var(--status-inferred);background:var(--status-inferred-bg)}
.badge[data-status=deprecated]{color:var(--status-deprecated);background:var(--status-deprecated-bg)}
.badge[data-status=superseded]{color:var(--status-superseded);background:var(--status-superseded-bg)}
.badge[data-status=unknown]{color:var(--status-unknown);background:var(--status-unknown-bg)}
button,.graph-link{font:600 .82rem/1 var(--font-sans);border-radius:var(--radius-sm);cursor:pointer}
button{padding:7px 12px;border:1px solid var(--border-strong);background:var(--bg-elevated);color:var(--fg);transition:background .15s ease,transform .1s ease,border-color .15s ease}
button:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
button:active:not(:disabled){transform:translateY(1px)}
button:disabled{opacity:.45;cursor:not-allowed}
.graph-link{display:inline-flex;align-items:center;padding:3px 10px;margin-left:var(--space-2);border:1px solid var(--border);background:var(--accent-muted);color:var(--accent)}
.graph-link:hover{text-decoration:none;border-color:var(--accent)}
.expand{display:block;margin-top:var(--space-2)}
dl{display:grid;grid-template-columns:max-content 1fr;gap:var(--space-2) var(--space-4);margin:var(--space-4) 0;align-items:center}
dt{font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;color:var(--fg-subtle);font-weight:600}
dd{margin:0}
#graph-toolbar{display:flex;align-items:center;gap:var(--space-3);flex-wrap:wrap;margin:var(--space-3) 0}
#graph-selected{font-size:.82rem;color:var(--fg-muted)}
#graph-status{color:var(--fg-subtle);font-size:.85rem}
#graph-canvas{display:block;width:100%;max-width:900px;height:auto;aspect-ratio:900/600;background:var(--bg-elevated);border:1px solid var(--border) !important;border-radius:var(--radius-lg);box-shadow:var(--shadow-sm)}
#graph-canvas:active{cursor:grabbing}
@media (max-width:640px){main{padding:var(--space-4)}h1{font-size:1.4rem}input[type=search]{min-width:0;width:100%}}
@media (prefers-reduced-motion:reduce){*{transition-duration:.01ms!important}}
"""
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="Deep-linkable explorer for the MSYS2 Architecture Knowledge Base graph: layers, packages, artifacts, libraries, runtimes, toolchains, and repositories, with textual search and force-directed graph views."><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%232f5fd6'/%3E%3Ctext x='16' y='22' font-family='ui-sans-serif,system-ui' font-size='16' font-weight='700' fill='white' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E"><title>AKB Explorer</title>
<style>{style}</style></head>
<body><main><header><h1>Architecture Explorer</h1><p>Search the composed graph, browse typed views, or open an object by its stable ID.</p></header><ul>{rows}</ul></main><script src="d3.v7.min.js"></script><script>{script}</script></body></html>"""
    index = output / "index.html"
    index.write_text(page, encoding="utf-8")
    d3_output = output / "d3.v7.min.js"
    shutil.copyfile(VENDOR_D3, d3_output)
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
    return [index, d3_output, svg, text]


if __name__ == "__main__":
    for path in build(load_graph()):
        print(path.relative_to(ROOT))
