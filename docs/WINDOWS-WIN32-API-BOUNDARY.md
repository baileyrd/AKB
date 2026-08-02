---
id: doc:volume-2:win32-api-boundary
title: Windows Win32 API and Loader Boundary
volume: 2
status: partial
model_refs:
  - platform:microsoft:windows
  - layer:msys2:1-windows-kernel-services
  - layer:msys2:2-windows-user-mode-apis
evidence_refs:
  - evidence:microsoft:dll-search-order-2026-08-02
last_verified: 2026-08-02
---

# Windows Win32 API and Loader Boundary

> **Contextual scope.** This page documents the *boundary* between MSYS2 and
> a Windows subsystem — what MSYS2 depends on, where this knowledge base's
> claims stop, and what evidence an exact claim would need. It is not a
> Windows internals reference. See
> [ADR 0001](../charter/adr/0001-windows-platform-contextual-scope.md).

## Purpose

Win32 is the API surface native MSYS2 programs call directly and the MSYS
runtime calls on behalf of POSIX programs. The image loader is what binds a
PE file's declared imports to actual DLLs at load time.

## What MSYS2 depends on

The Win32 API for every operation the POSIX layer approximates, and the
loader to resolve each executable's imports — including `msys-2.0.dll`
itself for MSYS-linked binaries.

## Where the boundary sits

**Declared imports are not resolved imports.** A PE import table states what
an image asks for; the loader's search order determines what it gets. Those
are different facts, and this knowledge base's
[binary dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md) records the first.

That gap is the mechanism behind
[Git for Windows DLL loading](GIT-FOR-WINDOWS-DLL-LOADING.md): two
MSYS2-derived installations can both supply `msys-2.0.dll`, and search order
decides.

## Evidence required for an exact claim

PE import evidence plus a controlled loader observation on a named build —
the second being what distinguishes declared from resolved.

## What this knowledge base holds

PE import extraction exists in the
[deep-inventory pipeline](DEEP-INVENTORY-CONTRACT.md) and has been run
against 2 of 15,711 packages. No loader observation of any kind exists, so
no resolved-import claim can be made here at all.

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
- [Binary-to-DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md)
- [Git for Windows DLL loading](GIT-FOR-WINDOWS-DLL-LOADING.md)
