---
id: doc:volume-6:wineditline-clang64
title: WinEditLine (CLANG64)
volume: 6
status: partial
model_refs:
  - library:mingweditline:wineditline@clang64
  - package:msys2:mingw-w64-clang-x86_64-wineditline
  - library:pcre:pcre2@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:mingweditline:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# WinEditLine (CLANG64)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:mingweditline:wineditline@clang64` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | MinGW Editline project |
| Environments | `clang64` |
| Upstream | <https://mingweditline.sourceforge.io/> |
| Packaged as | `package:msys2:mingw-w64-clang-x86_64-wineditline` |
| Version (observed) | 2.208-1 |
| License (observed) | spdx:BSD-3-Clause |
| Architecture (observed) | any |
| Installed size (observed) | 237.72 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:mingweditline:manual-2026-07-30` — WinEditLine (official project page) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-wineditline`,
the CLANG64-environment build of WinEditLine — a native-Windows-Console
readline-style line-editing library, targeting the native Windows
console rather than the MSYS/POSIX-emulated terminal
[libedit](LIBEDIT.md) targets. It is depended on by
[PCRE2 (CLANG64)](PCRE2-CLANG64.md). See the
[official WinEditLine project page](https://mingweditline.sourceforge.io/)
for the full reference.

## Architectural Classification

`library:mingweditline:wineditline@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-wineditline` (version `2.208-1`
in the current catalog snapshot, license `BSD-3-Clause`) — a
separately built, separate catalog entity from
[WinEditLine (UCRT64)](WINEDITLINE.md). It belongs to the CLANG64
environment.

## Responsibilities

- Providing readline-style interactive line editing (history,
  keybindings) for CLANG64-native console programs, consumed by
  [PCRE2 (CLANG64)](PCRE2-CLANG64.md#dependencies) for its own
  interactive test/demo tooling, the same role
  [WinEditLine (UCRT64)](WINEDITLINE.md#responsibilities) documents for
  its own environment.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[PCRE2 (UCRT64)](PCRE2.md) instead depends on
[WinEditLine (UCRT64)](WINEDITLINE.md#reverse-dependencies) — the two
are not interchangeable, matching the same distinction already drawn
throughout this volume for MSYS/UCRT64/CLANG64 sibling packages.
WinEditLine targets the native Windows console specifically, distinct
from [libedit](LIBEDIT.md), which targets the MSYS/POSIX-emulated
terminal.

## Interfaces

- The editline-compatible C API (`readline`, `add_history`, and
  related functions), the same interface
  [WinEditLine (UCRT64)](WINEDITLINE.md#interfaces) documents, per the
  documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-wineditline` beyond standard
toolchain runtime support.

## Reverse Dependencies

The catalog snapshot records 3 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-wineditline`. One is now modeled
in this knowledge base: [PCRE2 (CLANG64)](PCRE2-CLANG64.md)
(`relationship:foundation-libraries:pcre2-clang64-requires-wineditline-clang64`,
added 2026-08-02). The remaining recorded dependents (`pcre`,
`sqlitestudio`) are not individually modeled in this knowledge base;
see the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

WinEditLine has no persistent configuration file; behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, WinEditLine has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [PCRE2 (CLANG64)](PCRE2-CLANG64.md) in this dependency
chain. As a native MinGW-w64 library, this process model is
Windows-facing directly, using the native Windows Console API rather
than being mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[WinEditLine (UCRT64)](WINEDITLINE.md#runtime-behavior); see that page
for detail not specific to the CLANG64/UCRT64 packaging distinction.

## Compatibility and Variants

The CLANG64 and UCRT64 WinEditLine packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with the other without
matching the correct environment.

## Security Considerations

No WinEditLine-specific vulnerability review has been performed for
this volume. See [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture; no version-qualified
CVE review has been performed for the recorded `2.208-1` version.

## Failure Modes and Diagnostics

Interactive line-editing failures (missing history, keybinding
inconsistencies) in a dependent program should be checked against the
native Windows Console configuration before being treated as a
WinEditLine defect.

## Evidence, Assumptions, and Open Questions

The line-editing scope is backed by the official WinEditLine project
page (`evidence:mingweditline:manual-2026-07-30`), the same evidence
record [WinEditLine (UCRT64)](WINEDITLINE.md) cites. Package identity,
version, license, and the recorded dependent edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open: the two
remaining recorded reverse dependents (`pcre`, `sqlitestudio`) are not
individually modeled in this knowledge base.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["WinEditLine (CLANG64)"]
    u0["PCRE2 (CLANG64)"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:mingweditline:wineditline@clang64` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [WinEditLine (UCRT64)](WINEDITLINE.md)
- [libedit](LIBEDIT.md)
- [PCRE2 (CLANG64)](PCRE2-CLANG64.md)
