---
id: doc:volume-6:openssl-ucrt64
title: OpenSSL (UCRT64)
volume: 6
status: partial
model_refs:
  - library:openssl:openssl@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-openssl
  - library:curl:curl@ucrt64
  - library:libssh2:libssh2@ucrt64
  - library:mozilla:ca-certificates@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:openssl:project-site-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# OpenSSL (UCRT64)

## Purpose

This page documents the **UCRT64-environment** OpenSSL package
specifically — a TLS/SSL toolkit bundling both CLI and library in one
package, unlike the MSYS package's CLI/library split — depended on by
[curl (UCRT64)](CURL-UCRT64.md) for HTTPS/TLS support, closing one of
the ten sub-dependencies that page's own Dependencies section had left
explicitly unmodeled. With 124 recorded catalog dependents, it has the
widest reverse-dependency footprint of any library added in this
batch. See the
[official OpenSSL project site](https://openssl-library.org) for the
API and command-line reference.

## Architectural Classification

`library:openssl:openssl@ucrt64` is packaged in the UCRT64 environment
as `package:msys2:mingw-w64-ucrt-x86_64-openssl` (version `3.6.3-1` in
the current catalog snapshot, license `Apache-2.0`, matching both
[openssl (MSYS)'s](OPENSSL.md#architectural-classification) and
[libopenssl (MSYS)'s](LIBOPENSSL.md#architectural-classification) own
recorded license and version) — a separately built, separate catalog
entity from both [openssl (MSYS)](OPENSSL.md)'s `openssl` package and
[libopenssl (MSYS)](LIBOPENSSL.md)'s `libopenssl` package. Unlike the
MSYS environment's CLI/library split (`openssl` links against
`libopenssl`), this UCRT64 package bundles both the CLI tool and its
library together in one package, the same non-split pattern documented
for [curl (UCRT64)](CURL-UCRT64.md#architectural-classification).

## Responsibilities

- Providing TLS/SSL protocol implementations and general-purpose
  cryptographic primitives as both a linked library and a CLI tool,
  consumed by [curl (UCRT64)](CURL-UCRT64.md#dependencies) for
  HTTPS/TLS support.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[GnuPG](GNUPG.md), [OpenSSH](OPENSSH.md), and the general
MSYS-environment `curl` CLI instead depend on the MSYS-packaged
[openssl](OPENSSL.md#reverse-dependencies) and
[libopenssl](LIBOPENSSL.md#reverse-dependencies) packages — the two are
not interchangeable, matching the same distinction already made
throughout this volume for MSYS/UCRT64/CLANG64 sibling groups.

## Interfaces

- The OpenSSL `libssl`/`libcrypto` C API and CLI (TLS/SSL protocol
  functions plus general-purpose hashing, symmetric, and asymmetric
  cryptography primitives), identical to the API surface documented on
  [openssl (MSYS)](OPENSSL.md#interfaces) and
  [libopenssl (MSYS)](LIBOPENSSL.md#interfaces), per the documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-openssl` declares no
`runtime-depends-on` edges beyond standard toolchain runtime support;
it records only an *optional* dependency on
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
(`mingw-w64-ucrt-x86_64-ca-certificates`), which this page does not
promote to a formal graph edge, the same treatment optional
dependencies receive elsewhere in this volume (for example,
[CMake's](CMAKE.md#dependencies) own optional `emacs` dependency).

## Reverse Dependencies

The catalog snapshot records 124 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-openssl` — the widest
reverse-dependency footprint of any library added this session. Three
are now modeled in this knowledge base: [curl (UCRT64)](CURL-UCRT64.md)
(`relationship:foundation-libraries:curl-ucrt64-requires-openssl-ucrt64`),
[libssh2 (UCRT64)](LIBSSH2-UCRT64.md)
(`relationship:foundation-libraries:libssh2-ucrt64-requires-openssl-ucrt64`),
and [libarchive](LIBARCHIVE.md)
(`relationship:toolchain:libarchive-requires-openssl-ucrt64`). The
remaining ~121 recorded dependents (a broad mix of UCRT64 packages
including `arrow`, `cyrus-sasl`, `freerdp`, `git` (a separate
UCRT64-native git package, distinct from this knowledge base's MSYS
[Git](GIT-MSYS-PACKAGE.md) entity), and `python`) are not individually
modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

OpenSSL has no persistent configuration file as a library beyond the
system-wide `openssl.cnf` convention its consuming programs may read;
identical to [libopenssl (MSYS)](LIBOPENSSL.md#configuration) in this
respect.

## Initialization and Execution Flow

The CLI is an invoke-run-exit process; the library has no independent
process lifecycle and instead initializes and executes within the
process of whatever program links against it — [curl (UCRT64)](CURL-UCRT64.md)
in this dependency chain. As a native MinGW-w64 package, this process
model is Windows-facing directly rather than mediated by
`msys-2.0.dll`.

## Runtime Behavior

TLS/SSL handshake and cryptographic-primitive behavior is identical to
that documented for [libopenssl (MSYS)](LIBOPENSSL.md#runtime-behavior);
this page does not restate protocol-level detail not specific to the
UCRT64/MSYS packaging distinction.

## Compatibility and Variants

The UCRT64 and MSYS OpenSSL packages are separately versioned catalog
entities (see Architectural Classification); code built against one is
not automatically compatible with the other without matching the
correct package/environment. **Correction, 2026-07-30**: this closes
an open item [libopenssl's](LIBOPENSSL.md#compatibility-and-variants)
own page had left explicitly unconfirmed ("No separate native
(UCRT64/CLANG64/i686) `libopenssl` package was found in this catalog
snapshot") — no separate *split* `libopenssl`-named package exists for
UCRT64, but this bundled `openssl` package is its functional
counterpart.

## Security Considerations

OpenSSL is a security-critical library by definition, with an
extensive public CVE history; this page does not assert this specific
package version's patch status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `3.6.3-1` version.

## Failure Modes and Diagnostics

A TLS handshake failure in any consuming program should be checked
against OpenSSL's own error-queue diagnostics (`ERR_get_error` and
related functions) before being treated as a defect in the calling
program, the same triage order documented for
[libopenssl (MSYS)](LIBOPENSSL.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

TLS/SSL protocol and cryptographic-primitives scope is backed by the
official OpenSSL project site (`evidence:openssl:project-site-2026-07-30`),
the same evidence record [openssl (MSYS)](OPENSSL.md) and
[libopenssl (MSYS)](LIBOPENSSL.md) cite, matching the `project_url`
already recorded for `package:msys2:mingw-w64-ucrt-x86_64-openssl` in
the catalog. Package identity, version, license, and the one modeled
dependent edge are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Open, and explicitly out of scope for
this page: the ~123 remaining recorded dependents not individually
modeled, and header-level API surface / PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [OpenSSL (MSYS)](OPENSSL.md)
- [libopenssl (MSYS)](LIBOPENSSL.md)
- [curl (UCRT64)](CURL-UCRT64.md)
- [libssh2 (UCRT64)](LIBSSH2-UCRT64.md)
- [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
- [libarchive](LIBARCHIVE.md)
- [OpenSSL (CLANG64)](OPENSSL-CLANG64.md)
