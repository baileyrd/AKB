---
id: doc:volume-9:git-for-windows-boundary
title: Git for Windows Distribution Boundary
volume: 9
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs:
  - evidence:git-for-windows:local-installation-observation-2026-07-30
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
`C:\Program Files\Git\usr\bin\bash.exe`. In that same PowerShell host
command context, `ssh.exe` and `curl.exe` resolved to Windows system
locations, not the Git for Windows tree — but this is a PATH-ordering
effect of that specific shell context, not a fixed property of the
distribution: a follow-up observation from a Git Bash session found both
commands resolving to the bundled `Git\usr\bin\ssh.exe` and
`Git\mingw64\bin\curl.exe` instead, each a genuinely different binary
(different OpenSSH release, different TLS library, different compiled
curl feature set) from its system-resolved counterpart. See
[Launcher and Shell Startup](GIT-FOR-WINDOWS-LAUNCHER-STARTUP.md#controlled-local-installation-observation)
and
[Transport, Credentials, and DLL Boundaries](GIT-FOR-WINDOWS-TRANSPORT-BOUNDARIES.md#controlled-local-installation-observation)
for the full comparison. This remains local executable-resolution
evidence only; it does not establish launcher behavior, transport
selection, or bundled component versions for any invocation context not
directly observed.

## Related Views

- [GNU userland role model](GNU-USERLAND-ROLE-MODEL.md)
- [Git (MSYS2 package)](GIT-MSYS-PACKAGE.md) — the plain MSYS2 `git`
  package's own architecture and dependencies, distinct from this page's
  Git for Windows product boundary
- [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)
