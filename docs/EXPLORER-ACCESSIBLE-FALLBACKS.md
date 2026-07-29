---
id: doc:volume-10:explorer-accessible-fallbacks
title: Explorer Accessible SVG and Textual Fallbacks
volume: 10
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Explorer Accessible SVG and Textual Fallbacks

The explorer generator emits `generated/explorer/overview.svg` and
`overview.txt` beside the interactive HTML. The SVG supplies a programmatic
title/description and keyboard-focusable links to object routes. It is
intentionally bounded to 80 sorted objects for legibility. The text fallback
contains every composed object and relationship, allowing complete navigation
without SVG or client-side JavaScript.
