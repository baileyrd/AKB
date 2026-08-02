---
id: doc:volume-3:mount-manager
title: MSYS Mount Manager
volume: 3
status: partial
model_refs:
  - subsystem:msys2:mount-manager
  - subsystem:msys2:path-conversion
  - runtime:msys2:msys-2.0.dll
  - environment:msys2:msys
evidence_refs:
  - evidence:cygwin:user-guide-2026-08-02
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# MSYS Mount Manager

## Purpose

The mount manager holds the virtual mount table that maps POSIX path
prefixes onto Windows filesystem locations. It is what makes `/usr` mean the
installation's `usr` directory and `/c` mean the `C:` drive — the table
[path conversion](MSYS-PATH-CONVERSION.md) consults on every translation.

## Architectural Classification

`subsystem:msys2:mount-manager`, contained by
[`msys-2.0.dll`](MSYS-2-0-DLL.md). The mount table is virtual: it exists in
the runtime, not in the Windows filesystem namespace, and is invisible to
native programs.

## Responsibilities

- Reading `/etc/fstab` at runtime initialization and constructing the mount
  table from it.
- Providing the prefix-to-location mapping that path conversion applies.
- Presenting drive letters within the POSIX namespace so Windows volumes are
  reachable by POSIX path.

## Boundaries

The mount table binds MSYS-linked processes only. A native program handed a
POSIX path sees an invalid path, because nothing outside the runtime knows
the mapping exists. This is the mechanism behind most MSYS/native path
confusion.

## Interfaces

`/etc/fstab` is the documented configuration surface. `mount` reports the
active table.

## Dependencies

The Windows filesystem namespace, including drive letters and UNC paths.

## Reverse Dependencies

[Path conversion](MSYS-PATH-CONVERSION.md) depends on it directly. Every
MSYS process depends on it transitively.

## Configuration

`/etc/fstab`. This knowledge base has not recorded a specific installation's
table contents, and the mount table is installation-specific rather than a
property of the runtime version.

## Initialization and Execution Flow

Constructed during runtime initialization, before `main`. A process's view
of the table is fixed at start; see
[MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

No bounded probe in the 2026-07-30 collection captured the mount table. The
behavior map names "mount table and path-conversion observations" as the
required deep evidence, and it does not exist.

## Compatibility and Variants

MSYS-only. Installation-specific: two MSYS2 installations may present
different tables, so mount facts are not portable between hosts the way
runtime-version facts are.

## Security Considerations

No subsystem-specific vulnerability review has been performed. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general posture; the runtime version observed was `3.6.10`.

## Failure Modes and Diagnostics

A POSIX path that resolves in one installation and not another usually
indicates a mount-table difference rather than a program defect. `mount`
reports the active table; comparing it across hosts is the first diagnostic.

## Evidence, Assumptions, and Open Questions

Design is attributed to the
[Cygwin User's Guide](https://cygwin.com/cygwin-ug-net/cygwin-ug-net.html)
(`evidence:cygwin:user-guide-2026-08-02`), with MSYS2's mount behavior
diverging in ways this page does not characterize.

Open: no mount-table observation exists. No specific installation's table is
recorded. Whether the table can change after process start is unconfirmed.

## Related Objects

- [msys-2.0.dll](MSYS-2-0-DLL.md)
- [Path Conversion](MSYS-PATH-CONVERSION.md)
- [Filesystem Layer](MSYS-FILESYSTEM-LAYER.md)
