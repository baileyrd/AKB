---
id: doc:volume-20:performance-experiments
title: AKB Tooling Performance Experiments
volume: 20
status: partial
model_refs: []
evidence_refs:
  - evidence:akb-process:performance-benchmark-2026-07-31
last_verified: 2026-08-02
---

# AKB Tooling Performance Experiments

> **This page is about this repository's own tooling, not about MSYS2.**
> It was filed under Volume 17 (Performance) until 2026-08-02, which made
> the volume appear covered while the ecosystem's actual hot paths had no
> analysis at all. The ecosystem page is
> [MSYS2 Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md).
> This one is a Volume 20 reference appendix: how to benchmark the AKB's
> own generators as the graph grows.

Run `py -3 tools/benchmark_akb.py --repetitions 10` to produce a JSON report
for the current composed graph. The experiment measures three operations:

| Operation | Purpose | Interpretation |
| --- | --- | --- |
| `validate` | Schema/reference validation of composed graph | Growth in graph-check cost |
| `generate-indexes` | Markdown index and coverage generation | Generated-view write cost |
| `build-explorer` | Static HTML/SVG/text explorer generation | Navigability artifact cost |

Reports include entity/relationship/claim/evidence counts and minimum/median
milliseconds. Store comparison reports with the exact commit, Python version,
host characteristics, repetition count, and refresh snapshot. The command is
an experiment, not a CI performance gate: wall-clock thresholds vary by host.

## Recorded benchmark history

No comparison report had been stored here before this entry. On
2026-07-30, `py -3 tools/benchmark_akb.py --repetitions 10` ran against
commit `554c5ee`, Python `3.11.15`, host `Windows-11-10.0.26200-SP0`
(`Intel64 Family 6 Model 197 Stepping 2`), against the composed graph's
then-current 16,430 entities / 77,233 relationships / 39 claims / 106
evidence records — the tracked-only composed graph (`model/catalog`,
`model/graph.json`), not the much larger local-only deep-inventory
overlay some hosts additionally carry, which this benchmark does not
measure:

| Operation | Minimum (ms) | Median (ms) |
| --- | ---: | ---: |
| `validate` | 604.441 | 668.974 |
| `generate-indexes` | 914.109 | 936.937 |
| `build-explorer` | 580.849 | 593.913 |

This is a single host, single commit, ten-repetition sample. It
establishes a first comparison baseline for these three hot paths on the
tracked-only composed graph; it does not establish trend, regression
detection, or behavior on a host with a larger local-only overlay
attached.

A second same-host sample, on 2026-07-31 against commit `ba14e63`
(16,430 entities / 77,233 relationships / 39 claims / 110 evidence
records — one more evidence record than the first sample, otherwise the
same tracked-only composed graph shape), found all three operations
within roughly 1-3% of the first sample's minimum/median:

| Operation | Minimum (ms) | Median (ms) |
| --- | ---: | ---: |
| `validate` | 609.447 | 677.861 |
| `generate-indexes` | 911.794 | 946.869 |
| `build-explorer` | 582.391 | 594.465 |

Two same-host samples six commits apart is evidence of run-to-run
stability on this host, not yet a regression-detection trend line: a
real trend requires more samples across commits that materially change
hot-path code, or a host/graph-size sweep, neither of which has been
performed.

## Current Optimization Boundaries

- collectors stream JSONL evidence and validate hashes/counts before import;
- projections replace current views atomically after validation;
- explorer relationship rendering is progressively expanded and SVG is bounded
  to 80 nodes; and
- large-graph tests exercise 2,000 objects and 4,000 edges independently of
  a particular developer machine's browser performance.

## Related Objects

- [MSYS2 Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md)
  — the Volume 17 page this one was standing in for.
