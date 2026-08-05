---
id: doc:volume-6:zlib
title: zlib
volume: 6
status: partial
model_refs:
  - library:gnu:zlib
  - package:msys2:mingw-w64-ucrt-x86_64-zlib
  - environment:msys2:ucrt64
  - header-set:gnu:zlib-headers
  - pkg-config-module:gnu:zlib-pc
  - static-library:gnu:libz.a
  - import-library:gnu:libz.dll.a
  - dll:gnu:zlib1.dll
evidence_refs:
  - evidence:zlib:manual-2026-07-30
  - evidence:catalog:current
  - evidence:zlib:ucrt64-archive-analysis-2026-07-29
last_verified: 2026-07-30
---

# zlib

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnu:zlib` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Jean-loup Gailly and Mark Adler |
| Environments | `ucrt64` |
| Upstream | <https://www.zlib.net/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-zlib` |
| Version (observed) | 1.3.2-2 |
| License (observed) | spdx:Zlib |
| Architecture (observed) | any |
| Installed size (observed) | 427.78 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:zlib:manual-2026-07-30` — zlib Manual (`primary`, retrieved 2026-07-30)

**Claims about this object**

- `claim:library:zlib:hub` (`observation`, `verified`) — zlib is the most-depended-upon package observed in this catalog snapshot among all components and libraries modeled in this knowledge base, with 299 recorded reverse dependents, exceeding gcc-libs' 167.

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Zlib implements the DEFLATE compression algorithm behind gzip, PKZIP, and
countless other formats and libraries, and — per this snapshot — it is the
most-depended-upon package among the components and libraries this
knowledge base actually models (`claim:library:zlib:hub`), not the
highest reverse-dependency count in the full generated catalog view,
where several undocumented packages (Python, glib2, Qt6, Perl) exceed
it — see Reverse Dependencies below. This page documents its
architectural centrality; see the
[official zlib manual](https://www.zlib.net/manual.html) for the API
reference.

## Architectural Classification

`library:gnu:zlib` is packaged per native environment: this page cites the
UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-zlib` (version
`1.3.2-2` in the current catalog snapshot, license `Zlib` — the
library's own short, permissive license, distinct from the GPL/LGPL
licensing common elsewhere in this knowledge base), authored by Jean-loup
Gailly and Mark Adler. **Update, 2026-07-30**: the fuller
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology (headers, `pkg-config`/CMake metadata, PE import/export
analysis) is now applied here — the first library in this knowledge base
to receive it — via a static analysis of the package archive itself; see
Interfaces and Evidence below. **Update, 2026-07-31**: a second library,
[zstd (UCRT64)](LIBZSTD.md#family-classification), now has this same
treatment. The other documented library pages — 157 exist as of 2026-08-02 — do not yet have it
and remain scoped to package/dependency-level evidence only.

## Responsibilities

- Providing the DEFLATE compression/decompression algorithm as a shared
  library, consumed by other libraries and programs rather than used
  standalone from the command line (that role belongs to
  [GNU Gzip](GNU-GZIP.md), a separate, independent implementation of the
  same underlying format).

## Boundaries

Zlib is a library, not a CLI tool; it has no standalone user-facing
interface. It implements only DEFLATE-family compression, distinct from the
Burrows-Wheeler ([bzip2](BZIP2.md)), LZMA2 ([XZ Utils](XZ-UTILS.md)), and
other compression algorithms documented elsewhere in this knowledge base.

## Interfaces

- A C API (`deflate()`/`inflate()` and the higher-level `gzread()`/`gzwrite()`
  family) for in-process compression and decompression, consumed by
  linking, per the manual. This page does not enumerate the full
  header-level surface; that belongs to
  [Header and Development-Metadata Indexes](HEADER-AND-METADATA-INDEXES.md).

## Family Classification

A 2026-07-29 static analysis of the UCRT64 package archive
(`ucrt-zlib.pkg.tar.zst`) recorded all six member types the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology distinguishes, each now a separate typed entity in this
knowledge base's graph:

- **Headers** — `header-set:gnu:zlib-headers`: `zlib.h` and `zconf.h`
  (`/ucrt64/include/`).
- **`pkg-config` module** — `pkg-config-module:gnu:zlib-pc`: `zlib.pc`
  declares `-I/ucrt64/include` and `-L/ucrt64/lib -lz`, with no further
  `Requires:`.
- **Static library** — `static-library:gnu:libz.a`: 15 object members
  (`deflate.o`, `inflate.o`, the `gz*.o` family, and related), the
  library's own compiled implementation.
- **Import library** — `import-library:gnu:libz.dll.a`: 116 members —
  per-export link-time thunks for the DLL below, not a second copy of the
  implementation (Classification Rule 4).
- **Runtime DLL** — `dll:gnu:zlib1.dll`: 114 recorded exports and 9
  imported system DLLs (eight `api-ms-win-crt-*` UCRT split DLLs plus
  `kernel32.dll`) — no imported dependency on any other MSYS2-packaged
  library, consistent with the empty Dependencies table below.

All six are attributed to the same
`package:msys2:mingw-w64-ucrt-x86_64-zlib` package ownership. This
establishes classification evidence only — which artifacts exist and how
they relate structurally — not source-to-binary byte identity or ABI
compatibility across versions, per Classification Rule 5.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-zlib` beyond its membership in the
UCRT64 repository and environment — a minimal dependency footprint
consistent with zlib's small, self-contained, widely portable design.

## Reverse Dependencies

The snapshot records **299** relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-zlib` — the largest reverse-dependency
count of any *modeled* component or library in this knowledge base
(`claim:library:zlib:hub`), exceeding [gcc-libs](LIBSTDCXX.md#reverse-dependencies)'s
167 and far exceeding [ncurses](NCURSES.md#reverse-dependencies)'s 40.
**Correction, 2026-07-30**: this is not the largest count in the full
generated catalog view — `generated/reverse-dependency-impact.json`
itself records `mingw-w64-ucrt-x86_64-python` at 965, `glib2` at 186, and
several other undocumented packages above zlib's 297
`runtime-depends-on`-only count; no page in this knowledge base yet
documents Python, glib2, Qt6, or Perl, so the claim's own careful
scoping ("among all components and libraries modeled in this knowledge
base") was accurate, but the surrounding prose previously dropped that
qualifier. This reflects DEFLATE compression's use as a near-universal
building block
across compilers ([GCC](GNU-GCC.md), [Clang](CLANG.md), [LLD](LLD.md)),
build systems ([CMake](CMAKE.md)), network transfer
([curl (UCRT64)](CURL-UCRT64.md)), version control
([Git](GIT-MSYS-PACKAGE.md)), and archive tools
([GNU Tar](GNU-TAR.md)'s optional codec linkage question flagged on that
page) across this environment. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list. That page's worked example uses zlib to show
this **299** figure alongside two narrower, differently-scoped counts: 297
`runtime-depends-on`-only catalog edges, and 34 byte-level PE importers
observed on one bounded installation
(`generated/binary-dependency-graph.json`) — the same
`dll:gnu:zlib1.dll` this page's Family Classification section documents.

## Configuration

Zlib has no persistent configuration file or environment variables; its
behavior is controlled entirely by the compression-level and
stream-management parameters a calling program passes to its C API.

## Initialization and Execution Flow

As a library, zlib has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it, the
same model documented for [libstdc++](LIBSTDCXX.md#initialization-and-execution-flow)
and [libc++](LIBCXX.md#initialization-and-execution-flow).

## Runtime Behavior

Given 299 recorded dependents, zlib's compression/decompression correctness
and performance are load-bearing for a very large fraction of this
environment's software; this page does not attempt to characterize that
behavior beyond noting its centrality (per Reverse Dependencies above).

## Compatibility and Variants

The DEFLATE format zlib implements is a stable, widely standardized format
(the basis for gzip, PNG, and PKZIP's default compression method); this
page does not document zlib-specific API version compatibility beyond
noting the recorded `1.3.2-2` version.

## Security Considerations

Given its 299 recorded dependents, zlib carries the widest observed blast
radius of any component or library documented in this knowledge base: a
defect here would potentially affect nearly every other tool this
knowledge base has documented, from compilers to version control to
archive tools. This is a risk-concentration observation, not an assertion
of an actual defect. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review has
been performed for the recorded `1.3.2-2` version — a priority candidate
for one, given the dependency count recorded here.

## Failure Modes and Diagnostics

Zlib itself has no user-facing CLI to diagnose directly; compression- or
decompression-related failures in a dependent tool should be triaged
against that tool's own documentation first, since zlib's C API surfaces
errors through return codes a calling program is responsible for handling
and reporting.

## Evidence, Assumptions, and Open Questions

The compression model is backed by the official zlib manual
(`evidence:zlib:manual-2026-07-30`), matching the `project_url` already
recorded for `package:msys2:mingw-w64-ucrt-x86_64-zlib` in the catalog.
Package identity, version, license, and the reverse-dependency count are
backed by the pacman catalog snapshot (`evidence:catalog:current`) via
`claim:library:zlib:hub`. The Family Classification section above is
backed by a local, hash-verified package-archive static analysis
(`evidence:zlib:ucrt64-archive-analysis-2026-07-29`), local-only per
[Local-Only Evidence Retention](LOCAL-EVIDENCE-RETENTION.md) and
reproducible by re-running `tools/analyze_package_archive.py` against the
same archive. Still open: no version-qualified CVE review has been
performed despite this library's unusually wide blast radius; the family
classification applied here has not yet been applied to the other 103
documented library pages.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["zlib"]
    u0["CMake"]
    u0 -->|requires| subject
    u1["GNU Binutils"]
    u1 -->|requires| subject
    u2["GCC"]
    u2 -->|requires| subject
    u3["GDB"]
    u3 -->|requires| subject
    u4["curl (UCRT64)"]
    u4 -->|requires| subject
    u5["libxml2"]
    u5 -->|requires| subject
    u6["GnuTLS (UCRT64)"]
    u6 -->|requires| subject
    u7["libarchive"]
    u7 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnu:zlib` in the composed graph: 13 dependents and 0 dependencies, of which 5 are omitted here for legibility.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libstdc++](LIBSTDCXX.md)
- [libc++](LIBCXX.md)
- [GNU Gzip](GNU-GZIP.md)
- [libarchive](LIBARCHIVE.md)
- [CMake](CMAKE.md)
- [curl (UCRT64)](CURL-UCRT64.md)
- [GNU GCC](GNU-GCC.md)
- [GNU Binutils](GNU-BINUTILS.md)
- [GDB](GNU-GDB.md)
- [Zstandard (library)](LIBZSTD.md)
- [zlib (MSYS)](ZLIB-MSYS.md)
- [zlib (CLANG64)](ZLIB-CLANG64.md)
