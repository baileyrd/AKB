---
id: doc:volume-6:pcre2-msys
title: PCRE2 (MSYS)
volume: 6
status: partial
model_refs:
  - library:pcre:pcre2@msys
  - package:msys2:libpcre2_8
  - component:git:git
  - component:greenwood:less
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:pcre:pcre2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# PCRE2 (MSYS)

## Purpose

This page documents the **MSYS-environment** PCRE2 package
(`libpcre2_8`) specifically — a library implementing Perl-compatible
regular expressions — as a distinct catalog entity from this knowledge
base's existing [PCRE2 (UCRT64)](PCRE2.md) page: Git's `git grep
--perl-regexp` and less's search functionality both link against this
MSYS package, already cited by package name on
[GIT-MSYS-PACKAGE.md](GIT-MSYS-PACKAGE.md#dependencies) and
[LESS.md](LESS.md#dependencies) before this page existed. See the
[official PCRE project site](https://www.pcre.org/) for the full
reference shared with the UCRT64 package.

## Architectural Classification

`library:pcre:pcre2@msys` is packaged in the MSYS environment as
`package:msys2:libpcre2_8` (version `10.47-1` in the current catalog
snapshot) — a separately versioned catalog entity from
[PCRE2 (UCRT64)](PCRE2.md)'s `mingw-w64-ucrt-x86_64-pcre2` package. This
is the package [Git](GIT-MSYS-PACKAGE.md) and
[less](LESS.md) — both MSYS-environment components themselves — actually
depend on, the same MSYS-vs-native distinction applied consistently
throughout this volume.

## Responsibilities

- Implementing Perl-compatible regular expression matching, consumed by
  [Git's](GIT-MSYS-PACKAGE.md) `--perl-regexp` matching mode and by
  [less's](LESS.md) search functionality.

## Boundaries

This page's package implements PCRE2 (the current, actively developed
generation of the PCRE library) specifically; a separate, older PCRE1
package also exists in the MSYS environment, documented on
[PCRE (MSYS)](PCRE-MSYS.md) — the two are not interchangeable, and
[GNU Grep's](GNU-GREP.md) own `-P` engine depends on that older PCRE1
package instead of this one.

## Interfaces

- The PCRE2 C API (`pcre2_compile`, `pcre2_match`), the same 8-bit
  code-unit build (`libpcre2_8`, as opposed to the 16-bit or 32-bit
  variants PCRE2 also offers) [PCRE2 (UCRT64)](PCRE2.md) documents, per
  the documentation.

## Dependencies

The MSYS `package:msys2:libpcre2_8` declares a dependency on `gcc-libs`
only — the standard GCC runtime support libraries, not a library-family
dependency distinct enough to warrant its own page in this volume.

## Reverse Dependencies

The catalog snapshot records 12 relationships targeting
`package:msys2:libpcre2_8`: `package:msys2:git`
(`relationship:ssh-curl-git:git-requires-pcre2-msys` in this knowledge
base's graph), `package:msys2:less`
(`relationship:editors-pagers-terminals:less-requires-pcre2-msys`),
`package:msys2:ctags`, `package:msys2:fish`, `package:msys2:glib2`,
`package:msys2:libgit2`, its own `libpcre2posix` companion package and
`-devel` subpackage, `package:msys2:swig`, `package:msys2:wget`, and
`package:msys2:zsh`.

## Configuration

PCRE2 has no persistent configuration file; regex compilation options
are set entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, this package has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [Git](GIT-MSYS-PACKAGE.md) or [less](LESS.md) in this
dependency chain. As an MSYS-dependent library, this is adapted from
POSIX semantics onto Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Identical functional behavior to [PCRE2 (UCRT64)](PCRE2.md); see that
page for detail not specific to the MSYS/UCRT64 packaging distinction.

## Compatibility and Variants

The MSYS and native (UCRT64/CLANG64/i686) PCRE2 packages are separately
versioned catalog entities (see Architectural Classification); code
built against one is not automatically compatible with the other without
matching the correct environment.

## Security Considerations

Regular-expression evaluation against untrusted input is a documented
general source of denial-of-service risk (catastrophic backtracking);
this page does not assert this specific package version's mitigation
status. See [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `10.47-1` version.

## Failure Modes and Diagnostics

A `git grep --perl-regexp` or less search failure specific to regex
syntax should be checked against PCRE2 syntax documentation before being
treated as a Git or less defect.

## Evidence, Assumptions, and Open Questions

PCRE2 implementation scope is backed by the official PCRE project site
(`evidence:pcre:pcre2-manual-2026-07-30`), the same evidence record
[PCRE2 (UCRT64)](PCRE2.md) cites. Package identity, version, and the
recorded dependency/dependent edges are backed by the pacman catalog
snapshot (`evidence:catalog:current`). Open, and explicitly out of scope
for this page: header-level API surface and PE import/export-level
evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [Git (MSYS2 package)](GIT-MSYS-PACKAGE.md)
- [less](LESS.md)
- [PCRE2 (UCRT64)](PCRE2.md)
- [PCRE (MSYS)](PCRE-MSYS.md)
