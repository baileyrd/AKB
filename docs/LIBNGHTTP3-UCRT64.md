---
id: doc:volume-6:libnghttp3-ucrt64
title: libnghttp3 (UCRT64)
volume: 6
status: partial
model_refs:
  - library:nghttp2:libnghttp3@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-nghttp3
  - library:curl:curl@ucrt64
  - library:nghttp2:libngtcp2@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:nghttp2:libnghttp3-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libnghttp3 (UCRT64)

## Purpose

This page documents the **UCRT64-environment** libnghttp3 package
specifically — an HTTP/3 protocol library — depended on by
[curl (UCRT64)](CURL-UCRT64.md) for HTTP/3 protocol support alongside
[libngtcp2 (UCRT64)'s](LIBNGTCP2-UCRT64.md) QUIC transport, closing the
last of the sub-dependencies that page's own Dependencies section had
left explicitly unmodeled — completing full coverage of all twelve of
curl (UCRT64)'s declared dependencies. See the
[official nghttp3 project page](https://nghttp2.org/nghttp3) for the
full reference.

## Architectural Classification

`library:nghttp2:libnghttp3@ucrt64` is packaged in the UCRT64
environment as `package:msys2:mingw-w64-ucrt-x86_64-nghttp3` (version
`1.17.0-1` in the current catalog snapshot, license `MIT`) — a
separately built, separate catalog entity from
[libnghttp3 (MSYS)](LIBNGHTTP3.md)'s `libnghttp3` package. This is the
package [curl (UCRT64)](CURL-UCRT64.md) — a UCRT64-native component
itself — actually depends on.

## Responsibilities

- Providing the HTTP/3 protocol implementation, consumed by
  [curl (UCRT64)](CURL-UCRT64.md#dependencies) alongside
  [libngtcp2 (UCRT64)'s](LIBNGTCP2-UCRT64.md) QUIC transport to serve
  complete HTTP/3 support.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[curl (MSYS)](CURL.md) and [libcurl (MSYS)](LIBCURL.md) instead depend
on [libnghttp3 (MSYS)](LIBNGHTTP3.md#reverse-dependencies) — the two
are not interchangeable, matching the same distinction already made
throughout this volume for MSYS/UCRT64 sibling pairs. libnghttp3
implements the HTTP/3 application layer specifically; QUIC's own
transport layer remains [libngtcp2 (UCRT64)'s](LIBNGTCP2-UCRT64.md)
responsibility, per the same layering
[libnghttp3 (MSYS)](LIBNGHTTP3.md#boundaries) documents.

## Interfaces

- A C API for HTTP/3 request/response framing, designed to be paired
  with a QUIC transport implementation, the same interface
  [libnghttp3 (MSYS)](LIBNGHTTP3.md#interfaces) documents, per the
  documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-nghttp3` declares no
`runtime-depends-on` edges beyond standard toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 3 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-nghttp3`. One is now modeled in
this knowledge base: [curl (UCRT64)](CURL-UCRT64.md)
(`relationship:foundation-libraries:curl-ucrt64-requires-libnghttp3-ucrt64`).
The remaining recorded dependents (`curl-gnutls` and `wireshark`) are
not individually modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libnghttp3 has no persistent configuration file; behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libnghttp3 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [curl (UCRT64)](CURL-UCRT64.md) in this dependency chain.
As a native MinGW-w64 library, this process model is Windows-facing
directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[libnghttp3 (MSYS)](LIBNGHTTP3.md#runtime-behavior); see that page for
detail not specific to the UCRT64/MSYS packaging distinction.

## Compatibility and Variants

The UCRT64 and MSYS libnghttp3 packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct package/environment.

## Security Considerations

HTTP/3 frame parsing against untrusted network input is a documented
general source of protocol-implementation risk; this page does not
assert this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `1.17.0-1` version.

## Failure Modes and Diagnostics

An HTTP/3-specific curl transfer failure should be checked with curl's
own verbose/trace diagnostics before being treated as a libnghttp3 or
libngtcp2 (UCRT64) defect, the same triage order documented for
[libnghttp3 (MSYS)](LIBNGHTTP3.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

HTTP/3 protocol implementation scope is backed by the official nghttp3
project page (`evidence:nghttp2:libnghttp3-manual-2026-07-30`), the
same evidence record [libnghttp3 (MSYS)](LIBNGHTTP3.md) cites. Package
identity, version, license, and the one modeled dependent edge are
backed by the pacman catalog snapshot (`evidence:catalog:current`).
Open, and explicitly out of scope for this page: the remaining
recorded dependents not individually modeled, and header-level API
surface / PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libnghttp3 (MSYS)](LIBNGHTTP3.md)
- [curl (UCRT64)](CURL-UCRT64.md)
- [libngtcp2 (UCRT64)](LIBNGTCP2-UCRT64.md)
- [libnghttp3 (CLANG64)](LIBNGHTTP3-CLANG64.md)
