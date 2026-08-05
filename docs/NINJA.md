---
id: doc:volume-8:ninja
title: Ninja
volume: 8
status: partial
model_refs:
  - component:ninja-build:ninja
  - package:msys2:mingw-w64-ucrt-x86_64-ninja
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:ninja-build:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Ninja

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `component:ninja-build:ninja` |
| Kind | `component` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Evan Martin / Ninja community |
| Environments | `ucrt64` |
| Upstream | <https://ninja-build.org> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-ninja` |
| Version (observed) | 1.13.2-1 |
| License (observed) | spdx:Apache-2.0 |
| Architecture (observed) | any |
| Installed size (observed) | 421.17 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:ninja-build:manual-2026-07-30` — Ninja Manual (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Ninja is a small, fast build-file executor: it runs the exact commands
listed in a generated `build.ninja` file, and this page documents it first
among the build-system tools in this batch because both [CMake](CMAKE.md)
and [Meson](MESON.md) depend on it as their build backend. See the
[official Ninja manual](https://ninja-build.org/manual.html) for the
`build.ninja` file format reference.

## Architectural Classification

`component:ninja-build:ninja` is packaged per native environment: this page
cites the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-ninja`
(version `1.13.2-1` in the current catalog snapshot, license
`Apache-2.0`), originally authored by Evan Martin. It belongs to the UCRT64
environment and, like the rest of this volume's toolchain components, does
**not** depend on `msys-2.0.dll`, per the
[MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).

## Responsibilities

- Executing the exact build steps listed in a `build.ninja` file, with
  dependency-graph-based incremental rebuilds and parallel execution.

## Boundaries

Ninja deliberately does not generate its own build rules: it is designed to
be the fast execution target for a higher-level generator such as
[CMake](CMAKE.md) or [Meson](MESON.md), which produce the `build.ninja`
file it consumes. Hand-writing `build.ninja` files is possible but is a
documented minority use case, not Ninja's primary design intent.

## Interfaces

- The `ninja` command reading `build.ninja` from the current directory by
  default, with flags for parallelism (`-j`), specific targets, and a
  build-log/dependency database it maintains for incremental builds, per
  the manual.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-ninja`: `mingw-w64-ucrt-x86_64-cc-libs`,
the standard GCC-toolchain runtime libraries needed by any C++ program
built in this environment — Ninja itself is implemented in C++, and this is
its only dependency, consistent with its documented minimalism.

## Reverse Dependencies

The snapshot records 6 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-ninja`, including both
[CMake](CMAKE.md)'s and [Meson](MESON.md)'s invocation dependencies
(`relationship:toolchain:cmake-invokes-ninja`,
`relationship:toolchain:meson-invokes-ninja`). See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Ninja has no persistent configuration file beyond the `build.ninja` file
itself, which is treated as generated input rather than hand-maintained
configuration in the normal (CMake/Meson-driven) workflow.

## Initialization and Execution Flow

Ninja is ordinarily invoked as a backend subprocess by
[CMake](CMAKE.md#initialization-and-execution-flow) or
[Meson](MESON.md#initialization-and-execution-flow) after those tools
generate its input file, rather than run as the first step of a build. As a
native MinGW-w64 program, its process model is Windows-facing directly
rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Ninja's incremental-rebuild correctness depends entirely on the accuracy of
the dependency graph in the `build.ninja` file it was given; Ninja itself
does not discover dependencies, it only acts on what its generator declared
— a deliberate design boundary, not a limitation to work around.

## Compatibility and Variants

`build.ninja`'s file format is intentionally simple and stable, allowing
multiple independent generators ([CMake](CMAKE.md), [Meson](MESON.md), and
others outside this batch such as GN) to target it without coordinating
with each other, per the manual's stated design goals.

## Security Considerations

Ninja executes exactly the commands listed in its input file with no
additional sandboxing; a `build.ninja` file generated from an untrusted or
compromised project configuration can run arbitrary commands, the same
general risk class as any build-execution tool. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review has
been performed for the recorded `1.13.2-1` version.

## Failure Modes and Diagnostics

A stale or incorrect `build.ninja` file (for example, after manually
editing source files a generator didn't detect) is the most common source
of confusing incremental-build behavior; regenerating via
[CMake](CMAKE.md) or [Meson](MESON.md) rather than editing `build.ninja` by
hand is the documented resolution path.

## Evidence, Assumptions, and Open Questions

Design goals and file-format behavior are backed by the official Ninja
manual (`evidence:ninja-build:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-ninja` in the catalog. Package
identity, version, license, and its single dependency edge are backed by
the pacman catalog snapshot (`evidence:catalog:current`). No open items
beyond the general version-qualified security review noted above.

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [CMake](CMAKE.md)
- [Meson](MESON.md)
- [pkgconf](PKGCONF.md)
