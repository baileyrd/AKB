---
id: doc:volume-6:libcbor-clang64
title: libcbor (CLANG64)
volume: 6
status: partial
model_refs:
  - library:pjk:libcbor@clang64
  - package:msys2:mingw-w64-clang-x86_64-libcbor
  - library:yubico:libfido2@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:pjk:libcbor-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# libcbor (CLANG64)

## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-libcbor`,
the CLANG64-environment build of libcbor — a C library for parsing
and generating CBOR (Concise Binary Object Representation). It exists
solely to unblock [libfido2 (CLANG64)](LIBFIDO2-CLANG64.md), the same
role [libcbor (MSYS)](LIBCBOR.md) and
[libcbor (UCRT64)](LIBCBOR-UCRT64.md) serve for their own
environments. See the
[official libcbor project page](https://github.com/PJK/libcbor) for
the full reference.

## Architectural Classification

`library:pjk:libcbor@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-libcbor` (version `0.14.0-1` in
the current catalog snapshot, license `MIT`) — a separately built,
separate catalog entity from both [libcbor (MSYS)](LIBCBOR.md)'s
`libcbor` package and [libcbor (UCRT64)](LIBCBOR-UCRT64.md)'s
`mingw-w64-ucrt-x86_64-libcbor` package. It belongs to the CLANG64
environment.

## Responsibilities

- Parsing and generating CBOR-encoded binary data, consumed by
  [libfido2 (CLANG64)](LIBFIDO2-CLANG64.md) for the CBOR-encoded
  messages the FIDO2/CTAP protocol uses between a client and a
  hardware security key, the same functional role
  [libcbor (MSYS)](LIBCBOR.md#responsibilities) and
  [libcbor (UCRT64)](LIBCBOR-UCRT64.md#responsibilities) document for
  their own environments.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[libcbor (MSYS)](LIBCBOR.md#reverse-dependencies) and
[libcbor (UCRT64)](LIBCBOR-UCRT64.md#reverse-dependencies) instead
serve their own environments' consumers as separate, non-interchangeable
catalog entities — the same distinction already drawn throughout this
volume for MSYS/UCRT64/CLANG64 sibling packages.

## Interfaces

- A C API (`cbor_load`, `cbor_serialize`, and type-specific
  constructors) for building and parsing CBOR data structures, the
  same interface [libcbor (MSYS)](LIBCBOR.md#interfaces) and
  [libcbor (UCRT64)](LIBCBOR-UCRT64.md#interfaces) document, per the
  documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-libcbor` beyond standard
toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 1 relationship targeting
`package:msys2:mingw-w64-clang-x86_64-libcbor`: `package:msys2:mingw-w64-clang-x86_64-libfido2`
(`relationship:foundation-libraries:libfido2-clang64-requires-libcbor-clang64`,
added 2026-08-02) — its sole functional dependent in this snapshot,
the same single-dependent pattern
[libcbor (MSYS)](LIBCBOR.md#reverse-dependencies) and
[libcbor (UCRT64)](LIBCBOR-UCRT64.md#reverse-dependencies) document.

## Configuration

libcbor has no persistent configuration file; encoding/decoding
behavior is controlled entirely through its C API by the calling
program.

## Initialization and Execution Flow

As a library, libcbor has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [libfido2 (CLANG64)](LIBFIDO2-CLANG64.md) in this
dependency chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [libcbor (MSYS)](LIBCBOR.md#runtime-behavior)
and [libcbor (UCRT64)](LIBCBOR-UCRT64.md#runtime-behavior); see those
pages for detail not specific to the CLANG64 packaging distinction.

## Compatibility and Variants

The CLANG64, UCRT64, and MSYS libcbor packages are three separately
versioned catalog entities (see Architectural Classification); code
built against one is not automatically compatible with another without
matching the correct package/environment.

## Security Considerations

Parsing untrusted CBOR input carries the same general parser-defect
risk documented for [libcbor (MSYS)](LIBCBOR.md#security-considerations);
see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. No version-qualified
CVE review has been performed for the recorded `0.14.0-1` version.

## Failure Modes and Diagnostics

A libfido2 operation failing with a malformed-data error most commonly
indicates a CBOR-encoding mismatch between the client and device
firmware rather than a libcbor defect itself, the same triage order
[libcbor (MSYS)](LIBCBOR.md#failure-modes-and-diagnostics) documents.

## Evidence, Assumptions, and Open Questions

CBOR encoding/decoding scope is backed by the official libcbor project
page (`evidence:pjk:libcbor-manual-2026-07-30`), the same evidence
record [libcbor (MSYS)](LIBCBOR.md) and
[libcbor (UCRT64)](LIBCBOR-UCRT64.md) cite. Package identity, version,
license, and the recorded dependent edge are backed by the pacman
catalog snapshot (`evidence:catalog:current`). Open, and explicitly
out of scope for this page: header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libcbor (CLANG64)"]
    u0["libfido2 (CLANG64)"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:pjk:libcbor@clang64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libcbor (MSYS)](LIBCBOR.md)
- [libcbor (UCRT64)](LIBCBOR-UCRT64.md)
- [libfido2 (CLANG64)](LIBFIDO2-CLANG64.md)
