---
id: doc:volume-1:domain-decomposition
title: MSYS2 L2 Domain Decomposition
volume: 1
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs: []
last_verified: 2026-07-28
---

# MSYS2 L2 Domain Decomposition

| Domain | Responsibility | Primary volumes |
| --- | --- | --- |
| Windows integration | Win32, console, loader, filesystem, security boundaries | 2 |
| POSIX runtime | `msys-2.0.dll`, process adaptation, paths, mounts, PTYs | 3 |
| Environment and ABI | MSYS/native environments, CRT, compiler, architecture compatibility | 4 |
| Userland | Shells, GNU tools, configuration, startup | 5 |
| Libraries and artifacts | DLLs, archives, headers, metadata, ABI relationships | 6 and 11 |
| Package lifecycle | Pacman, repositories, signing, transactions, snapshots | 7 and 11 |
| Toolchains and builds | Compilers, linkers, debuggers, recipes, build systems | 8 and 14 |
| Distribution integrations | Git for Windows, launchers, transports, credentials | 9 |
| Evidence and navigation | Graph, sources, generated views, dependency analysis, explorer | 10, 12, 13, and 20 |
| Assurance and operations | Security, performance, developer and operator workflows | 16–19 |

## Boundary Rules

Domains are ownership and navigation boundaries, not containment claims.
Package ownership belongs to the package-lifecycle domain; runtime behavior
belongs to the POSIX-runtime or native-environment domain; evidence preserves
the source and confidence of each relationship.

## Related Views

- [Ecosystem context](ECOSYSTEM-CONTEXT.md)
- [Eight-layer architecture](EIGHT-LAYER-ARCHITECTURE.md)
- [Master volume index](MASTER-VOLUME-INDEX.md)
