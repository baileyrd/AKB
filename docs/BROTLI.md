---
id: doc:volume-6:brotli
title: Brotli
volume: 6
status: partial
model_refs:
  - library:google:brotli
  - package:msys2:brotli
  - library:curl:libcurl
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:google:brotli-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Brotli

## Purpose

Brotli is a general-purpose compression algorithm and library developed
by Google. This page documents its architectural role as a
directly-declared dependency of [libcurl](LIBCURL.md), which uses it to
back HTTP `Content-Encoding: br` compressed response support, already
noted as an unmodeled sub-dependency on
[LIBCURL.md](LIBCURL.md#dependencies) before this page existed. See the
[official Brotli project page](https://github.com/google/brotli) for
the full reference.

## Architectural Classification

`library:google:brotli` is packaged in the MSYS environment as
`package:msys2:brotli` (version `1.2.0-1` in the current catalog
snapshot). This is the package [libcurl](LIBCURL.md#dependencies)
actually depends on for Brotli-encoded HTTP response decompression.

## Responsibilities

- Providing Brotli compression and decompression, consumed by
  [libcurl](LIBCURL.md) to transparently decompress HTTP responses sent
  with `Content-Encoding: br`.

## Boundaries

Brotli provides one of several compression algorithms
[libcurl](LIBCURL.md) supports for HTTP response decompression,
alongside DEFLATE (via [zlib (MSYS)](ZLIB-MSYS.md)) and Zstandard (via
[Zstandard (MSYS library)](LIBZSTD-MSYS.md)) — each a separate
algorithm and dependency, not interchangeable implementations of the
same format.

## Interfaces

- A C API (`BrotliDecoderDecompress`, `BrotliEncoderCompress`, and
  streaming variants) for Brotli compression and decompression, per the
  documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:brotli` beyond standard MSYS runtime support.

## Reverse Dependencies

The catalog snapshot records 2 relationships targeting
`package:msys2:brotli`: its own `-devel` subpackage and
`package:msys2:libcurl`
(`relationship:foundation-libraries:libcurl-requires-brotli` in this
knowledge base's graph) — its sole functional dependent in this
snapshot.

## Configuration

Brotli has no persistent configuration file; compression level and
parameters are set entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, Brotli has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [libcurl](LIBCURL.md) in this dependency chain. As an
MSYS-dependent library, this is adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Brotli decompression is exercised only when a server responds with
`Content-Encoding: br`, one of several compression formats libcurl
negotiates support for; not every HTTP transfer exercises this
dependency.

## Compatibility and Variants

Whether other native environments (UCRT64, CLANG64, i686) in this
catalog package Brotli separately was not confirmed while writing this
page; this is recorded as an open item rather than assumed either way.

## Security Considerations

Decompressing untrusted Brotli-encoded HTTP response data is a
documented general source of decompression-related risk (such as
decompression-bomb resource exhaustion); this page does not assert this
specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.2.0-1` version.

## Failure Modes and Diagnostics

A curl transfer failing to decompress a `Content-Encoding: br` response
should be checked against the response's actual compression format
before being treated as a curl or libcurl defect.

## Evidence, Assumptions, and Open Questions

Brotli compression scope is backed by the official Brotli project page
(`evidence:google:brotli-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:brotli` in the catalog. Package
identity, version, and the modeled dependent edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open: whether
other native environments package Brotli separately was not confirmed.
Also explicitly out of scope for this page: header-level API surface
and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libcurl](LIBCURL.md)
- [zlib (MSYS)](ZLIB-MSYS.md)
- [Zstandard (MSYS library)](LIBZSTD-MSYS.md)
