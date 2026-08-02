---
id: doc:volume-6:pcre2-clang64
title: PCRE2 (CLANG64)
volume: 6
status: partial
model_refs:
  - library:pcre:pcre2@clang64
  - package:msys2:mingw-w64-clang-x86_64-pcre2
  - library:bzip2:bzip2@clang64
  - library:mingweditline:wineditline@clang64
  - library:gnu:zlib@clang64
  - library:libarchive:libarchive@clang64
  - library:gnu:ncurses@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:pcre:pcre2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# PCRE2 (CLANG64)

## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-pcre2`, the
CLANG64-environment build of PCRE2 — a library implementing Perl
5-style regular expressions. All three of its own recorded runtime
dependencies were modeled earlier in this same batch, letting this
addition close its full dependency footprint in a single pass. It is
in turn depended on by
[libarchive (CLANG64)](LIBARCHIVE-CLANG64.md#dependencies). See the
[official PCRE project site](https://pcre.org/) for the full
reference.

## Architectural Classification

`library:pcre:pcre2@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-pcre2` (version `10.47-1` in the
current catalog snapshot, license `BSD-3-Clause`) — a separately
built, separate catalog entity from [PCRE2 (UCRT64)](PCRE2.md) and
[PCRE2 (MSYS)](PCRE2-MSYS.md). It belongs to the CLANG64 environment.

## Responsibilities

- Providing Perl-compatible regular expression matching, consumed by
  [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md#dependencies) for its
  own filename-pattern matching logic, the same functional role
  [PCRE2 (UCRT64)](PCRE2.md#responsibilities) documents for its own
  environment's consumers.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[less](LESS.md) instead depends on
[PCRE2 (MSYS)](PCRE2-MSYS.md#reverse-dependencies) — the two are not
interchangeable, matching the same distinction already drawn
throughout this volume for MSYS/UCRT64/CLANG64 sibling packages.

## Interfaces

- The PCRE2 C API (`pcre2_compile`, `pcre2_match`, and related
  functions), the same interface [PCRE2 (UCRT64)](PCRE2.md#interfaces)
  documents, per the documentation.

## Dependencies

The catalog snapshot records three `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-pcre2`, all now modeled in this
knowledge base:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| [bzip2 (CLANG64)](BZIP2-CLANG64.md) | `package:msys2:mingw-w64-clang-x86_64-bzip2` | Backs bzip2-compressed test-data handling in pcre2's own build/test tooling. |
| [WinEditLine (CLANG64)](WINEDITLINE-CLANG64.md) | `package:msys2:mingw-w64-clang-x86_64-wineditline` | Backs interactive line editing for pcre2's own test/demo tooling on native Windows Console. |
| [zlib (CLANG64)](ZLIB-CLANG64.md) | `package:msys2:mingw-w64-clang-x86_64-zlib` | Backs compressed test-data handling in pcre2's own build/test tooling. |

## Reverse Dependencies

The catalog snapshot records 34 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-pcre2`. Two are now modeled in
this knowledge base: [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
(`relationship:foundation-libraries:libarchive-clang64-requires-pcre2-clang64`,
added 2026-08-02) and [ncurses (CLANG64)](NCURSES-CLANG64.md)
(`relationship:foundation-libraries:ncurses-clang64-requires-pcre2-clang64`,
added 2026-08-02). The remaining ~32 recorded dependents (a broad mix
of CLANG64 packages including `android-tools`, `crystal`, `ctags`,
`gdal`, `git` — a separate CLANG64-native git package, distinct from
this knowledge base's MSYS [Git](GIT-MSYS-PACKAGE.md) entity — and
many others) are not individually modeled in this knowledge base; see
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

PCRE2 has no persistent configuration file; regular-expression
compilation and matching behavior is set entirely through its C API by
the calling program.

## Initialization and Execution Flow

As a library, PCRE2 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md) in this
dependency chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to
[PCRE2 (UCRT64)](PCRE2.md#runtime-behavior); see that page for detail
not specific to the CLANG64/UCRT64 packaging distinction.

## Compatibility and Variants

The CLANG64, UCRT64, and MSYS PCRE2 packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with another without
matching the correct package/environment.

## Security Considerations

Applying an untrusted, adversarially crafted regular expression against
untrusted input is a documented general source of catastrophic
backtracking (ReDoS) risk for regex engines; this page does not assert
this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `10.47-1` version.

## Failure Modes and Diagnostics

A dependent program's pattern-matching failure should be checked
against the actual regular expression syntax and PCRE2 compile flags
in use before being treated as a PCRE2 defect.

## Evidence, Assumptions, and Open Questions

Perl-compatible regular expression scope is backed by the official
PCRE project site (`evidence:pcre:pcre2-manual-2026-07-30`), the same
evidence record [PCRE2 (UCRT64)](PCRE2.md) cites. Package identity,
version, license, and all three recorded dependency edges are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open: the
~33 remaining recorded reverse dependents are not individually modeled
in this knowledge base.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [PCRE2 (UCRT64)](PCRE2.md)
- [PCRE2 (MSYS)](PCRE2-MSYS.md)
- [bzip2 (CLANG64)](BZIP2-CLANG64.md)
- [WinEditLine (CLANG64)](WINEDITLINE-CLANG64.md)
- [zlib (CLANG64)](ZLIB-CLANG64.md)
- [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
