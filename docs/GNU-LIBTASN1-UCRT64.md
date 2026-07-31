---
id: doc:volume-6:gnu-libtasn1-ucrt64
title: GNU Libtasn1 (UCRT64)
volume: 6
status: partial
model_refs:
  - library:gnu:libtasn1@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-libtasn1
  - library:gnutls:gnutls@ucrt64
  - library:p11-glue:p11-kit@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnu:libtasn1-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GNU Libtasn1 (UCRT64)

## Purpose

This page documents the **UCRT64-environment** libtasn1 package
specifically — an ASN.1 structure parser and DER encoder library —
depended on by [GnuTLS (UCRT64)](GNUTLS-UCRT64.md) and
[p11-kit (UCRT64)](P11-KIT-UCRT64.md) for certificate parsing. See the
[official GNU Libtasn1 project page](https://www.gnu.org/software/libtasn1/)
for the full reference.

## Architectural Classification

`library:gnu:libtasn1@ucrt64` is packaged in the UCRT64 environment as
`package:msys2:mingw-w64-ucrt-x86_64-libtasn1` (version `4.21.0-1` in
the current catalog snapshot, license `GPL3, LGPL`) — a separately
built, separate catalog entity from
[GNU Libtasn1 (MSYS)](GNU-LIBTASN1.md)'s `libtasn1` package. This is
the package [GnuTLS (UCRT64)](GNUTLS-UCRT64.md) and
[p11-kit (UCRT64)](P11-KIT-UCRT64.md) — both UCRT64-native library
entities themselves — actually depend on.

## Responsibilities

- Providing ASN.1 structure parsing and DER encoding, consumed by
  [GnuTLS (UCRT64)](GNUTLS-UCRT64.md#dependencies) for certificate
  parsing and by [p11-kit (UCRT64)](P11-KIT-UCRT64.md#dependencies) for
  the same purpose.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[GnuTLS (MSYS)](GNUTLS.md) and [p11-kit (MSYS)](P11-KIT.md) instead
depend on [GNU Libtasn1 (MSYS)](GNU-LIBTASN1.md#reverse-dependencies)
— the two are not interchangeable, matching the same distinction
already made throughout this volume for MSYS/UCRT64 sibling pairs.

## Interfaces

- The libtasn1 C API (`asn1_parser2tree`, `asn1_der_decoding`, and
  related functions), the same interface
  [GNU Libtasn1 (MSYS)](GNU-LIBTASN1.md#interfaces) documents, per the
  documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-libtasn1` declares no
`runtime-depends-on` edges beyond standard toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 7 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libtasn1`. Two are now modeled in
this knowledge base: [GnuTLS (UCRT64)](GNUTLS-UCRT64.md)
(`relationship:foundation-libraries:gnutls-ucrt64-requires-libtasn1-ucrt64`)
and [p11-kit (UCRT64)](P11-KIT-UCRT64.md)
(`relationship:foundation-libraries:p11-kit-ucrt64-requires-libtasn1-ucrt64`).
The remaining recorded dependents (`libdsm`, `libmicrodns`, `qemu`,
`qemu-image-util`, and `shishi`) are not individually modeled in this
knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libtasn1 has no persistent configuration file; behavior is controlled
entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libtasn1 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [GnuTLS (UCRT64)](GNUTLS-UCRT64.md) or
[p11-kit (UCRT64)](P11-KIT-UCRT64.md) in this dependency chain. As a
native MinGW-w64 library, this process model is Windows-facing directly
rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[GNU Libtasn1 (MSYS)](GNU-LIBTASN1.md#runtime-behavior); see that page
for detail not specific to the UCRT64/MSYS packaging distinction.

## Compatibility and Variants

The UCRT64 and MSYS libtasn1 packages are separately versioned catalog
entities (see Architectural Classification); code built against one is
not automatically compatible with the other without matching the
correct package/environment.

## Security Considerations

ASN.1/DER parsing against untrusted certificate data is a documented
general source of parser vulnerabilities; this page does not assert
this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `4.21.0-1` version.

## Failure Modes and Diagnostics

A GnuTLS (UCRT64) or p11-kit (UCRT64) certificate-parsing failure
should be checked against the certificate's actual ASN.1/DER encoding
before being treated as a libtasn1 defect.

## Evidence, Assumptions, and Open Questions

ASN.1/DER parsing scope is backed by the official GNU Libtasn1 project
page (`evidence:gnu:libtasn1-manual-2026-07-30`), the same evidence
record [GNU Libtasn1 (MSYS)](GNU-LIBTASN1.md) cites. Package identity,
version, license, and the two modeled dependent edges are backed by
the pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: the remaining recorded
dependents not individually modeled, and header-level API surface / PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU Libtasn1 (MSYS)](GNU-LIBTASN1.md)
- [GnuTLS (UCRT64)](GNUTLS-UCRT64.md)
- [p11-kit (UCRT64)](P11-KIT-UCRT64.md)
