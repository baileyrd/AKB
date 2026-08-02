---
id: doc:volume-6:ca-certificates-clang64
title: ca-certificates (CLANG64)
volume: 6
status: partial
model_refs:
  - library:mozilla:ca-certificates@clang64
  - package:msys2:mingw-w64-clang-x86_64-ca-certificates
  - library:p11-glue:p11-kit@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:mozilla:ca-certificates-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# ca-certificates (CLANG64)

## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-ca-certificates`,
the CLANG64-environment build of the ca-certificates bundle — a curated
set of common Certificate Authority root certificates. It is the last
page in a five-entity dependency chain modeled in this batch (this
page → [p11-kit (CLANG64)](P11-KIT-CLANG64.md) →
{[GNU gettext (CLANG64)](GNU-GETTEXT-CLANG64.md),
[libffi (CLANG64)](LIBFFI-CLANG64.md),
[GNU Libtasn1 (CLANG64)](GNU-LIBTASN1-CLANG64.md)} →
[GNU libiconv (CLANG64)](GNU-LIBICONV-CLANG64.md)). See the
[official Mozilla CA certificate policy page](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/)
for the source of this bundle.

## Architectural Classification

`library:mozilla:ca-certificates@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-ca-certificates` (version
`20250419-1` in the current catalog snapshot, license `MPL;GPL`) — a
separately built, separate catalog entity from
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md) and
[ca-certificates (MSYS)](CA-CERTIFICATES.md). It belongs to the
CLANG64 environment. Its sole recorded runtime dependency,
[p11-kit (CLANG64)](P11-KIT-CLANG64.md), was modeled earlier in this
same batch, letting this addition close its full dependency footprint
in a single pass.

## Responsibilities

- Providing a curated, regularly-updated bundle of trusted root CA
  certificates for CLANG64-native consumers, the same role
  [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#responsibilities)
  documents for its own environment.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[curl (UCRT64)](CURL-UCRT64.md) instead depends on
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#reverse-dependencies)
— the two are not interchangeable, matching the same distinction
already drawn throughout this volume for MSYS/UCRT64/CLANG64 sibling
packages.

## Interfaces

No programmatic API; ca-certificates provides a static certificate
bundle file that consuming TLS libraries read at runtime, the same
non-code interface documented for
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#interfaces).

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-clang-x86_64-ca-certificates`, now modeled in
this knowledge base:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| [p11-kit (CLANG64)](P11-KIT-CLANG64.md) | `package:msys2:mingw-w64-clang-x86_64-p11-kit` | Backs trust-anchor registration and coordination through the p11-kit PKCS#11 trust module. |

## Reverse Dependencies

The catalog snapshot records 12 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-ca-certificates`: `curl`,
`curl-gnutls`, `git` (a separate CLANG64-native git package, distinct
from this knowledge base's MSYS [Git](GIT-MSYS-PACKAGE.md) entity),
`libressl`, `mono`, `neon`, `openssl`, `perl-lwp-protocol-https`,
`pidgin`, `python-httplib2`, `qca-qt5`, and `qca-qt6`. None of these
twelve are currently modeled as entities in this knowledge base; see
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

No user-facing configuration; the bundle is updated by upstream
Mozilla releases and repackaged for MSYS2, the same convention
documented for
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#configuration).

## Initialization and Execution Flow

As a static data package, ca-certificates has no process lifecycle of
its own: it is read from disk by whatever TLS library or program
consumes it, typically at TLS-handshake time.

## Runtime Behavior

Identical functional role to
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#runtime-behavior);
see that page for detail not specific to the CLANG64/UCRT64 packaging
distinction.

## Compatibility and Variants

The CLANG64, UCRT64, and MSYS ca-certificates packages are three
separately versioned catalog entities (see Architectural
Classification); a certificate bundle update to one does not
automatically apply to another without matching the correct
package/environment.

## Security Considerations

The trustworthiness of every TLS connection verified against this
bundle depends on the currency and integrity of its contents; this
page does not assert this specific package version's freshness beyond
its recorded catalog version. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture.

## Failure Modes and Diagnostics

A TLS certificate-verification failure in a dependent program should
be checked against this package's bundle currency before being treated
as a defect in that program, the same triage order documented for
[ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md#failure-modes-and-diagnostics).

## Evidence, Assumptions, and Open Questions

Trusted root certificate bundle scope is backed by the official
Mozilla CA certificate policy page
(`evidence:mozilla:ca-certificates-manual-2026-07-30`), the same
evidence record [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
cites. Package identity, version, license, and the recorded dependency
edge are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Open: the twelve recorded reverse
dependents are not individually modeled in this knowledge base.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
- [ca-certificates (MSYS)](CA-CERTIFICATES.md)
- [p11-kit (CLANG64)](P11-KIT-CLANG64.md)
- [OpenSSL (CLANG64)](OPENSSL-CLANG64.md)
