---
id: doc:volume-6:libzstd-clang64
title: Zstandard (CLANG64)
volume: 6
status: partial
model_refs:
  - library:facebook:zstd@clang64
  - package:msys2:mingw-w64-clang-x86_64-zstd
  - component:llvm:lld
  - environment:msys2:clang64
evidence_refs:
  - evidence:facebook:zstd-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Zstandard (CLANG64)

## Purpose

This page documents the **CLANG64-environment** Zstandard package
specifically — a fast lossless compression library — depended on by
[LLD](LLD.md) to back compressed debug-section support, already cited
by package name on [LLD.md](LLD.md#dependencies) before this page
existed. See the
[official Zstandard project site](https://facebook.github.io/zstd/) for
the full reference.

## Architectural Classification

`library:facebook:zstd@clang64` is packaged in the CLANG64 environment
as `package:msys2:mingw-w64-clang-x86_64-zstd` (version `1.5.7-2` in the
current catalog snapshot) — the same version number as the UCRT64
sibling documented on [Zstandard (library)](LIBZSTD.md), but a
separately built, separate catalog entity. This is the package
[LLD](LLD.md) — a CLANG64-native component itself — actually depends
on. This is the third distinct Zstandard-named catalog entity in this
knowledge base, alongside [Zstandard (UCRT64 library)](LIBZSTD.md) and
the [Zstandard MSYS CLI tool](ZSTD.md) documented in Volume 5.

## Responsibilities

- Providing Zstandard compression and decompression, consumed by
  [LLD](LLD.md) to back `--compress-debug-sections=zstd` and equivalent
  compressed debug-information support.

## Boundaries

This page's package serves CLANG64-environment consumers specifically;
[GCC](GNU-GCC.md) and [GNU Binutils](GNU-BINUTILS.md) instead link
[Zstandard (UCRT64 library)](LIBZSTD.md#reverse-dependencies) — the two
are not interchangeable, matching the same distinction already made
throughout this volume for MSYS/UCRT64/CLANG64 sibling sets.

## Interfaces

- The Zstandard C API (`ZSTD_compress`, `ZSTD_decompress`), the same
  interface [Zstandard (library)](LIBZSTD.md#interfaces) documents, per
  the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-clang-x86_64-zstd` beyond standard toolchain
runtime support.

## Reverse Dependencies

The catalog snapshot records 86 relationships targeting
`package:msys2:mingw-w64-clang-x86_64-zstd`. Four are already modeled in
this knowledge base: [curl (CLANG64)](CURL-CLANG64.md)
(`relationship:foundation-libraries:curl-clang64-requires-zstd-clang64`,
added 2026-08-02), `package:msys2:mingw-w64-clang-x86_64-lld`
(`relationship:toolchain:lld-requires-zstd-clang64`),
`package:msys2:mingw-w64-clang-x86_64-llvm-libs`
(`relationship:foundation-libraries:llvm-libs-requires-zstd-clang64`,
correcting [LLVM libraries'](LLVM-LIBS.md) own prior incorrect
no-dependencies claim; LLDB itself still does not depend on zstd, per
LLDB's own dependency table), and
[libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
(`relationship:foundation-libraries:libarchive-clang64-requires-zstd-clang64`,
added 2026-08-02). The remaining ~82 recorded dependents (a
broad mix of CLANG64 packages, mirroring the UCRT64 sibling's own broad
reverse-dependency set) are not individually modeled in this knowledge
base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Zstandard has no persistent configuration file as a library; compression
level and parameters are set entirely through its C API by the calling
program.

## Initialization and Execution Flow

As a library, Zstandard has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [LLD](LLD.md) in this dependency chain. As a native
MinGW-w64 library, this process model is Windows-facing directly rather
than mediated by `msys-2.0.dll`.

## Runtime Behavior

Compressed debug-section support is exercised only when a build
explicitly requests `--compress-debug-sections=zstd`; it plays no role
in ordinary linking without that flag.

## Compatibility and Variants

The CLANG64 and UCRT64 Zstandard library packages are separately
versioned catalog entities (see Architectural Classification); code
built against one is not automatically compatible with the other
without matching the correct environment.

## Security Considerations

Zstandard is not itself a security-sensitive component in the usual
sense; decompressing untrusted compressed debug data carries the
general trust considerations of any decompression library. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `1.5.7-2` version.

## Failure Modes and Diagnostics

An LLD `--compress-debug-sections=zstd` failure most commonly indicates
a version mismatch between the compressing and decompressing tools'
Zstandard support rather than a defect in this library itself.

## Evidence, Assumptions, and Open Questions

Zstandard compression scope is backed by the official Zstandard project
site (`evidence:facebook:zstd-manual-2026-07-30`), the same evidence
record [Zstandard (library)](LIBZSTD.md) cites. Package identity,
version, and the modeled dependent edge are backed by the pacman
catalog snapshot (`evidence:catalog:current`). Open, and explicitly out
of scope for this page: the ~82 remaining recorded dependents not
individually modeled, and header-level API surface / PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [Zstandard (library)](LIBZSTD.md)
- [Zstandard (MSYS CLI tool)](ZSTD.md)
- [LLD](LLD.md)
- [LLVM libraries](LLVM-LIBS.md)
- [zlib (CLANG64)](ZLIB-CLANG64.md)
- [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
- [curl (CLANG64)](CURL-CLANG64.md)
