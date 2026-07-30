---
id: doc:volume-6:npth
title: nPth (New Portable Threads)
volume: 6
status: partial
model_refs:
  - library:gnupg:npth
  - package:msys2:mingw-w64-ucrt-x86_64-npth
  - component:gnupg:gnupg
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnupg:npth-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# nPth (New Portable Threads)

## Purpose

nPth is GnuPG's own portable threading library, used internally for
GnuPG's concurrent operations — a separate, project-owned alternative to
depending on the platform's native threading library or a general-purpose
one like [libwinpthread](LIBWINPTHREAD.md). This page documents its
architectural role; see the [GnuPG project site](https://gnupg.org/) for
background.

## Architectural Classification

`library:gnupg:npth` is packaged per native environment: this page cites
the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-npth` (version
`1.8-1` in the current catalog snapshot, license `LGPL`).

## Responsibilities

- Providing GnuPG's internal threading primitives, used for concurrent
  operations within GnuPG's components rather than the general-purpose
  threading role [libwinpthread](LIBWINPTHREAD.md) or
  [GNU Readline](GNU-READLINE.md)-adjacent tools rely on.

## Boundaries

nPth is scoped to GnuPG's own internal use; it is not the general-purpose
threading library other native MinGW-w64 programs in this environment
link against — that role belongs to
[libwinpthread](LIBWINPTHREAD.md#responsibilities), which this library
does not replace or depend on.

## Interfaces

- A C API providing threading primitives GnuPG's own components use
  internally, per the project's general documentation; this page does not
  claim a stable, independently documented public API surface beyond
  GnuPG's own use.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-npth`:
`mingw-w64-ucrt-x86_64-gcc-libs`, the standard GCC-toolchain runtime
libraries documented as the hub of
[libstdc++'s dependents](LIBSTDCXX.md#reverse-dependencies).

## Reverse Dependencies

The snapshot records 2 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-npth`, including
[GnuPG](GNUPG.md#dependencies) itself
(`relationship:ssh-curl-git:gnupg-requires-npth`). See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

nPth has no persistent configuration file; its behavior is entirely
determined by the calling GnuPG component's own use of its threading API.

## Initialization and Execution Flow

As a library, nPth has no independent process lifecycle: it initializes
and executes within the GnuPG process that uses it for concurrent
operations, the same general library-linkage model documented for
[libgpg-error](LIBGPG-ERROR.md#initialization-and-execution-flow).

## Runtime Behavior

Given its narrow, GnuPG-internal scope, this page does not characterize
nPth's runtime behavior beyond noting it backs GnuPG's own concurrency
needs.

## Compatibility and Variants

nPth is a GnuPG-project-specific library; this page does not claim
interchangeability with other threading libraries in this volume, given
its narrower intended audience.

## Security Considerations

No nPth-specific vulnerability review has been performed for this volume;
see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `1.8-1` version.

## Failure Modes and Diagnostics

nPth itself has no user-facing CLI; concurrency-related issues in GnuPG
components should be diagnosed against GnuPG's own behavior first, given
this library's narrow internal role.

## Evidence, Assumptions, and Open Questions

The internal-threading role is backed by the official GnuPG project site
(`evidence:gnupg:npth-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:mingw-w64-ucrt-x86_64-npth` in the
catalog. Package identity, version, license, and the dependency edge are
backed by the pacman catalog snapshot (`evidence:catalog:current`). Open,
and explicitly out of scope for this page: header-level API surface and
PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GnuPG](GNUPG.md)
- [libwinpthread](LIBWINPTHREAD.md)
