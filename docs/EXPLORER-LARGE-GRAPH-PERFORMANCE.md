---
id: doc:volume-10:explorer-large-graph-performance
title: Explorer Large-Graph Performance Tests
volume: 10
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-30
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
