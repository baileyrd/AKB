---
id: doc:volume-5:gnu-gzip
title: GNU Gzip
volume: 5
status: partial
model_refs:
  - component:gnu:gzip
  - package:msys2:gzip
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:gzip-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Gzip

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `component:gnu:gzip` |
| Kind | `component` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Free Software Foundation |
| Environments | `msys` |
| Upstream | <https://www.gnu.org/software/gzip/> |
| Packaged as | `package:msys2:gzip` |
| Version (observed) | 1.14-2 |
| License (observed) | GPL3 |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 187.26 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:gnu:gzip-manual-2026-07-30` — GNU Gzip Manual (`primary`, retrieved 2026-07-30)

**Claims about this object**

- `claim:component:gzip:wrapper-scripts` (`inference`, `high`) — The MSYS gzip package's dependencies on bash and less reflect its bundled shell-script wrappers (zcat, zless, zgrep, zcmp, zdiff) rather than a dependency of the core gzip/gunzip binary itself.

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Gzip compresses and decompresses a single file or stream using the DEFLATE
algorithm. This page documents its architectural role, its bundled
wrapper-script family, and its composition with tar; see the
[official GNU Gzip manual](https://www.gnu.org/software/gzip/manual/gzip.html)
for full option semantics.

## Architectural Classification

`component:gnu:gzip` is a GNU-userland component packaged as
`package:msys2:gzip` (version `1.14-2` in the current catalog snapshot,
license `GPL3`), belonging to the MSYS environment. Like
[GNU Tar](GNU-TAR.md), it is one of the composable pieces behind the
`.tar.gz` convention rather than an archiver itself: gzip compresses exactly
one stream and carries no directory-tree metadata of its own.

## Responsibilities

- Compressing and decompressing a single file or stream via DEFLATE.
- Providing a family of wrapper commands — `zcat`, `zless`, `zgrep`,
  `zcmp`, `zdiff` — that let other tools operate on `.gz` files without a
  separate manual decompression step.

## Boundaries

Gzip does not archive multiple files into one output; that responsibility
belongs to [GNU Tar](GNU-TAR.md) or a true archive format. Gzip's wrapper
scripts are conveniences layered on top of the core `gzip`/`gunzip` binary,
not a distinct compression capability.

## Interfaces

- `-d`/`--decompress`, `-k`/`--keep` (retain the original file), `-c` (write
  to stdout), and `-1` through `-9`/`--best` for the compression-level/speed
  trade-off, per the manual.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:gzip`: `package:msys2:bash` and `package:msys2:less`. Unlike
the character-set/NLS dependencies seen elsewhere in this volume, these map
directly to gzip's bundled wrapper scripts rather than to the core
compression binary: `zless` is a shell wrapper invoking `less` to page
through compressed content, and `zcat`/`zgrep`/`zcmp`/`zdiff` are themselves
shell scripts requiring `bash` to run
(`claim:component:gzip:wrapper-scripts`).

## Reverse Dependencies

The snapshot records 5 relationships targeting `package:msys2:gzip`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Gzip has no persistent configuration file. The manual documents a `GZIP`
environment variable for default options, though explicit command-line
flags are the primary configuration surface.

## Initialization and Execution Flow

The core `gzip`/`gunzip` binary is an invoke-run-exit process. The wrapper
scripts are a layered execution model: a `bash` process interprets the
wrapper script, which in turn launches `gzip` and/or `less` as child
processes — each an MSYS-runtime process-creation event adapted by
`msys-2.0.dll`, per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Gzip compresses exactly one file or stream per invocation and stores limited
metadata for that single file (such as the original name and modification
time) in its own header, distinct from the richer, multi-file metadata model
`tar` maintains for an archive.

## Compatibility and Variants

The gzip file format is a fixed, standardized format distinct from and
incompatible with the [bzip2](BZIP2.md) and [XZ Utils](XZ-UTILS.md) formats;
files must be identified by extension or content, not assumed interchangeable.
`pigz`, a parallel-gzip-compatible alternative, is not present in this
catalog snapshot.

## Security Considerations

Decompressing an untrusted `.gz` file carries the general decompression-bomb
risk shared by all the compressors in this batch (small compressed input
expanding to a very large output); see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture. No gzip-specific CVE review has been
performed for the recorded `1.14-2` version.

## Failure Modes and Diagnostics

Attempting to compress a file that is already a recognized compressed format
(gzip detects and typically refuses or warns), or piping non-gzip data into
`gunzip`, produces a clear "not in gzip format" error rather than a silent
failure, per the manual.

## Evidence, Assumptions, and Open Questions

Compression behavior and the wrapper-script family are backed by the
official GNU Gzip manual (`evidence:gnu:gzip-manual-2026-07-30`). Package
identity, version, license, and the bash/less dependency-to-feature mapping
are backed by the pacman catalog snapshot (`evidence:catalog:current`) via
`claim:component:gzip:wrapper-scripts`. No open items beyond the general
version-qualified security review noted above.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["GNU Gzip"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `component:gnu:gzip` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Tar](GNU-TAR.md)
- [bzip2](BZIP2.md)
- [XZ Utils](XZ-UTILS.md)
- [MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md)
