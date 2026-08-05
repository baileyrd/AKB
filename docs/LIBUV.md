---
id: doc:volume-6:libuv
title: libuv
volume: 6
status: partial
model_refs:
  - library:libuv:libuv
  - package:msys2:mingw-w64-ucrt-x86_64-libuv
  - component:cmake:cmake
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:libuv:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libuv

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:libuv:libuv` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | libuv project |
| Environments | `ucrt64` |
| Upstream | <https://libuv.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-libuv` |
| Version (observed) | 1.52.1-1 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 1122.81 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:libuv:manual-2026-07-30` — libuv (official project site) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

libuv is a cross-platform asynchronous I/O library, providing an
event-loop abstraction over platform-specific asynchronous I/O primitives
(originally developed for Node.js, and since adopted broadly). This page
documents its architectural role as a directly-declared dependency of
[CMake](CMAKE.md), which uses it internally for asynchronous I/O; see the
[official libuv project site](https://libuv.org/) for the full API
reference.

## Architectural Classification

`library:libuv:libuv` is packaged per native environment: this page
cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-libuv` (version `1.52.1-1` in the
current catalog snapshot). It belongs to the UCRT64 environment and, like
[CMake](CMAKE.md#architectural-classification) itself and the rest of
Volume 8's toolchain components, does not depend on `msys-2.0.dll`, per
the [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).

## Responsibilities

- Providing a cross-platform event-loop and asynchronous I/O abstraction
  (file, network, and process I/O; timers; thread pooling), consumed by
  [CMake](CMAKE.md) for internal asynchronous I/O, historically introduced
  for CMake's now-legacy server mode and retained for other async
  operations, per CMake's own dependency documentation.

## Boundaries

libuv provides a general-purpose asynchronous I/O abstraction
specifically; it is not itself a networking protocol library or an
archive/build-file library — those roles in CMake's dependency set belong
to [libnghttp2](LIBNGHTTP2.md)-family libraries (via `curl`, a separate
CMake dependency) and [libarchive](LIBARCHIVE.md) respectively. libuv
already appeared by package name in
[CMake's dependency table](CMAKE.md#dependencies) before this page
existed.

## Interfaces

- A C API centered on an event loop (`uv_loop_t`) plus handle types for
  asynchronous file, network, timer, and process operations
  (`uv_fs_*`, `uv_tcp_*`, `uv_timer_*`, `uv_spawn`), per the
  documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-libuv` — the only library added in
this batch with no recorded runtime dependencies of its own, alongside
[libxcrypt](LIBXCRYPT.md) from an earlier batch in this volume.

## Reverse Dependencies

The catalog snapshot records 6 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libuv`:
`package:msys2:mingw-w64-ucrt-x86_64-cmake`
(`relationship:toolchain:cmake-requires-libuv` in this knowledge base's
graph), `package:msys2:mingw-w64-ucrt-x86_64-libluv` (a Lua binding to
libuv), `package:msys2:mingw-w64-ucrt-x86_64-libwebsockets`,
`package:msys2:mingw-w64-ucrt-x86_64-neovim`,
`package:msys2:mingw-w64-ucrt-x86_64-python-winloop`, and
`package:msys2:mingw-w64-ucrt-x86_64-ttyd`, none of which are otherwise
documented in this knowledge base.

## Configuration

libuv has no persistent configuration file of its own; event-loop and
handle behavior are controlled entirely through its C API by the calling
program.

## Initialization and Execution Flow

As a library, libuv has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it —
[CMake](CMAKE.md) in this dependency chain, running its own event loop
internally for the asynchronous operations CMake's dependency
documentation describes. As a native MinGW-w64 library, this process
model is Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Which specific asynchronous operations CMake actually exercises through
libuv at a given time was not characterized while writing this page;
CMake's own dependency note (cited in Responsibilities) attributes the
dependency to internal async I/O rather than a single, narrowly scoped
feature.

## Compatibility and Variants

Whether other native environments (CLANG64, i686) in this catalog package
libuv separately was not confirmed while writing this page; this is
recorded as an open item rather than assumed either way.

## Security Considerations

libuv is not itself a cryptography or authentication component; its
asynchronous I/O role in CMake carries the general trust considerations
of any file/network I/O layer rather than a distinct security surface of
its own. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.52.1-1` version.

## Failure Modes and Diagnostics

This page does not characterize libuv-specific failure modes within
CMake, since CMake's own dependency documentation does not attribute a
single, distinctly diagnosable feature to this dependency the way it does
for [cppdap](CPPDAP.md) (debugger) or [rhash](RHASH.md) (hashing).

## Evidence, Assumptions, and Open Questions

Asynchronous I/O abstraction scope is backed by the official libuv
project site (`evidence:libuv:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-libuv` in the catalog. Package
identity, version, and the recorded dependent edges are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open: whether other
native environments package libuv separately was not confirmed, and which
specific CMake operations currently exercise libuv was not directly
characterized. Also explicitly out of scope for this page: header-level
API surface and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libuv"]
    u0["CMake"]
    u0 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:libuv:libuv` in the composed graph: 1 dependent and 0 dependencies.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [CMake](CMAKE.md)
- [libarchive](LIBARCHIVE.md)
