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
last_verified: 2026-07-30
---

# MSYS2 Runtime Environment Comparison and Migration Matrix

## Purpose

This page compares the six modeled MSYS2 environments. It is a decision aid,
not an ABI-compatibility guarantee. Package names, installed artifacts, and
current tool versions belong to the generated inventory.

The [Level 4 environment matrix](../diagrams/level-4-environment-matrix.svg)
provides linked navigation for the architecture, CRT, and lifecycle axes.

The linked [Level 2 runtime and package flow](../diagrams/level-2-runtime-package-flow.svg)
shows where this comparison sits: repository metadata and package payloads are
handled from the MSYS control plane, then project into each native environment.

## Architectural Classification

| Environment | Prefix | Default toolchain | Architecture | C runtime | C++ library | Lifecycle |
| --- | --- | --- | --- | --- | --- | --- |
| MSYS | `/usr` | GCC | x86_64 | Cygwin-compatible runtime | libstdc++ | Active system environment |
| UCRT64 | `/ucrt64` | GCC | x86_64 | UCRT | libstdc++ | Default recommendation |
| CLANG64 | `/clang64` | LLVM/Clang + LLD | x86_64 | UCRT | libc++ | Active |
| CLANGARM64 | `/clangarm64` | LLVM/Clang + LLD | AArch64 | UCRT | libc++ | Active |
| MINGW64 | `/mingw64` | GCC | x86_64 | MSVCRT | libstdc++ | Deprecated by MSYS2 on 2026-03-15 |
| MINGW32 | `/mingw32` | GCC | i686 | MSVCRT | libstdc++ | In phase-out |

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

## Related Objects

- [Runtime observation contract](RUNTIME-OBSERVATION-CONTRACT.md)
- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Master volume index](MASTER-VOLUME-INDEX.md)
