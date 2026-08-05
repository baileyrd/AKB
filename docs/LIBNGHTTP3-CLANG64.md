---
id: doc:volume-6:libnghttp3-clang64
title: libnghttp3 (CLANG64)
volume: 6
status: partial
model_refs:
  - library:nghttp2:libnghttp3@clang64
  - package:msys2:mingw-w64-clang-x86_64-nghttp3
  - library:curl:curl@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:nghttp2:libnghttp3-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# libnghttp3 (CLANG64)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:nghttp2:libnghttp3@clang64` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | nghttp2 project |
| Environments | `clang64` |
| Upstream | <https://nghttp2.org/> |
| Packaged as | `package:msys2:mingw-w64-clang-x86_64-nghttp3` |
| Version (observed) | 1.18.0-1 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 610.38 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:nghttp2:libnghttp3-manual-2026-07-30` — nghttp3 project page (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-nghttp3`,
the CLANG64-environment build of nghttp3 — an HTTP/3 protocol library.
It is depended on by [curl (CLANG64)](CURL-CLANG64.md) to back HTTP/3
support. See the [official nghttp2 project site](https://nghttp2.org/)
(nghttp3 is developed alongside nghttp2 by the same project) for the
full reference.

## Architectural Classification

`library:nghttp2:libnghttp3@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-nghttp3` (version `1.17.0-1` in
the current catalog snapshot, license `MIT`) — a separately built,
separate catalog entity from
[libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md). It belongs to the CLANG64
environment.

## Responsibilities

- Providing an HTTP/3 protocol implementation, consumed by
  [curl (CLANG64)](CURL-CLANG64.md#dependencies) for HTTP/3 transfer
  support, the same functional role
  [libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md#responsibilities)
  documents for its own environment.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[curl (UCRT64)](CURL-UCRT64.md) instead depends on
[libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md#reverse-dependencies) — the
two are not interchangeable, matching the same distinction already
drawn throughout this volume for MSYS/UCRT64/CLANG64 sibling packages.
nghttp3 implements the HTTP/3 framing layer specifically, distinct
from [libngtcp2 (CLANG64)](LIBNGTCP2-CLANG64.md)'s QUIC transport
layer that HTTP/3 runs over.

## Interfaces

- The nghttp3 C API (`nghttp3_conn_client_new`, and related functions),
  the same interface
  [libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md#interfaces) documents,
  per the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-nghttp3` beyond standard
toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 3 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-nghttp3`. One is now modeled in
this knowledge base: [curl (CLANG64)](CURL-CLANG64.md)
(`relationship:foundation-libraries:curl-clang64-requires-libnghttp3-clang64`,
added 2026-08-02). The remaining recorded dependents (`curl-gnutls`,
`wireshark`) are not individually modeled in this knowledge base; see
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

nghttp3 has no persistent configuration file; behavior is controlled
entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, nghttp3 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [curl (CLANG64)](CURL-CLANG64.md) in this dependency
chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md#runtime-behavior); see that
page for detail not specific to the CLANG64/UCRT64 packaging
distinction.

## Compatibility and Variants

The CLANG64 and UCRT64 nghttp3 packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct environment.

## Security Considerations

No nghttp3-specific vulnerability review has been performed for this
volume. See [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture; no version-qualified
CVE review has been performed for the recorded `1.17.0-1` version.

## Failure Modes and Diagnostics

A dependent program's HTTP/3 transfer failure should be checked
against nghttp3's own protocol-level diagnostics before being treated
as a defect in the consuming program.

## Evidence, Assumptions, and Open Questions

HTTP/3 protocol scope is backed by the official nghttp2 project site
(`evidence:nghttp2:libnghttp3-manual-2026-07-30`), the same evidence
record [libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md) cites. Package
identity, version, license, and the recorded dependent edge are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open: the
two remaining recorded reverse dependents are not individually
modeled in this knowledge base.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libnghttp3 (CLANG64)"]
    u0["curl (CLANG64)"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:nghttp2:libnghttp3@clang64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libnghttp3 (UCRT64)](LIBNGHTTP3-UCRT64.md)
- [libngtcp2 (CLANG64)](LIBNGTCP2-CLANG64.md)
- [curl (CLANG64)](CURL-CLANG64.md)
