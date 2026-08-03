---
id: doc:volume-5:p7zip
title: p7zip
volume: 5
status: partial
model_refs:
  - component:p7zip:p7zip
  - package:msys2:p7zip
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:p7zip:project-site-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# p7zip

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `component:p7zip:p7zip` |
| Kind | `component` |
| Status | `partial` |
| Confidence | `high` |
| Authority | p7zip project |
| Environments | `msys` |
| Upstream | <https://github.com/p7zip-project/p7zip> |
| Packaged as | `package:msys2:p7zip` |
| Version (observed) | 17.06-1 |
| License (observed) | LGPL;custom:unRAR |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 10.8 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:p7zip:project-site-2026-07-30` — p7zip (official project site) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

P7zip is a command-line port of 7-Zip, supporting the high-ratio `.7z`
format alongside read/write support for several other archive formats. This
page documents its architectural role and dependency footprint; see the
[official p7zip project site](https://github.com/p7zip-project/p7zip) for
the full command reference.

## Architectural Classification

`component:p7zip:p7zip` is packaged as `package:msys2:p7zip` (version
`17.06-1` in the current catalog snapshot, license `LGPL;custom:unRAR`),
belonging to the MSYS environment. The `.7z` format and core algorithms
(including LZMA/LZMA2) originate with Igor Pavlov's 7-Zip; p7zip is a
separate command-line port project, not an official 7-Zip release.

## Responsibilities

- Multi-format archive creation and extraction, most notably `.7z`, with
  additional read (and in some cases write) support for other formats such
  as `.zip` and `.tar` depending on build configuration.

## Boundaries

Unlike the single-purpose compressors elsewhere in this batch, p7zip is a
multi-format archiver comparable in scope to [Zip](INFO-ZIP-ZIP.md)/
[UnZip](INFO-ZIP-UNZIP.md) rather than to single-stream tools like
[bzip2](BZIP2.md) or [XZ Utils](XZ-UTILS.md).

## Interfaces

- `7z`/`7za`/`7zr` executables with subcommands (`a` add, `x` extract with
  full paths, `e` extract flat, `l` list, `t` test), per the project
  documentation. The mixed-license note above (custom `unRAR` license
  component) reflects optional RAR-format read support in some p7zip
  builds; whether this MSYS2 build includes it is unconfirmed without a
  file-level inventory.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:p7zip`:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Interactive shell | `package:msys2:bash` | p7zip's source distribution has historically bundled a thin shell-script wrapper around its executables; this is the likely but not file-confirmed explanation for the dependency, recorded here at medium confidence pending package file-inventory evidence. |
| C/C++ runtime | `package:msys2:gcc-libs` | Standard GCC-toolchain runtime libraries (`libgcc`/`libstdc++`) for a package built with GCC in this environment. |

## Reverse Dependencies

The snapshot records 2 relationships targeting `package:msys2:p7zip`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

P7zip has no persistent configuration file; behavior is controlled entirely
through command-line flags and subcommands.

## Initialization and Execution Flow

P7zip's core executables are invoke-run-exit processes, adapted from POSIX
semantics onto Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

`.7z` archiving supports solid compression (concatenating multiple files
before compressing as one block for better ratio), a structurally different
model from the per-entry compression used by [Zip](INFO-ZIP-ZIP.md)/
[UnZip](INFO-ZIP-UNZIP.md).

## Compatibility and Variants

Whether a given p7zip build supports RAR-format extraction depends on
whether the optional unRAR-licensed code was included at build time, per
the mixed license recorded in the catalog; this has not been confirmed for
this snapshot.

## Security Considerations

Extracting an untrusted multi-format archive inherits the general
path-traversal and decompression-bomb risks documented elsewhere in this
batch (see [Info-ZIP UnZip](INFO-ZIP-UNZIP.md#security-considerations) and
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)); no
p7zip-specific CVE review has been performed for the recorded `17.06-1`
version, which is a materially older release relative to some other tools
in this batch and worth flagging as a version-currency question for a
future security review.

## Failure Modes and Diagnostics

`t` (test) is the documented way to verify an archive's integrity before
extracting; format-detection failures should first be checked against
whether the archive's format is actually supported by this build (see
Compatibility and Variants).

## Evidence, Assumptions, and Open Questions

Command structure and format support are backed by the official p7zip
project site (`evidence:p7zip:project-site-2026-07-30`), matching the
`project_url` already recorded for `package:msys2:p7zip` in the catalog.
Package identity, version, license, and the gcc-libs dependency are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open: the
`bash` dependency's exact cause and whether RAR-format support is enabled
in this build are both unconfirmed pending package file-inventory evidence.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["p7zip"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `component:p7zip:p7zip` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [Info-ZIP Zip](INFO-ZIP-ZIP.md)
- [Info-ZIP UnZip](INFO-ZIP-UNZIP.md)
- [XZ Utils](XZ-UTILS.md)
