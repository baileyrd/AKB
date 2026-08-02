---
id: doc:volume-18:developer-guide
title: MSYS2 Developer Guide
volume: 18
status: partial
model_refs:
  - environment:msys2:msys
  - environment:msys2:ucrt64
  - environment:msys2:clang64
  - environment:msys2:mingw64
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:msys2:creating-packages-2026-08-02
  - evidence:msys2:package-management-2026-08-02
  - evidence:msys2:environments-2026-07-28
  - evidence:msys2:porting-2026-08-02
last_verified: 2026-08-02
---

# MSYS2 Developer Guide

Volume 18 answers one question in five parts: **how should software be
selected, built, debugged, packaged, and migrated on MSYS2?**

This page is the entry point and covers **selection** — the choice that
constrains every later one. The other four parts:

| Part | Page |
| --- | --- |
| Build | [Building Software on MSYS2](DEVELOPER-BUILDING-SOFTWARE.md) |
| Debug | [Debugging on MSYS2](DEVELOPER-DEBUGGING.md) |
| Package | [Packaging for MSYS2](DEVELOPER-PACKAGING.md) |
| Migrate | [Migrating Between Environments](DEVELOPER-MIGRATION.md) |

## Who this volume is for

Someone writing or porting software that will run on Windows, who has
MSYS2 installed and has to decide what to target. It is not for someone
operating an MSYS2 installation — that is Volume 19 — and it is not about
this knowledge base's own tooling, which is
[AKB developer workflow](DEVELOPER-WORKFLOW.md)
in Volume 20.

## The one decision that matters

Every other decision in this volume follows from this one:

> **Does the program link `msys-2.0.dll`?**

MSYS2's own documentation draws the line in exactly those terms:

> `msys` software (from the `msys` repository) is software that depends on
> `msys-2.0.dll` and is very similar to Cygwin software […] Native Windows
> software (from this project's perspective) is software that doesn't
> depend on `msys-2.0.dll`.

Everything downstream follows:

| | MSYS side | Native side (UCRT64, CLANG64, MINGW64, MINGW32, CLANGARM64) |
| --- | --- | --- |
| Links `msys-2.0.dll` | Yes | No |
| POSIX API (`fork`, signals, PTYs, POSIX paths) | Emulated, available | Not available |
| Emulation cost | Paid — see [Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md) | Not paid |
| Ships to end users as a normal Windows program | No — carries the runtime | Yes |
| Package prefix | none (`bash`, `make`) | `mingw-w64-<arch>-` with a `ucrt`/`clang` secondary prefix |
| Linkable against the other side | No | No |

The last row is a hard constraint, stated upstream:

> You also can't link a `mingw` program against an `msys` library.

There is no partial answer. A program is on one side or the other, and
the two sides do not share libraries.

## Choosing a side

Upstream states the intended split directly:

> You should think of these two systems as separate where `msys` packages
> should generally only be build dependencies of `mingw` packages.

The set of things that legitimately belong on the MSYS side is described
upstream as "pretty small":

1. Essential POSIX infrastructure — `filesystem`, `msys2-runtime`.
2. The native toolchain itself — `gcc`, `binutils`, `gdb`.
3. Programs that are hard to port — `pacman`, `bash`, `automake`, `make`.
4. Gap-bridging programs — `mintty`, `winpty`.
5. Portable support programs kept there anyway — `python`, `man`, `vim`,
   `git` — and carefully chosen tools such as `mc`, `ssh`, `rsync`, `lftp`.

Upstream's own summary of the rule:

> if a program is needed to build native software, but is itself hard to
> port, it can be made into an `msys` package. Anything else needs to be
> done as a `mingw` package or vetted individually.

**Default to native.** Choose MSYS only if the program genuinely requires
POSIX semantics that the emulation provides and Windows does not, or if it
exists to support the build itself.

## Choosing among the native environments

Once "native" is settled, the remaining choice is which native
environment, and it is a C runtime and toolchain question rather than a
POSIX question. The per-environment detail lives in Volume 4:

- [UCRT64](ENVIRONMENT-UCRT64.md) — GCC against the Universal CRT. The
  current default recommendation for new work.
- [MINGW64](ENVIRONMENT-MINGW64.md) — GCC against `msvcrt.dll`. The
  historical default; choose it for compatibility with older expectations.
- [CLANG64](ENVIRONMENT-CLANG64.md) — Clang/LLVM against the UCRT, with
  LLD and libc++.
- [CLANGARM64](ENVIRONMENT-CLANGARM64.md) — the ARM64 target.
- [MINGW32](ENVIRONMENT-MINGW32.md) — 32-bit. Choose only when a 32-bit
  artifact is required.

The comparison table with all eleven attributes side by side is
[Runtime Environments](RUNTIME-ENVIRONMENTS.md).

## Detecting the side from inside the build

When a build system has to branch, the identifiers are documented
upstream. The important asymmetry: **MSYS2 presents itself as Cygwin to
most checks**, because it is a Cygwin fork.

| Identifier | True on | Used in |
| --- | --- | --- |
| `__MSYS__` | MSYS side only | C preprocessor |
| `__CYGWIN__` | MSYS side **and** Cygwin | C preprocessor |
| `__MINGW32__` | all native environments | C preprocessor |
| `__MINGW64__` | 64-bit native | C preprocessor |
| `_WIN32` / `_WIN64` | native (and MSVC) | C preprocessor |
| `x86_64-pc-cygwin` | 64-bit MSYS (current host triplet) | `configure`-style scripts |
| `x86_64-pc-msys` | 64-bit MSYS (older triplet) | `configure`-style scripts |
| `x86_64-w64-mingw32` | 64-bit native | `configure`-style scripts |
| `sys.platform == "cygwin"` | MSYS side | Python |
| `sys.platform == "win32"` | native | Python |

Two traps follow directly from that table:

- **A `__CYGWIN__` check does not distinguish MSYS2 from Cygwin.** Use
  `__MSYS__` when the difference matters. It usually does, because MSYS2
  diverges from Cygwin precisely in path translation and mount behavior.
- **The MSYS host triplet changed.** Scripts matching `*-pc-msys` will
  silently fail to match the newer `*-pc-cygwin` form. Match both.

## What this volume does not establish

- **No MSYS2 installation has ever been observed by this knowledge base.**
  Every command shown in Volume 18 comes from upstream documentation, not
  from a run on a host. The five bounded probes of 2026-07-30 established
  command outcomes for a narrow set of runtime behaviors and nothing about
  building.
- **`makepkg.conf` defaults for MSYS2 are not captured**, so the effective
  compiler flags, integrity-check algorithm, and package compression are
  unestablished here.
- **Toolchain version numbers are not pinned.** Where a version matters,
  check the installed package rather than trusting this page.

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

- [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)
- [Runtime Environments](RUNTIME-ENVIRONMENTS.md)
- [msys-2.0.dll](MSYS-2-0-DLL.md)
- [Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md)
