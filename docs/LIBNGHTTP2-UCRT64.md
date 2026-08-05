---
id: doc:volume-6:libnghttp2-ucrt64
title: libnghttp2 (UCRT64)
volume: 6
status: partial
model_refs:
  - library:nghttp2:libnghttp2@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-nghttp2
  - library:curl:curl@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:nghttp2:libnghttp2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libnghttp2 (UCRT64)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:nghttp2:libnghttp2@ucrt64` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | nghttp2 project |
| Environments | `ucrt64` |
| Upstream | <https://nghttp2.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-nghttp2` |
| Version (observed) | 1.70.0-1 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 944.62 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:nghttp2:libnghttp2-manual-2026-07-30` — nghttp2 project site (libnghttp2) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents the **UCRT64-environment** libnghttp2 package
specifically — a reusable C library implementing the framing layer of
HTTP/2 — depended on by [curl (UCRT64)](CURL-UCRT64.md) for HTTP/2
protocol support, closing one of the sub-dependencies that page's own
Dependencies section had left explicitly unmodeled. See the
[official nghttp2 project site](https://nghttp2.org/) for the full
reference.

## Architectural Classification

`library:nghttp2:libnghttp2@ucrt64` is packaged in the UCRT64
environment as `package:msys2:mingw-w64-ucrt-x86_64-nghttp2` (version
`1.69.0-1` in the current catalog snapshot, license `MIT`) — a
separately built, separate catalog entity from
[libnghttp2 (MSYS)](LIBNGHTTP2.md)'s `libnghttp2` package. This is the
package [curl (UCRT64)](CURL-UCRT64.md) — a UCRT64-native component
itself — actually depends on.

## Responsibilities

- Providing the HTTP/2 framing layer, consumed by
  [curl (UCRT64)](CURL-UCRT64.md#dependencies) for HTTP/2 protocol
  support.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[curl (MSYS)](CURL.md) and [libcurl (MSYS)](LIBCURL.md) instead depend
on [libnghttp2 (MSYS)](LIBNGHTTP2.md#reverse-dependencies) — the two
are not interchangeable, matching the same distinction already made
throughout this volume for MSYS/UCRT64 sibling pairs.

## Interfaces

- The nghttp2 C API (`nghttp2_session_client_new`,
  `nghttp2_session_send`, and related functions), the same interface
  [libnghttp2 (MSYS)](LIBNGHTTP2.md#interfaces) documents, per the
  documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-nghttp2` declares no
`runtime-depends-on` edges beyond standard toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 6 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-nghttp2`. One is now modeled in
this knowledge base: [curl (UCRT64)](CURL-UCRT64.md)
(`relationship:foundation-libraries:curl-ucrt64-requires-libnghttp2-ucrt64`).
The remaining recorded dependents (`libsoup3`, `qemu-image-util`,
`wget2`, and `wireshark`) are not individually modeled in this
knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libnghttp2 has no persistent configuration file; behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libnghttp2 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [curl (UCRT64)](CURL-UCRT64.md) in this dependency chain.
As a native MinGW-w64 library, this process model is Windows-facing
directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[libnghttp2 (MSYS)](LIBNGHTTP2.md#runtime-behavior); see that page for
detail not specific to the UCRT64/MSYS packaging distinction.

## Compatibility and Variants

The UCRT64 and MSYS libnghttp2 packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct package/environment.

## Security Considerations

HTTP/2 frame parsing against untrusted network input is a documented
general source of protocol-implementation risk; this page does not
assert this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `1.69.0-1` version.

## Failure Modes and Diagnostics

An HTTP/2-specific curl transfer failure should be checked with curl's
own verbose diagnostics before being treated as a libnghttp2 defect,
the same triage order documented for
[libnghttp2 (MSYS)](LIBNGHTTP2.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

HTTP/2 protocol framing scope is backed by the official nghttp2
project site (`evidence:nghttp2:libnghttp2-manual-2026-07-30`), the
same evidence record [libnghttp2 (MSYS)](LIBNGHTTP2.md) cites. Package
identity, version, license, and the one modeled dependent edge are
backed by the pacman catalog snapshot (`evidence:catalog:current`).
Open, and explicitly out of scope for this page: the remaining
recorded dependents not individually modeled, and header-level API
surface / PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libnghttp2 (UCRT64)"]
    u0["curl (UCRT64)"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:nghttp2:libnghttp2@ucrt64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libnghttp2 (MSYS)](LIBNGHTTP2.md)
- [curl (UCRT64)](CURL-UCRT64.md)
- [libnghttp2 (CLANG64)](LIBNGHTTP2-CLANG64.md)
