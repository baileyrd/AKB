---
id: doc:volume-6:nettle-msys
title: Nettle (MSYS)
volume: 6
status: partial
model_refs:
  - library:nettle:nettle@msys
  - package:msys2:nettle
  - component:gnupg:gnupg
  - library:nettle:libnettle@msys
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:nettle:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Nettle (MSYS)

## Purpose

This page documents the **MSYS-environment** `nettle` package
specifically — a low-level cryptographic library backing GnuPG's
additional cryptographic primitives — as a correction:
[GNUPG.md](GNUPG.md) and [Nettle (UCRT64)](NETTLE.md) originally recorded
`component:gnupg:gnupg`'s `requires` edge as pointing to the
UCRT64-packaged `nettle`
(`package:msys2:mingw-w64-ucrt-x86_64-nettle`), but
`package:msys2:gnupg` is itself an MSYS-environment package whose actual
catalog-recorded dependency is `package:msys2:nettle` — a separate
catalog entity, though coincidentally the same version. This page
documents that correct target; see the
[official Nettle project page](https://www.lysator.liu.se/~nisse/nettle/)
for the API reference shared with the UCRT64 package.

## Architectural Classification

`library:nettle:nettle@msys` is packaged in the MSYS environment as
`package:msys2:nettle` (version `4.0-1` in the current catalog snapshot)
— the same version number as the UCRT64 sibling documented on
[Nettle (UCRT64)](NETTLE.md), but a genuinely separate catalog entity
with its own dependency structure (see Dependencies). This is the
package [GnuPG](GNUPG.md#architectural-classification) actually depends
on.

## Responsibilities

- Backing additional cryptographic primitives directly for
  [GnuPG's](GNUPG.md) MSYS-packaged build, the same functional role
  [Nettle (UCRT64)](NETTLE.md) documents for the UCRT64 packaging
  context. This is a separate package (`package:msys2:nettle`) from
  [libnettle (MSYS)](LIBNETTLE-MSYS.md) (`package:msys2:libnettle`)
  [GnuTLS](GNUTLS.md) itself depends on directly for its own Nettle use
  backing GnuPG's `dirmngr` TLS connections and GNU Emacs' Network
  Security Manager — this `nettle` meta-package depends on `libnettle`
  in turn (see Dependencies), so the two are related but should not be
  conflated.

## Boundaries

Functionally identical in scope to [Nettle (UCRT64)](NETTLE.md) — this
page exists specifically to document the correct MSYS-packaged catalog
entity that GnuPG's own MSYS build depends on.

## Interfaces

Identical API surface to [Nettle (UCRT64)](NETTLE.md); see that page for
interface details, since both packages share the same upstream project.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:nettle`: `package:msys2:libnettle` — the MSYS-packaged
base Nettle cryptographic library, documented fully on
[libnettle (MSYS)](LIBNETTLE-MSYS.md)
(`relationship:foundation-libraries:nettle-msys-requires-libnettle-msys`).
**Correction, 2026-07-30**: this page originally stated a direct
`libhogweed` dependency here; the catalog's actual edge targets
`libnettle` instead, with [Hogweed](LIBHOGWEED-MSYS.md) one level
further down `libnettle`'s own dependency chain — a distinction now
made explicit across both new pages rather than left conflated. This is
a different sub-dependency structure from [Nettle (UCRT64)](NETTLE.md)'s
own package.

## Reverse Dependencies

The catalog snapshot records 1 relationship targeting
`package:msys2:nettle`: `package:msys2:gnupg`
(`relationship:ssh-curl-git:gnupg-requires-nettle` in this knowledge
base's graph, corrected 2026-07-30 to point here instead of the UCRT64
package) — its sole recorded dependent in this snapshot.

## Configuration

No persistent configuration file; identical to
[Nettle (UCRT64)](NETTLE.md) in this respect.

## Initialization and Execution Flow

As a library, this package has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [GnuPG](GNUPG.md) in this dependency chain. As an
MSYS-dependent library, this is adapted from POSIX semantics onto Windows
process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md), unlike the
UCRT64 sibling, which does not depend on `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [Nettle (UCRT64)](NETTLE.md); see that
page for detail not specific to the MSYS/UCRT64 packaging distinction.

## Compatibility and Variants

This is the correction record for the MSYS/UCRT64 packaging distinction
itself: the two `nettle` packages share the same version (`4.0-1`) but
are separately built, separate catalog entities with different
sub-dependency structures (this MSYS package depends on `libnettle`; see
Dependencies) and are not interchangeable at the binary level.

## Security Considerations

Identical security posture to [Nettle (UCRT64)](NETTLE.md); see that
page. No version-qualified CVE review has been performed for the
recorded `4.0-1` version specifically.

## Failure Modes and Diagnostics

Identical to [Nettle (UCRT64)](NETTLE.md); GnuPG's cryptographic
operation failures should be checked against this MSYS package's
behavior specifically, not the UCRT64 sibling's, since GnuPG links
against this one.

## Evidence, Assumptions, and Open Questions

The cryptographic-primitives role is backed by the official Nettle
project page (`evidence:nettle:manual-2026-07-30`), the same evidence
record [Nettle (UCRT64)](NETTLE.md) cites. Package identity, version, and
the recorded dependency/dependent edges (including the 2026-07-30
correction to `relationship:ssh-curl-git:gnupg-requires-nettle`, and the
2026-07-30 correction of this page's own Dependencies section from
`libhogweed` to `libnettle`) are backed by the pacman catalog snapshot
(`evidence:catalog:current`). No open items beyond the general
header-level API surface / PE import/export-level evidence noted
elsewhere in this volume's methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GnuPG](GNUPG.md)
- [Nettle (UCRT64)](NETTLE.md)
- [GnuTLS](GNUTLS.md)
- [libnettle (MSYS)](LIBNETTLE-MSYS.md)
- [Hogweed (MSYS)](LIBHOGWEED-MSYS.md)
