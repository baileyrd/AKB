---
id: doc:volume-8:lldb
title: LLDB
volume: 8
status: partial
model_refs:
  - component:llvm:lldb
  - package:msys2:mingw-w64-clang-x86_64-lldb
  - library:llvm:llvm-libs
  - library:llvm:clang-libs
  - library:gnu:zlib@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:llvm:lldb-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# LLDB

## Purpose

LLDB is the LLVM project's debugger, the default debugger for LLVM-oriented
MinGW-w64 environments. This page documents its architectural role and its
dependency footprint alongside [GDB](GNU-GDB.md), its GCC-oriented
counterpart; see the [official LLDB project site](https://lldb.llvm.org/)
for the full command reference.

## Architectural Classification

`component:llvm:lldb` is packaged per native environment: this page cites
the CLANG64 build, `package:msys2:mingw-w64-clang-x86_64-lldb` (version
`22.1.8-1` in the current catalog snapshot, license
`Apache-2.0 WITH LLVM-exception`). Per the
[MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md), it is the
LLVM-oriented debugger counterpart to [GDB](GNU-GDB.md)'s role in
GCC-oriented environments; debugger selection does not itself change a
program's ABI.

## Responsibilities

- Interactive and scripted debugging of native programs, with a Python
  scripting API mirroring the extensibility pattern documented for
  [GDB](GNU-GDB.md#responsibilities) (`claim:component:lldb:python-scripting`).

## Boundaries

LLDB inspects and controls target processes; it does not build them (that
is [Clang](CLANG.md)'s role). Like Clang and LLD, this CLANG64 package does
**not** depend on `msys-2.0.dll` as a native MinGW-w64 package, per the
[MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).

## Interfaces

- Command-line debugging commands broadly analogous in purpose to
  [GDB](GNU-GDB.md#interfaces)'s (breakpoints, stepping, expression
  evaluation) with LLDB's own command syntax, plus a Python scripting API,
  per the documentation.

## Dependencies

The catalog snapshot records six `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-lldb`:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Clang's own libraries | `mingw-w64-clang-x86_64-clang-libs` | LLDB reuses Clang's parsing/semantic-analysis libraries for expression evaluation during debugging sessions. Documented fully in [Clang libraries](CLANG-LIBS.md). |
| LLVM's shared libraries | `mingw-w64-clang-x86_64-llvm-libs` | The same LLVM infrastructure libraries documented as a dependency for [LLD](LLD.md#dependencies). Documented fully in [LLVM libraries](LLVM-LIBS.md). |
| XML parsing | `mingw-w64-clang-x86_64-libxml2` | Backs XML-format target descriptions and remote-protocol data, the same rationale documented for [GDB](GNU-GDB.md#dependencies)'s `expat` dependency, using a different XML library. |
| Scripting API | `mingw-w64-clang-x86_64-python` | Backs LLDB's Python scripting API (`claim:component:lldb:python-scripting`). |
| Compressed debug sections | `mingw-w64-clang-x86_64-xz`, `mingw-w64-clang-x86_64-zlib` | Back reading debug information compressed with either algorithm, the same rationale documented for [GDB](GNU-GDB.md#dependencies). Documented fully in [zlib (CLANG64)](ZLIB-CLANG64.md); the CLANG64 `xz` package is not individually modeled in this knowledge base. |

## Reverse Dependencies

The snapshot records 4 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-lldb`. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

LLDB supports a startup-command file analogous in role to
[GDB](GNU-GDB.md#configuration)'s `.gdbinit`, executed as LLDB commands
(optionally including Python) at startup, per the documentation.

## Initialization and Execution Flow

LLDB is a longer-lived interactive process for the duration of a debugging
session, the same lifecycle shape documented for
[GDB](GNU-GDB.md#initialization-and-execution-flow). As a native MinGW-w64
program, its own process model is Windows-facing directly rather than
mediated by `msys-2.0.dll`, per the Boundaries section above.

## Runtime Behavior

As with GDB, LLDB's ability to produce a full backtrace and variable
inspection depends on the target binary having been built with debug
information by [Clang](CLANG.md); this is a build-time prerequisite, not an
LLDB configuration option.

## Compatibility and Variants

LLDB's expression evaluator reusing Clang's own parsing libraries (via the
`clang-libs` dependency) is a notable architectural difference from
[GDB](GNU-GDB.md), which implements its own expression parser rather than
sharing a compiler frontend's; this is a documented design distinction
between the two debuggers, not a completeness gap in either.

## Security Considerations

No LLDB-specific vulnerability review has been performed for this volume;
see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE review
has been performed for the recorded `22.1.8-1` version.

## Failure Modes and Diagnostics

Missing debug information should be checked first, the same diagnostic
priority already documented for
[GDB](GNU-GDB.md#failure-modes-and-diagnostics), before treating unhelpful
backtraces as an LLDB defect.

## Evidence, Assumptions, and Open Questions

Command and scripting behavior are backed by the official LLDB project
site (`evidence:llvm:lldb-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:mingw-w64-clang-x86_64-lldb` in the
catalog. Package identity, version, license, and all recorded dependency
edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`) via `claim:component:lldb:python-scripting`.
Open: the exact Windows-debugging-API mechanism LLDB uses on this platform
has not been directly observed, the same open item already flagged for
[GDB](GNU-GDB.md#evidence-assumptions-and-open-questions).

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [Clang](CLANG.md)
- [LLD](LLD.md)
- [GDB](GNU-GDB.md)
- [LLVM libraries](LLVM-LIBS.md)
- [Clang libraries](CLANG-LIBS.md)
- [zlib (CLANG64)](ZLIB-CLANG64.md)
