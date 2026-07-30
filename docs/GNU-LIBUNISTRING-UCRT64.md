---
id: doc:volume-6:gnu-libunistring-ucrt64
title: GNU libunistring (UCRT64)
volume: 6
status: partial
model_refs:
  - library:gnu:libunistring@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-libunistring
  - library:gnu:libidn2@ucrt64
  - library:libpsl:libpsl@ucrt64
  - library:gnu:libiconv
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnu:libunistring-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GNU libunistring (UCRT64)

## Purpose

This page documents the **UCRT64-environment** libunistring package
specifically — a library for manipulating Unicode strings and C
strings — depended on by [GNU libidn2 (UCRT64)](GNU-LIBIDN2-UCRT64.md)
and [libpsl (UCRT64)](LIBPSL-UCRT64.md), closing a dependency chain
opened while covering [curl (UCRT64)'s](CURL-UCRT64.md) own
sub-dependencies. See the
[official libunistring project site](https://www.gnu.org/software/libunistring)
for the full reference.

## Architectural Classification

`library:gnu:libunistring@ucrt64` is packaged in the UCRT64 environment
as `package:msys2:mingw-w64-ucrt-x86_64-libunistring` (version
`1.4.2-1` in the current catalog snapshot, license
`LGPL-3.0-or-later OR GPL-3.0-or-later`) — a separately built, separate
catalog entity from [GNU libunistring (MSYS)](GNU-LIBUNISTRING.md)'s
`libunistring` package. This is the package
[GNU libidn2 (UCRT64)](GNU-LIBIDN2-UCRT64.md) and
[libpsl (UCRT64)](LIBPSL-UCRT64.md) — both UCRT64-native library
entities themselves — actually depend on.

## Responsibilities

- Providing Unicode string manipulation functions (normalization,
  case-mapping, and related operations), consumed by
  [GNU libidn2 (UCRT64)](GNU-LIBIDN2-UCRT64.md#dependencies) and
  [libpsl (UCRT64)](LIBPSL-UCRT64.md#dependencies) for internationalized
  domain name and Public Suffix List processing respectively.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[curl (MSYS)](CURL.md) and its dependency chain instead link
[GNU libunistring (MSYS)](GNU-LIBUNISTRING.md#reverse-dependencies) —
the two are not interchangeable, matching the same distinction already
made throughout this volume for MSYS/UCRT64 sibling pairs.

## Interfaces

- The libunistring C API (`u8_normalize`, `u8_casefold`, and related
  functions), the same interface
  [GNU libunistring (MSYS)](GNU-LIBUNISTRING.md#interfaces) documents,
  per the documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-libunistring` declares
one `runtime-depends-on` edge: [GNU libiconv](GNU-LIBICONV.md)
(character-set conversion,
`relationship:foundation-libraries:libunistring-ucrt64-requires-libiconv`).

## Reverse Dependencies

The catalog snapshot records 6 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libunistring`. Two are now
modeled in this knowledge base:
[GNU libidn2 (UCRT64)](GNU-LIBIDN2-UCRT64.md)
(`relationship:foundation-libraries:libidn2-ucrt64-requires-libunistring-ucrt64`)
and [libpsl (UCRT64)](LIBPSL-UCRT64.md)
(`relationship:foundation-libraries:libpsl-ucrt64-requires-libunistring-ucrt64`).
The remaining recorded dependents (`gnutls` — a UCRT64-native GnuTLS
package not individually modeled in this knowledge base — `notcurses`,
`qemu`, and `qemu-image-util`) are not individually modeled in this
knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libunistring has no persistent configuration file; behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libunistring has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [GNU libidn2 (UCRT64)](GNU-LIBIDN2-UCRT64.md) or
[libpsl (UCRT64)](LIBPSL-UCRT64.md) in this dependency chain. As a
native MinGW-w64 library, this process model is Windows-facing directly
rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[GNU libunistring (MSYS)](GNU-LIBUNISTRING.md#runtime-behavior); see
that page for detail not specific to the UCRT64/MSYS packaging
distinction.

## Compatibility and Variants

The UCRT64 and MSYS libunistring packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct package/environment.

## Security Considerations

No libunistring-specific vulnerability review has been performed for
this volume; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `1.4.2-1` version.

## Failure Modes and Diagnostics

libunistring itself has no user-facing CLI; Unicode-processing
failures in a dependent program should be checked against that
program's own input encoding assumptions before being treated as a
libunistring defect.

## Evidence, Assumptions, and Open Questions

Unicode string-processing scope is backed by the official libunistring
project site (`evidence:gnu:libunistring-manual-2026-07-30`), the same
evidence record [GNU libunistring (MSYS)](GNU-LIBUNISTRING.md) cites.
Package identity, version, license, and the two modeled dependent
edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Open, and explicitly out of scope for
this page: the remaining recorded dependents not individually modeled
(including the UCRT64-native `gnutls` package), and header-level API
surface / PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU libunistring (MSYS)](GNU-LIBUNISTRING.md)
- [GNU libidn2 (UCRT64)](GNU-LIBIDN2-UCRT64.md)
- [libpsl (UCRT64)](LIBPSL-UCRT64.md)
- [GNU libiconv](GNU-LIBICONV.md)
