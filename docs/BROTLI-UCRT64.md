---
id: doc:volume-6:brotli-ucrt64
title: Brotli (UCRT64)
volume: 6
status: partial
model_refs:
  - library:google:brotli@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-brotli
  - library:curl:curl@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:google:brotli-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Brotli (UCRT64)

## Purpose

This page documents the **UCRT64-environment** Brotli package
specifically — Google's general-purpose compression library — depended
on by [curl (UCRT64)](CURL-UCRT64.md) to back HTTP
`Content-Encoding: br` compressed response support, closing one of the
sub-dependencies that page's own Dependencies section had left
explicitly unmodeled. See the
[official Brotli project page](https://github.com/google/brotli) for
the full reference.

## Architectural Classification

`library:google:brotli@ucrt64` is packaged in the UCRT64 environment as
`package:msys2:mingw-w64-ucrt-x86_64-brotli` (version `1.2.0-1` in the
current catalog snapshot, license `MIT`, matching
[Brotli (MSYS)'s](BROTLI.md#architectural-classification) own recorded
version) — a separately built, separate catalog entity from
[Brotli (MSYS)](BROTLI.md)'s `brotli` package. This is the package
[curl (UCRT64)](CURL-UCRT64.md) — a UCRT64-native component itself —
actually depends on.

## Responsibilities

- Providing Brotli compression and decompression, consumed by
  [curl (UCRT64)](CURL-UCRT64.md) to transparently decompress HTTP
  responses sent with `Content-Encoding: br`, the same functional role
  [Brotli (MSYS)](BROTLI.md#responsibilities) documents for libcurl.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[libcurl (MSYS)](LIBCURL.md) instead depends on
[Brotli (MSYS)](BROTLI.md#reverse-dependencies) — the two are not
interchangeable, matching the same distinction already made throughout
this volume for MSYS/UCRT64 sibling pairs.

## Interfaces

- A C API (`BrotliDecoderDecompress`, `BrotliEncoderCompress`, and
  streaming variants) for Brotli compression and decompression, the
  same interface [Brotli (MSYS)](BROTLI.md#interfaces) documents, per
  the documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-brotli` declares no
`runtime-depends-on` edges beyond standard toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 20 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-brotli`. Two are now modeled in
this knowledge base: [curl (UCRT64)](CURL-UCRT64.md)
(`relationship:foundation-libraries:curl-ucrt64-requires-brotli-ucrt64`)
and [GnuTLS (UCRT64)](GNUTLS-UCRT64.md)
(`relationship:foundation-libraries:gnutls-ucrt64-requires-brotli-ucrt64`).
The remaining ~18 recorded dependents (a broad mix of UCRT64 packages
including `arrow`, `freetype`, `libheif`, `wget2`, and `wireshark`) are
not individually modeled in this knowledge base; see
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Brotli has no persistent configuration file; compression level and
parameters are set entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, Brotli has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [curl (UCRT64)](CURL-UCRT64.md) in this dependency chain.
As a native MinGW-w64 library, this process model is Windows-facing
directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [Brotli (MSYS)](BROTLI.md#runtime-behavior);
see that page for detail not specific to the UCRT64/MSYS packaging
distinction.

## Compatibility and Variants

The UCRT64 and MSYS Brotli packages are separately versioned catalog
entities (see Architectural Classification); code built against one is
not automatically compatible with the other without matching the
correct package/environment.

## Security Considerations

Decompressing untrusted Brotli-encoded HTTP response data is a
documented general source of decompression-related risk (such as
decompression-bomb resource exhaustion); this page does not assert this
specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `1.2.0-1` version.

## Failure Modes and Diagnostics

A curl transfer failing to decompress a `Content-Encoding: br` response
should be checked against the response's actual compression format
before being treated as a curl defect, the same triage order documented
for [Brotli (MSYS)](BROTLI.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

Brotli compression scope is backed by the official Brotli project page
(`evidence:google:brotli-manual-2026-07-30`), the same evidence record
[Brotli (MSYS)](BROTLI.md) cites. Package identity, version, license,
and the one modeled dependent edge are backed by the pacman catalog
snapshot (`evidence:catalog:current`). Open, and explicitly out of
scope for this page: the ~19 remaining recorded dependents not
individually modeled, and header-level API surface / PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [Brotli (MSYS)](BROTLI.md)
- [curl (UCRT64)](CURL-UCRT64.md)
- [GnuTLS (UCRT64)](GNUTLS-UCRT64.md)
