---
id: doc:volume-1:domain-decomposition
title: MSYS2 L2 Domain Decomposition
volume: 1
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs: []
last_verified: 2026-07-30
---

# MSYS2 L2 Domain Decomposition

| Domain | Responsibility | Primary volumes | Drill-down |
| --- | --- | --- | --- |
| Windows integration | Win32, console, loader, filesystem, security boundaries | 2 | [Windows platform boundaries](WINDOWS-PLATFORM-BOUNDARIES.md) |
| POSIX runtime | `msys-2.0.dll`, process adaptation, paths, mounts, PTYs | 3 | [MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md) |
| Environment and ABI | MSYS/native environments, CRT, compiler, architecture compatibility | 4 | [Runtime environments](RUNTIME-ENVIRONMENTS.md) |
| Userland | Shells, GNU tools, configuration, startup | 5 | [GNU userland role model](GNU-USERLAND-ROLE-MODEL.md) (29 per-tool pages) |
| Libraries and artifacts | DLLs, archives, headers, metadata, ABI relationships | 6 and 11 | [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md) |
| Package lifecycle | Pacman, repositories, signing, transactions, snapshots | 7 and 11 | [Pacman architecture](PACMAN-ARCHITECTURE.md) |
| Toolchains and builds | Compilers, linkers, debuggers, recipes, build systems | 8 and 14 | [Toolchain role model](TOOLCHAIN-ROLE-MODEL.md) (14 per-tool pages), [Build system role model](BUILD-SYSTEM-ROLE-MODEL.md) |
| Distribution integrations | Git for Windows, launchers, transports, credentials | 9 | [Git for Windows distribution boundary](GIT-FOR-WINDOWS-BOUNDARY.md), [Git (MSYS2 package)](GIT-MSYS-PACKAGE.md) |
| Evidence and navigation | Graph, sources, generated views, dependency analysis, explorer | 10, 12, 13, and 20 | [Diagram hierarchy](DIAGRAM-HIERARCHY.md), [Reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md) |
| Assurance and operations | Security, performance, developer and operator workflows | 16–19 | [Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md), [Developer workflow](DEVELOPER-WORKFLOW.md), [Operator refresh workflow](OPERATOR-REFRESH-WORKFLOW.md) |

## Boundary Rules

Domains are ownership and navigation boundaries, not containment claims.
Package ownership belongs to the package-lifecycle domain; runtime behavior
belongs to the POSIX-runtime or native-environment domain; evidence preserves
the source and confidence of each relationship.

## Related Views

- [Ecosystem context](ECOSYSTEM-CONTEXT.md)
- [Eight-layer architecture](EIGHT-LAYER-ARCHITECTURE.md)
- [Master volume index](MASTER-VOLUME-INDEX.md)
