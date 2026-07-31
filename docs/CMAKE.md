---
id: doc:volume-8:cmake
title: CMake
volume: 8
status: partial
model_refs:
  - component:cmake:cmake
  - package:msys2:mingw-w64-ucrt-x86_64-cmake
  - library:google:cppdap
  - library:jsoncpp:jsoncpp
  - library:libarchive:libarchive
  - library:libuv:libuv
  - library:rhash:rhash
  - library:libexpat:expat
  - library:gnu:zlib
  - library:curl:curl@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:cmake:documentation-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# CMake

## Purpose

CMake is a cross-platform build-system generator, and it is the widest and
most feature-rich generator documented in this batch, with dependencies
spanning networking, archiving, hashing, and debugging support. This page
documents its architectural role and its unusually feature-driven
dependency set; see the
[official CMake documentation](https://cmake.org/cmake/help/latest/) for
the full `CMakeLists.txt` language and command reference.

## Architectural Classification

`component:cmake:cmake` is packaged per native environment: this page
cites the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-cmake`
(version `4.4.0-1` in the current catalog snapshot, license `MIT`),
developed by Kitware, Inc. It belongs to the UCRT64 environment and, like
the rest of this volume's toolchain components, does **not** depend on
`msys-2.0.dll`, per the
[MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).

## Responsibilities

- Reading a project's `CMakeLists.txt` build description and generating
  build files — in this environment, by default invoking
  [Ninja](NINJA.md) as its generated backend
  (`relationship:toolchain:cmake-invokes-ninja`) — rather than compiling
  anything itself.
- Supplying a broad set of built-in commands well beyond core build-file
  generation: network downloads, archive creation, file hashing, and a
  Debug Adapter Protocol server for debugging CMake scripts themselves
  (`claim:component:cmake:feature-dependencies`).

## Boundaries

Like [Meson](MESON.md), CMake is a generator, not a build executor; the
actual compiler and linker invocations are carried out by whichever backend
it targets. CMake supports multiple generators (Makefiles, Ninja, Visual
Studio project files, and others) depending on platform and configuration;
this package's dependency on `ninja` specifically reflects Ninja's role as
a commonly used default in this environment, not the only generator CMake
supports.

## Interfaces

- `cmake` (configure/generate), `cmake --build` (a frontend that invokes
  the underlying generator's build tool), `ctest` (test execution), `cpack`
  (packaging), and the `CMakeLists.txt`/`CMakePresets.json` description
  files, per the documentation.

## Dependencies

The catalog snapshot records ten `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-cmake` — the widest dependency
footprint of any build-system tool documented in this batch, each mapping
to a specific built-in CMake feature
(`claim:component:cmake:feature-dependencies`):

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Debug Adapter Protocol | `mingw-w64-ucrt-x86_64-cppdap` | Backs CMake's `--debugger` DAP server, letting IDEs debug `CMakeLists.txt` script execution itself. Documented fully in [cppdap](CPPDAP.md). |
| Network downloads | `mingw-w64-ucrt-x86_64-curl` | Backs `file(DOWNLOAD)` and `ExternalProject`'s network-fetch operations. Documented fully in [curl (UCRT64)](CURL-UCRT64.md) — **correction, 2026-07-30**: this row previously (falsely) claimed this was "the same library documented fully in [curl](CURL.md)," but CURL.md documents the MSYS curl CLI, a separate catalog entity from this UCRT64-native package. |
| XML parsing | `mingw-w64-ucrt-x86_64-expat` | Backs XML-format handling used by some CMake generators and CTest/CDash reporting. Documented fully in [Expat](EXPAT.md). |
| JSON support | `mingw-w64-ucrt-x86_64-jsoncpp` | Backs CMake's JSON-based file-api and `CMakePresets.json`/`CMakeUserPresets.json` support. Documented fully in [JsonCpp](JSONCPP.md). |
| Archive creation/extraction | `mingw-w64-ucrt-x86_64-libarchive` | Backs `file(ARCHIVE_CREATE)`/`file(ARCHIVE_EXTRACT)` and CPack's archive-format generator. Documented fully in [libarchive](LIBARCHIVE.md). |
| Asynchronous I/O | `mingw-w64-ucrt-x86_64-libuv` | Backs internal asynchronous I/O, historically introduced for CMake's server mode and retained for other async operations. Documented fully in [libuv](LIBUV.md). |
| Build backend | `mingw-w64-ucrt-x86_64-ninja` | Invoked as CMake's generated backend in this environment (`relationship:toolchain:cmake-invokes-ninja`), documented fully in [Ninja](NINJA.md). |
| Dependency discovery | `mingw-w64-ucrt-x86_64-pkgconf` | Backs `find_package`'s pkg-config search mode, documented fully in [pkgconf](PKGCONF.md). |
| File hashing | `mingw-w64-ucrt-x86_64-rhash` | Backs `file(MD5)`/`file(SHA256)`-style hashing commands across multiple algorithms. Documented fully in [RHash](RHASH.md). |
| Compression | `mingw-w64-ucrt-x86_64-zlib` | Backs compression used internally by the archive and networking features above. Documented fully in [zlib](ZLIB.md). |

An optional dependency on `emacs` backs CMake's Emacs editing mode, per the
package's own dependency note.

**Correction, 2026-07-30**: the expat and zlib rows above were already
marked "documented fully in" in this table since publication, but two
of the ten edges (to Expat and zlib) had never actually been added to
the graph — `relationship:toolchain:cmake-requires-expat` and
`relationship:toolchain:cmake-requires-zlib` are now added to close the
gap, matching the graph-completeness corrections found elsewhere in
this volume this session.

## Reverse Dependencies

The snapshot records 12 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-cmake` — the highest
reverse-dependency count of any build-system tool documented in this batch.
See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

`CMakeLists.txt` is the primary project build description;
`CMakePresets.json`/`CMakeUserPresets.json` (backed by the `jsoncpp`
dependency above) provide a newer, shareable way to declare common
configure/build/test option sets without embedding them in scripts.

## Initialization and Execution Flow

`cmake` reads `CMakeLists.txt`, resolves dependencies (invoking
[pkgconf](PKGCONF.md) as needed), and generates backend build files; a
subsequent `cmake --build` invokes the backend
([Ninja](NINJA.md#initialization-and-execution-flow) by default in this
environment) as a subprocess. As a native MinGW-w64 program, this process
model is Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

As with [Meson](MESON.md#runtime-behavior), once generation is complete,
actual build execution and its parallelism/incremental-rebuild behavior are
delegated to and follow [Ninja](NINJA.md)'s documented behavior; CMake's own
runtime role concentrates in the configure/generate phase and in
higher-level commands like `ctest`/`cpack`.

## Compatibility and Variants

CMake's multi-generator support (this page's UCRT64 package specifically
depends on Ninja, but CMake itself is generator-agnostic) means a project's
actual build tool is a configuration choice, not fixed by CMake itself;
scripts assuming a specific generator's behavior are a documented
portability risk the CMake language itself does not fully abstract away.

## Security Considerations

`file(DOWNLOAD)`/`ExternalProject` fetching from network sources
(via the `curl` dependency) inherits [curl](CURL.md#security-considerations)'s
general network-trust considerations; CMake scripts, like Meson's, can run
arbitrary external commands during configuration. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review has
been performed for the recorded `4.4.0-1` version.

## Failure Modes and Diagnostics

Dependency-discovery failures should first be checked against
[pkgconf](PKGCONF.md#failure-modes-and-diagnostics)'s guidance; build-execution
failures after successful configuration should be checked against
[Ninja](NINJA.md#failure-modes-and-diagnostics); network-fetch failures in
`file(DOWNLOAD)`/`ExternalProject` should be checked against
[curl](CURL.md#failure-modes-and-diagnostics)'s diagnostics.

## Evidence, Assumptions, and Open Questions

Generator design and command behavior are backed by the official CMake
documentation (`evidence:cmake:documentation-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-cmake` in the catalog. Package
identity, version, license, and all recorded dependency edges are backed by
the pacman catalog snapshot (`evidence:catalog:current`) via
`claim:component:cmake:feature-dependencies`. No open items beyond the
general version-qualified security review noted above.

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [Ninja](NINJA.md)
- [pkgconf](PKGCONF.md)
- [Meson](MESON.md)
- [curl (UCRT64)](CURL-UCRT64.md)
- [cppdap](CPPDAP.md)
- [JsonCpp](JSONCPP.md)
- [libarchive](LIBARCHIVE.md)
- [libuv](LIBUV.md)
- [RHash](RHASH.md)
