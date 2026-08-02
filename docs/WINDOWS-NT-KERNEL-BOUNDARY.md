---
id: doc:volume-2:nt-kernel-boundary
title: Windows NT Kernel Boundary
volume: 2
status: partial
model_refs:
  - platform:microsoft:windows
  - layer:msys2:1-windows-kernel-services
  - layer:msys2:2-windows-user-mode-apis
evidence_refs:
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# Windows NT Kernel Boundary

> **Contextual scope.** This page documents the *boundary* between MSYS2 and
> a Windows subsystem — what MSYS2 depends on, where this knowledge base's
> claims stop, and what evidence an exact claim would need. It is not a
> Windows internals reference. See
> [ADR 0001](../charter/adr/0001-windows-platform-contextual-scope.md).

## Purpose

The NT kernel provides the process, thread, memory, and scheduling services
every MSYS2 program ultimately runs on. MSYS2 does not extend or replace it.

## What MSYS2 depends on

Process and thread creation, virtual memory, handles, and scheduling. The
[MSYS process manager](MSYS-PROCESS-MANAGER.md) builds POSIX process
semantics on top of these; native environment programs use them directly
with no intermediate layer.

## Where the boundary sits

`fork` is the clearest case. The kernel provides no `fork`, so the MSYS
runtime emulates it by creating a process and reproducing the parent's
address space. Everything about that emulation's cost and fidelity is an
MSYS2 fact; everything about the process-creation primitive underneath is a
Windows fact.

A POSIX process ID in an MSYS session is a runtime-maintained identity, not
a Windows process ID. Conflating them is the characteristic error at this
boundary.

## Evidence required for an exact claim

Version-qualified runtime source plus a controlled process probe on a named
Windows build.

## What this knowledge base holds

The 2026-07-30 MSYS probes establish that a background child existed and
exited with status 0, and that a shell `exec` replaced the shell. Neither
characterizes kernel behavior — they characterize the runtime's presentation
of it.

No fork-emulation cost measurement exists.

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
- [MSYS process manager](MSYS-PROCESS-MANAGER.md)
- [msys-2.0.dll](MSYS-2-0-DLL.md)
