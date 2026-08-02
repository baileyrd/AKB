---
id: doc:volume-4:runtime-environments
title: MSYS2 Runtime Environment Comparison and Migration Matrix
volume: 4
status: partial
model_refs:
  - environment:msys2:msys
  - environment:msys2:ucrt64
  - environment:msys2:clang64
  - environment:msys2:clangarm64
  - environment:msys2:mingw64
  - environment:msys2:mingw32
evidence_refs:
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-08-02
---

# MSYS2 Runtime Environment Comparison and Migration Matrix

## Purpose

This page compares the six modeled MSYS2 environments. It is a decision aid,
not an ABI-compatibility guarantee. Package names, installed artifacts, and
current tool versions belong to the generated inventory.

The [Level 2 subsystem diagram](../diagrams/level-2.svg)
provides linked navigation for the architecture, CRT, and lifecycle axes.

The linked [Level 4 package diagram](../diagrams/level-4.svg)
shows where this comparison sits: repository metadata and package payloads are
handled from the MSYS control plane, then project into each native environment.

## Architectural Classification

Each environment has its own page covering the full attribute set — ABI,
compiler, runtime, CRT, linker, executable format, package repository,
strengths, weaknesses, compatibility, and migration strategy. This table is
the comparison; the pages are the architecture.

| Environment | Prefix | Default toolchain | Architecture | C runtime | C++ library | Packages | Lifecycle |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| [MSYS](ENVIRONMENT-MSYS.md) | `/usr` | GCC | x86_64 | Cygwin-compatible runtime | libstdc++ | 798 | Active system environment |
| [UCRT64](ENVIRONMENT-UCRT64.md) | `/ucrt64` | GCC | x86_64 | UCRT | libstdc++ | 3,898 | Default recommendation |
| [CLANG64](ENVIRONMENT-CLANG64.md) | `/clang64` | LLVM/Clang + LLD | x86_64 | UCRT | libc++ | 3,822 | Active |
| [CLANGARM64](ENVIRONMENT-CLANGARM64.md) | `/clangarm64` | LLVM/Clang + LLD | AArch64 | UCRT | libc++ | 3,779 | Active |
| [MINGW64](ENVIRONMENT-MINGW64.md) | `/mingw64` | GCC | x86_64 | MSVCRT | libstdc++ | 3,100 | Deprecated by MSYS2 on 2026-03-15 |
| [MINGW32](ENVIRONMENT-MINGW32.md) | `/mingw32` | GCC | i686 | MSVCRT | libstdc++ | 314 | In phase-out |

Package counts are from the current pacman catalog snapshot
(`evidence:catalog:current`). They are the clearest available signal of
where packaging effort sits: UCRT64 leads, MINGW64 trails the active
environments by about 20%, and MINGW32 carries 12× fewer packages than
UCRT64.

## Boundaries

MSYS is the POSIX-oriented system environment and is always present beneath
native environments. Native environments add their own prefix before `/usr`.
They are not interchangeable build targets: architecture, CRT, compiler,
linker, and C++ standard library are separate compatibility axes.

## Compatibility and Migration

| Situation | Target | Migration guidance |
| --- | --- | --- |
| New native x86_64 GCC project | UCRT64 | Default choice unless a project has a tested reason to retain a different ABI/toolchain. |
| New native x86_64 LLVM project | CLANG64 | Use when LLVM/LLD and libc++ are intended project dependencies. |
| Native Windows on ARM64 | CLANGARM64 | Build and validate separately for AArch64; do not reuse x86_64 objects. |
| Existing MINGW64 project | UCRT64 or CLANG64 | Rebuild all objects and static libraries; audit CRT crossings and third-party binary dependencies. |
| Existing MINGW32 project | Supported 64-bit target | Treat as a port: rebuild, reassess pointer-width assumptions, and retain a separate test matrix if 32-bit support is required. |
| Shell, pacman, POSIX tools | MSYS | Keep in MSYS unless the produced program is intentionally a native target. |

Do not link object files or static libraries across target/CRT boundaries.
DLLs using different CRTs may coexist only when they do not exchange CRT-owned
objects such as `FILE*` across their interface; this remains an integration
constraint to verify for each boundary.

## Evidence, Assumptions, and Open Questions

The environment properties and lifecycle labels above are based on the
[official MSYS2 environment documentation](https://www.msys2.org/docs/environments/),
retrieved 2026-07-28. Bounded local observations currently cover all six
modeled environment selections. They establish selected environment variables
and discovered tool identity only; CLANGARM64 target tools were not executable
on the x86_64 observation host. Per-package availability and exact tool
versions are time-sensitive and must be answered from a catalog or runtime
observation.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["MSYS"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `environment:msys2:msys` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS](ENVIRONMENT-MSYS.md)
- [UCRT64](ENVIRONMENT-UCRT64.md)
- [CLANG64](ENVIRONMENT-CLANG64.md)
- [CLANGARM64](ENVIRONMENT-CLANGARM64.md)
- [MINGW64](ENVIRONMENT-MINGW64.md)
- [MINGW32](ENVIRONMENT-MINGW32.md)
- [Runtime observation contract](RUNTIME-OBSERVATION-CONTRACT.md)
- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Master volume index](MASTER-VOLUME-INDEX.md)
