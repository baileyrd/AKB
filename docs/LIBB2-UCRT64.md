---
id: doc:volume-6:libb2-ucrt64
title: BLAKE2 (libb2) (UCRT64)
volume: 6
status: partial
model_refs:
  - library:blake2:libb2@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-libb2
  - library:libarchive:libarchive
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:blake2:project-site-2026-08-02
  - evidence:catalog:current
last_verified: 2026-08-02
---

# BLAKE2 (libb2) (UCRT64)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:blake2:libb2@ucrt64` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | BLAKE2 project |
| Environments | `ucrt64` |
| Upstream | <https://blake2.net/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-libb2` |
| Version (observed) | 0.98.1-3 |
| License (observed) | custom:CC0 |
| Architecture (observed) | any |
| Installed size (observed) | 87.79 KiB |

**Evidence on this object**

- `evidence:blake2:project-site-2026-08-02` — BLAKE2 (official project site) (`primary`, retrieved 2026-08-02)
- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents `package:msys2:mingw-w64-ucrt-x86_64-libb2`, the
UCRT64-environment build of libb2 — a library implementing the BLAKE2
cryptographic hash function family. It closes the last of
[libarchive's](LIBARCHIVE.md#dependencies) own three previously-declined
UCRT64-native dependencies (alongside [bzip2 (UCRT64)](BZIP2-UCRT64.md)
and [LZ4 (UCRT64)](LZ4-UCRT64.md), both closed in an earlier batch).
See the [official BLAKE2 project site](https://blake2.net/) for the
full reference.

## Architectural Classification

`library:blake2:libb2@ucrt64` is packaged as
`package:msys2:mingw-w64-ucrt-x86_64-libb2` (version `0.98.1-3` in the
current catalog snapshot, license `CC0`) — a separately built, separate
catalog entity from [BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md)'s
`mingw-w64-clang-x86_64-libb2` package. It belongs to the UCRT64
environment.

## Responsibilities

- Providing BLAKE2 cryptographic hash functions (BLAKE2b, BLAKE2s,
  and related variants), consumed by
  [libarchive](LIBARCHIVE.md#dependencies) for BLAKE2-based checksum
  support, the same functional role
  [BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md#responsibilities)
  documents for its own environment.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md#reverse-dependencies)
instead serves CLANG64-environment consumers as a separate,
non-interchangeable catalog entity — the same distinction already
drawn throughout this volume for MSYS/UCRT64/CLANG64 sibling packages.
libb2 provides the BLAKE2 hash algorithm specifically; it is a
distinct, independently designed hash family from the SHA-2/SHA-3
families, not a variant or wrapper of either.

## Interfaces

- The BLAKE2 C API (`blake2b`, `blake2s`, and streaming variants), the
  same interface [BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md#interfaces)
  documents, per the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-libb2` beyond standard toolchain
runtime support.

## Reverse Dependencies

The catalog snapshot records 3 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libb2`. One is now modeled in
this knowledge base: [libarchive](LIBARCHIVE.md)
(`relationship:foundation-libraries:libarchive-requires-libb2-ucrt64`,
added 2026-08-02). The remaining recorded dependents (`python`,
`qt6-base`) are not individually modeled in this knowledge base; see
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libb2 has no persistent configuration file; hash algorithm and output
length are selected entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libb2 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [libarchive](LIBARCHIVE.md) in this dependency chain. As
a native MinGW-w64 library, this process model is Windows-facing
directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md#runtime-behavior); see
that page for detail not specific to the UCRT64 packaging distinction.

## Compatibility and Variants

The UCRT64 and CLANG64 libb2 packages are separately versioned catalog
entities (see Architectural Classification); code built against one is
not automatically compatible with the other without matching the
correct package/environment. BLAKE2 itself defines two primary
variants, BLAKE2b (optimized for 64-bit platforms) and BLAKE2s
(optimized for 8- to 32-bit platforms); this page does not confirm
which variant(s) libarchive's own BLAKE2 checksum support exercises.

## Security Considerations

As a cryptographic hash function library, libb2 sits in a
security-relevant position for whatever program links against it and
relies on its hash output for integrity verification; this page does
not assert this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `0.98.1-3` version.

## Failure Modes and Diagnostics

libb2 itself has no user-facing CLI; a checksum mismatch in a
dependent program should be checked against the actual algorithm and
output length requested before being treated as a libb2 defect.

## Evidence, Assumptions, and Open Questions

The BLAKE2 hash-function scope is backed by the official BLAKE2
project site (`evidence:blake2:project-site-2026-08-02`), the same
evidence record [BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md) cites.
Package identity, version, license, and the recorded dependent edge
are backed by the pacman catalog snapshot (`evidence:catalog:current`).
Open: the two remaining recorded reverse dependents (`python`,
`qt6-base`) are not individually modeled in this knowledge base.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["BLAKE2 (libb2) (UCRT64)"]
    u0["libarchive"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:blake2:libb2@ucrt64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [BLAKE2 (libb2) (CLANG64)](LIBB2-CLANG64.md)
- [libarchive](LIBARCHIVE.md)
