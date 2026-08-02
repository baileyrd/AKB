---
id: doc:volume-6:ncurses-clang64
title: ncurses (CLANG64)
volume: 6
status: partial
model_refs:
  - library:gnu:ncurses@clang64
  - package:msys2:mingw-w64-clang-x86_64-ncurses
  - component:gnu:ncurses
  - library:gnu:ncurses@ucrt64
  - library:pcre:pcre2@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:gnu:ncurses-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# ncurses (CLANG64)

## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-ncurses`,
the CLANG64-environment build of ncurses — the terminal-capability and
screen-handling library. This page closes a gap surfaced by a
triple-environment (MSYS/UCRT64/CLANG64) catalog scan: both
[ncurses (MSYS)](NCURSES.md) and [ncurses (UCRT64)](NCURSES-UCRT64.md)
were already modeled, but the CLANG64 sibling was not. See the
[official GNU Ncurses project site](https://www.gnu.org/software/ncurses/)
for the API and terminfo reference.

## Architectural Classification

`library:gnu:ncurses@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-ncurses` (version `6.6-4` in the
current catalog snapshot, license `MIT`) — a separately built, separate
catalog entity from both [ncurses (MSYS)](NCURSES.md)'s `ncurses`
package and [ncurses (UCRT64)](NCURSES-UCRT64.md)'s
`mingw-w64-ucrt-x86_64-ncurses` package, even though all three share
the same upstream project and license. It belongs to the CLANG64
environment.

## Responsibilities

- Providing a portable API for cursor positioning, screen updates,
  color, and keyboard input across different terminal types, the same
  functional role [ncurses (MSYS)](NCURSES.md#responsibilities) and
  [ncurses (UCRT64)](NCURSES-UCRT64.md#responsibilities) document for
  their own environments' consumers.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[ncurses (MSYS)](NCURSES.md#reverse-dependencies) and
[ncurses (UCRT64)](NCURSES-UCRT64.md#reverse-dependencies) instead
serve their own environments' consumers — the three are not
interchangeable, matching the same distinction already made throughout
this volume for MSYS/UCRT64/CLANG64 sibling triples.

## Interfaces

- The ncurses C API (cursor positioning, screen updates, color, and
  keyboard input functions), the same interface
  [ncurses (MSYS)](NCURSES.md#interfaces) and
  [ncurses (UCRT64)](NCURSES-UCRT64.md#interfaces) document, per the
  documentation.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-ncurses`:
[PCRE2 (CLANG64)](PCRE2-CLANG64.md) (regular-expression support,
`relationship:foundation-libraries:ncurses-clang64-requires-pcre2-clang64`,
added 2026-08-02, the same rationale already documented for
[ncurses (UCRT64)'s](NCURSES-UCRT64.md#dependencies) own PCRE2
dependency) and `mingw-w64-clang-x86_64-libsystre` — the latter not
individually modeled as a separate dependency edge from this entity in
this knowledge base, the same treatment
[ncurses (UCRT64)](NCURSES-UCRT64.md#dependencies) gives its own
`libsystre` sub-dependency.

## Reverse Dependencies

The catalog snapshot records 11 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-ncurses` — the same order of
magnitude as [ncurses (UCRT64)'s](NCURSES-UCRT64.md#reverse-dependencies)
own 11, and dramatically fewer than
[ncurses (MSYS)'s](NCURSES.md#reverse-dependencies) 40, reflecting that
most CLANG64-native programs are GUI- or toolchain-oriented rather than
terminal-UI programs, the same pattern already observed for the UCRT64
sibling. None of the 11 (`avrdude`, `bitwise`, `gdb`, `global`,
`gnucobol`, `notcurses`, `python`, and others) are individually
modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

ncurses has no persistent configuration file; behavior is controlled
through terminfo capability databases and the calling program's own API
usage, identical to [ncurses (MSYS)](NCURSES.md#configuration) and
[ncurses (UCRT64)](NCURSES-UCRT64.md#configuration).

## Initialization and Execution Flow

As a library, ncurses has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [ncurses (MSYS)](NCURSES.md#runtime-behavior)
and [ncurses (UCRT64)](NCURSES-UCRT64.md#runtime-behavior); see those
pages for detail not specific to the CLANG64 packaging distinction.

## Compatibility and Variants

The CLANG64, UCRT64, and MSYS ncurses packages are three separately
versioned catalog entities (see Architectural Classification); code
built against one is not automatically compatible with another without
matching the correct package/environment.

## Security Considerations

No ncurses-specific vulnerability review has been performed for this
volume; see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. No version-qualified
CVE review has been performed for the recorded `6.6-4` version.

## Failure Modes and Diagnostics

A CLANG64-native program's rendering failure should be checked against
the terminal's own terminfo entry before being treated as a defect in
that program or in ncurses itself, the same triage order applicable to
any ncurses-based program.

## Evidence, Assumptions, and Open Questions

Terminal-capability library scope is backed by the official GNU
Ncurses project site (`evidence:gnu:ncurses-manual-2026-07-30`), the
same evidence record [ncurses (MSYS)](NCURSES.md) and
[ncurses (UCRT64)](NCURSES-UCRT64.md) cite. Package identity, version,
license, and the recorded dependency edge are backed by the pacman
catalog snapshot (`evidence:catalog:current`). Open, and explicitly out
of scope for this page: the 11 recorded reverse dependents not
individually modeled, this package's own `libsystre` sub-dependency,
and header-level API surface / PE import/export-level evidence, per
the [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["ncurses (CLANG64)"]
    d0["PCRE2 (CLANG64)"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnu:ncurses@clang64` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [ncurses (MSYS)](NCURSES.md)
- [ncurses (UCRT64)](NCURSES-UCRT64.md)
- [PCRE2 (CLANG64)](PCRE2-CLANG64.md)
