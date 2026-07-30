---
id: doc:volume-6:gnutls
title: GnuTLS
volume: 6
status: partial
model_refs:
  - library:gnutls:gnutls
  - package:msys2:libgnutls
  - component:gnupg:gnupg
  - component:gnu:emacs
  - library:gnu:libidn2
  - library:gnu:libtasn1
  - library:p11-glue:p11-kit
  - library:gnu:libintl
  - library:gnu:libiconv@msys
  - library:gnu:gmp@msys
  - library:nettle:libnettle@msys
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnutls:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GnuTLS

## Purpose

GnuTLS implements TLS/SSL and related cryptographic protocols, and it is
the library backing [GnuPG](GNUPG.md#dependencies)'s `dirmngr` network
lookups and [GNU Emacs](GNU-EMACS.md#dependencies)'s Network Security
Manager, both already cited on those pages before this page existed. This
page documents its architectural role; see the
[official GnuTLS project site](https://www.gnutls.org/) for the API
reference.

## Architectural Classification

`library:gnutls:gnutls` is packaged in the MSYS environment as
`package:msys2:libgnutls` (version `3.8.13-2` in the current catalog
snapshot, license `GPL-3.0-or-later;LGPL-2.1-or-later`). A separately
packaged, differently versioned (`3.8.13-3`) and differently
dependency-structured `gnutls` library also exists for UCRT64
(`mingw-w64-ucrt-x86_64-gnutls`); this page documents the MSYS package
specifically, since that is the one [GnuPG](GNUPG.md) and
[GNU Emacs](GNU-EMACS.md) — both MSYS-environment packages themselves —
actually depend on. The two should not be conflated as the same catalog
entity, the same distinction already made carefully for
[SQLite](SQLITE3.md#boundaries) and [PCRE2](PCRE2.md#boundaries)
elsewhere in this volume.

## Responsibilities

- Implementing TLS/SSL client (and server) protocol support as a library,
  consumed by [GnuPG](GNUPG.md)'s `dirmngr` component for encrypted
  key-server and OCSP-responder connections, and by
  [GNU Emacs](GNU-EMACS.md)'s Network Security Manager for encrypted
  network connections from within Emacs itself.

## Boundaries

GnuTLS provides TLS/SSL specifically; it is architecturally comparable to
[OpenSSL](OPENSSL.md) in role but is a fully independent implementation,
not a fork or wrapper — [GnuPG](GNUPG.md#boundaries) already documents
that its OpenPGP cryptography (via [libgcrypt](LIBGCRYPT.md)) is
deliberately independent of OpenSSL, and its network-facing TLS use (via
GnuTLS) is the one exception to that independence, since `dirmngr` needs
TLS specifically for HTTPS-based key-server lookups.

## Interfaces

- A C API for TLS session establishment, certificate verification, and
  encrypted data transfer (`gnutls_init`, `gnutls_handshake`), per the
  documentation.

## Dependencies

The MSYS `package:msys2:libgnutls` declares dependencies on `gcc-libs`,
[libidn2](GNU-LIBIDN2.md) (internationalized domain name support),
[libiconv (MSYS)](GNU-LIBICONV-MSYS.md), [libintl](GNU-LIBINTL.md),
[GNU MP (MSYS)](GNU-GMP-MSYS.md), [libnettle (MSYS)](LIBNETTLE-MSYS.md),
[p11-kit](P11-KIT.md) (PKCS#11 module support, for hardware security
tokens and smart cards), [libtasn1](GNU-LIBTASN1.md) (ASN.1/DER parsing
for certificates), and `zlib` — all separate MSYS-environment sibling
packages. Seven of these (libidn2, libintl, p11-kit, libtasn1, libiconv,
gmp, libnettle) now have their own pages and explicit `requires` edges
from `library:gnutls:gnutls` in the model graph
(`relationship:foundation-libraries:gnutls-requires-libidn2`,
`relationship:foundation-libraries:gnutls-msys-requires-libintl`,
`relationship:foundation-libraries:gnutls-requires-p11-kit`,
`relationship:foundation-libraries:gnutls-requires-libtasn1`,
`relationship:foundation-libraries:gnutls-msys-requires-libiconv-msys`,
`relationship:foundation-libraries:gnutls-msys-requires-gmp-msys`,
`relationship:ssh-curl-git:gnutls-requires-libnettle-msys`) —
closing an item this page originally left explicitly unmodeled,
correcting a prior version of this paragraph that declined to add
`gmp`/`libiconv` edges at all rather than modeling the correct MSYS
siblings. This page does not add a formal dependency edge to this
knowledge base's existing `library:nettle:nettle` (the UCRT64-packaged
Nettle entity, distinct from [libnettle (MSYS)](LIBNETTLE-MSYS.md)) or
`library:gnu:zlib` entities, because those remain the UCRT64-packaged
versions of the same-named libraries, not this MSYS package's actual
dependencies — the same package/environment distinction this page's own
Architectural Classification section makes about GnuTLS itself.

## Reverse Dependencies

Reverse-dependency figures for `package:msys2:libgnutls` were not
separately queried for this page; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current data. [GnuPG](GNUPG.md#dependencies) and
[GNU Emacs](GNU-EMACS.md#dependencies) are both confirmed dependents,
each now with an explicit `requires` edge in the model graph
(`relationship:ssh-curl-git:gnupg-requires-gnutls`,
`relationship:gnu-userland:emacs-requires-gnutls`).

## Configuration

GnuTLS has no persistent configuration file of its own; its behavior
(supported protocol versions, cipher suites, certificate verification) is
controlled through its C API by the calling program, and by the system's
PKCS#11 module configuration via `libp11-kit` when hardware tokens are
involved.

## Initialization and Execution Flow

As a library, GnuTLS has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it —
`dirmngr` within [GnuPG](GNUPG.md)'s multi-process architecture, or Emacs
itself. As an MSYS-dependent library, this is adapted from POSIX semantics
onto Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

GnuTLS's negotiated protocol version and cipher suite for a given
connection determine what security properties that connection actually
has; this page does not characterize specific negotiation outcomes.

## Compatibility and Variants

The MSYS and UCRT64 GnuTLS packages are separately versioned and
separately dependency-structured (see Architectural Classification); code
built against one is not automatically compatible with the other without
matching the correct environment.

## Security Considerations

As the TLS implementation behind both [GnuPG](GNUPG.md)'s network lookups
and [GNU Emacs](GNU-EMACS.md)'s network security, GnuTLS sits in a
security-critical position for both. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `3.8.13-2` version.

## Failure Modes and Diagnostics

TLS handshake or certificate-verification failures in `dirmngr` or Emacs'
network features should be checked against GnuTLS's negotiated protocol
and the relevant certificate trust store before being treated as a defect
in the calling program.

## Evidence, Assumptions, and Open Questions

TLS protocol implementation is backed by the official GnuTLS project site
(`evidence:gnutls:manual-2026-07-30`), matching the `project_url` already
recorded for `package:msys2:libgnutls` in the catalog. Package identity,
version, license, and the two confirmed dependent relationships are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: this package's remaining
sub-dependency (`gcc-libs`) is not individually modeled as a component
in this knowledge base; header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology, also remain open.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GnuPG](GNUPG.md)
- [GNU Emacs](GNU-EMACS.md)
- [GNU libiconv (MSYS)](GNU-LIBICONV-MSYS.md)
- [GNU MP (MSYS)](GNU-GMP-MSYS.md)
- [OpenSSL](OPENSSL.md)
- [Nettle](NETTLE.md)
- [libnettle (MSYS)](LIBNETTLE-MSYS.md)
- [GNU libidn2](GNU-LIBIDN2.md)
- [GNU Libtasn1](GNU-LIBTASN1.md)
- [GNU libintl](GNU-LIBINTL.md)
- [p11-kit](P11-KIT.md)
