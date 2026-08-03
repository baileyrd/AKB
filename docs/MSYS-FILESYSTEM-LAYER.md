---
id: doc:volume-3:filesystem-layer
title: MSYS Filesystem Layer
volume: 3
status: partial
model_refs:
  - subsystem:msys2:filesystem-layer
  - subsystem:msys2:mount-manager
  - runtime:msys2:msys-2.0.dll
  - environment:msys2:msys
evidence_refs:
  - evidence:cygwin:user-guide-2026-08-02
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# MSYS Filesystem Layer

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `subsystem:msys2:filesystem-layer` |
| Kind | `subsystem` |
| Status | `partial` |
| Confidence | `medium` |
| Authority | MSYS2 |
| Environments | `msys` |

**Evidence on this object**

- `evidence:cygwin:user-guide-2026-08-02` — Cygwin User's Guide (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

The filesystem layer presents POSIX file semantics — permissions, ownership,
links, and file types — over NTFS and the Win32 file APIs, which model those
concepts differently or not at all. Symlink representation is the sharpest
case and the one this knowledge base has direct evidence about.

## Architectural Classification

`subsystem:msys2:filesystem-layer`, contained by
[`msys-2.0.dll`](MSYS-2-0-DLL.md). Operates on paths resolved through the
[mount manager](MSYS-MOUNT-MANAGER.md).

## Responsibilities

- Presenting POSIX file operations (`open`, `stat`, `chmod`, `link`,
  `symlink`) over Win32 file APIs.
- Representing symbolic links, which have no single native equivalent — the
  documented options include Windows symlinks, junctions, and marker files,
  each with different visibility to native programs.
- Mapping POSIX permission and ownership concepts onto NTFS security
  descriptors.

## Boundaries

The layer serves MSYS-linked processes. A native program reading a file
created here sees whatever NTFS actually holds, which may not carry the
POSIX meaning the MSYS side intended — the symlink representation being the
clearest instance.

## Interfaces

The POSIX file API families, via [the POSIX API surface](MSYS-POSIX-API.md).

## Dependencies

NTFS and ReFS semantics, and the Win32 file APIs. Named in
[Windows platform boundaries](WINDOWS-PLATFORM-BOUNDARIES.md).

## Reverse Dependencies

Every MSYS process that touches a file. [GNU Coreutils](GNU-COREUTILS.md)
and [GNU Tar](GNU-TAR.md) exercise the symlink and permission surfaces
hardest.

## Runtime Behavior

One bounded probe from 2026-07-30 is the most informative single observation
in Volume 3:

> `ln -s` succeeded and the target was readable, but `test -L` returned
> non-zero.

The link worked as a link — the target was reachable through it — while the
POSIX predicate that asks "is this a symbolic link" said no. Creation and
classification disagreed.

The collector preserved this discrepancy rather than smoothing it, and this
page does not resolve it either: the cause is not established. It could
follow from the symlink representation in use on that host, from filesystem
type, from privilege level, or from the shell builtin's own logic. What is
established is that on MSYS 3.6.10 on that host, those two commands
disagreed — which is sufficient reason not to assume POSIX symlink parity.

## Configuration

Symlink representation is documented as influenced by the `MSYS` environment
variable. No controlled observation of that influence exists here.

## Initialization and Execution Flow

No independent lifecycle; the layer serves calls from the process that links
the runtime.

## Compatibility and Variants

MSYS-only. Behavior is host-dependent in a way most subsystems are not:
filesystem type and privilege level plausibly affect it, so an observation
on one host does not transfer.

## Security Considerations

No subsystem-specific vulnerability review has been performed. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general posture; the runtime version observed was `3.6.10`.

## Failure Modes and Diagnostics

An archive or build that mishandles symlinks is the characteristic failure,
and it is frequently misattributed to the tool rather than to the
representation underneath. Test `test -L` alongside readability before
concluding the tool is at fault — the probe above shows they can disagree.

## Evidence, Assumptions, and Open Questions

Design is attributed to the
[Cygwin User's Guide](https://cygwin.com/cygwin-ug-net/cygwin-ug-net.html)
(`evidence:cygwin:user-guide-2026-08-02`). The symlink observation is from
the bounded collector
(`evidence:msys2:runtime-behavior-probes-2026-07-30`).

Open: the cause of the `ln -s` / `test -L` discrepancy is unexplained. No
filesystem-type-qualified probe matrix exists, and the behavior map requires
"filesystem probes by host/version" for this row.

## Related Objects

- [msys-2.0.dll](MSYS-2-0-DLL.md)
- [Mount Manager](MSYS-MOUNT-MANAGER.md)
- [MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
