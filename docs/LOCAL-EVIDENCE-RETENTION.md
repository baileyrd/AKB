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

The same workstation also retains a normalized source-recipe snapshot from a
shallow official `MSYS2/MINGW-packages` checkout at commit
`89036253520d039d5f7165c18ff2f06c7e296b55`. Collected on 2026-07-29, it
contains 3,336 declaratively parsed and SHA-256-hashed `PKGBUILD` records with
zero parser warnings. It is source-provenance evidence only: it does not prove
that a package archive was built from that source or that its bytes match a
published artifact.

A companion shallow official `MSYS2/MSYS2-packages` checkout is retained at
commit `68febe1146dc5c92b54cb30f941a2e593b7b43a8`. Its 2026-07-29 snapshot
contains 606 declaratively parsed and SHA-256-hashed `PKGBUILD` records with
zero parser warnings and has the same source-provenance-only scope.

An isolated MSYS2 runtime installation is also retained locally. A bounded
installed-package collection on 2026-07-29 recorded 22,279 owned paths,
3,055 PE import records, 70,008 PE export records, 179,552 archive members,
and 19 development-metadata records. The collection is byte-level evidence
only for that installed state; it does not establish behavior for unobserved
environments, package revisions, or loader/runtime execution.
Its integrated projection has five unresolved metadata dependencies because
their provider artifacts were not part of that bounded installation; they are
retained as unresolved rather than inferred.

The same isolated installation retains bounded runtime observations for all
six modeled selections: MSYS, UCRT64, CLANG64, CLANGARM64, MINGW64, and
MINGW32. Each records an allow-listed environment subset, tool identity,
`uname`, MSYS path conversion, the mount table, and the executing utility's
`/proc/self/exe` view. The latter probes describe the MSYS shell/runtime that
executes the collector; they do not prove native loader, process, or filesystem
behavior. On this x86_64 host, CLANGARM64 target binaries were discovered but
reported `executed: false`, so no target-execution claim is made.

It additionally retains a hash-verified expanded installed-artifact snapshot
from 2026-07-30 with 48,258 owned paths, 7,876 PE imports, 309,193 PE
exports, 987,057 archive members, 81 development-metadata records, and zero
collector warnings. It is retained independently of the current composite
projection because an in-memory accumulation of multi-million-record local
snapshots exceeds the workstation-safe publication/import budget.

It also retains a controlled MSYS-shell behavior observation from
2026-07-30. The process-lifecycle, shell `exec`, and `USR1` signal probes
returned status 0, and `/dev/tty` existed. The self-cleaning symlink probe
created and read its target successfully, while `test -L` returned non-zero;
this is retained as an observed classification discrepancy, not treated as
proof of POSIX symlink parity or general filesystem behavior.

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
retention mode. This also includes the local `work/mingw-packages-source/`
checkout and `work/mingw-recipes/` collector output, plus the companion
`work/msys2-packages-source/` checkout and `work/msys2-recipes/` output.
It further includes `work/isolated-runtime-inventory/`, the isolated MSYS2
installation, and local `model/runtime/` projections.
Publish only reproducible tooling, documentation, compact
coverage summaries explicitly marked local-only, or externally hosted raw
artifacts after a separate storage decision.
