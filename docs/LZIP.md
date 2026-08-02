---
id: doc:volume-5:lzip
title: Lzip
volume: 5
status: partial
model_refs:
  - component:lzip:lzip
  - package:msys2:lzip
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:lzip:manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# Lzip

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `component:lzip:lzip` |
| Kind | `component` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Antonio Diaz Diaz |
| Environments | `msys` |
| Upstream | <https://www.nongnu.org/lzip/lzip.html> |
| Packaged as | `package:msys2:lzip` |
| Version (observed) | 1.26-1 |
| License (observed) | spdx:GPL-2.0-or-later |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 147.1 KB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:lzip:manual-2026-07-30` — Lzip (official project site) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Lzip compresses a single file using an LZMA-based algorithm, with a format
the project explicitly designs around long-term data safety and a
simple, fully specified container rather than maximum speed or throughput
features. This page documents its architectural role and dependency
footprint; see the
[official Lzip project site](https://www.nongnu.org/lzip/lzip.html) for
the format and design rationale.

## Architectural Classification

`component:lzip:lzip` is packaged as `package:msys2:lzip` (version
`1.26-1` in the current catalog snapshot, license `GPL-2.0-or-later`),
authored by Antonio Diaz Diaz. It belongs to the MSYS environment. Despite
using the same underlying LZMA family of algorithms as [XZ Utils](XZ-UTILS.md),
lzip is an independent project with its own container format, not an
alternative front-end to `liblzma`.

## Responsibilities

- Single-file compression and decompression using the LZMA algorithm
  within lzip's own, deliberately simple format.

## Boundaries

Like the other single-stream compressors in this batch, lzip does not
archive multiple files itself.

## Interfaces

- `-d`/`--decompress`, `-k`/`--keep`, `-0` through `-9` level presets,
  `-t`/`--test` for integrity verification without decompressing, per the
  project documentation.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:lzip`: `package:msys2:gcc-libs`, the standard GCC-toolchain
runtime libraries (`libgcc`/`libstdc++`) for a package built with GCC in
this environment — lzip is implemented in C++, unlike the C-implemented
[XZ Utils](XZ-UTILS.md).

## Reverse Dependencies

The snapshot records 3 relationships targeting `package:msys2:lzip`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Lzip has no persistent configuration file; behavior is controlled entirely
through command-line flags.

## Initialization and Execution Flow

Lzip is an invoke-run-exit process, adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

The project's stated design goal is a format robust enough that a
member/block-structured file can, in principle, allow partial recovery of
undamaged data from a corrupted archive — a similar motivation to the
block-based recovery property documented for [bzip2](BZIP2.md#runtime-behavior),
though achieved through a different container design.

## Compatibility and Variants

Lzip's `.lz` format is distinct from and incompatible with the `.xz` format
documented for [XZ Utils](XZ-UTILS.md), despite both using LZMA-family
compression internally; they are not interchangeable.

## Security Considerations

Decompressing an untrusted `.lz` file carries the same general
decompression-bomb risk shared by the other compressors in this batch; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture. No lzip-specific CVE review has
been performed for the recorded `1.26-1` version.

## Failure Modes and Diagnostics

`-t`/`--test` is the documented way to verify an archive's integrity before
relying on it, consistent with the pattern established for the other
compressors in this batch.

## Evidence, Assumptions, and Open Questions

The compression model and format-safety design rationale are backed by the
official Lzip project site (`evidence:lzip:manual-2026-07-30`), matching
the `project_url` already recorded for `package:msys2:lzip` in the catalog.
Package identity, version, license, and the gcc-libs dependency are backed
by the pacman catalog snapshot (`evidence:catalog:current`). No open items
beyond the general version-qualified security review noted above.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["Lzip"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `component:lzip:lzip` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [XZ Utils](XZ-UTILS.md)
- [bzip2](BZIP2.md)
