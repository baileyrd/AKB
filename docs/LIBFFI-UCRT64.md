---
id: doc:volume-6:libffi-ucrt64
title: libffi (UCRT64)
volume: 6
status: partial
model_refs:
  - library:libffi:libffi@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-libffi
  - library:p11-glue:p11-kit@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:libffi:project-site-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libffi (UCRT64)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:libffi:libffi@ucrt64` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | libffi project |
| Environments | `ucrt64` |
| Upstream | <https://sourceware.org/libffi> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-libffi` |
| Version (observed) | 3.7.1-1 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 160.2 KB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:libffi:project-site-2026-07-30` — libffi (official project site) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents the **UCRT64-environment** libffi package
specifically — a portable, high-level foreign function interface (FFI)
library — depended on by [p11-kit (UCRT64)](P11-KIT-UCRT64.md) for
loading PKCS#11 modules dynamically, the third distinct libffi-named
catalog entity in this knowledge base alongside
[libffi (MSYS)](LIBFFI-MSYS.md) and
[libffi (CLANG64)](LIBFFI-CLANG64.md). See the
[official libffi project site](https://sourceware.org/libffi) for the
full reference.

## Architectural Classification

`library:libffi:libffi@ucrt64` is packaged in the UCRT64 environment as
`package:msys2:mingw-w64-ucrt-x86_64-libffi` (version `3.7.1-1` in the
current catalog snapshot, license `MIT`, matching
[libffi (MSYS)'s](LIBFFI-MSYS.md#architectural-classification) and
[libffi (CLANG64)'s](LIBFFI-CLANG64.md#architectural-classification)
own recorded version) — a separately built, separate catalog entity
from both. This is the package
[p11-kit (UCRT64)](P11-KIT-UCRT64.md) — a UCRT64-native library entity
itself — actually depends on.

## Responsibilities

- Providing a foreign function interface (calling functions whose
  signature is determined at runtime rather than compile time),
  consumed by [p11-kit (UCRT64)](P11-KIT-UCRT64.md#dependencies) for
  its PKCS#11 module-loading mechanism, the same functional role
  [libffi (MSYS)](LIBFFI-MSYS.md#responsibilities) documents for
  p11-kit (MSYS).

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[p11-kit (MSYS)](P11-KIT.md) instead depends on
[libffi (MSYS)](LIBFFI-MSYS.md#reverse-dependencies) and
[LLVM libraries](LLVM-LIBS.md) depends on
[libffi (CLANG64)](LIBFFI-CLANG64.md#reverse-dependencies) — the three
are not interchangeable, matching the same distinction already made
throughout this volume for MSYS/UCRT64/CLANG64 sibling groups.

## Interfaces

- The libffi C API (`ffi_prep_cif`, `ffi_call`, and related functions),
  the same interface [libffi (MSYS)](LIBFFI-MSYS.md#interfaces) and
  [libffi (CLANG64)](LIBFFI-CLANG64.md#interfaces) document, per the
  documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-libffi` declares no
`runtime-depends-on` edges beyond standard toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libffi`. One is now modeled in
this knowledge base: [p11-kit (UCRT64)](P11-KIT-UCRT64.md)
(`relationship:foundation-libraries:p11-kit-ucrt64-requires-libffi-ucrt64`).
The remaining recorded dependents are not individually modeled in this
knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libffi has no persistent configuration file; call-interface
descriptions are constructed entirely through its C API by the calling
program.

## Initialization and Execution Flow

As a library, libffi has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [p11-kit (UCRT64)](P11-KIT-UCRT64.md) in this dependency
chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [libffi (MSYS)](LIBFFI-MSYS.md#runtime-behavior)
and [libffi (CLANG64)](LIBFFI-CLANG64.md#runtime-behavior); see those
pages for detail not specific to this package's own environment.

## Compatibility and Variants

The UCRT64, MSYS, and CLANG64 libffi packages are three separately
versioned catalog entities (see Architectural Classification); code
built against one is not automatically compatible with another without
matching the correct package/environment.

## Security Considerations

A foreign-function-interface library sits in a security-sensitive
position by nature, since it mediates calls into dynamically resolved
code; this page does not assert this specific package version's
robustness. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `3.7.1-1` version.

## Failure Modes and Diagnostics

A p11-kit (UCRT64) module-loading failure traceable to a call-signature
mismatch should be checked against the target PKCS#11 module's actual
exported symbols before being treated as a libffi defect, the same
triage order documented for
[libffi (MSYS)](LIBFFI-MSYS.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

Foreign-function-interface scope is backed by the official libffi
project site (`evidence:libffi:project-site-2026-07-30`), the same
evidence record [libffi (MSYS)](LIBFFI-MSYS.md) and
[libffi (CLANG64)](LIBFFI-CLANG64.md) cite. Package identity, version,
license, and the one modeled dependent edge are backed by the pacman
catalog snapshot (`evidence:catalog:current`). Open, and explicitly
out of scope for this page: the remaining recorded dependents not
individually modeled, and header-level API surface / PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libffi (UCRT64)"]
    u0["p11-kit (UCRT64)"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:libffi:libffi@ucrt64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libffi (MSYS)](LIBFFI-MSYS.md)
- [libffi (CLANG64)](LIBFFI-CLANG64.md)
- [p11-kit (UCRT64)](P11-KIT-UCRT64.md)
