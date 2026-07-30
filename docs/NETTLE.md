---
id: doc:volume-6:nettle
title: Nettle
volume: 6
status: partial
model_refs:
  - library:nettle:nettle
  - package:msys2:mingw-w64-ucrt-x86_64-nettle
  - library:gnu:gmp
  - component:gnupg:gnupg
  - component:gnu:emacs
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:nettle:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Nettle

## Purpose

Nettle is a low-level cryptographic library, and it already appears twice
elsewhere in this knowledge base as a dependency: for
[GnuPG](GNUPG.md#dependencies)'s `dirmngr` TLS connections (via GnuTLS)
and for [GNU Emacs](GNU-EMACS.md#dependencies)'s Network Security
Manager. This page documents its architectural role; see the
[official Nettle project site](https://www.lysator.liu.se/~nisse/nettle)
for the API reference.

## Architectural Classification

`library:nettle:nettle` is packaged per native environment: this page
cites the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-nettle`
(version `4.0-1` in the current catalog snapshot, license
`GPL-2.0-or-later;LGPL-3.0-or-later`), authored by Niels Möller.

## Responsibilities

- Providing low-level cryptographic primitives (block ciphers, hash
  functions, public-key algorithms) designed to be used as a backend by
  higher-level libraries such as GnuTLS, rather than typically consumed
  directly by application code.

## Boundaries

Nettle provides cryptographic primitives at a lower level than
[libgcrypt](LIBGCRYPT.md); both exist in this environment for different
consumers ([GnuPG](GNUPG.md) itself uses libgcrypt directly and Nettle
transitively via GnuTLS for `dirmngr`), and this page does not claim they
are interchangeable or that one supersedes the other.

## Interfaces

- A C API organized around individual cryptographic primitives (AES,
  SHA-family hashes, RSA), deliberately low-level and without the
  higher-level protocol logic (such as TLS handshaking) that a library
  like GnuTLS builds on top of it, per the documentation.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-nettle`:
`mingw-w64-ucrt-x86_64-cc-libs` (low-level compiler runtime support) and
`mingw-w64-ucrt-x86_64-gmp` (arbitrary-precision arithmetic for
public-key algorithms, documented fully in [GNU MP](GNU-GMP.md)).

## Reverse Dependencies

The snapshot records 10 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-nettle`, including
[GnuPG](GNUPG.md#dependencies) itself
(`relationship:ssh-curl-git:gnupg-requires-nettle`) and, transitively,
[GNU Emacs](GNU-EMACS.md#dependencies) via GnuTLS. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Nettle has no persistent configuration file; algorithm selection is made
through its C API at the point of use.

## Initialization and Execution Flow

As a library, Nettle has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it
(directly or transitively through GnuTLS), the same general
library-linkage model documented for
[GNU MP](GNU-GMP.md#initialization-and-execution-flow).

## Runtime Behavior

Nettle's primitives are exercised whenever a consumer (directly, or
transitively via GnuTLS) performs a cryptographic operation; this page
does not characterize specific algorithm performance.

## Compatibility and Variants

Nettle's API has evolved across major versions with documented
compatibility notes in its own release history; this page does not
enumerate them.

## Security Considerations

As a cryptographic primitives library consumed transitively by both
[GnuPG](GNUPG.md) and [GNU Emacs](GNU-EMACS.md)'s network security
features, Nettle sits in a security-relevant position in this
environment's dependency graph. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `4.0-1` version.

## Failure Modes and Diagnostics

Nettle itself has no user-facing CLI; cryptographic-operation failures in
a dependent (directly or via GnuTLS) should be triaged against that
dependent's own documentation and, where applicable, GnuTLS's
intermediary role before assuming a Nettle defect.

## Evidence, Assumptions, and Open Questions

The low-level cryptographic-primitives role is backed by the official
Nettle project site (`evidence:nettle:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-nettle` in the catalog. Package
identity, version, license, and the GMP dependency edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU MP (GMP)](GNU-GMP.md)
- [GnuPG](GNUPG.md)
- [GNU Emacs](GNU-EMACS.md)
