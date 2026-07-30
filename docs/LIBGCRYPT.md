---
id: doc:volume-6:libgcrypt
title: libgcrypt
volume: 6
status: partial
model_refs:
  - library:gnupg:libgcrypt
  - package:msys2:mingw-w64-ucrt-x86_64-libgcrypt
  - library:gnupg:libgpg-error
  - component:gnupg:gnupg
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnupg:libgcrypt-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libgcrypt

## Purpose

Libgcrypt is GnuPG's own general-purpose cryptographic library, and it is
the primary low-level crypto library backing
[GnuPG](GNUPG.md#dependencies) itself, already cited on that page as
"GnuPG's primary cryptographic library, independent of OpenSSL's." This
page documents its architectural role; see the
[official libgcrypt project page](https://gnupg.org/software/libgcrypt/index.html)
for the API reference.

## Architectural Classification

`library:gnupg:libgcrypt` is packaged per native environment: this page
cites the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-libgcrypt`
(version `1.12.2-2` in the current catalog snapshot, license `LGPL`).

## Responsibilities

- Providing symmetric and public-key cryptographic primitives (cipher
  algorithms, hash functions, random-number generation) for
  [GnuPG](GNUPG.md) and other GnuPG-family software, deliberately
  independent of [OpenSSL](OPENSSL.md), per
  [GnuPG's own Architectural Classification](GNUPG.md#architectural-classification).

## Boundaries

Libgcrypt implements OpenPGP-relevant cryptographic primitives; it is not
a TLS/X.509 library the way [OpenSSL](OPENSSL.md) is — GnuPG's separate
`libgnutls` dependency (documented on [GnuPG's page](GNUPG.md#dependencies))
covers TLS-secured network connections for `dirmngr`, a distinct concern
from libgcrypt's cryptographic primitives.

## Interfaces

- A C API for symmetric ciphers, hash functions, MACs, public-key
  operations, and cryptographically secure random-number generation, per
  the documentation.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-libgcrypt`:
`mingw-w64-ucrt-x86_64-cc-libs` (low-level compiler runtime support) and
`mingw-w64-ucrt-x86_64-libgpg-error` (the shared error-code vocabulary
documented fully in [libgpg-error](LIBGPG-ERROR.md)).

## Reverse Dependencies

The snapshot records 19 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libgcrypt`, including
[GnuPG](GNUPG.md#dependencies) itself
(`relationship:ssh-curl-git:gnupg-requires-libgcrypt`). See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Libgcrypt has no persistent configuration file; algorithm and key-size
selection are made through its C API at the point of use by the calling
program.

## Initialization and Execution Flow

As a library, libgcrypt has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [GnuPG](GNUPG.md), for instance — the same model documented
for [libgpg-error](LIBGPG-ERROR.md#initialization-and-execution-flow).

## Runtime Behavior

Libgcrypt performs self-tests at initialization in FIPS-oriented
configurations, a documented general characteristic of GnuPG-family
cryptographic libraries; this page does not confirm whether this specific
build enables that mode.

## Compatibility and Variants

Libgcrypt's API has evolved across major versions with documented
deprecation cycles for older algorithms; this page does not enumerate
version-specific algorithm support, deferring to the project's own
documentation.

## Security Considerations

As GnuPG's primary cryptographic library, libgcrypt is itself
security-critical infrastructure; a defect here would directly affect
[GnuPG](GNUPG.md)'s encryption, decryption, and signing correctness. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.12.2-2` version — a priority
candidate for one given its role.

## Failure Modes and Diagnostics

Libgcrypt itself has no user-facing CLI; cryptographic operation failures
in [GnuPG](GNUPG.md) should be checked against libgcrypt's own
documented algorithm and key-size support before being treated as a
GnuPG-specific defect.

## Evidence, Assumptions, and Open Questions

The cryptographic-primitives role is backed by the official libgcrypt
project page (`evidence:gnupg:libgcrypt-manual-2026-07-30`). Package
identity, version, license, and the dependency edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: header-level API surface, PE
import/export-level evidence, and whether this build enables
FIPS-oriented self-tests, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libgpg-error](LIBGPG-ERROR.md)
- [GnuPG](GNUPG.md)
- [OpenSSL](OPENSSL.md)
