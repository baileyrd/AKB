---
id: doc:volume-6:pcre-msys
title: PCRE (MSYS)
volume: 6
status: partial
model_refs:
  - library:pcre:pcre
  - package:msys2:libpcre
  - component:gnu:grep
  - library:pcre:pcre2@msys
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:pcre:pcre1-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# PCRE (MSYS)

## Purpose

This page documents the original PCRE library (commonly called PCRE1,
to distinguish it from its successor PCRE2) as packaged in the MSYS
environment — `libpcre`, depended on by
[GNU Grep's](GNU-GREP.md) `-P`/`--perl-regexp` matching engine, already
cited in [GNU-GREP.md's dependency table](GNU-GREP.md#dependencies) and
prose before this page existed. See the
[official PCRE project site](https://www.pcre.org/) for the full
reference.

## Architectural Classification

`library:pcre:pcre` is packaged in the MSYS environment as
`package:msys2:libpcre` (version `8.45-5` in the current catalog
snapshot) — the older, legacy PCRE1 generation, distinct from
[PCRE2 (MSYS)](PCRE2-MSYS.md)'s `libpcre2_8` package (also MSYS-packaged,
but a materially different code line) and from
[PCRE2 (UCRT64)](PCRE2.md)'s native package. This is the package
[GNU Grep](GNU-GREP.md#dependencies) actually depends on for its `-P`
engine.

## Responsibilities

- Implementing Perl-compatible regular expression matching (the original
  PCRE1 API), consumed by [GNU Grep's](GNU-GREP.md) `-P`/`--perl-regexp`
  matching engine.

## Boundaries

PCRE1 (this page) and PCRE2 (documented separately on
[PCRE2 (MSYS)](PCRE2-MSYS.md) and [PCRE2 (UCRT64)](PCRE2.md)) are
upstream-distinct code lines with different, non-drop-in-compatible APIs
— PCRE1 is in maintenance-only status upstream, with PCRE2 being the
actively developed successor; [GNU Grep's](GNU-GREP.md#compatibility-and-variants)
own page already notes this build depends on the older PCRE1 line
specifically, not an oversight this page repeats without comment.

## Interfaces

- The legacy PCRE1 C API (`pcre_compile`, `pcre_exec`), distinct from
  PCRE2's own API (`pcre2_compile`, `pcre2_match`) documented on
  [PCRE2 (MSYS)](PCRE2-MSYS.md#interfaces), per the documentation.

## Dependencies

The MSYS `package:msys2:libpcre` declares a dependency on `gcc-libs`
only — the standard GCC runtime support libraries, not a library-family
dependency distinct enough to warrant its own page in this volume.

## Reverse Dependencies

The catalog snapshot records 5 relationships targeting
`package:msys2:libpcre`: `package:msys2:grep`
(`relationship:gnu-userland:grep-requires-pcre` in this knowledge base's
graph), its own `libpcrecpp` and `libpcreposix` companion packages, and
its own `-devel` subpackage — the narrowest reverse-dependency footprint
of any library added in this batch, consistent with most other MSYS
consumers having already migrated to PCRE2.

## Configuration

PCRE1 has no persistent configuration file; regex compilation options
are set entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, this package has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [GNU Grep](GNU-GREP.md) in this dependency chain. As an
MSYS-dependent library, this is adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

PCRE1 is exercised only when `grep -P`/`--perl-regexp` is actually used;
grep's default (non-Perl) matching modes do not exercise this
dependency.

## Compatibility and Variants

PCRE1 is in maintenance-only status upstream; new regex-engine features
in PCRE2 are not backported to this line, a compatibility consideration
already flagged on [GNU Grep's own page](GNU-GREP.md#compatibility-and-variants).

## Security Considerations

Regular-expression evaluation against untrusted input is a documented
general source of denial-of-service risk (catastrophic backtracking);
this page does not assert this specific package version's mitigation
status, and PCRE1's maintenance-only upstream status is itself a
relevant consideration for long-term security-patch availability. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `8.45-5` version.

## Failure Modes and Diagnostics

A `grep -P` regex-syntax failure should be checked against PCRE1 syntax
documentation (which differs in some respects from PCRE2's) before being
treated as a GNU Grep defect.

## Evidence, Assumptions, and Open Questions

PCRE1 implementation scope is backed by the official PCRE project site
(`evidence:pcre:pcre1-manual-2026-07-30`). Package identity, version, and
the recorded dependency/dependent edges are backed by the pacman catalog
snapshot (`evidence:catalog:current`). Open, and explicitly out of scope
for this page: header-level API surface and PE import/export-level
evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU Grep](GNU-GREP.md)
- [PCRE2 (MSYS)](PCRE2-MSYS.md)
- [PCRE2 (UCRT64)](PCRE2.md)
