---
id: doc:volume-6:rhash
title: RHash
volume: 6
status: partial
model_refs:
  - library:rhash:rhash
  - package:msys2:mingw-w64-ucrt-x86_64-rhash
  - component:cmake:cmake
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:rhash:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# RHash

## Purpose

RHash is a library and command-line utility for computing hash sums
across many algorithms (MD5, SHA-family, CRC32, and others). This page
documents its architectural role as a directly-declared dependency of
[CMake](CMAKE.md), which uses it to implement its `file(MD5)`/`file(SHA256)`-style
hashing commands; see the
[official RHash project page](https://sourceforge.net/projects/rhash/)
for the full reference.

## Architectural Classification

`library:rhash:rhash` is packaged per native environment: this page
cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-rhash` (version `1.4.6-1` in the
current catalog snapshot). It belongs to the UCRT64 environment and, like
[CMake](CMAKE.md#architectural-classification) itself and the rest of
Volume 8's toolchain components, does not depend on `msys-2.0.dll`, per
the [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).
RHash also ships a standalone `rhash` command-line utility upstream,
though this page and the CMake dependency it documents concern the
library form specifically.

## Responsibilities

- Computing hash sums across multiple algorithms, consumed by
  [CMake](CMAKE.md)'s `file(MD5)`, `file(SHA256)`, and related
  `file()` hashing subcommands.

## Boundaries

RHash provides multi-algorithm hash computation specifically; it is not a
cryptographic library in the broader sense (no encryption, no key
management) — its role in CMake is limited to the `file()` command's
hashing subcommands, distinct from the actual TLS/cryptographic
dependencies documented elsewhere in this knowledge base ([OpenSSL](OPENSSL.md),
[GnuTLS](GNUTLS.md)). RHash already appeared by package name in
[CMake's dependency table](CMAKE.md#dependencies) before this page
existed.

## Interfaces

- A C API (`rhash_library_init`, `rhash_init`, `rhash_update`,
  `rhash_final`) for computing one or more hash algorithms over a data
  stream, per the documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-rhash` declares a
dependency on `mingw-w64-ucrt-x86_64-gettext-runtime` (gettext-based
message translation runtime, not yet given its own page in this volume).

## Reverse Dependencies

The catalog snapshot records 1 relationship targeting
`package:msys2:mingw-w64-ucrt-x86_64-rhash`:
`package:msys2:mingw-w64-ucrt-x86_64-cmake`
(`relationship:toolchain:cmake-requires-rhash` in this knowledge base's
graph) — the narrowest reverse-dependency footprint of any library added
in this batch alongside [cppdap](CPPDAP.md), reflecting file-hashing
support as a comparatively narrow CMake feature relative to its other
dependencies.

## Configuration

RHash has no persistent configuration file of its own when used as a
library; algorithm selection is controlled entirely through its C API by
the calling program.

## Initialization and Execution Flow

As a library, RHash has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it —
[CMake](CMAKE.md) in this dependency chain, specifically during
`file(MD5)`/`file(SHA256)`-style command execution. As a native
MinGW-w64 library, this process model is Windows-facing directly rather
than mediated by `msys-2.0.dll`.

## Runtime Behavior

RHash's hashing role is exercised only when a CMake script explicitly
invokes a `file()` hashing subcommand; it plays no role in an ordinary
build's compile/link steps.

## Compatibility and Variants

Whether other native environments (CLANG64, i686) in this catalog package
RHash separately was not confirmed while writing this page; this is
recorded as an open item rather than assumed either way.

## Security Considerations

`file(MD5)` specifically exposes a cryptographically broken hash
algorithm through CMake's own command surface; whether a given CMake
script uses MD5 versus a stronger algorithm (SHA-256 and others RHash
also supports) is the calling script's choice, not something this page
characterizes. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.4.6-1` version.

## Failure Modes and Diagnostics

A `file(MD5)`/`file(SHA256)`-style command failing to produce a hash most
commonly indicates the target file could not be read, rather than an
RHash-specific defect.

## Evidence, Assumptions, and Open Questions

Multi-algorithm hash computation scope is backed by the official RHash
project page (`evidence:rhash:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-rhash` in the catalog. Package
identity, version, and the recorded dependency/dependent edges are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open:
whether other native environments package RHash separately was not
confirmed. Also explicitly out of scope for this page: the
`gettext-runtime` sub-dependency is not individually modeled as a
component in this knowledge base; header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology, also remain open.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [CMake](CMAKE.md)
- [cppdap](CPPDAP.md)
