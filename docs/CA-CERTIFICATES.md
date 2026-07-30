---
id: doc:volume-6:ca-certificates
title: ca-certificates
volume: 6
status: partial
model_refs:
  - library:mozilla:ca-certificates
  - package:msys2:ca-certificates
  - component:curl:curl
  - library:curl:libcurl
  - library:libssh2:libssh2
  - environment:msys2:msys
last_verified: 2026-07-30
evidence_refs:
  - evidence:mozilla:ca-certificates-manual-2026-07-30
  - evidence:catalog:current
---

# ca-certificates

## Purpose

ca-certificates is a curated bundle of common Certificate Authority root
certificates, maintained per the Mozilla CA Certificate Program. This
page documents its architectural role as a directly-declared dependency
of both [curl](CURL.md) and [libcurl](LIBCURL.md), which use it to back
TLS certificate-chain verification against a trusted root store, already
noted by package name on both pages' dependency tables before this page
existed. See the
[Mozilla CA Certificate Program page](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/)
for the trust-store policy reference.

## Architectural Classification

`library:mozilla:ca-certificates` is packaged in the MSYS environment as
`package:msys2:ca-certificates` (version `20250419-1` in the current
catalog snapshot, a date-versioned release reflecting the periodic
nature of CA bundle updates). This is the package
[curl](CURL.md#dependencies) and [libcurl](LIBCURL.md#dependencies)
actually depend on directly, as two independent dependents.

## Responsibilities

- Providing a trusted root certificate bundle, consumed by
  [curl](CURL.md) and [libcurl](LIBCURL.md) (and, transitively, any
  program linking libcurl) to validate TLS server certificate chains
  during HTTPS connections.

## Boundaries

ca-certificates provides trust-store data only; it implements no TLS
protocol logic itself — that is [curl](CURL.md)/[libcurl](LIBCURL.md)'s
own responsibility, delegated further to their own TLS backend
([OpenSSL](OPENSSL.md), per [libcurl's dependency table](LIBCURL.md#dependencies)).
This is a data package, not a code library in the conventional sense,
though it is modeled with `kind: library` in this knowledge base
consistent with how it is consumed (linked into the trust-verification
path) rather than invoked as a standalone tool.

## Interfaces

Not applicable in the conventional API sense: consuming programs read
the bundled certificate file(s) directly (typically via their TLS
backend's configured trust-store path) rather than calling a
ca-certificates-specific API.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:ca-certificates`.

## Reverse Dependencies

The catalog snapshot records 5 relationships targeting
`package:msys2:ca-certificates`. Three are already modeled in this
knowledge base: `package:msys2:curl`
(`relationship:ssh-curl-git:curl-requires-ca-certificates` in this
knowledge base's graph), `package:msys2:libcurl`
(`relationship:foundation-libraries:libcurl-requires-ca-certificates`),
and `package:msys2:libssh2`
(`relationship:foundation-libraries:libssh2-requires-ca-certificates`,
added 2026-07-30 — **correction**: this section previously stated
libssh2 did not itself record a direct `ca-certificates` dependency;
the catalog does in fact record one). The remaining 2 recorded
dependents (`lftp` and `libneon`) are not
individually modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

The bundled certificate file's location is fixed by the package
installation; individual programs may override the trust store via
their own configuration (for example, curl's `--cacert` flag) rather
than modifying this package directly.

## Initialization and Execution Flow

As a data package, ca-certificates has no process lifecycle of its own;
its bundled certificate data is read by whatever program (or its TLS
backend) needs to validate a certificate chain, at the time of TLS
handshake verification.

## Runtime Behavior

The trust decisions ca-certificates' bundle enables are exercised on
every TLS handshake [curl](CURL.md)/[libcurl](LIBCURL.md) perform where
certificate verification is not explicitly disabled.

## Compatibility and Variants

Whether other native environments (UCRT64, CLANG64, i686) in this
catalog package ca-certificates separately was not confirmed while
writing this page; this is recorded as an open item rather than assumed
either way.

## Security Considerations

ca-certificates sits at the foundation of TLS trust decisions for every
program that relies on it; an out-of-date or compromised bundle would
directly undermine certificate-chain verification. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; the periodic, date-versioned
release cadence itself is a relevant freshness signal not otherwise
assessed on this page.

## Failure Modes and Diagnostics

A TLS certificate-verification failure in curl (`SSL certificate
problem: unable to get local issuer certificate`) should be checked
against this bundle's currency and completeness before being treated as
a server-side misconfiguration.

## Evidence, Assumptions, and Open Questions

Trusted root certificate bundle scope is backed by the official Mozilla
CA Certificate Program page
(`evidence:mozilla:ca-certificates-manual-2026-07-30`). Package
identity, version, and the two modeled dependent edges are backed by
the pacman catalog snapshot (`evidence:catalog:current`). Open: whether
other native environments package ca-certificates separately was not
confirmed.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [curl](CURL.md)
- [libcurl](LIBCURL.md)
- [OpenSSL](OPENSSL.md)
- [ca-certificates (UCRT64)](CA-CERTIFICATES-UCRT64.md)
- [libssh2](LIBSSH2.md)
