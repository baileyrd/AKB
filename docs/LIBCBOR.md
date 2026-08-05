---
id: doc:volume-6:libcbor
title: libcbor
volume: 6
status: partial
model_refs:
  - library:pjk:libcbor
  - package:msys2:libcbor
  - library:yubico:libfido2
  - library:pjk:libcbor@ucrt64
  - library:pjk:libcbor@clang64
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:pjk:libcbor-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# libcbor

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:pjk:libcbor` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | PJK (Pavel Kalvoda) |
| Environments | `msys` |
| Upstream | <https://github.com/PJK/libcbor> |
| Packaged as | `package:msys2:libcbor` |
| Version (observed) | 0.14.0-2 |
| License (observed) | spdx:MIT |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 63.85 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:pjk:libcbor-manual-2026-07-30` — libcbor (GitHub project page) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

libcbor is a C library for parsing and generating CBOR (Concise Binary
Object Representation), a general-purpose schema-less binary data
format. This page documents its architectural role as a directly-declared
dependency of [libfido2](LIBFIDO2.md), which uses it for its own
CBOR-encoded FIDO2/U2F protocol data, already noted as an unmodeled
sub-dependency on [LIBFIDO2.md](LIBFIDO2.md#dependencies) before this
page existed. See the
[official libcbor project page](https://github.com/PJK/libcbor) for the
full reference.

## Architectural Classification

`library:pjk:libcbor` is packaged in the MSYS environment as
`package:msys2:libcbor` (version `0.14.0-2` in the current catalog
snapshot). This is the package [libfido2](LIBFIDO2.md#dependencies)
actually depends on for CBOR encoding/decoding — FIDO2's own protocol
data is CBOR-encoded per the FIDO2/CTAP specification.

## Responsibilities

- Parsing and generating CBOR-encoded binary data, consumed by
  [libfido2](LIBFIDO2.md) for the CBOR-encoded messages the FIDO2/CTAP
  protocol uses between a client and a hardware security key.

## Boundaries

libcbor provides general-purpose CBOR encoding/decoding specifically; it
implements no FIDO2/U2F protocol logic itself — that remains
[libfido2's](LIBFIDO2.md) own responsibility, with libcbor serving only
as the underlying binary-format layer.

## Interfaces

- A C API (`cbor_load`, `cbor_serialize`, and type-specific constructors)
  for building and parsing CBOR data structures, per the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:libcbor` beyond standard MSYS runtime support.

## Reverse Dependencies

The catalog snapshot records 2 relationships targeting
`package:msys2:libcbor`: its own `-devel` subpackage and
`package:msys2:libfido2`
(`relationship:foundation-libraries:libfido2-requires-libcbor` in this
knowledge base's graph) — its sole functional dependent in this
snapshot.

## Configuration

libcbor has no persistent configuration file; encoding/decoding
behavior is controlled entirely through its C API by the calling
program.

## Initialization and Execution Flow

As a library, libcbor has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [libfido2](LIBFIDO2.md) in this dependency chain. As an
MSYS-dependent library, this is adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

libcbor's encoding/decoding role is exercised on every FIDO2/CTAP
message exchange between [libfido2](LIBFIDO2.md) and a physical security
key, since the protocol itself is CBOR-encoded end to end.

## Compatibility and Variants

**Correction, 2026-08-02**: this section previously stated it was
unconfirmed whether other native environments packaged libcbor
separately. They do: [libcbor (UCRT64)](LIBCBOR-UCRT64.md) and
[libcbor (CLANG64)](LIBCBOR-CLANG64.md) are now modeled as separate
catalog entities, each unblocking their own environment's libfido2
sibling.

## Security Considerations

Parsing untrusted CBOR input (data received from a FIDO2 hardware key,
or crafted input in an attack scenario) is a documented general source
of parser vulnerabilities for binary-format libraries; this page does
not assert this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `0.14.0-2` version.

## Failure Modes and Diagnostics

A libfido2 operation failing with a malformed-data error most commonly
indicates a CBOR-encoding mismatch between the client and device
firmware rather than a libcbor defect itself.

## Evidence, Assumptions, and Open Questions

CBOR encoding/decoding scope is backed by the official libcbor project
page (`evidence:pjk:libcbor-manual-2026-07-30`), matching the
`project_url` already recorded for `package:msys2:libcbor` in the
catalog. Package identity, version, and the recorded dependent edge are
backed by the pacman catalog snapshot (`evidence:catalog:current`).
Open: whether other native environments package libcbor separately was
not confirmed. Also explicitly out of scope for this page: header-level
API surface and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libcbor"]
    u0["libfido2"]
    u0 -->|requires| subject
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:pjk:libcbor` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libfido2](LIBFIDO2.md)
- [libcbor (UCRT64)](LIBCBOR-UCRT64.md)
- [libcbor (CLANG64)](LIBCBOR-CLANG64.md)
