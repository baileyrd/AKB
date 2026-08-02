---
id: doc:volume-6:pcre2
title: PCRE2
volume: 6
status: partial
model_refs:
  - library:pcre:pcre2
  - package:msys2:mingw-w64-ucrt-x86_64-pcre2
  - library:gnu:zlib
  - library:mingweditline:wineditline
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:pcre:pcre2-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# PCRE2

## Purpose

PCRE2 implements Perl 5-style regular expressions as a library, and it is
the engine already cited as backing the `-P`/`--perl-regexp` matching
modes documented for [GNU Grep](GNU-GREP.md#dependencies) and
[less](LESS.md#dependencies) (both of which depend on the MSYS-environment
`libpcre2_8` package rather than this UCRT64 build, per Boundaries, now
documented on its own page, [PCRE2 (MSYS)](PCRE2-MSYS.md)). This
page documents its architectural role; see the
[official PCRE2 project site](https://pcre.org/) for the pattern-syntax
reference.

## Architectural Classification

`library:pcre:pcre2` is packaged per native environment: this page cites
the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-pcre2` (version
`10.47-1` in the current catalog snapshot, license `BSD-3-Clause`),
originally authored by Philip Hazel. PCRE2 is the successor API to the
original PCRE library; MSYS2 packages both, and this page covers PCRE2
only.

## Responsibilities

- Providing Perl-compatible regular-expression matching as a linked
  library, plus a bundled `pcre2grep` command-line tool and `pcre2test`
  interactive test harness.

## Boundaries

This UCRT64 `pcre2` package is a distinct catalog entity from the
MSYS-environment `libpcre2_8` package that [GNU Grep](GNU-GREP.md#dependencies)
and [less](LESS.md#dependencies) actually depend on, documented on
[PCRE2 (MSYS)](PCRE2-MSYS.md) — the same upstream PCRE2 project, packaged
separately per environment, the same pattern already documented for
[zlib](ZLIB.md) and other libraries in this volume. This page does not
claim those two tools depend on this specific UCRT64 package.

## Interfaces

- The `pcre2_*` C API (`pcre2_compile`, `pcre2_match`) for embedding
  Perl-compatible regex matching in a program, per the documentation.

## Dependencies

The catalog snapshot records three `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-pcre2`:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Compression | `mingw-w64-ucrt-x86_64-zlib` | Backs `pcre2grep`'s support for searching gzip-compressed files, the same `zgrep`-style composition pattern documented for [GNU Gzip](GNU-GZIP.md#dependencies). |
| Interactive line editing | `mingw-w64-ucrt-x86_64-wineditline` | Backs interactive line editing in the bundled `pcre2test` tool, a Windows port of the BSD editline library serving a comparable role to [GNU Readline](GNU-READLINE.md) elsewhere in this volume (`claim:library:pcre2-wineditline-interactive-tool`). Documented fully in [WinEditLine](WINEDITLINE.md). |
| Compression (bzip2) | `mingw-w64-ucrt-x86_64-bzip2` | Backs `pcre2grep`'s support for searching bzip2-compressed files; this is a separate UCRT64 `bzip2` package, distinct from the MSYS-environment `bzip2` component already documented in Volume 5. **Correction, 2026-08-02**: this dependency is now formally modeled as [bzip2 (UCRT64)](BZIP2-UCRT64.md) (`relationship:foundation-libraries:pcre2-requires-bzip2-ucrt64`); it had previously only been cited here by package name. |

## Reverse Dependencies

The snapshot records 35 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-pcre2`. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

PCRE2 has no persistent configuration file; pattern-compilation options
(case sensitivity, multiline mode, Unicode support) are set through its C
API at compile time for each pattern.

## Initialization and Execution Flow

As a library, PCRE2 has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it, the
same model documented for [zlib](ZLIB.md#initialization-and-execution-flow).
The bundled `pcre2grep` and `pcre2test` tools are separate invoke-run-exit
processes.

## Runtime Behavior

Pattern compilation and matching are separate steps in PCRE2's API; a
program that recompiles the same pattern repeatedly rather than caching
the compiled form pays an avoidable performance cost, a documented general
characteristic of the library's design rather than a defect.

## Compatibility and Variants

PCRE2 (this package) and the original PCRE library are separate,
API-incompatible generations MSYS2 packages independently; software
written against one does not automatically build against the other
without porting.

## Security Considerations

Compiling and matching patterns derived from untrusted input carries the
same general catastrophic-backtracking risk already noted for
[GNU Grep](GNU-GREP.md#security-considerations)'s `-P` mode, which this
library's engine backs. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `10.47-1` version.

## Failure Modes and Diagnostics

Pattern-compilation errors are reported through PCRE2's own error-code API
with a byte-offset into the pattern string; a dependent tool's regex
failure should first be checked against the exact pattern syntax being
used before assuming a library defect.

## Evidence, Assumptions, and Open Questions

Pattern-matching behavior is backed by the official PCRE2 project site
(`evidence:pcre:pcre2-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:mingw-w64-ucrt-x86_64-pcre2` in the
catalog. Package identity, version, license, and all three dependency
edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`) via
`claim:library:pcre2-wineditline-interactive-tool`. Open, and explicitly
out of scope for this page: header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU Grep](GNU-GREP.md)
- [less](LESS.md)
- [GNU Readline](GNU-READLINE.md)
- [zlib](ZLIB.md)
- [libarchive](LIBARCHIVE.md)
- [WinEditLine](WINEDITLINE.md)
- [PCRE2 (CLANG64)](PCRE2-CLANG64.md)
- [PCRE2 (MSYS)](PCRE2-MSYS.md)
- [bzip2 (UCRT64)](BZIP2-UCRT64.md)
