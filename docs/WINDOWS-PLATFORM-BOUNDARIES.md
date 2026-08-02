---
id: doc:volume-2:windows-platform-boundaries
title: Windows Platform Boundaries for MSYS2
volume: 2
status: partial
model_refs:
  - ecosystem:msys2:msys2
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# Windows Platform Boundaries for MSYS2

Windows is the host platform for both the MSYS POSIX-emulation runtime and
native MinGW-w64 environment executables. This volume records only the host
services needed to understand those boundaries; it is not a general Windows
internals reference.

**That narrowing is now recorded as a decision** rather than left implicit:
[ADR 0001](../charter/adr/0001-windows-platform-contextual-scope.md). It also
explains why this volume will stay thinner than volumes covering MSYS2's own
components — permanently, and by design.

Each row below has its own boundary page as of 2026-08-02.

| Host concern | Boundary relevant to MSYS2 | Evidence needed for an exact claim |
| --- | --- | --- |
| [NT kernel](WINDOWS-NT-KERNEL-BOUNDARY.md) — process and handles | MSYS-dependent processes adapt POSIX-facing lifecycle expectations; native programs use Windows process semantics directly | Version-qualified runtime source and controlled process probe |
| [Win32 APIs and loader](WINDOWS-WIN32-API-BOUNDARY.md) | PE executables and DLLs are loaded by the Windows loader; import tables identify declared imports, not the resolved runtime load result | PE import evidence plus controlled loader observation |
| [Console and ConPTY](WINDOWS-CONSOLE-CONPTY-BOUNDARY.md) | Terminal-facing behavior crosses between Windows console facilities, pipes, PTYs, and the selected shell/runtime | Terminal/PTY test matrix on a named Windows build |
| [Filesystems](WINDOWS-FILESYSTEM-BOUNDARY.md) | Drive letters, UNC paths, file attributes, case behavior, and reparse points remain host filesystem concerns | Filesystem probes on the target volume and policy configuration |
| [Registry](WINDOWS-REGISTRY-BOUNDARY.md) | Windows registry integration is a host/application concern, not an implied MSYS runtime service | Specific application configuration evidence |
| [Security](WINDOWS-SECURITY-BOUNDARY.md) | ACLs, tokens, process integrity, signing, and credential stores are Windows boundaries; package signatures are a separate distribution trust control | Host-security configuration and package-signature evidence |
| [Networking](WINDOWS-NETWORKING-BOUNDARY.md) | Native Winsock/TLS behavior and MSYS process adaptation are distinct layers | Captured transport configuration and execution trace |

## Runtime distinction

An MSYS process may expose POSIX paths and mounts while still executing on a
Windows host. A UCRT64, MINGW64, or CLANG64 executable is a native Windows PE
program unless direct binary evidence shows it depends on `msys-2.0.dll`.
Distribution branding, shell selection, and a package-name prefix do not prove
that dependency.

The bounded local MSYS observation records path conversion and the mount table
of the shell that executed it. It is evidence of that MSYS runtime context,
not proof of Windows loader, registry, filesystem, console, or networking
behavior generally.

## Controlled local host observation

On 2026-07-30, non-privileged host APIs reported Windows NT `10.0.26200.8973`
on x64, with `C:\Windows\system32` as the system directory. Console output
was redirected in the automated collection context. WMI operating-system and
volume queries were denied by host access policy, so this observation does not
claim filesystem type, edition, or management-API behavior.

## Interface map

```mermaid
flowchart LR
    H["Windows host: process, loader, console, filesystem"]
    M["MSYS runtime and shell"]
    N["Native UCRT64/MINGW/CLANG program"]
    H --> M
    H --> N
    M -. "POSIX-facing adaptation" .-> H
    N -. "Win32-facing execution" .-> H
```

## Related views

- [MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
- [Binary DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md)
- [Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["MSYS2"]
    d0["Microsoft Windows"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `ecosystem:msys2:msys2` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->
