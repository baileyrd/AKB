---
id: doc:volume-6:libisl
title: isl (Integer Set Library)
volume: 6
status: partial
model_refs:
  - library:libisl:isl
  - package:msys2:mingw-w64-ucrt-x86_64-isl
  - library:gnu:gmp
  - component:gnu:gcc
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:libisl:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# isl (Integer Set Library)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:libisl:isl` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | The isl team (Sven Verdoolaege et al.) |
| Environments | `ucrt64` |
| Upstream | <https://libisl.sourceforge.io/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-isl` |
| Version (observed) | 0.28-1 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 13059.68 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:libisl:manual-2026-07-30` — isl (official project site) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Isl manipulates sets and relations of integer points bounded by linear
constraints — the polyhedral-model math underneath
[GCC](GNU-GCC.md#dependencies)'s Graphite loop-optimization framework,
already cited on that page. This page documents its architectural role;
see the [official isl project site](https://libisl.sourceforge.io/) for
the API reference.

## Architectural Classification

`library:libisl:isl` is packaged per native environment: this page cites
the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-isl` (version
`0.28-1` in the current catalog snapshot, license `MIT`), maintained by
the isl team including Sven Verdoolaege.

## Responsibilities

- Providing polyhedral-model set/relation operations over integer points
  bounded by linear constraints, the mathematical machinery Graphite uses
  to analyze and transform loop nests for optimizations such as loop
  tiling, fusion, and parallelization.

## Boundaries

Isl provides the polyhedral mathematics; it does not itself decide which
loop transformations to apply — that decision logic lives in
[GCC](GNU-GCC.md)'s Graphite pass, which uses isl as a computational
library.

## Interfaces

- A C API for constructing and manipulating integer sets, maps, and
  polyhedra under linear constraints, per the documentation.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-isl`: `mingw-w64-ucrt-x86_64-gmp`,
the arbitrary-precision arithmetic foundation documented fully in
[GNU MP](GNU-GMP.md) — isl's exact-integer polyhedral computations rely
on GMP rather than fixed-width integers to avoid overflow in constraint
arithmetic.

## Reverse Dependencies

The snapshot records 12 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-isl`, including
[GCC](GNU-GCC.md#dependencies). See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Isl has no persistent configuration file; its behavior is controlled
entirely through its C API, driven by the calling compiler's optimization
pass.

## Initialization and Execution Flow

As a library, isl has no independent process lifecycle: it initializes
and executes within [GCC](GNU-GCC.md)'s compilation process during the
Graphite optimization pass, the same general library-linkage model
documented for [GNU MP](GNU-GMP.md#initialization-and-execution-flow).

## Runtime Behavior

Isl's polyhedral computations are exercised only when Graphite
optimizations are enabled and applicable to a given loop nest; most
ordinary compilations do not deeply exercise isl even when it is linked
in, since Graphite's transformations target specific loop patterns.

## Compatibility and Variants

Isl's API version compatibility tracks its own release notes; GCC's
supported isl version range is a documented GCC build requirement this
page does not restate.

## Security Considerations

No isl-specific vulnerability review has been performed for this volume;
see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `0.28-1` version.

## Failure Modes and Diagnostics

Isl itself has no user-facing CLI; unexpected Graphite-optimization
behavior (or its absence) in GCC should be checked against whether
Graphite optimization flags were actually requested before being treated
as an isl defect.

## Evidence, Assumptions, and Open Questions

The polyhedral-model computation role is backed by the official isl
project site (`evidence:libisl:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-isl` in the catalog. Package
identity, version, license, and the dependency edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["isl (Integer Set Library)"]
    u0["GCC"]
    u0 -->|requires| subject
    d0["GNU MP (GMP)"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:libisl:isl` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU MP (GMP)](GNU-GMP.md)
- [GCC](GNU-GCC.md)
- [isl (CLANG64)](LIBISL-CLANG64.md)
