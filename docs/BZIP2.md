---
id: doc:volume-5:bzip2
title: bzip2
volume: 5
status: partial
model_refs:
  - component:bzip2:bzip2
  - package:msys2:bzip2
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:bzip2:project-site-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# bzip2

## Purpose

Bzip2 compresses and decompresses a single file or stream using a
Burrows-Wheeler-transform-based algorithm that generally reaches a higher
compression ratio than gzip at the cost of speed. This page documents its
architectural role, its library/CLI split, and its distinguishing
block-structured design; see the
[official bzip2 project site](http://www.bzip.org) for the format and
algorithm reference.

## Architectural Classification

`component:bzip2:bzip2` is packaged as `package:msys2:bzip2` (version
`1.0.8-4` in the current catalog snapshot). Unlike the other tools in this
batch, bzip2 is **not** a GNU project: it is authored by Julian Seward and
distributed under its own permissive, BSD-style license, matching the
catalog's recorded `licenses: custom` (not GPL). It belongs to the MSYS
environment.

## Responsibilities

- Single-file/stream compression and decompression via a
  Burrows-Wheeler-transform, move-to-front, and Huffman-coding pipeline.
- Providing `bzip2recover`, a companion tool documented as part of the
  bzip2 distribution for attempting to recover data from a damaged `.bz2`
  file; whether this environment's package includes it has not been
  confirmed against a file-level inventory.

## Boundaries

Like [GNU Gzip](GNU-GZIP.md), bzip2 compresses exactly one stream and does
not archive multiple files; the `.tar.bz2` convention pairs it with
[GNU Tar](GNU-TAR.md).

## Interfaces

- `-d`/`--decompress`, `-c` (stdout), `-1` through `-9` (block size,
  100 KB to 900 KB — larger blocks improve ratio at the cost of memory and
  speed), `-t` (integrity test without decompressing).

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:bzip2`: `package:msys2:libbz2`. This reflects a common
library/CLI split pattern — the `bzip2` command-line package links
dynamically against `libbz2`, its shared compression library, rather than
statically bundling the codec (`claim:component:bzip2:libbz2-split`).
Documented fully in [libbz2](LIBBZ2.md).

## Reverse Dependencies

The snapshot records 5 relationships targeting `package:msys2:bzip2`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Bzip2 has no persistent configuration file; `BZIP2`/`BZIP` environment
variables set default options, mirroring the same pattern documented for
[GNU Gzip](GNU-GZIP.md)'s `GZIP` variable.

## Initialization and Execution Flow

Bzip2 is an invoke-run-exit process, adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md); this page
does not restate that mechanism.

## Runtime Behavior

Bzip2 compresses input in independent, fixed-size blocks (up to the selected
`-1`..`-9` block size) rather than as one continuous stream. This is a
distinguishing design point from gzip's stream-oriented format: because each
block is independently compressed, `bzip2recover` can attempt to salvage the
still-intact blocks of a partially corrupted archive, a form of partial
recovery gzip's format does not offer in the same way. Larger block sizes
are documented to require correspondingly more memory during both
compression and decompression.

## Compatibility and Variants

The bzip2 format is distinct from and incompatible with the
[gzip](GNU-GZIP.md) and [XZ Utils](XZ-UTILS.md) formats. `pbzip2`, a
parallel-compression-compatible variant, is not present in this catalog
snapshot.

## Security Considerations

Decompressing an untrusted `.bz2` file carries the same general
decompression-bomb risk shared by the other compressors in this batch; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture. No bzip2-specific CVE review has
been performed for the recorded `1.0.8-4` version.

## Failure Modes and Diagnostics

`-t` (test mode) is the documented way to verify archive integrity without
committing to a full decompression; for a partially corrupted archive,
`bzip2recover`'s block-level recovery is the documented next step rather
than treating the whole archive as a total loss.

## Evidence, Assumptions, and Open Questions

The compression model and library/CLI split are backed by the official
bzip2 project site (`evidence:bzip2:project-site-2026-07-30`), which matches
the `project_url` already recorded for `package:msys2:bzip2` in the catalog.
Package identity, version, license, and the libbz2 dependency are backed by
the pacman catalog snapshot (`evidence:catalog:current`). Open: whether this
environment's package includes `bzip2recover` is unconfirmed pending
package file-inventory evidence.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Tar](GNU-TAR.md)
- [GNU Gzip](GNU-GZIP.md)
- [XZ Utils](XZ-UTILS.md)
- [libbz2](LIBBZ2.md)
- [Package File Inventory](PACKAGE-FILE-INVENTORY.md)
