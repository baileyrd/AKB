---
id: doc:volume-14:build-system-role-model
title: MSYS2 Build System Role Model
volume: 14
status: partial
model_refs:
  - environment:msys2:ucrt64
  - component:gnu:autoconf
  - component:gnu:automake
  - component:gnu:libtool
  - component:cmake:cmake
  - component:mesonbuild:meson
  - component:gnu:make
  - component:ninja-build:ninja
  - component:pkgconf:pkgconf
evidence_refs: []
last_verified: 2026-07-30
---

# MSYS2 Build System Role Model

| Tool | Role | Evidence boundary | Component architecture |
| --- | --- | --- | --- |
| Autotools | Generates/configures portable make-based builds | `configure` inputs and generated files are build evidence | [GNU Autoconf](GNU-AUTOCONF.md), [GNU Automake](GNU-AUTOMAKE.md), [GNU Libtool](GNU-LIBTOOL.md) |
| CMake | Generates build graphs and package-consumption metadata | Cache, toolchain file, imported targets, and generator are configuration evidence | [CMake](CMAKE.md) |
| Meson | Configures project graph and invokes backend | Native/cross files and introspection are configuration evidence | [Meson](MESON.md) |
| Make | Executes declared dependency rules | Makefiles and environment determine effective behavior | [GNU Make](GNU-MAKE.md) |
| Ninja | Executes generated dependency graph efficiently | `build.ninja` is generated build evidence | [Ninja](NINJA.md) |
| `pkg-config` | Resolves compile/link metadata for logical libraries | `.pc` modules identify metadata, not complete ABI compatibility | [pkgconf](PKGCONF.md) |

The rightmost column links to each tool's Volume 8 component page —
dependencies, packaging, invocation model, and per-tool evidence. This
table stays focused on the build-evidence framing specific to this volume;
it does not restate that architectural material, per the cross-volume rule
that a concept is defined once and referenced elsewhere by stable object ID.

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
