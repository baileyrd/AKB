---
id: doc:volume-6:gnu-mpfr-clang64
title: GNU MPFR (CLANG64)
volume: 6
status: partial
model_refs:
  - library:gnu:mpfr@clang64
  - package:msys2:mingw-w64-clang-x86_64-mpfr
  - library:gnu:gmp@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:gnu:mpfr-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# GNU MPFR (CLANG64)

## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-mpfr`, the
CLANG64-environment build of GNU MPFR — multiple-precision,
correctly-rounded binary floating-point arithmetic built on
[GMP (CLANG64)](GNU-GMP-CLANG64.md), one of the concrete future-batch
candidates that page's own Reverse Dependencies section flagged before
this page existed. See the
[official MPFR project site](https://www.mpfr.org) for the API
reference.

## Architectural Classification

`library:gnu:mpfr@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-mpfr` (version `4.2.2-3` in the
current catalog snapshot, license `LGPL-3.0-or-later`) — the same
version number as the UCRT64 sibling documented on
[GNU MPFR](GNU-MPFR.md), but a separately built, separate catalog
entity. It belongs to the CLANG64 environment. Its sole recorded
non-boilerplate runtime dependency, [GMP (CLANG64)](GNU-GMP-CLANG64.md),
was already a modeled entity in this knowledge base (added earlier in
this same session), letting this addition close its full dependency
footprint in a single pass.

## Responsibilities

- Providing correctly-rounded floating-point arithmetic (each result
  guaranteed as if computed with infinite precision and rounded once)
  at arbitrary, user-selected precision for CLANG64-native consumers,
  the same role [GNU MPFR (UCRT64)](GNU-MPFR.md#responsibilities)
  documents for its own environment.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[GCC](GNU-GCC.md) and [GDB](GNU-GDB.md) instead link
[GNU MPFR (UCRT64)](GNU-MPFR.md#reverse-dependencies) — the two are not
interchangeable, matching the same distinction already drawn throughout
this volume for MSYS/UCRT64/CLANG64 sibling triples.

## Interfaces

- The `mpfr_*` C function family, the same interface
  [GNU MPFR (UCRT64)](GNU-MPFR.md#interfaces) documents, per the
  documentation.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-mpfr`; the `cc-libs` C/C++
runtime row is excluded per this volume's boilerplate-dependency
policy, and the remaining one is modeled in this knowledge base:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| [GMP (CLANG64)](GNU-GMP-CLANG64.md) | `package:msys2:mingw-w64-clang-x86_64-gmp` | MPFR is built directly atop GMP's own arbitrary-precision integer and floating-point primitives, adding correctly-rounded semantics. |

## Reverse Dependencies

The catalog snapshot records 26 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-mpfr`. One is now modeled in
this knowledge base: [GNU MPC (CLANG64)](GNU-MPC-CLANG64.md)
(`relationship:foundation-libraries:mpc-clang64-requires-mpfr-clang64`,
added 2026-08-02). The remaining 25 include
`mingw-w64-clang-x86_64-gdb` (the CLANG64 sibling of
[GDB](GNU-GDB.md), not yet modeled) and are not currently
modeled as entities in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

MPFR has no persistent configuration file; precision and rounding mode
are set per-operation or per-variable through its C API, the same
model documented for [GNU MPFR (UCRT64)](GNU-MPFR.md#configuration).

## Initialization and Execution Flow

As a library, MPFR has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it.
As a native MinGW-w64 library, this process model is Windows-facing
directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [GNU MPFR (UCRT64)](GNU-MPFR.md); see
that page for detail not specific to the CLANG64/UCRT64 packaging
distinction.

## Compatibility and Variants

The CLANG64 and UCRT64 MPFR packages are separately versioned catalog
entities (see Architectural Classification); code built against one is
not automatically compatible with the other without matching the
correct environment.

## Security Considerations

No MPFR-specific vulnerability review has been performed for this
volume; see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. No version-qualified
CVE review has been performed for the recorded `4.2.2-3` version.

## Failure Modes and Diagnostics

MPFR itself has no user-facing CLI; precision-related failures in a
dependent tool should be checked against the requested precision and
rounding mode before being treated as an MPFR defect, the same guidance
already given for [GNU MPFR (UCRT64)](GNU-MPFR.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

The correct-rounding arithmetic model is backed by the official MPFR
project site (`evidence:gnu:mpfr-manual-2026-07-30`), the same evidence
record [GNU MPFR (UCRT64)](GNU-MPFR.md) cites. Package identity,
version, license, and the recorded dependency edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open: 25 of the
26 recorded reverse dependents are not individually modeled in this
knowledge base.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU MPFR (UCRT64)](GNU-MPFR.md)
- [GNU MPFR (MSYS)](GNU-MPFR-MSYS.md)
- [GNU MPC (CLANG64)](GNU-MPC-CLANG64.md)
- [GMP (CLANG64)](GNU-GMP-CLANG64.md)
