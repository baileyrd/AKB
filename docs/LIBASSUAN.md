---
id: doc:volume-6:libassuan
title: libassuan
volume: 6
status: partial
model_refs:
  - library:gnupg:libassuan
  - package:msys2:mingw-w64-ucrt-x86_64-libassuan
  - library:gnupg:libgpg-error
  - library:gnupg:libassuan@msys
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnupg:libassuan-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libassuan

## Purpose

Libassuan implements the Assuan IPC protocol GnuPG uses for communication
between its cooperating processes — `gpg`, `dirmngr`, and `pinentry`. This
page documents the **UCRT64**-packaged build specifically; the
MSYS-packaged `package:msys2:gnupg` component GnuPG.md documents actually
depends on a separately versioned MSYS sibling package, corrected
2026-07-30 and documented on
[libassuan (MSYS)](LIBASSUAN-MSYS.md) — the split-process architecture
GnuPG.md describes is backed by that MSYS package, not this one. See the
[official libassuan project page](https://gnupg.org/related_software/libassuan)
for the protocol reference shared by both packages.

## Architectural Classification

`library:gnupg:libassuan` is packaged per native environment: this page
cites the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-libassuan`
(version `2.5.7-1` in the current catalog snapshot, license
`LGPL-2.1-or-later OR GPL-3.0-or-later`).

## Responsibilities

- Implementing the Assuan IPC protocol: a simple, line-based protocol for
  request/response communication between GnuPG-family cooperating
  processes built against this UCRT64 packaging, letting passphrase
  entry (`pinentry`) and network lookups (`dirmngr`) stay isolated in
  separate processes while still coordinating with the main `gpg`
  process. [GnuPG's](GNUPG.md#initialization-and-execution-flow) own
  MSYS-packaged split-process architecture is backed by
  [libassuan (MSYS)](LIBASSUAN-MSYS.md) instead.

## Boundaries

Libassuan provides the IPC transport and protocol only; it does not
implement cryptography ([libgcrypt](LIBGCRYPT.md)'s role) or certificate
parsing ([libksba](LIBKSBA.md)'s role) — it is purely the communication
layer between GnuPG's processes.

## Interfaces

- A C API for both the client and server sides of the Assuan protocol
  (`assuan_new`, `assuan_transact`), per the documentation.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-libassuan`:
`mingw-w64-ucrt-x86_64-gcc-libs` (GCC's bundled runtime support, the same
package documented as the hub of [libstdc++](LIBSTDCXX.md#dependencies))
and `mingw-w64-ucrt-x86_64-libgpg-error` (the shared error-code
vocabulary documented fully in [libgpg-error](LIBGPG-ERROR.md)).

## Reverse Dependencies

The snapshot records 3 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libassuan`. [GnuPG](GNUPG.md) is
**not** among them — that was a pre-2026-07-30 modeling error, corrected
in favor of
[libassuan (MSYS)](LIBASSUAN-MSYS.md#reverse-dependencies), which
GnuPG's own MSYS-packaged catalog dependency actually targets. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list of this UCRT64 package's actual dependents.

## Configuration

Libassuan has no persistent configuration file; its behavior is a
transport/protocol implementation configured by the calling program's API
usage, not external configuration.

## Initialization and Execution Flow

As a library, libassuan has no independent process lifecycle: it
initializes and executes within each of the cooperating processes that
use it to talk to one another, the same general mechanism
[GnuPG's MSYS-packaged build](GNUPG.md#initialization-and-execution-flow)
uses via [libassuan (MSYS)](LIBASSUAN-MSYS.md) rather than this UCRT64
package.

## Runtime Behavior

Assuan connections are typically local (Unix-domain-socket-style or named
pipes), not network sockets; this is consistent with its role coordinating
cooperating local processes rather than remote communication.

## Compatibility and Variants

Libassuan's protocol is specific to the GnuPG ecosystem; this page does
not claim general-purpose IPC interchangeability with other IPC
mechanisms.

## Security Considerations

Because libassuan mediates communication that includes passphrase entry
(via `pinentry`), the integrity of this IPC channel is directly relevant
to the security model of whatever GnuPG-family software links against
this UCRT64 build. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `2.5.7-1` version.

## Failure Modes and Diagnostics

Passphrase prompts failing to appear (a symptom
[GnuPG's own page](GNUPG.md#failure-modes-and-diagnostics) flags, though
backed by [libassuan (MSYS)](LIBASSUAN-MSYS.md) rather than this UCRT64
package) should be checked against IPC connectivity between `gpg` and
`pinentry` as one possible cause, alongside `pinentry` configuration
itself.

## Evidence, Assumptions, and Open Questions

The IPC protocol role is backed by the official libassuan project page
(`evidence:gnupg:libassuan-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:mingw-w64-ucrt-x86_64-libassuan` in
the catalog. Package identity, version, license, and both dependency
edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Correction (2026-07-30): this page
previously claimed a direct `component:gnupg:gnupg` dependency and cited
`relationship:ssh-curl-git:gnupg-requires-libassuan` as evidence; that
relationship's target has since been corrected to
[libassuan (MSYS)](LIBASSUAN-MSYS.md), since `package:msys2:gnupg` is an
MSYS-environment package and this page's UCRT64 package was never its
actual catalog-recorded dependency. Open, and explicitly out of scope for
this page: header-level API surface and PE import/export-level evidence,
per the [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libgpg-error](LIBGPG-ERROR.md)
- [libassuan (MSYS)](LIBASSUAN-MSYS.md)
- [libassuan (CLANG64)](LIBASSUAN-CLANG64.md)
