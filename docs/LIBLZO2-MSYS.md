---
id: doc:volume-6:liblzo2-msys
title: LZO (MSYS)
volume: 6
status: partial
model_refs:
  - library:oberhumer:liblzo2@msys
  - package:msys2:liblzo2
  - environment:msys2:msys
evidence_refs:
  - evidence:oberhumer:lzo-manual-2026-08-02
  - evidence:catalog:current
last_verified: 2026-08-02
---

# LZO (MSYS)

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:oberhumer:liblzo2@msys` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Markus F.X.J. Oberhumer |
| Environments | `msys` |
| Upstream | <https://www.oberhumer.com/opensource/lzo> |
| Packaged as | `package:msys2:liblzo2` |
| Version (observed) | 2.10-3 |
| License (observed) | GPL |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 184.7 KB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:oberhumer:lzo-manual-2026-08-02` — LZO (official project site) (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

This page documents `package:msys2:liblzo2`, a portable lossless data
compression library prioritizing decompression speed over compression
ratio, consumed by `lzop` and `squashfs-tools` (neither yet a modeled
entity in this knowledge base). See the
[official LZO project site](https://www.oberhumer.com/opensource/lzo)
for the full reference.

## Architectural Classification

`library:oberhumer:liblzo2@msys` is packaged as `package:msys2:liblzo2`
(version `2.10-3` in the current catalog snapshot, license `GPL`),
authored by Markus F.X.J. Oberhumer. It belongs to the MSYS environment.
Its sole recorded runtime dependency is the standard `gcc-libs`
boilerplate row, excluded from this knowledge base's graph edges per
this volume's established policy — the same minimal dependency
footprint documented for [xxHash (MSYS)](XXHASH-MSYS.md).

## Responsibilities

- Providing LZO-format lossless compression and decompression, tuned
  for very fast decompression (the design goal that distinguishes it
  from the other codec libraries documented in this volume).

## Boundaries

LZO trades compression ratio for decompression speed, the same
general trade-off already documented for [LZ4](LZ4.md) and
[liblz4 (MSYS)](LIBLZ4-MSYS.md); it is a distinct format and
implementation from either, sharing no code lineage with the LZ4
project despite the similar performance goals.

## Interfaces

- The LZO C API (`lzo1x_compress`, `lzo1x_decompress`, and related
  functions), per the project documentation.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:liblzo2`: the standard `gcc-libs` C/C++ runtime
dependency-table row, excluded from this knowledge base's graph edges
per this volume's established boilerplate-dependency policy (see
[MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)).

## Reverse Dependencies

The catalog snapshot records 3 relationships targeting
`package:msys2:liblzo2`: `liblzo2-devel`, `lzop`, and
`squashfs-tools`. None of these three are currently modeled as
entities in this knowledge base; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

LZO has no persistent configuration file; compression behavior is
controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, LZO has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it,
the same model documented for
[liblz4 (MSYS)](LIBLZ4-MSYS.md#initialization-and-execution-flow).

## Runtime Behavior

LZO's defining runtime characteristic, per the project documentation,
is very fast decompression at a lower compression ratio than
general-purpose compressors — a deliberate design trade-off, the same
class of speed/ratio choice already documented for
[LZ4](LZ4.md#runtime-behavior).

## Compatibility and Variants

The `.lzo` format is distinct from and incompatible with the other
compression formats documented in this volume (gzip, bzip2, XZ/LZMA,
LZ4, Zstandard).

## Security Considerations

Decompressing untrusted LZO-compressed data carries the same general
decompression-bomb risk shared by the other compressors in this
volume; see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. No version-qualified
CVE review has been performed for the recorded `2.10-3` version.

## Failure Modes and Diagnostics

A dependent program's LZO decompression failure should be checked
against the input data's actual LZO-format validity before being
treated as a liblzo2 defect.

## Evidence, Assumptions, and Open Questions

The compression model is backed by the official LZO project site
(`evidence:oberhumer:lzo-manual-2026-08-02`), matching the
`project_url` recorded for `package:msys2:liblzo2` in the catalog.
Package identity, version, license, and the three recorded (but not
individually modeled) reverse dependents are backed by the pacman
catalog snapshot (`evidence:catalog:current`). Open: whether `lzop` or
`squashfs-tools` warrant their own pages in a future batch, per this
volume's ongoing gap-closing methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [LZ4](LZ4.md)
- [liblz4 (MSYS)](LIBLZ4-MSYS.md)
- [xxHash (MSYS)](XXHASH-MSYS.md)
