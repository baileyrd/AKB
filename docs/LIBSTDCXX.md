---
id: doc:volume-6:libstdcxx
title: libstdc++
volume: 6
status: partial
model_refs:
  - library:gnu:libstdc++
  - package:msys2:mingw-w64-ucrt-x86_64-gcc-libs
  - component:gnu:gcc
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnu:libstdcxx-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libstdc++

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnu:libstdc++` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Free Software Foundation |
| Environments | `ucrt64` |
| Upstream | <https://gcc.gnu.org/onlinedocs/libstdc++/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-gcc-libs` |
| Version (observed) | 16.1.0-5 |
| License (observed) | spdx:GPL-3.0-or-later WITH GCC-exception-3.1 AND LGPL-2.1-or-later |
| Architecture (observed) | any |
| Installed size (observed) | 3.5 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:gnu:libstdcxx-manual-2026-07-30` — The GNU C++ Library Documentation (`primary`, retrieved 2026-07-30)

**Claims about this object**

- `claim:library:libstdcxx:bundled-in-gcc-libs` (`fact`, `verified`) — libstdc++ is not packaged as a standalone MSYS2 package; it is bundled inside gcc-libs alongside libgcc, libgomp, and other GCC runtime support libraries.

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

libstdc++ is GCC's implementation of the C++ standard library, and it
resolves the "C++ library" row left open in the
[MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md). This page documents
its packaging and its ABI relationship to [libc++](LIBCXX.md); see the
[GNU C++ Library documentation](https://gcc.gnu.org/onlinedocs/libstdc++/)
for the API reference.

## Architectural Classification

`library:gnu:libstdc++` is a C++ standard library implementation, part of
the GNU project and developed alongside [GCC](GNU-GCC.md). This page cites
the UCRT64 environment; the same architecture applies to MINGW64 and
MINGW32's own gcc-libs packages. This page is scoped to Volume 6's
package/dependency-level evidence; the fuller
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology (headers, `pkg-config`/CMake metadata, PE import/export
analysis) has not been applied here and remains open, per the Evidence
section below.

## Responsibilities

- Implementing the C++ standard library (containers, algorithms, iostreams,
  and the rest of the ISO C++ standard library surface) that C++ programs
  compiled with [GCC](GNU-GCC.md) link against by default.

## Boundaries

libstdc++ is not packaged standalone in this environment: it is bundled
inside `gcc-libs` alongside `libgcc` (low-level compiler runtime support)
and `libgomp` (OpenMP runtime), rather than shipped as its own MSYS2
package (`claim:library:libstdcxx:bundled-in-gcc-libs`). It is not the
only C++ standard library available in this environment; see
[libc++](LIBCXX.md) for the LLVM alternative, which this environment also
packages for UCRT64.

## Interfaces

- The full ISO C++ standard library API surface (headers such as
  `<vector>`, `<string>`, `<iostream>`), consumed at compile time by any
  C++ translation unit and linked at build time, per the documentation.
  This page does not enumerate the header-level surface; that belongs to
  [Header and Development-Metadata Indexes](HEADER-AND-METADATA-INDEXES.md).

## Dependencies

libstdc++ is bundled with `package:msys2:mingw-w64-ucrt-x86_64-gcc-libs`,
which itself records two `runtime-depends-on` edges in the catalog
snapshot: [libwinpthread](LIBWINPTHREAD.md) (threading support,
`relationship:toolchain:libstdcxx-requires-libwinpthread`, added
2026-07-30) and
`mingw-w64-ucrt-x86_64-tzdata` (timezone database, backing C++20's
`<chrono>` timezone support, not individually modeled in this
knowledge base). The package also `provides` the
`mingw-w64-ucrt-x86_64-cc-libs` virtual capability, which
[libc++](LIBCXX.md#dependencies) in this same environment depends on for
low-level compiler runtime support even when a project chooses libc++ over
libstdc++ (`claim:library:libcxx:cc-libs-capability`).

## Reverse Dependencies

`package:msys2:mingw-w64-ucrt-x86_64-gcc-libs` records **167** relationships
targeting it in this snapshot — larger than
[ncurses](NCURSES.md#reverse-dependencies)'s 40 and
[OpenSSL](OPENSSL.md#reverse-dependencies)'s 21, though smaller than
[zlib](ZLIB.md#reverse-dependencies)'s 299, the largest recorded in this
knowledge base. This is a directly observed fact, not an inference: nearly
every C/C++ program built with GCC in this environment needs the runtime
libraries this package bundles. One is now modeled in this knowledge
base: [GCC](GNU-GCC.md#dependencies) itself
(`relationship:toolchain:gcc-requires-libstdcxx`, added 2026-07-30 to
close a gap in [GCC's own dependency table](GNU-GCC.md#dependencies),
which had cited this package by name without a corresponding graph
edge). See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libstdc++ has some compile-time-selectable behaviors (for example, the
`_GLIBCXX_ASSERTIONS` hardening macro, or Dual ABI considerations for
`std::string`/`std::list` inherited from historical GCC releases), but no
persistent runtime configuration file; this page does not enumerate those
macros, which belong to the library's own reference documentation.

## Initialization and Execution Flow

As a library rather than a standalone program, libstdc++ has no
independent process lifecycle: it is linked into and initializes within
the process of whatever program links against it, alongside that
program's own startup.

## Runtime Behavior

Given its role as GCC's default C++ standard library, libstdc++'s runtime
behavior (allocation strategy, exception-handling personality routines via
`libgcc`) is the behavior nearly every GCC-built C++ program in this
environment exhibits; this page does not attempt to characterize that
behavior beyond noting its centrality (per Reverse Dependencies above).

## Compatibility and Variants

libstdc++ and [libc++](LIBCXX.md) both implement the C++ standard library
API, but object files and static libraries built against one are not
link-compatible with the other without rebuilding
(`relationship:cxx-library:libcxx-compatible-with-libstdcxx`), per
[Runtime Environments](RUNTIME-ENVIRONMENTS.md#boundaries)'s general
C++-library compatibility guidance, restated here specifically for this
pair rather than duplicated in full.

## Security Considerations

No libstdc++-specific vulnerability review has been performed for this
volume; given its 167 recorded dependents, a defect here would have a very
wide blast radius — second only to [zlib](ZLIB.md#security-considerations)'s
299 among the components and libraries documented in this knowledge base
so far — the same risk-concentration observation already made for
[ncurses](NCURSES.md#security-considerations) and
[OpenSSL](OPENSSL.md#security-considerations), at a larger scale. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture.

## Failure Modes and Diagnostics

ABI-mismatch link errors (mixing objects built against libstdc++ with
objects built against [libc++](LIBCXX.md), or across incompatible GCC
versions' Dual ABI settings) are the most likely failure mode this library
surfaces; per Compatibility and Variants, rebuilding consistently is the
documented resolution rather than mixing.

## Evidence, Assumptions, and Open Questions

Bundling and dependency facts are backed by the pacman catalog snapshot
(`evidence:catalog:current`) via
`claim:library:libstdcxx:bundled-in-gcc-libs`; the library's general
architecture is backed by the official libstdc++ documentation
(`evidence:gnu:libstdcxx-manual-2026-07-30`). Open, and explicitly out of
scope for this page: header-level API surface, `pkg-config`/CMake metadata,
and PE import/export-level ABI evidence, which the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology calls for and which this page does not attempt to supply.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libstdc++"]
    u0["GCC"]
    u0 -->|requires| subject
    d0["libwinpthread"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnu:libstdc++` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libc++](LIBCXX.md)
- [GCC](GNU-GCC.md)
