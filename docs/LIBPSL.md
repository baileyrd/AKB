---
id: doc:volume-6:libpsl
title: libpsl
volume: 6
status: partial
model_refs:
  - library:libpsl:libpsl
  - package:msys2:libpsl
  - component:curl:curl
  - library:gnu:libidn2
  - library:gnu:libunistring
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:libpsl:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libpsl

## Purpose

libpsl parses and evaluates domain names against Mozilla's Public Suffix
List — the data set of domain suffixes (such as `.com`, `.co.uk`) under
which independent parties can register names — which is what lets a
client correctly decide "is this a registrable domain, or a shared public
suffix" before scoping a cookie to it. This page documents its
architectural role as a directly-declared dependency of both
[curl](CURL.md) and its own `libcurl` transfer library; see the
[official libpsl project page](https://github.com/rockdaboot/libpsl) for
the full API reference.

## Architectural Classification

`library:libpsl:libpsl` is packaged in the MSYS environment as
`package:msys2:libpsl` (version `0.21.5-2` in the current catalog
snapshot). A separately packaged, native (UCRT64/CLANG64/i686) `libpsl`
also exists in the catalog; this page documents the MSYS package
specifically, since that is the one [curl](CURL.md#dependencies) actually
depends on — the same MSYS-vs-native distinction applied consistently to
[GnuTLS](GNUTLS.md#architectural-classification) and its own
sub-dependencies elsewhere in this volume.

## Responsibilities

- Parsing and matching domain names against the Public Suffix List, so
  that calling programs (curl among them) can correctly scope
  cookie-domain decisions and avoid setting cookies for overly broad
  public suffixes.

## Boundaries

libpsl provides Public Suffix List parsing and matching specifically; it
does not implement HTTP, cookie storage, or any other part of the transfer
stack — those remain [curl](CURL.md)'s and `libcurl`'s own responsibility.
libpsl already appeared by package name in
[curl's dependency table](CURL.md#dependencies) before this page existed.

## Interfaces

- A C API (`psl_is_public_suffix`, `psl_registrable_domain`, and related
  functions) for evaluating a domain name against the loaded Public
  Suffix List, per the documentation.

## Dependencies

The MSYS `package:msys2:libpsl` declares dependencies on
[libidn2](GNU-LIBIDN2.md) (internationalized domain name handling) and
[libunistring](GNU-LIBUNISTRING.md) (Unicode-aware string handling) — both
now separately documented in this volume, with explicit `requires` edges
from `library:libpsl:libpsl`
(`relationship:foundation-libraries:libpsl-requires-libidn2`,
`relationship:foundation-libraries:libpsl-requires-libunistring`).

## Reverse Dependencies

The catalog snapshot records 4 relationships targeting
`package:msys2:libpsl`: `package:msys2:curl`
(`relationship:ssh-curl-git:curl-requires-libpsl` in this knowledge base's
graph, a direct dependency of the CLI package itself, not merely of
`libcurl`), `package:msys2:libcurl`, its own `-devel` subpackage, and
`package:msys2:wget`.

## Configuration

libpsl has no persistent configuration file of its own; it loads the
Public Suffix List data either from a bundled copy or from ICU data
depending on build configuration, and is otherwise controlled entirely
through its C API by the calling program.

## Initialization and Execution Flow

As a library, libpsl has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it —
[curl](CURL.md) in this dependency chain. As an MSYS-dependent library,
this is adapted from POSIX semantics onto Windows process primitives by
`msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Whether a given domain name is correctly classified as a registrable
domain versus a public suffix depends on how current the linked Public
Suffix List data is relative to the live list maintained by Mozilla; this
page does not characterize the specific data snapshot bundled with this
package version.

## Compatibility and Variants

The MSYS and native (UCRT64/CLANG64/i686) libpsl packages are separately
versioned catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct environment.

## Security Considerations

libpsl's correct operation directly defends against a documented class of
cookie-scoping vulnerabilities (a stale or incorrect Public Suffix List
evaluation could let a cookie be set too broadly), already noted as a
security-relevant dependency on [curl's own page](CURL.md#security-considerations).
See [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `0.21.5-2` version.

## Failure Modes and Diagnostics

A cookie unexpectedly rejected or accepted across a domain boundary should
first be checked against libpsl's Public Suffix List evaluation for that
domain before being treated as a defect in the calling program.

## Evidence, Assumptions, and Open Questions

Public Suffix List parsing/matching scope is backed by the official
libpsl project page (`evidence:libpsl:manual-2026-07-30`), matching the
`project_url` already recorded for `package:msys2:libpsl` in the catalog.
Package identity, version, and the recorded dependency/dependent edges are
backed by the pacman catalog snapshot (`evidence:catalog:current`). Open,
and explicitly out of scope for this page: header-level API surface and
PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology, remain open.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [curl](CURL.md)
- [GNU libidn2](GNU-LIBIDN2.md)
- [GNU libunistring](GNU-LIBUNISTRING.md)
- [libpsl (UCRT64)](LIBPSL-UCRT64.md)
