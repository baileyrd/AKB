---
id: doc:volume-6:gnu-libidn2
title: GNU libidn2
volume: 6
status: partial
model_refs:
  - library:gnu:libidn2
  - package:msys2:libidn2
  - library:gnutls:gnutls
  - library:gnu:libunistring
  - library:libpsl:libpsl
  - component:curl:curl
  - library:gnu:libintl
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:libidn2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GNU libidn2

## Purpose

GNU libidn2 implements the IDNA2008, Punycode, and TR46 specifications for
internationalized domain names (IDNs) — the mechanism that lets domain
names containing non-ASCII characters be converted to and from the
ASCII-compatible encoding (ACE) form actually used in DNS. This page
documents its architectural role as a shared dependency of
[GnuTLS](GNUTLS.md) and (indirectly, via libcurl) [curl](CURL.md); see the
[official GNU libidn2 project page](https://www.gnu.org/software/libidn/#libidn2)
for the full API reference.

## Architectural Classification

`library:gnu:libidn2` is packaged in the MSYS environment as
`package:msys2:libidn2` (version `2.3.8-1` in the current catalog
snapshot). A separately packaged, native (UCRT64/CLANG64/i686) `libidn2`
also exists in the catalog (for example
`mingw-w64-ucrt-x86_64-libidn2`); this page documents the MSYS package
specifically, since that is the one [GnuTLS](GNUTLS.md#dependencies)
actually depends on — the same MSYS-vs-native distinction already made
for [GnuTLS](GNUTLS.md#architectural-classification) itself, [SQLite](SQLITE3.md#boundaries),
and [PCRE2](PCRE2.md#boundaries) elsewhere in this volume.

## Responsibilities

- Converting internationalized domain name labels to and from their
  ASCII-compatible (Punycode) DNS encoding, per the IDNA2008 and TR46
  specifications.

## Boundaries

libidn2 handles domain-name label encoding specifically; it does not
perform DNS resolution itself, nor does it implement the older IDNA2003
standard (the GNU project's separate, deprecated `libidn` library covered
that; this page and its catalog package concern `libidn2` only).

## Interfaces

- A C API (`idn2_lookup_u8`, `idn2_to_ascii_8z`, and related functions)
  for converting domain-name labels between Unicode and ACE form, per the
  documentation.

## Dependencies

The MSYS `package:msys2:libidn2` declares dependencies on
[GNU libintl](GNU-LIBINTL.md) (gettext-based message translation,
`relationship:foundation-libraries:libidn2-requires-libintl`) and
[libunistring](GNU-LIBUNISTRING.md) (Unicode string processing).

## Reverse Dependencies

The catalog snapshot records 9 relationships targeting
`package:msys2:libidn2`, including `package:msys2:libgnutls`
(`relationship:foundation-libraries:gnutls-requires-libidn2` in this
knowledge base's graph) and `package:msys2:libcurl` — the latter a
dependency of [curl](CURL.md)'s own `libcurl` transfer library rather than
of the `curl` CLI package directly, so no `requires` edge from
`component:curl:curl` is recorded for it in this graph; see
[curl's dependency table](CURL.md#dependencies) for the CLI package's own
directly-declared dependencies. Other recorded dependents include the
FTP/SFTP client `lftp`, the mail clients `mutt`/`neomutt`, and `whois`.

## Configuration

libidn2 has no persistent configuration file of its own; its behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libidn2 has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it. As
an MSYS-dependent library, this is adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Whether a specific domain-name label round-trips correctly through
IDNA2008 encoding depends on the label's Unicode content matching the
specification's validity rules; this page does not characterize specific
encoding outcomes.

## Compatibility and Variants

The MSYS and native (UCRT64/CLANG64/i686) libidn2 packages are separately
versioned catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct environment. IDNA2008 (this library) and the older
IDNA2003 standard are also not drop-in compatible for all inputs, per the
upstream documentation.

## Security Considerations

Incorrect IDN handling is a documented class of security concern (for
example, visually similar characters from different scripts being used
for domain-name spoofing); libidn2's conformance to the IDNA2008/TR46
specifications is the relevant mitigation. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `2.3.8-1` version.

## Failure Modes and Diagnostics

A domain label rejected by `idn2_lookup_u8`/`idn2_to_ascii_8z` most
commonly indicates the label violates IDNA2008 validity rules (invalid
code points, disallowed script mixing) rather than a defect in the calling
program.

## Evidence, Assumptions, and Open Questions

IDNA2008/Punycode/TR46 implementation scope is backed by the official GNU
libidn2 project page (`evidence:gnu:libidn2-manual-2026-07-30`), matching
the `project_url` already recorded for `package:msys2:libidn2` in the
catalog. Package identity, version, and the recorded dependency/dependent
edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Open, and explicitly out of scope for this
page: header-level API surface and PE import/export-level evidence, per
the [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GnuTLS](GNUTLS.md)
- [curl](CURL.md)
- [GNU libunistring](GNU-LIBUNISTRING.md)
- [libpsl](LIBPSL.md)
- [GNU libintl](GNU-LIBINTL.md)
