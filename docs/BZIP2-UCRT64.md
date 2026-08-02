---
id: doc:volume-6:bzip2-ucrt64
title: bzip2 (UCRT64)
volume: 6
status: partial
model_refs:
  - library:bzip2:bzip2@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-bzip2
  - library:pcre:pcre2
  - library:libarchive:libarchive
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:bzip2:project-site-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# bzip2 (UCRT64)

## Purpose

This page documents `package:msys2:mingw-w64-ucrt-x86_64-bzip2`, the
UCRT64-environment build of bzip2 — the Burrows-Wheeler compression
codec. Unlike the MSYS environment's CLI/`libbz2` split (see
[bzip2 (MSYS)](BZIP2.md) and [libbz2](LIBBZ2.md)), this UCRT64
package bundles both the CLI tool and its library together in one
package, the same non-split pattern documented for
[bzip2 (CLANG64)](BZIP2-CLANG64.md). This page closes a gap both
[PCRE2](PCRE2.md#dependencies) and [libarchive](LIBARCHIVE.md#dependencies)
had already cited by package name but left unmodeled as a formal
entity. See the
[official bzip2 project site](https://sourceware.org/bzip2/) for the
full reference.

## Architectural Classification

`library:bzip2:bzip2@ucrt64` is packaged as
`package:msys2:mingw-w64-ucrt-x86_64-bzip2` (version `1.0.8-3` in the
current catalog snapshot, license `custom`), authored by Julian
Seward. It belongs to the UCRT64 environment.

## Responsibilities

- Providing Burrows-Wheeler compression and decompression as both a
  linked library and a CLI tool, consumed by
  [PCRE2](PCRE2.md#dependencies) and [libarchive](LIBARCHIVE.md#dependencies).

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[bzip2 (MSYS)](BZIP2.md) and [libbz2](LIBBZ2.md) instead serve
MSYS-environment consumers as a split CLI/library pair, while
[bzip2 (CLANG64)](BZIP2-CLANG64.md) serves CLANG64-environment
consumers as a separate, non-interchangeable catalog entity — the same
distinction already drawn throughout this volume for MSYS/UCRT64/CLANG64
sibling packages.

## Interfaces

- The bzip2 C API (`BZ2_bzCompress`, `BZ2_bzDecompress`, and related
  functions), the same interface [libbz2](LIBBZ2.md#interfaces) and
  [bzip2 (CLANG64)](BZIP2-CLANG64.md#interfaces) document, per the
  documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-bzip2` beyond standard toolchain
runtime support.

## Reverse Dependencies

The catalog snapshot records 46 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-bzip2`. Two are now modeled in
this knowledge base: [PCRE2](PCRE2.md)
(`relationship:foundation-libraries:pcre2-requires-bzip2-ucrt64`,
added 2026-08-02 — backing `pcre2grep`'s support for searching
bzip2-compressed files) and [libarchive](LIBARCHIVE.md)
(`relationship:foundation-libraries:libarchive-requires-bzip2-ucrt64`,
added 2026-08-02 — backing the bzip2 compression filter within
libarchive's supported archive formats). The remaining ~44 recorded
dependents (a broad mix of UCRT64 packages including `adios2`,
`arrow`, `boost-libs`, `ffmpeg`, and many others) are not individually
modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

bzip2 has no persistent configuration file; behavior is controlled
entirely through command-line flags or its C API by the calling
program.

## Initialization and Execution Flow

The CLI is an invoke-run-exit process; the library has no independent
process lifecycle and instead initializes and executes within the
process of whatever program links against it — PCRE2 or libarchive in
this dependency chain. As a native MinGW-w64 package, this process
model is Windows-facing directly rather than mediated by
`msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [bzip2 (MSYS)](BZIP2.md#runtime-behavior),
[libbz2](LIBBZ2.md#runtime-behavior), and
[bzip2 (CLANG64)](BZIP2-CLANG64.md#runtime-behavior); see those pages
for detail not specific to the UCRT64 packaging distinction.

## Compatibility and Variants

The UCRT64 package bundles CLI and library together, matching the
[CLANG64](BZIP2-CLANG64.md) packaging but unlike the MSYS environment's
split; the compressed `.bz2` format itself is portable across all
packagings.

## Security Considerations

Decompressing an untrusted bzip2 stream carries the same general
decompression-scale risk documented for
[bzip2 (MSYS)](BZIP2.md#security-considerations); see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `1.0.8-3` version.

## Failure Modes and Diagnostics

A dependent program's bzip2 decompression failure should be checked
against the input data's actual bzip2-format validity before being
treated as a defect in the consuming program.

## Evidence, Assumptions, and Open Questions

The compression model is backed by the official bzip2 project site
(`evidence:bzip2:project-site-2026-07-30`), the same evidence record
[bzip2 (MSYS)](BZIP2.md) cites. Package identity, version, license, and
both recorded dependent edges are backed by the pacman catalog
snapshot (`evidence:catalog:current`). Open: the ~44 remaining recorded
reverse dependents are not individually modeled in this knowledge
base.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [bzip2 (MSYS)](BZIP2.md)
- [libbz2](LIBBZ2.md)
- [bzip2 (CLANG64)](BZIP2-CLANG64.md)
- [PCRE2](PCRE2.md)
- [libarchive](LIBARCHIVE.md)
