---
id: doc:volume-6:expat-clang64
title: Expat (CLANG64)
volume: 6
status: partial
model_refs:
  - library:libexpat:expat@clang64
  - package:msys2:mingw-w64-clang-x86_64-expat
  - library:libarchive:libarchive@clang64
  - environment:msys2:clang64
evidence_refs:
  - evidence:libexpat:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Expat (CLANG64)

## Purpose

This page documents `package:msys2:mingw-w64-clang-x86_64-expat`, the
CLANG64-environment build of Expat — a full-featured XML parsing
library, depended on by [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
for XML-based archive format support (e.g. xar). Unlike the MSYS
environment — which packages both `expat` and `libexpat` as two
distinct catalog packages, only the latter modeled on
[Expat (MSYS)](EXPAT-MSYS.md) — the CLANG64 environment packages only
`expat`, matching the naming already established for
[Expat (UCRT64)](EXPAT.md). See the
[official Expat project page](https://libexpat.github.io/) for the
full reference.

## Architectural Classification

`library:libexpat:expat@clang64` is packaged as
`package:msys2:mingw-w64-clang-x86_64-expat` (version `2.8.2-1` in the
current catalog snapshot, license `MIT`) — a separately built, separate
catalog entity from [Expat (UCRT64)](EXPAT.md) and
[Expat (MSYS)](EXPAT-MSYS.md). It belongs to the CLANG64 environment.

## Responsibilities

- Providing XML parsing functionality, consumed by
  [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md#dependencies) for
  XML-based archive format support, the same functional role
  [Expat (UCRT64)](EXPAT.md) documents in a general sense for its own
  environment's consumers.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[LLDB](LLDB.md) instead depends on
[libxml2 (CLANG64)](LIBXML2-CLANG64.md) for its own XML needs, a
different XML library entirely, matching the same
per-consumer-library-choice pattern already documented throughout this
volume.

## Interfaces

- The Expat C API (`XML_ParserCreate`, `XML_Parse`, and related
  functions), the same interface [Expat (UCRT64)](EXPAT.md#interfaces)
  documents, per the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-expat` beyond standard toolchain
runtime support.

## Reverse Dependencies

The catalog snapshot records 38 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-expat`. One is now modeled in
this knowledge base: [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
(`relationship:foundation-libraries:libarchive-clang64-requires-expat-clang64`,
added 2026-08-02). The remaining ~37 recorded dependents (a broad mix
of CLANG64 packages including `apr-util`, `cmake` — the separate
CLANG64 `cmake` package, distinct from the UCRT64 `cmake` package
[CMake's own page](CMAKE.md) documents — `dbus-c++`, `exiv2`, and many
others) are not individually modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Expat has no persistent configuration file; parsing behavior is set
entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, Expat has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md) in this
dependency chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [Expat (UCRT64)](EXPAT.md#runtime-behavior);
see that page for detail not specific to the CLANG64/UCRT64 packaging
distinction.

## Compatibility and Variants

The CLANG64, UCRT64, and MSYS Expat packages are separately versioned
catalog entities (see Architectural Classification); code built
against one is not automatically compatible with another without
matching the correct package/environment.

## Security Considerations

Parsing untrusted XML input is a documented general source of parser
vulnerabilities (XXE, entity expansion); this page does not assert
this specific package version's mitigation status. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `2.8.2-1` version.

## Failure Modes and Diagnostics

A dependent program's XML parsing failure should be checked against
the input data's actual XML well-formedness before being treated as an
Expat defect.

## Evidence, Assumptions, and Open Questions

XML parsing library scope is backed by the official Expat project page
(`evidence:libexpat:manual-2026-07-30`), the same evidence record
[Expat (UCRT64)](EXPAT.md) cites. Package identity, version, license,
and the recorded dependent edge are backed by the pacman catalog
snapshot (`evidence:catalog:current`). Open: the ~37 remaining recorded
reverse dependents are not individually modeled in this knowledge
base.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [Expat (UCRT64)](EXPAT.md)
- [Expat (MSYS)](EXPAT-MSYS.md)
- [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
