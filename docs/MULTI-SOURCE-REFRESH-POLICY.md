---
id: doc:volume-19:multi-source-refresh-policy
title: Multi-Source Refresh Policy
volume: 19
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-08-02
---

# Multi-Source Refresh Policy

The machine-readable policy in `evidence/refresh-policy.json` assigns a
cadence, adapter, and priority to every registered primary source. Run
`py -3 tools/validate_refresh_policy.py` before scheduling or changing a
refresh plan; it rejects unknown, omitted, or duplicated source policies and
invalid retention or alert thresholds.

## Orchestration

The orchestrator plans only sources due under their configured cadence. Each
adapter collects into an isolated staging area, writes its own manifest, and
validates its source-specific projection before promotion. A successful source
can be retained and promoted independently; a failed or invalid source must
not overwrite its prior current projection or turn a partial multi-source run
into a synthetic whole snapshot.

The operator records a run ID, source ID, adapter version, observation time,
source revision or retrieval date, manifest digest, outcome, and diagnostic
location. A promoted view is composed only from individually validated source
projections, so consumers can see exactly which source observations it uses.

## Retention

Successful snapshots retain at least 30 snapshots and 90 days. Failed runs
retain at least 10 records and 30 days, including their manifests and safe
diagnostics. Retention applies to immutable evidence, never the currently
promoted projection. Removal is eligible only when both minimums have elapsed
and a newer validated projection remains available; deletion decisions are
logged with the affected source and snapshot IDs.

## Alerts

The policy alerts after three consecutive source failures, immediately after a
snapshot-validation failure, and when unresolved dependencies grow by 10% or
more. Alerts must name the source, run and snapshot IDs, threshold, observed
value, diagnostic location, and whether the previous projection remains in
service. They must not include credentials, tokens, or package payloads.
