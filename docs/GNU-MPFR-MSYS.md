---
id: doc:volume-6:gnu-mpfr-msys
title: GNU MPFR (MSYS)
volume: 6
status: partial
model_refs:
  - library:gnu:mpfr@msys
  - package:msys2:mpfr
  - library:gnu:gmp@msys
  - component:gnu:gawk
  - environment:msys2:msys
evidence_refs:
  - evidence:gnu:mpfr-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GNU MPFR (MSYS)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnu:mpfr@msys` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | GNU Project |
| Environments | `msys` |
| Upstream | <https://www.mpfr.org/> |
| Packaged as | `package:msys2:mpfr` |
| Version (observed) | 4.2.2-1 |
| License (observed) | spdx:LGPL-3.0-or-later |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 852.1 KB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:gnu:mpfr-manual-2026-07-30` — GNU MPFR (official project site) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents the **MSYS-environment** MPFR package (`mpfr`)
specifically — a correctly-rounded, arbitrary-precision floating-point
library built on GMP — as a distinct catalog entity from this knowledge
base's existing [GNU MPFR (UCRT64)](GNU-MPFR.md) page: gawk's
`--bignum` arbitrary-precision mode links against this MSYS package,
already cited by package name on
[GNU-AWK.md's dependency table](GNU-AWK.md#dependencies) before this
page existed. See the [official MPFR project site](https://www.mpfr.org)
for the API reference shared with the UCRT64 package.

## Architectural Classification

`library:gnu:mpfr@msys` is packaged in the MSYS environment as
`package:msys2:mpfr` (version `4.2.2-1` in the current catalog
snapshot, license `LGPL-3.0-or-later`) — a separately versioned catalog
entity from [GNU MPFR (UCRT64)](GNU-MPFR.md)'s
`mingw-w64-ucrt-x86_64-mpfr` package. This is the package
[gawk](GNU-AWK.md) — an MSYS-environment component itself — actually
depends on, the same MSYS-vs-native distinction applied consistently
throughout this volume.

## Responsibilities

- Providing correctly-rounded floating-point arithmetic at arbitrary,
  user-selected precision, consumed by [gawk's](GNU-AWK.md) `--bignum`
  mode for arbitrary-precision integer and floating-point support.

## Boundaries

Like [GNU MPFR (UCRT64)](GNU-MPFR.md#boundaries), this package adds
correct-rounding floating-point semantics on top of
[GNU MP (MSYS)](GNU-GMP-MSYS.md)'s arithmetic primitives; it does not
itself provide complex-number support or any gawk-specific
functionality beyond the arithmetic primitives gawk's `--bignum` mode
calls into.

## Interfaces

- The `mpfr_*` C function family, identical to the API documented on
  [GNU MPFR (UCRT64)](GNU-MPFR.md#interfaces), per the documentation.

## Dependencies

The MSYS `package:msys2:mpfr` declares one `runtime-depends-on` edge:
`package:msys2:gmp` (the arithmetic foundation MPFR builds on,
documented fully in [GNU MP (MSYS)](GNU-GMP-MSYS.md),
`relationship:foundation-libraries:mpfr-msys-requires-gmp-msys`).

## Reverse Dependencies

The catalog snapshot records 5 relationships targeting
`package:msys2:mpfr`: `package:msys2:gawk`
(`relationship:gnu-userland:gawk-requires-mpfr-msys` in this knowledge
base's graph), its own `-devel` subpackage, and three further MSYS
packages — `package:msys2:gcc`, `package:msys2:gdb`, and
`package:msys2:mpc` — the MSYS-native builds of the toolchain
components this knowledge base's [GCC](GNU-GCC.md#dependencies) and
[GDB](GNU-GDB.md#dependencies) pages already document via their
separately versioned UCRT64 MPFR dependency; these three MSYS-native
toolchain packages are not individually modeled in this knowledge base,
distinct from the UCRT64/CLANG64-targeting toolchain components this
knowledge base otherwise documents. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

MPFR has no persistent configuration file; precision and rounding mode
are set per-operation or per-variable through its C API, identical to
[GNU MPFR (UCRT64)](GNU-MPFR.md#configuration).

## Initialization and Execution Flow

As a library, this package has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [gawk](GNU-AWK.md) in this dependency chain, only when
`--bignum` mode is actually requested. As an MSYS-dependent library,
this is adapted from POSIX semantics onto Windows process primitives by
`msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Identical functional behavior to [GNU MPFR (UCRT64)](GNU-MPFR.md#runtime-behavior);
see that page for the correct-rounding reproducibility guarantee, not
specific to the MSYS/UCRT64 packaging distinction.

## Compatibility and Variants

The MSYS and native (UCRT64/CLANG64/i686) MPFR packages are separately
versioned catalog entities (see Architectural Classification); code
built against one is not automatically compatible with the other
without matching the correct environment.

## Security Considerations

No MPFR-specific vulnerability review has been performed for this
volume; see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `4.2.2-1` version.

## Failure Modes and Diagnostics

MPFR itself has no user-facing CLI; a `gawk --bignum` precision-related
failure should be checked against the requested precision and rounding
mode before being treated as an MPFR defect, the same triage order
documented for [GNU MPFR (UCRT64)](GNU-MPFR.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

The correct-rounding arithmetic model is backed by the official MPFR
project site (`evidence:gnu:mpfr-manual-2026-07-30`), the same evidence
record [GNU MPFR (UCRT64)](GNU-MPFR.md) cites, matching the
`project_url` already recorded for `package:msys2:mpfr` in the catalog.
Package identity, version, license, and the recorded dependency/dependent
edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Open, and explicitly out of scope for this
page: the three MSYS-native toolchain reverse dependents (`gcc`, `gdb`,
`mpc`) are not individually modeled in this knowledge base; header-level
API surface and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology, also remain open.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["GNU MPFR (MSYS)"]
    u0["GNU Awk (gawk)"]
    u0 -->|requires| subject
    d0["GNU MP (MSYS)"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnu:mpfr@msys` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU MPFR (UCRT64)](GNU-MPFR.md)
- [GNU MP (MSYS)](GNU-GMP-MSYS.md)
- [gawk](GNU-AWK.md)
- [GNU MPFR (CLANG64)](GNU-MPFR-CLANG64.md)
