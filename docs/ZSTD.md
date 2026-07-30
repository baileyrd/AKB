---
id: doc:volume-5:zstd
title: Zstandard (zstd)
volume: 5
status: partial
model_refs:
  - component:zstd:zstd
  - package:msys2:zstd
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:zstd:project-site-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# Zstandard (zstd)

## Purpose

Zstd compresses and decompresses a single file or stream, targeting a
speed/ratio trade-off tunable across a wide level range plus a
long-distance-matching mode. This page documents its architectural role and
library/CLI split; see the
[official Zstandard project site](https://facebook.github.io/zstd/) for the
format and algorithm reference.

## Architectural Classification

`component:zstd:zstd` is packaged as `package:msys2:zstd` (version
`1.5.7-1` in the current catalog snapshot, license `BSD`). It originated at
Meta (as Facebook) under Yann Collet, the same author as [LZ4](LZ4.md). It
belongs to the MSYS environment.

## Responsibilities

- Single-file/stream compression and decompression across a wide level
  range (negative "fast" levels through `-19`, with `--ultra` extending
  further), documented as tunable for either speed or ratio.

## Boundaries

Like the other single-stream compressors in this batch, zstd does not
archive multiple files; the `.tar.zst` convention pairs it with
[GNU Tar](GNU-TAR.md).

## Interfaces

- `-d`/`--decompress`, `-k`/`--keep`, level flags (`-1`..`-19`, `--ultra`
  for higher), `--long` for long-distance matching, `-T`/`--threads` for
  multithreaded compression — the same multithreading capability documented
  for [XZ Utils](XZ-UTILS.md#interfaces).

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:zstd`:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Codec library | `package:msys2:libzstd` | The `zstd` CLI links against `libzstd`, its shared codec library, following the same library/CLI split pattern documented for [bzip2](BZIP2.md#dependencies) and [XZ Utils](XZ-UTILS.md#dependencies). |
| C/C++ runtime | `package:msys2:gcc-libs` | Standard GCC-toolchain runtime libraries (`libgcc`/`libstdc++`) for a package built with GCC in this environment. |

## Reverse Dependencies

The snapshot records 4 relationships targeting `package:msys2:zstd`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Zstd has no persistent configuration file; behavior is controlled entirely
through command-line flags.

## Initialization and Execution Flow

Zstd is an invoke-run-exit process by default, adapted from POSIX semantics
onto Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md). `-T`
multithreaded mode uses the same worker-thread-based block-parallel
execution model documented for [XZ Utils](XZ-UTILS.md#initialization-and-execution-flow).

## Runtime Behavior

Higher compression levels and `--long` mode trade increased memory and CPU
time for better ratio; the project documents this trade-off explicitly
rather than presenting a single fixed cost/benefit profile.

## Compatibility and Variants

The `.zst` format is distinct from and incompatible with the
[gzip](GNU-GZIP.md), [bzip2](BZIP2.md), and [XZ Utils](XZ-UTILS.md) formats.

## Security Considerations

Decompressing an untrusted `.zst` file carries the same general
decompression-bomb risk shared by the other compressors in this batch; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture. No zstd-specific CVE review has
been performed for the recorded `1.5.7-1` version.

## Failure Modes and Diagnostics

As with the other codecs in this batch, verifying archive integrity before
relying on a compressed backup is the recommended practice; zstd's format
includes frame checksums for this purpose per the project documentation.

## Evidence, Assumptions, and Open Questions

The compression model and library/CLI split are backed by the official
Zstandard project site (`evidence:zstd:project-site-2026-07-30`), which
matches the `project_url` already recorded for `package:msys2:zstd` in the
catalog. Package identity, version, license, and dependency edges are
backed by the pacman catalog snapshot (`evidence:catalog:current`). No
open items beyond the general version-qualified security review noted
above.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Tar](GNU-TAR.md)
- [XZ Utils](XZ-UTILS.md)
- [LZ4](LZ4.md)
- [Zstandard (library)](LIBZSTD.md)
