---
id: doc:volume-6:winpthreads
title: winpthreads
volume: 6
status: partial
model_refs:
  - library:mingw-w64:winpthreads
  - package:msys2:mingw-w64-ucrt-x86_64-winpthreads
  - library:mingw-w64:libwinpthread
  - component:gnu:gcc
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:mingw-w64:libwinpthread-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# winpthreads

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:mingw-w64:winpthreads` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `low` |
| Authority | MinGW-w64 project |
| Environments | `ucrt64` |
| Upstream | <https://www.mingw-w64.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-winpthreads` |
| Version (observed) | 14.0.0.r248.g7735a1a63-1 |
| License (observed) | spdx:MIT;AND;BSD-3-Clause-Clear |
| Architecture (observed) | any |
| Installed size (observed) | 451.35 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:mingw-w64:libwinpthread-manual-2026-07-30` — MinGW-w64 (official project site) (`primary`, retrieved 2026-07-30)

**Claims about this object**

- `claim:library:winpthreads:libwinpthread-split` (`inference`, `low`) — The MSYS2 winpthreads package's exact relationship to libwinpthread is unresolved from package-level evidence alone: the version-pinned dependency and near-identical summaries are consistent with a development/runtime split, but a separate winpthreads-stub package that provides/conflicts with winpthreads (a near-empty, 8-byte-installed placeholder swappable for it) argues against a simple dev-headers theory and toward winpthreads containing a real, optionally-replaceable implementation component instead. Neither theory is confirmed against file contents.

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Winpthreads is a version-pinned companion package to
[libwinpthread](LIBWINPTHREAD.md), and this page exists specifically to
document the honest uncertainty around what distinguishes the two rather
than assume they are redundant. See the
[official MinGW-w64 project site](https://www.mingw-w64.org/) for the
project overview.

## Architectural Classification

`library:mingw-w64:winpthreads` is packaged per native environment: this
page cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-winpthreads` (version
`14.0.0.r220.gd999af622-1` in the current catalog snapshot — identical to
[libwinpthread](LIBWINPTHREAD.md)'s recorded version — license
`MIT AND BSD-3-Clause-Clear`).

## Responsibilities

Unresolved from package-level evidence. The initial working theory —
development headers/import library, with
[libwinpthread](LIBWINPTHREAD.md) providing the runtime DLL — is
complicated by a separate `mingw-w64-ucrt-x86_64-winpthreads-stub`
package discovered in this same catalog snapshot: it `provides` and
`conflicts` with `winpthreads`, is a near-empty placeholder (8 bytes
installed, license `NONE`), and exists for CLANG64, CLANGARM64, and
MINGW64 as well as UCRT64. A package a project can swap for an empty
stub is a poor fit for "required development headers" — that pattern
reads more like an optional or replaceable implementation component.
Both theories remain unconfirmed (`claim:library:winpthreads:libwinpthread-split`,
recorded at `low` confidence after this finding, down from the earlier
`medium`).

## Boundaries

This page deliberately does not restate [libwinpthread](LIBWINPTHREAD.md)'s
threading-API documentation; whatever this package actually contains, its
purpose is to complement that package, not duplicate it.

## Interfaces

Not established at package/dependency-level evidence; see Evidence,
Assumptions, and Open Questions.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-winpthreads`:
`mingw-w64-ucrt-x86_64-crt` (the MinGW-w64 C runtime and Windows API
headers this build targets) and a version-pinned
`mingw-w64-ucrt-x86_64-libwinpthread=14.0.0.r220.gd999af622` — the exact
version match is the strongest evidence for the dev/runtime split
inference, though not conclusive on its own.

## Reverse Dependencies

The snapshot records **5** relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-winpthreads`, one of which is now
modeled in this knowledge base: [GCC](GNU-GCC.md#dependencies)
(`relationship:toolchain:gcc-requires-winpthreads`, added 2026-07-30 to
close a gap in [GCC's own dependency table](GNU-GCC.md#dependencies),
which had cited this package by name without a corresponding graph edge)
— dramatically fewer overall
than [libwinpthread](LIBWINPTHREAD.md#reverse-dependencies)'s 152, which
is itself circumstantial support for a runtime-vs-development-package
split (most consumers need the runtime at execution time; far fewer
declare a build-time dependency on this package specifically). See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Not established at package/dependency-level evidence.

## Initialization and Execution Flow

Unresolved. If the (now weakened) dev-package theory holds, this package
would have no runtime execution role, consumed only at build/link time.
If instead it is a real, stub-replaceable implementation component, it
would have a genuine runtime role like [libwinpthread](LIBWINPTHREAD.md)'s.
This page does not pick one theory over the other.

## Runtime Behavior

Not established at package/dependency-level evidence.

## Compatibility and Variants

Given the identical recorded version and the near-identical package
summaries ("MinGW-w64 winpthreads library" for both packages in the
catalog), this page treats winpthreads and
[libwinpthread](LIBWINPTHREAD.md) as tightly coupled companions rather
than independent, separately versionable libraries. Separately,
`winpthreads-stub` is a documented, catalog-observed alternative to this
package specifically (`provides`/`conflicts: winpthreads`) across
UCRT64, CLANG64, CLANGARM64, and MINGW64 — a real packaging variant this
page flags but does not model as its own component, given its
near-zero content.

## Security Considerations

Not established at package/dependency-level evidence; if this is
genuinely a headers/import-library-only package with no runtime
component, its security exposure would be limited to build-time supply
chain concerns rather than runtime attack surface — but this page does
not assert that conclusion given the underlying uncertainty.

## Failure Modes and Diagnostics

Not established at package/dependency-level evidence.

## Evidence, Assumptions, and Open Questions

Package identity, version, both dependency edges, and the
`winpthreads-stub` provides/conflicts relationship are backed by the
pacman catalog snapshot (`evidence:catalog:current`) via
`claim:library:winpthreads:libwinpthread-split`. Open, and the primary
purpose of this page: what this package actually contains remains
unresolved — the original dev/runtime-split theory and the
stub-replaceable-implementation reading it prompted are both live,
unconfirmed hypotheses, not a settled fact; resolving it requires package
file-inventory evidence (per
[Package File Inventory](PACKAGE-FILE-INVENTORY.md)) that this snapshot
does not include. Nearly every section above is marked "not established"
or "unresolved" rather than filled with speculation dressed as fact, and
this page's own confidence was revised downward (medium to low) when the
new stub-package evidence complicated rather than confirmed the initial
theory — a deliberate record of updating a claim when new evidence
warrants it, not just adding new claims.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["winpthreads"]
    u0["GCC"]
    u0 -->|requires| subject
    d0["libwinpthread"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:mingw-w64:winpthreads` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libwinpthread](LIBWINPTHREAD.md)
- [GCC](GNU-GCC.md)
- [Package File Inventory](PACKAGE-FILE-INVENTORY.md)
