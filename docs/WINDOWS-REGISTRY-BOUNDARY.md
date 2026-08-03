---
id: doc:volume-2:registry-boundary
title: Windows Registry Boundary
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

# Windows Registry Boundary

> **Contextual scope.** This page documents the *boundary* between MSYS2 and
> a Windows subsystem — what MSYS2 depends on, where this knowledge base's
> claims stop, and what evidence an exact claim would need. It is not a
> Windows internals reference. See
> [ADR 0001](../charter/adr/0001-windows-platform-contextual-scope.md).

## Purpose

The registry is Windows' configuration store. This page exists mainly to
record what MSYS2 does **not** take from it.

## What MSYS2 depends on

Nothing structural. The MSYS runtime's configuration comes from `/etc/fstab`
and environment variables, not from the registry. Registry integration is a
host or per-application concern rather than an implied MSYS runtime service —
the existing boundary table states this and it remains correct.

Individual applications distributed through MSYS2 may read the registry;
that is the application's behavior, not the runtime's.

## Where the boundary sits

Installers and launchers may record locations in the registry, and that is
where an installation's own footprint becomes a registry fact. The
distinction to preserve: an MSYS2 program reading a registry key is doing
Windows-native work, not POSIX work, regardless of which environment it was
packaged for.

## Evidence required for an exact claim

Specific application configuration evidence — a named program, a named key,
and an observation of the read.

## What this knowledge base holds

None. No registry key is recorded anywhere in this knowledge base, and no
program's registry use has been observed. Given the negative claim above,
that absence is consistent rather than concerning, but it is an absence
either way.

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
- [MSYS environment manager](MSYS-ENVIRONMENT-MANAGER.md)
