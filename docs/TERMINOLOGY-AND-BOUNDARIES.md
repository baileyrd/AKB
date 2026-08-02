---
id: doc:volume-1:terminology-and-boundaries
title: MSYS2 Terminology and Boundary Decisions
volume: 1
status: partial
model_refs:
  - ecosystem:msys2:msys2
  - runtime:msys2:msys-2.0.dll
evidence_refs: []
last_verified: 2026-07-28
---

# MSYS2 Terminology and Boundary Decisions

| Term | Canonical meaning | Must not be conflated with |
| --- | --- | --- |
| MSYS2 | The Windows software distribution, build platform, repositories, and tooling ecosystem | The MSYS runtime or one shell |
| MSYS | POSIX-oriented environment and package set under `/usr` | Native MinGW/UCRT/Clang outputs |
| MSYS runtime | `msys-2.0.dll` compatibility runtime used by MSYS-dependent programs | A Windows CRT or MinGW-w64 |
| Environment | A selected prefix, toolchain/CRT/ABI convention, and package namespace | A package repository alone |
| Package | A versioned pacman archive/metadata identity | An installed file or logical library |
| Artifact | A concrete installed or archive file: EXE, DLL, header, `.a`, `.pc`, etc. | Its owning package or logical API |
| CRT | C runtime ABI and object-ownership boundary | Compiler family or C++ standard library |
| ABI | Binary compatibility contract for a target, including architecture and runtime constraints | API source compatibility |
| Observation | Timestamped generated fact from collector evidence | Reviewed architectural conclusion |

## Boundary Decisions

1. Model distribution, environment, repository, package, artifact, and logical library as separate entities.
2. Treat generated catalog/inventory/runtime data as observations; it cannot overwrite authored conclusions.
3. Treat MSYS-dependent and native programs as distinct runtime classes.
4. Do not infer ABI compatibility from a package-name prefix alone; verify target, CRT, architecture, and boundary behavior.
5. Generate reverse relationships from directional evidence rather than maintaining duplicate facts.

## Related Views

- [Ecosystem context](ECOSYSTEM-CONTEXT.md)
- [Domain decomposition](DOMAIN-DECOMPOSITION.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)

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
