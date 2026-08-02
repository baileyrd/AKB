---
id: doc:volume-6:liblz4-msys
title: liblz4 (MSYS)
volume: 6
status: partial
model_refs:
  - library:lz4:liblz4
  - package:msys2:liblz4
  - component:lz4:lz4
  - environment:msys2:msys
evidence_refs:
  - evidence:lz4:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# liblz4 (MSYS)

## Purpose

This page documents `package:msys2:liblz4`, the LZ4 compression codec
library — a genuinely distinct MSYS catalog package from the `lz4` CLI
already documented on [LZ4](LZ4.md), not merely a naming variant of it.
See the [official LZ4 project site](https://lz4.github.io/lz4/) for the
format and algorithm reference.

## Architectural Classification

`library:lz4:liblz4` is packaged as `package:msys2:liblz4` (version
`1.10.0-1` in the current catalog snapshot, license `LGPL`), authored by
Yann Collet — the same author and upstream project as
[LZ4](LZ4.md#architectural-classification). It belongs to the MSYS
environment. This is the same split-library/CLI pattern already
documented across this volume for
[libbz2](LIBBZ2.md#architectural-classification),
[libzstd (MSYS)](LIBZSTD-MSYS.md#architectural-classification), and
[liblzma (MSYS)](LIBLZMA-MSYS.md#architectural-classification): the
upstream project ships both a CLI package and a separately catalogued
codec library package under related but distinct names.

## Responsibilities

- Providing the LZ4 compression and decompression codec as a shared
  library, consumed by archive and version-control tooling that links
  against LZ4 compression directly rather than shelling out to the
  [lz4](LZ4.md) CLI.

## Boundaries

This page's package is the codec library; [LZ4](LZ4.md) documents the
separate CLI package. The two share an upstream project and algorithm
but are distinct catalog entities with independent versioning, matching
the same distinction already drawn for the
[libbz2](LIBBZ2.md#boundaries)/[bzip2](BZIP2.md) pair.

## Interfaces

- The LZ4 C API (`LZ4_compress_default`, `LZ4_decompress_safe`, and
  related functions, including the streaming and HC high-compression
  variants), per the project documentation.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:liblz4`: the standard `gcc-libs` C/C++ runtime
dependency-table row, excluded from this knowledge base's graph edges
per this volume's established boilerplate-dependency policy (see
[MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)).

## Reverse Dependencies

The catalog snapshot records 7 relationships targeting
`package:msys2:liblz4`: `bsdcpio`, `bsdtar`,
[libarchive (MSYS)](LIBARCHIVE-MSYS.md) — a distinct catalog entity
from this knowledge base's UCRT64-modeled [LibArchive](LIBARCHIVE.md),
now itself modeled with a `requires` edge back to this page
(`relationship:foundation-libraries:libarchive-msys-requires-liblz4`,
added 2026-08-02) — `liblz4-devel`, `rsync`, `squashfs-tools`, and
`subversion`. The remaining six of seven are not currently modeled as
entities in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

liblz4 has no persistent configuration file; compression behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, liblz4 has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it, the same model documented for
[libbz2](LIBBZ2.md#initialization-and-execution-flow).

## Runtime Behavior

Identical compression algorithm and speed/ratio trade-off to the
[lz4](LZ4.md#runtime-behavior) CLI, since both packages share the same
upstream codec implementation.

## Compatibility and Variants

`package:msys2:liblz4` and `package:msys2:lz4` are separately versioned
catalog entities (both currently at `1.10.0-1`, but independently
packaged); code linking against this library does not require the CLI
package to be installed.

## Security Considerations

Decompressing untrusted LZ4-compressed data carries the same general
decompression-scale risk documented for the
[lz4](LZ4.md#security-considerations) CLI; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `1.10.0-1` version.

## Failure Modes and Diagnostics

A dependent program's LZ4 decompression failure should be checked
against the input data's actual LZ4-format validity before being
treated as a liblz4 defect.

## Evidence, Assumptions, and Open Questions

The compression model is backed by the official LZ4 project site
(`evidence:lz4:manual-2026-07-30`), the same evidence record
[LZ4](LZ4.md) cites. Package identity, version, license, and the
seven recorded (but not individually modeled) reverse dependents are
backed by the pacman catalog snapshot (`evidence:catalog:current`).
**Update, 2026-08-02**: one of the seven reverse dependents,
[libarchive (MSYS)](LIBARCHIVE-MSYS.md), is now modeled (see Reverse
Dependencies above). Open: whether the remaining six (particularly
`subversion`) warrant their own pages in a future batch, per this
volume's ongoing gap-closing methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [LZ4](LZ4.md)
- [libbz2](LIBBZ2.md)
- [libzstd (MSYS)](LIBZSTD-MSYS.md)
- [liblzma (MSYS)](LIBLZMA-MSYS.md)
- [libarchive (MSYS)](LIBARCHIVE-MSYS.md)
- [LZ4 (CLANG64)](LZ4-CLANG64.md)
