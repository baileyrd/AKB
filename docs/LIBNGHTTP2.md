---
id: doc:volume-6:libnghttp2
title: libnghttp2
volume: 6
status: partial
model_refs:
  - library:nghttp2:libnghttp2
  - package:msys2:libnghttp2
  - component:curl:curl
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:nghttp2:libnghttp2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libnghttp2

## Purpose

libnghttp2 implements the framing layer of HTTP/2 as a reusable C
library, providing the protocol machinery that lets a client like curl
negotiate and speak HTTP/2 rather than only HTTP/1.1. This page documents
its architectural role as a directly-declared dependency of
[curl](CURL.md); see the
[official nghttp2 project site](https://nghttp2.org/) for the full API
reference.

## Architectural Classification

`library:nghttp2:libnghttp2` is packaged in the MSYS environment as
`package:msys2:libnghttp2` (version `1.69.0-1` in the current catalog
snapshot). A separately packaged, native (UCRT64/CLANG64/i686)
`libnghttp2` also exists in the catalog; this page documents the MSYS
package specifically, since that is the one
[curl](CURL.md#dependencies) actually depends on — the same
MSYS-vs-native distinction applied consistently across this batch's
sibling pages, [libnghttp3](LIBNGHTTP3.md) and [libngtcp2](LIBNGTCP2.md).
The nghttp2 project also separately packages an `nghttp2` command-line
tool suite (`package:msys2:nghttp2`), distinct from this runtime library
package.

## Responsibilities

- Implementing the HTTP/2 framing layer (stream multiplexing, header
  compression via HPACK, flow control) as a reusable library, consumed by
  [curl](CURL.md) to negotiate and speak HTTP/2.

## Boundaries

libnghttp2 provides the HTTP/2 protocol layer specifically; it does not
implement HTTP/3 or QUIC — those are provided by the related but separate
[libnghttp3](LIBNGHTTP3.md) and [libngtcp2](LIBNGTCP2.md) libraries from
the same upstream project, each packaged and versioned independently.
libnghttp2 already appeared by package name in
[curl's dependency table](CURL.md#dependencies) before this page existed.

## Interfaces

- A C API for HTTP/2 session, stream, and frame handling, per the
  documentation.

## Dependencies

The MSYS `package:msys2:libnghttp2` declares a dependency on `gcc-libs`
only — the GCC runtime support libraries, not a library-family dependency
distinct enough to warrant its own page in this volume.

## Reverse Dependencies

The catalog snapshot records 4 relationships targeting
`package:msys2:libnghttp2`: `package:msys2:curl`
(`relationship:ssh-curl-git:curl-requires-libnghttp2` in this knowledge
base's graph, a direct dependency of the CLI package itself, not merely of
`libcurl`), `package:msys2:libcurl`, its own `-devel` subpackage, and the
separate `package:msys2:nghttp2` command-line tool suite.

## Configuration

libnghttp2 has no persistent configuration file of its own; HTTP/2
session parameters are controlled entirely through its C API by the
calling program.

## Initialization and Execution Flow

As a library, libnghttp2 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [curl](CURL.md) in this dependency chain. As an
MSYS-dependent library, this is adapted from POSIX semantics onto Windows
process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Whether a given curl invocation actually negotiates HTTP/2 or falls back
to HTTP/1.1 depends on server-side protocol negotiation (ALPN), not solely
on this library's presence, already noted as a general point on
[curl's own page](CURL.md#runtime-behavior).

## Compatibility and Variants

The MSYS and native (UCRT64/CLANG64/i686) libnghttp2 packages are
separately versioned catalog entities (see Architectural Classification);
code built against one is not automatically compatible with the other
without matching the correct environment.

## Security Considerations

HTTP/2 implementations have historically been subject to protocol-level
denial-of-service classes (such as header-compression or
stream-multiplexing abuse); this page does not assert this specific
package version's exposure or mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.69.0-1` version.

## Failure Modes and Diagnostics

An HTTP/2-specific connection failure (as opposed to a general network
failure) should be checked with curl's `-v`/`--trace` diagnostic flags,
already documented on [curl's own page](CURL.md#failure-modes-and-diagnostics),
before being treated as a libnghttp2 defect.

## Evidence, Assumptions, and Open Questions

HTTP/2 framing-layer implementation scope is backed by the official
nghttp2 project site (`evidence:nghttp2:libnghttp2-manual-2026-07-30`),
matching the `project_url` already recorded for
`package:msys2:libnghttp2` in the catalog. Package identity, version, and
the recorded dependency/dependent edges are backed by the pacman catalog
snapshot (`evidence:catalog:current`). Open, and explicitly out of scope
for this page: header-level API surface and PE import/export-level
evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology, remain open.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [curl](CURL.md)
- [libnghttp3](LIBNGHTTP3.md)
- [libngtcp2](LIBNGTCP2.md)
- [libnghttp2 (UCRT64)](LIBNGHTTP2-UCRT64.md)
