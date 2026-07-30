---
id: doc:volume-6:icu
title: ICU (International Components for Unicode)
volume: 6
status: partial
model_refs:
  - library:unicode:icu
  - package:msys2:mingw-w64-ucrt-x86_64-icu
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:unicode:icu-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# ICU (International Components for Unicode)

## Purpose

ICU provides mature, comprehensive Unicode and internationalization
support: text handling, locale-aware collation and formatting, and time
zone/calendar data, well beyond what a C runtime or
[GNU gettext](GNU-GETTEXT.md) alone provide. This page documents its
architectural role; see the
[official ICU project site](https://icu.unicode.org/home/) for the API
reference.

## Architectural Classification

`library:unicode:icu` is packaged per native environment: this page cites
the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-icu` (version
`78.3-3` in the current catalog snapshot, license `ICU` — the project's
own permissive license), maintained under the Unicode Consortium.

## Responsibilities

- Unicode text processing (normalization, bidirectional text, break
  iteration), locale-aware collation and number/date/currency formatting,
  and bundled time zone and calendar data.

## Boundaries

ICU is a general internationalization toolkit, distinct in scope from
[GNU gettext](GNU-GETTEXT.md)'s narrower message-translation role: a
program can use gettext for translated strings while separately using ICU
for locale-aware sorting or date formatting, and the two are not
substitutes for each other.

## Interfaces

- C and C++ APIs (`ucol_*` for collation, `udat_*` for date formatting,
  `ubrk_*` for text segmentation), per the documentation. This page does
  not enumerate the header-level surface; that belongs to
  [Header and Development-Metadata Indexes](HEADER-AND-METADATA-INDEXES.md).

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-icu`: `mingw-w64-ucrt-x86_64-cc-libs`,
the virtual capability [gcc-libs provides](LIBSTDCXX.md#dependencies) in
this environment (or that [libc++ provides](LIBCXX.md#dependencies) in
CLANG64), for low-level compiler runtime support — the same pattern
already documented for [libc++](LIBCXX.md#dependencies).

## Reverse Dependencies

The snapshot records 46 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-icu`. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

ICU bundles its own locale and time zone data rather than reading external
configuration files; a program selects a locale via its C/C++ API calls
rather than through persistent configuration.

## Initialization and Execution Flow

As a library, ICU has no independent process lifecycle: it initializes
and executes within the process of whatever program links against it, the
same model documented for [zlib](ZLIB.md#initialization-and-execution-flow).

## Runtime Behavior

ICU's bundled time zone database can drift out of date relative to
real-world time zone rule changes between package updates; this is a
documented general characteristic of any library that bundles its own
copy of frequently updated time zone data, not specific to this package.

## Compatibility and Variants

ICU's API has had major version transitions historically (C API namespace
versioning); a program built against one ICU major version's ABI is not
guaranteed compatible with another without rebuilding, per the project's
own versioning documentation.

## Security Considerations

No ICU-specific vulnerability review has been performed for this volume;
see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `78.3-3` version.

## Failure Modes and Diagnostics

Unexpected collation or formatting output should first be checked against
which locale a dependent program actually requested from ICU, before
being treated as an ICU defect.

## Evidence, Assumptions, and Open Questions

The internationalization feature set is backed by the official ICU
project site (`evidence:unicode:icu-manual-2026-07-30`), matching the
`project_url` already recorded for `package:msys2:mingw-w64-ucrt-x86_64-icu`
in the catalog. Package identity, version, license, and the dependency
edge are backed by the pacman catalog snapshot (`evidence:catalog:current`).
Open, and explicitly out of scope for this page: header-level API surface
and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU gettext](GNU-GETTEXT.md)
- [libc++](LIBCXX.md)
