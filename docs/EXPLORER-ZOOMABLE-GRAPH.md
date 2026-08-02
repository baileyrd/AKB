---
id: doc:volume-10:explorer-zoomable-graph
title: Explorer Zoomable Graph Rendering
volume: 10
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-08-02
---

# Explorer Zoomable Graph Rendering

## What it is

Route `#/graph/<object-id>` in `generated/explorer/index.html` renders one
object's dependency neighbourhood as an interactive SVG that pans and
zooms. Every object detail page links to its own graph view.

Before this, the explorer's only picture was `overview.svg` — a
fixed-size, bounded snapshot of the first eighty objects, with no way to
look closer at any one of them.

## The zoom model

**The SVG `viewBox` is the entire zoom implementation.** Pan and zoom are
arithmetic on four numbers — `x`, `y`, `width`, `height` — reassigned on
the live element. There is no layout library, no canvas, and no
transform matrix to keep in step with hit-testing, because the browser
does the hit-testing against the same coordinate space it draws in.

That choice follows from the repository's zero-dependency posture
([ADR 0002](../charter/adr/0002-dependency-free-schema-checking.md)):
there is no dependency manifest and no CI install step, so a graph
library was not available to spend.

Zoom is clamped to between one eighth and four times the base width. An
unclamped viewBox lets a user zoom until the figure is off-screen with no
indication of which direction to travel back.

## Layout

Deterministic, so the same object always draws the same picture:

- The subject sits at the centre.
- **Dependents fan out to the left**, ordered by object id.
- **Dependencies fan out to the right**, ordered by object id.
- Each side is bounded to fourteen neighbours.

Ordering by id rather than by degree or by insertion order is what makes
the output stable across rebuilds. Deduplication is by neighbour, so an
object connected by two edge types appears once.

## Interaction, and its keyboard equivalents

Pointer gestures are not an interface on their own. Every gesture has a
button and a key:

| Action | Pointer | Button | Key |
| --- | --- | --- | --- |
| Zoom in | scroll up | **Zoom in** | <kbd>+</kbd> |
| Zoom out | scroll down | **Zoom out** | <kbd>-</kbd> |
| Pan | drag | — | arrow keys |
| Reset | — | **Reset view** | <kbd>0</kbd> |

The figure carries `tabindex="0"` so it is reachable by keyboard, and a
visible focus ring when it has focus. Zoom scrolling calls
`preventDefault`, so the page does not scroll out from under the figure
while the pointer is over it.

Wheel zoom is anchored at the pointer; button and key zoom are anchored at
the centre of the current view. Anchoring at the pointer is what makes
"zoom towards that node" work without a separate pan.

## Accessibility

- The figure has a `<title>` and a `<desc>` naming the subject and the
  count of dependents and dependencies, referenced through
  `aria-labelledby`.
- Every node is a link with an `aria-label` carrying both the object's
  name and its full identifier, and a focus ring distinct from the
  figure's.
- Node labels are `pointer-events: none`, so a click anywhere on a node
  reaches the link rather than being swallowed by the text.
- **A complete textual equivalent sits below every figure**, listing each
  dependent and dependency with its relationship type as an ordinary link
  list. It is not a summary of the figure — it is the same data, and it is
  unbounded where the figure is bounded.
- The caption discloses the bound: it states how many neighbours were
  omitted, or says that all are shown.

## Verification

`tests/test_explorer_graph.py` holds ten properties, including that no
external script, CDN reference, `import()`, or `require()` appears in the
page; that the zoom controls and key handlers exist; that the bound is
declared and disclosed; and that the same graph produces the same page
byte for byte.

The interaction itself was exercised in headless Chromium during
development rather than only asserted as strings. Zooming in narrowed the
viewBox, <kbd>ArrowRight</kbd> moved it right, <kbd>0</kbd> restored it
exactly, and forty consecutive zoom-out clicks stopped at the clamp rather
than running away. That was a development check, not a CI test: the test
suite must run with Python alone.

## Related Objects

- [Explorer Accessible SVG and Textual Fallbacks](EXPLORER-ACCESSIBLE-FALLBACKS.md)
- [Explorer Dependency Navigation](EXPLORER-DEPENDENCY-NAVIGATION.md)
- [Explorer Progressive Expansion](EXPLORER-PROGRESSIVE-EXPANSION.md)
- [Explorer Large-Graph Performance](EXPLORER-LARGE-GRAPH-PERFORMANCE.md)
- [Explorer Stable Routes](EXPLORER-STABLE-ROUTES.md)
