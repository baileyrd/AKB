---
id: doc:volume-2:filesystem-boundary
title: Windows Filesystem Boundary
volume: 2
status: partial
model_refs:
  - platform:microsoft:windows
  - layer:msys2:1-windows-kernel-services
  - layer:msys2:2-windows-user-mode-apis
evidence_refs:
  - evidence:microsoft:file-naming-2026-08-02
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# Windows Filesystem Boundary

> **Contextual scope.** This page documents the *boundary* between MSYS2 and
> a Windows subsystem — what MSYS2 depends on, where this knowledge base's
> claims stop, and what evidence an exact claim would need. It is not a
> Windows internals reference. See
> [ADR 0001](../charter/adr/0001-windows-platform-contextual-scope.md).

## Purpose

Windows filesystems supply the storage MSYS2's POSIX file semantics are
presented over. Path form, case behavior, and link representation all differ
between the two models.

## What MSYS2 depends on

Drive letters, UNC paths, file attributes, case behavior, and reparse
points. The [MSYS filesystem layer](MSYS-FILESYSTEM-LAYER.md) presents POSIX
operations over these; the [mount manager](MSYS-MOUNT-MANAGER.md) maps POSIX
prefixes onto them.

## Where the boundary sits

Symbolic links are the sharpest case. POSIX symlinks have no single native
equivalent, and the representation chosen determines whether a native
program sees a link, a junction, or a file.

This is not hypothetical here. The 2026-07-30 probe found `ln -s` succeeding
with the target readable while `test -L` returned non-zero — creation and
classification disagreeing on the same object. The cause is unexplained, and
filesystem type is one of the candidates, which is exactly why filesystem
type is a boundary fact this volume needs and does not have.

## Evidence required for an exact claim

Filesystem probes on the target volume, plus the volume's type and policy
configuration.

## What this knowledge base holds

The symlink discrepancy above, and nothing about volume type: **WMI volume
queries were denied by host access policy** during the one host observation.
So the most likely explanation for the most interesting result in Volume 3
is precisely the thing this volume was prevented from collecting.

## Host observation

The one controlled host observation this knowledge base holds, from
2026-07-30: Windows NT `10.0.26200.8973` on x64, system directory
`C:\Windows\system32`. WMI operating-system and volume queries were
**denied by host access policy**, so edition, filesystem type, and
management-API behavior are not established. Console output was redirected
in the collection context.

Every page in this volume inherits that boundary: one host, one build, no
privileged queries.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["Microsoft Windows"]
    u0["MSYS2"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `platform:microsoft:windows` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [Windows platform boundaries](WINDOWS-PLATFORM-BOUNDARIES.md)
- [MSYS filesystem layer](MSYS-FILESYSTEM-LAYER.md)
- [MSYS mount manager](MSYS-MOUNT-MANAGER.md)
