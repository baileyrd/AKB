---
id: doc:volume-6:libnghttp2-clang64
title: libnghttp2 (CLANG64)
volume: 6
status: partial
model_refs:
  - library:nghttp2:libnghttp2@clang64
  - package:msys2:mingw-w64-clang-x86_64-nghttp2
  - library:curl:curl@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:nghttp2:libnghttp2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# libnghttp2 (CLANG64)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:nghttp2:libnghttp2@clang64` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | nghttp2 project |
| Environments | `clang64` |
| Upstream | <https://nghttp2.org/> |
| Packaged as | `package:msys2:mingw-w64-clang-x86_64-nghttp2` |
| Version (observed) | 1.70.0-1 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 859.92 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:nghttp2:libnghttp2-manual-2026-07-30` — nghttp2 project site (libnghttp2) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-nghttp2`,
the CLANG64-environment build of nghttp2 — an HTTP/2 protocol library.
It is depended on by [curl (CLANG64)](CURL-CLANG64.md) to back HTTP/2
support, the first entity modeled in this batch's curl (CLANG64)
dependency chain. See the
[official nghttp2 project site](https://nghttp2.org/) for the full
reference.

## Architectural Classification

`library:nghttp2:libnghttp2@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-nghttp2` (version `1.69.0-1` in
the current catalog snapshot, license `MIT`) — a separately built,
separate catalog entity from
[libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md). It belongs to the CLANG64
environment.

## Responsibilities

- Providing an HTTP/2 protocol implementation, consumed by
  [curl (CLANG64)](CURL-CLANG64.md#dependencies) for HTTP/2 transfer
  support, the same functional role
  [libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md#responsibilities)
  documents for its own environment.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[curl (UCRT64)](CURL-UCRT64.md) instead depends on
[libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md#reverse-dependencies) — the
two are not interchangeable, matching the same distinction already
drawn throughout this volume for MSYS/UCRT64/CLANG64 sibling packages.

## Interfaces

- The nghttp2 C API (`nghttp2_session_client_new`,
  `nghttp2_submit_request`, and related functions), the same interface
  [libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md#interfaces) documents, per
  the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-nghttp2` beyond standard
toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 6 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-nghttp2`. One is now modeled in
this knowledge base: [curl (CLANG64)](CURL-CLANG64.md)
(`relationship:foundation-libraries:curl-clang64-requires-libnghttp2-clang64`,
added 2026-08-02). The remaining recorded dependents (`curl-gnutls`,
`libsoup3`, `qemu-image-util`, `wget2`, `wireshark`) are not
individually modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

nghttp2 has no persistent configuration file; behavior is controlled
entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, nghttp2 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [curl (CLANG64)](CURL-CLANG64.md) in this dependency
chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md#runtime-behavior); see that
page for detail not specific to the CLANG64/UCRT64 packaging
distinction.

## Compatibility and Variants

The CLANG64 and UCRT64 nghttp2 packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct environment.

## Security Considerations

No nghttp2-specific vulnerability review has been performed for this
volume. See [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture; no version-qualified
CVE review has been performed for the recorded `1.69.0-1` version.

## Failure Modes and Diagnostics

A dependent program's HTTP/2 transfer failure should be checked
against nghttp2's own protocol-level diagnostics before being treated
as a defect in the consuming program.

## Evidence, Assumptions, and Open Questions

HTTP/2 protocol scope is backed by the official nghttp2 project site
(`evidence:nghttp2:libnghttp2-manual-2026-07-30`), the same evidence
record [libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md) cites. Package
identity, version, license, and the recorded dependent edge are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open: the
five remaining recorded reverse dependents are not individually
modeled in this knowledge base.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libnghttp2 (CLANG64)"]
    u0["curl (CLANG64)"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:nghttp2:libnghttp2@clang64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md)
- [curl (CLANG64)](CURL-CLANG64.md)
