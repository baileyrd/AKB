---
id: doc:volume-6:p11-kit-ucrt64
title: p11-kit (UCRT64)
volume: 6
status: partial
model_refs:
  - library:p11-glue:p11-kit@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-p11-kit
  - library:mozilla:ca-certificates@ucrt64
  - library:gnutls:gnutls@ucrt64
  - library:gnu:libtasn1@ucrt64
  - library:libffi:libffi@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:p11-glue:p11-kit-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# p11-kit (UCRT64)

## Purpose

This page documents the **UCRT64-environment** p11-kit package
specifically — a PKCS#11 module discovery and coordination library —
depended on by [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
and [GnuTLS (UCRT64)](GNUTLS-UCRT64.md), closing two dependencies those
pages had left explicitly unmodeled. See the
[official p11-kit project page](https://p11-glue.github.io/p11-glue/p11-kit.html)
for the full reference.

## Architectural Classification

`library:p11-glue:p11-kit@ucrt64` is packaged in the UCRT64 environment
as `package:msys2:mingw-w64-ucrt-x86_64-p11-kit` (version `0.26.4-1`
in the current catalog snapshot, license `BSD-3-Clause`) — a
separately built, separate catalog entity from
[p11-kit (MSYS)](P11-KIT.md)'s `libp11-kit` package. This is the
package [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md) and
[GnuTLS (UCRT64)](GNUTLS-UCRT64.md) — both UCRT64-native library
entities themselves — actually depend on.

## Responsibilities

- Coordinating the discovery, configuration, and loading of PKCS#11
  cryptographic modules, consumed by
  [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#dependencies)
  and [GnuTLS (UCRT64)](GNUTLS-UCRT64.md#dependencies), the same
  functional role [p11-kit (MSYS)](P11-KIT.md#responsibilities)
  documents for GnuTLS (MSYS).

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[GnuTLS (MSYS)](GNUTLS.md) instead depends on
[p11-kit (MSYS)](P11-KIT.md#reverse-dependencies) — the two are not
interchangeable, matching the same distinction already made throughout
this volume for MSYS/UCRT64 sibling pairs. p11-kit coordinates PKCS#11
module discovery specifically; it does not itself implement TLS or
cryptographic algorithms — those remain the responsibility of its
dependents and of the PKCS#11 modules it loads on the caller's behalf.

## Interfaces

- A C API for PKCS#11 module discovery, loading, and coordination
  (`p11_kit_registered_modules` and related functions), the same
  interface [p11-kit (MSYS)](P11-KIT.md#interfaces) documents, per the
  documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-p11-kit` declares
dependencies on [GNU Libtasn1 (UCRT64)](GNU-LIBTASN1-UCRT64.md)
(ASN.1/DER parsing for certificates,
`relationship:foundation-libraries:p11-kit-ucrt64-requires-libtasn1-ucrt64`),
[libffi (UCRT64)](LIBFFI-UCRT64.md) (foreign function interface,
`relationship:foundation-libraries:p11-kit-ucrt64-requires-libffi-ucrt64`
— the third distinct libffi-named entity in this knowledge base), and
[GNU gettext](GNU-GETTEXT.md) (gettext-based message translation,
`relationship:foundation-libraries:p11-kit-ucrt64-requires-gettext`).

## Reverse Dependencies

The catalog snapshot records 4 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-p11-kit`. Two are now modeled in
this knowledge base:
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
(`relationship:foundation-libraries:ca-certificates-ucrt64-requires-p11-kit-ucrt64`,
correcting that page's own prior explicitly-unmodeled note) and
[GnuTLS (UCRT64)](GNUTLS-UCRT64.md)
(`relationship:foundation-libraries:gnutls-ucrt64-requires-p11-kit-ucrt64`).
The remaining recorded dependents (`qemu` and `qemu-image-util`) are
not individually modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

p11-kit reads a system-wide module configuration directory
(conventionally listing which PKCS#11 modules to load), the same
convention documented for [p11-kit (MSYS)](P11-KIT.md#configuration).

## Initialization and Execution Flow

As a library, p11-kit has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md) or
[GnuTLS (UCRT64)](GNUTLS-UCRT64.md) in this dependency chain. As a
native MinGW-w64 library, this process model is Windows-facing directly
rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[p11-kit (MSYS)](P11-KIT.md#runtime-behavior); see that page for
detail not specific to the UCRT64/MSYS packaging distinction.

## Compatibility and Variants

The UCRT64 and MSYS p11-kit packages are separately versioned catalog
entities (see Architectural Classification); code built against one is
not automatically compatible with the other without matching the
correct package/environment.

## Security Considerations

p11-kit mediates loading of dynamically-selected PKCS#11 cryptographic
modules, a security-sensitive role by nature; this page does not
assert this specific package version's robustness. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `0.26.4-1` version.

## Failure Modes and Diagnostics

A ca-certificates (UCRT64) or GnuTLS (UCRT64) failure to locate or load
a PKCS#11 module should be checked against p11-kit's own module
configuration before being treated as a defect in the calling program.

## Evidence, Assumptions, and Open Questions

PKCS#11 coordination scope is backed by the official p11-kit project
page (`evidence:p11-glue:p11-kit-manual-2026-07-30`), the same evidence
record [p11-kit (MSYS)](P11-KIT.md) cites. Package identity, version,
license, and the recorded dependency/dependent edges are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: the remaining recorded
dependents not individually modeled, and header-level API surface / PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [p11-kit (MSYS)](P11-KIT.md)
- [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
- [GnuTLS (UCRT64)](GNUTLS-UCRT64.md)
- [GNU Libtasn1 (UCRT64)](GNU-LIBTASN1-UCRT64.md)
- [libffi (UCRT64)](LIBFFI-UCRT64.md)
- [p11-kit (CLANG64)](P11-KIT-CLANG64.md)
