---
id: doc:volume-14:build-system-role-model
title: MSYS2 Build System Role Model
volume: 14
status: partial
model_refs:
  - environment:msys2:ucrt64
evidence_refs: []
last_verified: 2026-07-28
---

# MSYS2 Build System Role Model

| Tool | Role | Evidence boundary |
| --- | --- | --- |
| Autotools | Generates/configures portable make-based builds | `configure` inputs and generated files are build evidence |
| CMake | Generates build graphs and package-consumption metadata | Cache, toolchain file, imported targets, and generator are configuration evidence |
| Meson | Configures project graph and invokes backend | Native/cross files and introspection are configuration evidence |
| Make | Executes declared dependency rules | Makefiles and environment determine effective behavior |
| Ninja | Executes generated dependency graph efficiently | `build.ninja` is generated build evidence |
| `pkg-config` | Resolves compile/link metadata for logical libraries | `.pc` modules identify metadata, not complete ABI compatibility |

## Decision Rules

1. Select the MSYS2 environment before configuration so prefix, compiler, CRT,
   and dependency metadata are coherent.
2. Preserve configuration inputs, generator version, and effective flags as
   evidence for reproducible build claims.
3. Do not infer build outputs from source recipes alone; inspect generated
   artifacts and package contents.
4. Treat CMake and `pkg-config` metadata as separate artifact types linked to
   packages and logical libraries.

## Related Views

- [Toolchain role model](TOOLCHAIN-ROLE-MODEL.md)
- [Pacman architecture](PACMAN-ARCHITECTURE.md)
