---
id: doc:volume-6:boost
title: Boost
volume: 6
status: partial
model_refs:
  - library:boost:boost
  - package:msys2:mingw-w64-ucrt-x86_64-boost
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:boost:documentation-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Boost

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:boost:boost` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Boost Steering Committee / Boost community |
| Environments | `ucrt64` |
| Upstream | <https://www.boost.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-boost` |
| Version (observed) | 1.91.0-3 |
| License (observed) | spdx:BSL-1.0 |
| Architecture (observed) | any |
| Installed size (observed) | 183.9 MB |

**Evidence on this object**

- `evidence:boost:documentation-2026-07-30` — Boost (official project site) (`primary`, retrieved 2026-07-30)
- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Boost is a large, peer-reviewed collection of portable C++ source
libraries covering everything from smart pointers and containers to
networking and coroutines — a library-of-libraries rather than a single
focused component, unlike every other Volume 6 page so far. This page
documents its architectural role at the package level; see the
[official Boost project site](https://www.boost.org/) for the per-library
documentation.

## Architectural Classification

`library:boost:boost` is packaged per native environment: this page cites
the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-boost` (version
`1.91.0-3` in the current catalog snapshot, license `BSL-1.0`, the Boost
Software License), maintained by the Boost community and Boost Steering
Committee — no single authority the way most other libraries in this
knowledge base have one.

## Responsibilities

- Providing dozens of independent C++ libraries (this page does not
  enumerate them individually) under one umbrella package, several of
  which have historically served as incubators for later C++ standard
  library features (for example, `shared_ptr`, `filesystem`, and
  `optional` all originated in or were heavily influenced by Boost before
  standardization).

## Boundaries

Boost is a collection, not a single logical library the way
[zlib](ZLIB.md) or [Expat](EXPAT.md) are; different Boost sub-libraries
have very different purposes, dependency needs, and (for the small subset
requiring compilation, as opposed to the many header-only libraries)
separate compiled components in the optional `boost-libs` package this
page's `boost` package requires.

## Interfaces

- Individual Boost libraries each have their own header/API surface; this
  page does not enumerate them. See
  [Header and Development-Metadata Indexes](HEADER-AND-METADATA-INDEXES.md)
  for that level of detail when available.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-boost`:
`mingw-w64-ucrt-x86_64-boost-libs`, the package containing Boost's compiled
(non-header-only) library components, separated from this metapackage.
Optional dependencies on `python` and `python-numpy` back Boost.Python's
Python-interoperability sub-library specifically, not Boost as a whole.

## Reverse Dependencies

The snapshot records 18 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-boost` — notably lower than several
other libraries in this batch despite Boost's broad scope, since many
consuming projects depend directly on `boost-libs` or on individual Boost
sub-libraries' headers rather than on this umbrella package. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Boost has no unified configuration mechanism; individual libraries within
the collection have their own compile-time macros and, where applicable,
runtime configuration, none of which this page enumerates.

## Initialization and Execution Flow

As a header-and-library collection, Boost has no independent process
lifecycle; header-only sub-libraries are compiled directly into a
consuming program, while sub-libraries requiring linkage (via
`boost-libs`) initialize within the consuming program's process, the same
general library-linkage model documented for [zlib](ZLIB.md#initialization-and-execution-flow).

## Runtime Behavior

Runtime behavior is entirely sub-library-specific; this page does not
attempt to characterize it in aggregate given Boost's breadth.

## Compatibility and Variants

Boost's release cadence and per-library API stability vary considerably
across the collection; some libraries are considered stable and mature,
others experimental, a distinction the project's own documentation makes
explicit per-library rather than at the collection level.

## Security Considerations

No Boost-specific (collection-wide) vulnerability review has been
performed for this volume; individual sub-libraries would need their own
review given the collection's breadth. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review has
been performed for the recorded `1.91.0-3` version.

## Failure Modes and Diagnostics

Build failures against Boost are frequently sub-library-specific (a
missing compiled component in `boost-libs`, or a header-only library
requiring a newer C++ standard than the project is compiled with); this
page does not attempt a general diagnostic guide given the collection's
breadth.

## Evidence, Assumptions, and Open Questions

The collection's scope and governance model are backed by the official
Boost project site (`evidence:boost:documentation-2026-07-30`), matching
the `project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-boost` in the catalog. Package
identity, version, license, and the dependency edge are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open, and explicitly
out of scope for this page: individual sub-library documentation
(deliberately deferred given the collection's scale), header-level API
surface, and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libstdc++](LIBSTDCXX.md)
- [libc++](LIBCXX.md)
