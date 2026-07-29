---
id: doc:local-evidence-retention
title: Local-Only Evidence Retention
volume: 20
status: verified
model_refs: []
evidence_refs: []
last_verified: 2026-07-29
---

# Local-Only Evidence Retention

This workstation retains a complete imported projection from the six official
MSYS2 pacman `.files` databases. The projection is intentionally local-only:
the current inventory is approximately 5.8 GB before its immutable snapshots,
which exceeds ordinary Git repository limits.

The local import completed on 2026-07-29 with 5,318,126 inventory entities,
5,369,585 relationships, and zero unresolved references. It covers 15,678 of
15,711 catalog packages (99.79%) as package-to-file ownership observations.

## Scope and interpretation

The retained records establish package ownership of paths from signed
repository file indexes. They have `present: false` and are not byte, DLL
export, ABI, installed-state, or runtime-behavior evidence.

## Regeneration

Download the six official `.files` databases, convert each with
`tools/import_repository_file_db.py`, then import each verified output through
`tools/import_deep_inventory.py --accumulate`. The importer records hashes and
snapshot-qualified provenance. The helper is documented in
[Package File Inventory](PACKAGE-FILE-INVENTORY.md).

## Publication boundary

Do not stage `model/inventory/current.json`, the corresponding local
`evidence/inventory-snapshots/` directories, or derived large reports from this
retention mode. Publish only reproducible tooling, documentation, compact
coverage summaries explicitly marked local-only, or externally hosted raw
artifacts after a separate storage decision.
