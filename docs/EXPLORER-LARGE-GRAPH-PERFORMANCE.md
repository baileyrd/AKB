---
id: doc:volume-18:explorer-large-graph-performance
title: Explorer Large-Graph Performance Tests
volume: 18
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Explorer Large-Graph Performance Tests

The Explorer test suite builds a synthetic graph containing 2,000 objects and
4,000 typed edges. It requires deterministic generation in under ten seconds,
checks that the final object's route and textual-fallback entry survive, and
verifies that the SVG overview stays bounded to 80 nodes. The limit guards the
static-generator hot path while avoiding brittle machine-specific UI timing.
