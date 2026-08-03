---
id: doc:volume-10:explorer-large-graph-performance
title: Explorer Large-Graph Performance Tests
volume: 10
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-08-03
---

# Explorer Large-Graph Performance Tests

The Explorer test suite builds a synthetic graph containing 2,000 objects and
4,000 typed edges. It requires deterministic generation in under ten seconds,
checks that the final object's route and textual-fallback entry survive, and
verifies that the SVG overview stays bounded to 80 nodes. The limit guards the
static-generator hot path while avoiding brittle machine-specific UI timing.

`tests.test_explorer.ExplorerTests.test_large_graph_build_is_bounded_and_complete`
implements exactly this test. Run directly on 2026-07-30, it completed in
approximately 0.1 seconds — two orders of magnitude under the 10-second
bound on this host, single-run evidence of real headroom rather than a
threshold the build regularly approaches.

## Payload size, and why it is bounded

Generation speed was measured; **output size was not**, and it grew until
`generated/explorer/index.html` reached 75.1 MiB — past the 50 MB point at
which GitHub warns on every push, in a file regenerated on every build and
therefore rewritten in full in every diff and every clone.

The cause was the embedded payload, not the number of objects. Each of the
141,518 relationships was serialised with all ten of its modelled fields
and both endpoint identifiers in full, so the edges alone came to 61.7 MB
against the 14.1 MB of entities they connected — the edges outweighed the
graph they described by four to one. Seven of those ten fields, and three
entity fields (`confidence`, `authority`, `applicability`), are read by no
view in the explorer.

The page now embeds a compact wire form and decodes it on load:

| | Before | After |
| --- | ---: | ---: |
| Entities | 14.1 MB | 11.8 MB |
| Relationships | 61.7 MB | 2.1 MB |
| `index.html` on disk | 75.1 MiB | 16.1 MiB |

Each edge became `[sourceIndex, targetIndex, typeIndex]` — two indexes into
the entity array and one into a table of the 19 distinct type names. That
is what makes the payload scale with the shape of the graph rather than
with the length of its identifiers. Entities kept every field a view
renders and dropped the three it does not, along with empty values.

The remaining 11.8 MB of entity data is not waste: 6.8 MB is observed
package properties and 1.2 MB is authored summaries, both displayed on
object detail pages. Compressing further would mean showing less.

**The ceiling is enforced, not just documented.** `MAX_INDEX_BYTES` in
`tools/build_explorer.py` is 32 MiB — roughly double the current payload,
so the graph can grow substantially before it binds, and still under
GitHub's warning threshold.
`tests.test_explorer.ExplorerTests.test_embedded_page_stays_under_its_size_ceiling`
fails the build when the file exceeds it. Crossing that line is then a
decision someone makes deliberately, rather than something noticed after
the file has already been pushed.

Two further tests keep the encoding honest, since a wire format that
silently loses data would be worse than a large file: one round-trips
every edge back to `(source, target, type)` and compares against the
composed graph, the other asserts every entity field a view reads survives
packing. Both were confirmed to fail when deliberately broken.

`generated/explorer/overview.txt`, the complete textual fallback, is 17 MB
and is not bounded — it is a plain listing of every object and edge, and
truncating it would defeat its purpose as the accessible complete view.
