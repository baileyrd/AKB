---
id: doc:volume-6:libcxx
title: libc++
volume: 6
status: partial
model_refs:
  - library:llvm:libc++
  - package:msys2:mingw-w64-ucrt-x86_64-libc++
  - component:llvm:clang
  - environment:msys2:ucrt64
  - environment:msys2:clang64
evidence_refs:
  - evidence:llvm:libcxx-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libc++

## Purpose

libc++ is the LLVM project's implementation of the C++ standard library,
and together with [libstdc++](LIBSTDCXX.md) it resolves the "C++ library"
row left open in the
[MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md). This page documents
a genuinely distinguishing packaging fact: libc++ is available across
GCC-oriented and LLVM-oriented environments alike, not confined to
CLANG64; see the [official libc++ project site](https://libcxx.llvm.org/)
for the API reference.

## Architectural Classification

`library:llvm:libc++` is a C++ standard library implementation developed by
the LLVM Project. This page cites the UCRT64 package,
`package:msys2:mingw-w64-ucrt-x86_64-libc++` (version `22.1.8-1`, license
`Apache-2.0 WITH LLVM-exception`); separate `mingw-w64-clang-x86_64-libc++`
and `mingw-w64-x86_64-libc++` packages exist for CLANG64 and MINGW64
respectively (`claim:library:libcxx:cross-environment-availability`). This
page is scoped to Volume 6's package/dependency-level evidence; the fuller
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology (headers, `pkg-config`/CMake metadata, PE import/export
analysis) has not been applied here and remains open, per the Evidence
section below.

## Responsibilities

- Implementing the C++ standard library API surface as an alternative to
  [libstdc++](LIBSTDCXX.md), usable by [Clang](CLANG.md) (and, in this
  environment, by [GCC](GNU-GCC.md) as well) via an explicit opt-in flag.

## Boundaries

libc++ is packaged standalone, unlike [libstdc++](LIBSTDCXX.md)'s
bundled-in-gcc-libs packaging. Being installed does not make it the
default: [GCC](GNU-GCC.md) links against [libstdc++](LIBSTDCXX.md) by
default and [Clang](CLANG.md) links against libc++ by default in this
environment's CLANG64 configuration, per the
[MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md); using the
non-default pairing requires explicit compiler flags this page does not
enumerate.

## Interfaces

- The full ISO C++ standard library API surface, the same standard
  libstdc++ implements, per the documentation. This page does not
  enumerate the header-level surface; that belongs to
  [Header and Development-Metadata Indexes](HEADER-AND-METADATA-INDEXES.md).

## Dependencies

The catalog snapshot shows an environment-dependent dependency structure
for libc++, precisely reflecting where a GCC runtime package does and does
not exist (`claim:library:libcxx:cc-libs-capability`):

| Environment | Dependency | Architectural reason |
| --- | --- | --- |
| UCRT64 | `mingw-w64-ucrt-x86_64-cc-libs` (a virtual capability [gcc-libs](LIBSTDCXX.md#dependencies) provides) | libc++ still needs low-level compiler runtime support (exception-handling personality routines from `libgcc`) even though it replaces libstdc++'s C++-specific implementation. |
| CLANG64 | `mingw-w64-clang-x86_64-libunwind` directly, and the package itself `provides` the `gcc-libs`/`cc-libs` capability | CLANG64 has no separate GCC runtime package at all; libc++ (paired with LLVM's libunwind for stack unwinding) is what satisfies that capability for any other CLANG64 package declaring a `cc-libs` dependency. |

## Reverse Dependencies

The UCRT64 package records 3 relationships targeting it in this snapshot —
far fewer than [libstdc++](LIBSTDCXX.md#reverse-dependencies)'s 167,
reflecting that libstdc++ remains the default and far more widely
consumed C++ library in this environment even though libc++ is installable
alongside it. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Selecting libc++ over the default C++ library is a compiler-flag decision
(for example, Clang's `-stdlib=libc++`) made per build, not a persistent
configuration file; this page does not enumerate those flags.

## Initialization and Execution Flow

As a library rather than a standalone program, libc++ has no independent
process lifecycle: it is linked into and initializes within the process of
whatever program links against it, the same model documented for
[libstdc++](LIBSTDCXX.md#initialization-and-execution-flow).

## Runtime Behavior

libc++'s runtime behavior is exercised only by programs explicitly built
against it; in this environment that is the default outcome for CLANG64
builds and an opt-in outcome for UCRT64/MINGW64 builds, per Boundaries
above.

## Compatibility and Variants

libc++ and [libstdc++](LIBSTDCXX.md) both implement the C++ standard
library API, but object files and static libraries built against one are
not link-compatible with the other without rebuilding
(`relationship:cxx-library:libcxx-compatible-with-libstdcxx`), the same
fact stated from libstdc++'s side. Its cross-environment availability
(UCRT64 and MINGW64 alongside CLANG64) means the CRT/architecture axis and
the C++-library axis are independently selectable within a GCC-oriented
environment, a nuance the environment-comparison table in
[Runtime Environments](RUNTIME-ENVIRONMENTS.md) does not itself spell out
at this level of detail.

## Security Considerations

No libc++-specific vulnerability review has been performed for this
volume; see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. Its smaller reverse-dependency
footprint in this snapshot means a defect here has a narrower observed
blast radius than [libstdc++](LIBSTDCXX.md#security-considerations)'s, though
that reflects current adoption in this snapshot, not a structural property
of the library itself.

## Failure Modes and Diagnostics

Attempting to link objects built with `-stdlib=libc++` against objects
built against the default libstdc++ (or vice versa) is the most likely
failure mode; per Compatibility and Variants, rebuilding consistently
against one C++ library is the documented resolution.

## Evidence, Assumptions, and Open Questions

The environment-dependent dependency structure and cross-environment
packaging are backed by the pacman catalog snapshot
(`evidence:catalog:current`) via `claim:library:libcxx:cc-libs-capability`
and `claim:library:libcxx:cross-environment-availability`; the library's
general architecture is backed by the official libc++ project site
(`evidence:llvm:libcxx-manual-2026-07-30`). Open, and explicitly out of
scope for this page: header-level API surface, `pkg-config`/CMake metadata,
and PE import/export-level ABI evidence, which the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology calls for and which this page does not attempt to supply.

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libstdc++](LIBSTDCXX.md)
- [Clang](CLANG.md)
