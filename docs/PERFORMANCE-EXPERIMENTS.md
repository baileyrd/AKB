---
id: doc:volume-17:performance-experiments
title: AKB Performance Experiments and Hot Paths
volume: 17
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# AKB Performance Experiments and Hot Paths

Run `py -3 tools/benchmark_akb.py --repetitions 10` to produce a JSON report
for the current composed graph. The experiment measures three hot paths:

| Operation | Purpose | Interpretation |
| --- | --- | --- |
| `validate` | Schema/reference validation of composed graph | Growth in graph-check cost |
| `generate-indexes` | Markdown index and coverage generation | Generated-view write cost |
| `build-explorer` | Static HTML/SVG/text explorer generation | Navigability artifact cost |

Reports include entity/relationship/claim/evidence counts and minimum/median
milliseconds. Store comparison reports with the exact commit, Python version,
host characteristics, repetition count, and refresh snapshot. The command is
an experiment, not a CI performance gate: wall-clock thresholds vary by host.

## Current Optimization Boundaries

- collectors stream JSONL evidence and validate hashes/counts before import;
- projections replace current views atomically after validation;
- explorer relationship rendering is progressively expanded and SVG is bounded
  to 80 nodes; and
- large-graph tests exercise 2,000 objects and 4,000 edges independently of
  a particular developer machine's browser performance.
