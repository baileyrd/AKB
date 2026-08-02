---
id: doc:volume-6:lz4-ucrt64
title: LZ4 (UCRT64)
volume: 6
status: partial
model_refs:
  - library:lz4:lz4@ucrt64
  - package:msys2:mingw-w64-ucrt-x86_64-lz4
  - library:libarchive:libarchive
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:lz4:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# LZ4 (UCRT64)

## Purpose

This page documents `package:msys2:mingw-w64-ucrt-x86_64-lz4`, the
UCRT64-environment build of LZ4 — a very fast lossless compression
algorithm. Unlike the MSYS environment's CLI/`liblz4` split (see
[LZ4](LZ4.md) and [liblz4 (MSYS)](LIBLZ4-MSYS.md)), this UCRT64
package bundles both the CLI tool and its library together in one
package, the same non-split pattern documented for
[LZ4 (CLANG64)](LZ4-CLANG64.md). This page closes a gap
[libarchive](LIBARCHIVE.md#dependencies) had already cited by package
name but left unmodeled as a formal entity. See the
[official LZ4 project site](https://lz4.github.io/lz4/) for the
format and algorithm reference.

## Architectural Classification

`library:lz4:lz4@ucrt64` is packaged as
`package:msys2:mingw-w64-ucrt-x86_64-lz4` (version `1.10.0-1` in the
current catalog snapshot, license `BSD;GPL2`), authored by Yann
Collet. It belongs to the UCRT64 environment.

## Responsibilities

- Providing LZ4 compression and decompression as both a linked library
  and a CLI tool, consumed by
  [libarchive](LIBARCHIVE.md#dependencies) for the LZ4 compression
  filter.

## Boundaries

This page's package serves UCRT64-environment consumers specifically;
[LZ4 (MSYS)](LZ4.md) and [liblz4 (MSYS)](LIBLZ4-MSYS.md) instead serve
MSYS-environment consumers as a split CLI/library pair, while
[LZ4 (CLANG64)](LZ4-CLANG64.md) serves CLANG64-environment consumers
as a separate, non-interchangeable catalog entity — the same
distinction already drawn throughout this volume for MSYS/UCRT64/CLANG64
sibling packages.

## Interfaces

- The LZ4 C API (`LZ4_compress_default`, `LZ4_decompress_safe`, and
  related functions), the same interface
  [liblz4 (MSYS)](LIBLZ4-MSYS.md#interfaces) and
  [LZ4 (CLANG64)](LZ4-CLANG64.md#interfaces) document, per the
  documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-lz4` beyond standard toolchain
runtime support.

## Reverse Dependencies

The catalog snapshot records 25 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-lz4`. One is now modeled in this
knowledge base: [libarchive](LIBARCHIVE.md)
(`relationship:foundation-libraries:libarchive-requires-lz4-ucrt64`,
added 2026-08-02 — backing the LZ4 compression filter within
libarchive's supported archive formats). The remaining ~24 recorded
dependents (a broad mix of UCRT64 packages including `android-tools`,
`arrow`, `blosc`, `gdal`, and many others) are not individually
modeled in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

LZ4 has no persistent configuration file; behavior is controlled
entirely through command-line flags or its C API by the calling
program.

## Initialization and Execution Flow

The CLI is an invoke-run-exit process; the library has no independent
process lifecycle and instead initializes and executes within the
process of whatever program links against it —
[libarchive](LIBARCHIVE.md) in this dependency chain. As a native
MinGW-w64 package, this process model is Windows-facing directly
rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Identical functional behavior to [LZ4 (MSYS)](LZ4.md#runtime-behavior),
[liblz4 (MSYS)](LIBLZ4-MSYS.md#runtime-behavior), and
[LZ4 (CLANG64)](LZ4-CLANG64.md#runtime-behavior); see those pages for
detail not specific to the UCRT64 packaging distinction.

## Compatibility and Variants

The UCRT64 package bundles CLI and library together, matching the
[CLANG64](LZ4-CLANG64.md) packaging but unlike the MSYS environment's
split; the `.lz4` format itself is portable across all packagings.

## Security Considerations

Decompressing an untrusted `.lz4` stream carries the same general
decompression-scale risk documented for
[LZ4 (MSYS)](LZ4.md#security-considerations); see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `1.10.0-1` version.

## Failure Modes and Diagnostics

A dependent program's LZ4 decompression failure should be checked
against the input data's actual LZ4-format validity before being
treated as a defect in the consuming program.

## Evidence, Assumptions, and Open Questions

The compression model is backed by the official LZ4 project site
(`evidence:lz4:manual-2026-07-30`), the same evidence record
[LZ4](LZ4.md) cites. Package identity, version, license, and the
recorded dependent edge are backed by the pacman catalog snapshot
(`evidence:catalog:current`). Open: the ~24 remaining recorded reverse
dependents are not individually modeled in this knowledge base.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [LZ4](LZ4.md)
- [liblz4 (MSYS)](LIBLZ4-MSYS.md)
- [LZ4 (CLANG64)](LZ4-CLANG64.md)
- [libarchive](LIBARCHIVE.md)
