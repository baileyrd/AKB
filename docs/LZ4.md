---
id: doc:volume-5:lz4
title: LZ4
volume: 5
status: partial
model_refs:
  - component:lz4:lz4
  - package:msys2:lz4
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:lz4:manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# LZ4

## Purpose

LZ4 compresses and decompresses a single file or stream, prioritizing very
high speed over compression ratio. This page documents its architectural
role and an interesting self-referential dependency edge observed in the
catalog snapshot; see the
[official LZ4 project site](https://lz4.github.io/lz4/) for the format and
algorithm reference.

## Architectural Classification

`component:lz4:lz4` is packaged as `package:msys2:lz4` (version `1.10.0-1`
in the current catalog snapshot, license `LGPL`), authored by Yann Collet —
the same author as [Zstandard](ZSTD.md), which succeeded LZ4 as Collet's
primary compression-format project. It belongs to the MSYS environment.

## Responsibilities

- Single-file/stream compression and decompression, tuned for very high
  throughput rather than maximum compression ratio.

## Boundaries

Like the other single-stream compressors in this batch, lz4 does not
archive multiple files itself.

## Interfaces

- `-d`/`--decompress`, `-k`/`--keep`, `-1` through `-9`/`--best` level
  presets (the format also defines a separate "HC" high-compression mode
  distinct from the fast default mode), per the project documentation.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:lz4`:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| C/C++ runtime | `package:msys2:gcc-libs` | Standard GCC-toolchain runtime libraries (`libgcc`/`libstdc++`) for a package built with GCC in this environment. |
| Codec library (self) | `package:msys2:lz4` (version-pinned `lz4=1.10.0`) | The MSYS2 `lz4` package bundles both the CLI and its shared library in one package; the version-pinned dependency most likely reflects a build-time constraint tying the CLI to an exact matching library version that happens to resolve to the same package rather than a distinct dependency (`claim:component:lz4:self-versioned-dependency`). |

The self-referential edge is a genuine, observed artifact of this snapshot,
not a data error introduced by this knowledge base; it is recorded at
`medium` confidence pending clarification against the package's actual
build/split structure.

## Reverse Dependencies

The snapshot records 1 relationship targeting `package:msys2:lz4`, the
lowest of any tool covered in this or the prior archive/compression batch.
See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

LZ4 has no persistent configuration file; behavior is controlled entirely
through command-line flags.

## Initialization and Execution Flow

LZ4 is an invoke-run-exit process, adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

LZ4's defining runtime characteristic, per the project documentation, is
very fast compression and especially decompression speed at a lower
compression ratio than the other codecs in this batch — a deliberate
design trade-off rather than an incidental limitation.

## Compatibility and Variants

The `.lz4` format is distinct from and incompatible with the
[gzip](GNU-GZIP.md), [bzip2](BZIP2.md), [XZ Utils](XZ-UTILS.md), and
[Zstandard](ZSTD.md) formats, despite the shared authorship with zstd.

## Security Considerations

Decompressing an untrusted `.lz4` file carries the same general
decompression-bomb risk shared by the other compressors in this batch,
arguably with a lower per-byte compute cost to trigger given lz4's own
speed-optimized decompression; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture. No lz4-specific CVE review has been
performed for the recorded `1.10.0-1` version.

## Failure Modes and Diagnostics

As with the other codecs in this batch, verifying archive integrity before
relying on a compressed output is the recommended practice.

## Evidence, Assumptions, and Open Questions

The compression model is backed by the official LZ4 project site
(`evidence:lz4:manual-2026-07-30`), matching the `project_url` already
recorded for `package:msys2:lz4` in the catalog. Package identity, version,
license, and dependency edges — including the self-referential one — are
backed by the pacman catalog snapshot (`evidence:catalog:current`). Open:
the exact reason for the self-versioned dependency is a medium-confidence
inference, not a confirmed build-system fact.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [Zstandard (zstd)](ZSTD.md)
- [liblz4 (MSYS)](LIBLZ4-MSYS.md)
- [LZO (MSYS)](LIBLZO2-MSYS.md)
