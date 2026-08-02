---
id: doc:volume-9:git-for-windows-boundary
title: Git for Windows Distribution Boundary
volume: 9
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs: []
last_verified: 2026-07-30
---

# Git for Windows Distribution Boundary

Git for Windows is a distinct distribution that packages native Git for
Windows users while incorporating MSYS-derived tooling where that supports the
shell and Unix-like workflow. It is not an MSYS2 installation and does not
share a pacman-managed lifecycle with one.

| Concern | Git for Windows boundary | MSYS2 boundary |
| --- | --- | --- |
| Distribution lifecycle | Git for Windows releases/installers and bundled components | Pacman repositories and local package database |
| Git executable | Native Windows Git is the primary product boundary | Git may be MSYS-dependent or native by selected package/environment |
| Shell experience | Git Bash and bundled terminal/shell integration | MSYS shell/environment and native MSYS2 environments |
| Runtime artifacts | Bundled and release-qualified | Installed package artifacts and evidence snapshots |

## Decision Rules

1. Model Git for Windows and MSYS2 as related distributions with separate
   package and release provenance.
2. Trace an executable’s runtime DLLs and launch path before claiming a shared
   runtime behavior.
3. Treat SSH, credential management, HTTP/libcurl, OpenSSL, and DLL loading as
   dedicated integration domains rather than attributes of Git alone.

## Controlled local installation observation

On 2026-07-30, the installed command resolved to
`C:\Program Files\Git\cmd\git.exe`, reporting Git for Windows
`2.55.0.windows.3`; the bundled Bash resolved to
`C:\Program Files\Git\usr\bin\bash.exe`. In the same host command context,
`ssh.exe` and `curl.exe` resolved to Windows system locations, not the Git for
Windows tree. This is local executable-resolution evidence only; it does not
establish launcher behavior, transport selection, DLL loading, or bundled
component versions not directly observed.

## Related Views

- [GNU userland role model](GNU-USERLAND-ROLE-MODEL.md)
- [Git (MSYS2 package)](GIT-MSYS-PACKAGE.md) — the plain MSYS2 `git`
  package's own architecture and dependencies, distinct from this page's
  Git for Windows product boundary
- [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)

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
