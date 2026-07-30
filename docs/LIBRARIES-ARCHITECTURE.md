---
id: doc:volume-6:libraries-architecture
title: MSYS2 Library Architecture
volume: 6
status: partial
model_refs:
  - library:gnu:libstdc++
  - library:llvm:libc++
  - library:gnu:zlib
  - library:gnu:libiconv
  - library:gnu:gettext
  - library:libexpat:expat
  - library:gnome:libxml2
  - library:unicode:icu
  - library:boost:boost
  - library:sqlite:sqlite3
  - library:gnu:readline
evidence_refs:
  - evidence:gnu:libstdcxx-manual-2026-07-30
  - evidence:llvm:libcxx-manual-2026-07-30
  - evidence:zlib:manual-2026-07-30
  - evidence:gnu:libiconv-manual-2026-07-30
  - evidence:gnu:gettext-manual-2026-07-30
  - evidence:libexpat:manual-2026-07-30
  - evidence:gnome:libxml2-manual-2026-07-30
  - evidence:unicode:icu-manual-2026-07-30
  - evidence:boost:documentation-2026-07-30
  - evidence:sqlite:documentation-2026-07-30
  - evidence:gnu:readline-manual-2026-07-30
last_verified: 2026-07-30
---

# MSYS2 Library Architecture

This volume organizes library families as logical interfaces connected to
separate package, binary, development, and dependency objects. It is a
navigation layer over the canonical package-inventory evidence in Volume 11;
it does not make package names or file suffixes into ABI claims.

## Architecture layers

```mermaid
flowchart LR
    F["logical library family"] --> P["package(s)"]
    P --> B["runtime DLL / executable"]
    P --> D["headers, .pc, CMake metadata"]
    P --> L["import and static libraries"]
    B --> I["PE imports and exports"]
    D --> R["declared build requirements"]
```

| Question | Canonical evidence | Not established by that evidence |
| --- | --- | --- |
| Which package owns a library-related path? | Snapshot-qualified package/file ownership | Local byte presence or ABI compatibility |
| What does a DLL declare or export? | Hash-qualified PE import/export analysis | Dynamic loader selection or successful execution |
| Which headers and metadata describe a consumption surface? | Package paths plus parsed `.pc`/CMake metadata | Public API stability or a successful build |
| Which archive members exist? | Hash-qualified archive-member inventory | Runtime behavior or object-level ABI compatibility |
| Which binaries consume a DLL? | Static `imports-dll` relationships in one observation | Transitive runtime loading or reverse package dependency |

## First library pages

[libstdc++](LIBSTDCXX.md), [libc++](LIBCXX.md), [zlib](ZLIB.md),
[GNU libiconv](GNU-LIBICONV.md), [GNU gettext](GNU-GETTEXT.md),
[Expat](EXPAT.md), [libxml2](LIBXML2.md), [ICU](ICU.md), [Boost](BOOST.md),
[SQLite](SQLITE3.md), and [GNU Readline](GNU-READLINE.md) are this
volume's first per-library pages. The
first pair resolved the "C++ library" row the
[Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md) left open; the rest are
foundational libraries cited by dependency rationale across dozens of
pages elsewhere in this knowledge base (character-set conversion, NLS,
DEFLATE compression, XML parsing) that had not yet been given pages of
their own. zlib's 299 recorded reverse dependents make it the
most-depended-upon package identified anywhere in this knowledge base to
date (`claim:library:zlib-hub`). One cross-package mixup was caught and
corrected while writing [SQLite](SQLITE3.md): GnuPG depends on a
*separate*, MSYS-environment `libsqlite` package, not the UCRT64
`sqlite3` package this page documents — the same upstream project, two
distinct catalog entities, now stated explicitly rather than conflated.
All eleven pages are deliberately scoped to package/dependency-level evidence
only — package identity, bundling, provides/depends relationships, and
reverse-dependency counts — and all explicitly flag that the fuller
methodology below (headers, `pkg-config`/CMake metadata, PE import/export
analysis) has not been applied to them and remains open. They are a
starting point for this volume, not a demonstration that its full
evidence model is populated.

## Family navigation

Start with a logical family and carry environment, architecture, CRT/ABI,
package version, and evidence snapshot through every drill-down. Follow
package ownership to artifacts, then use the appropriate specialized view:

1. [Library family classification](LIBRARY-FAMILY-CLASSIFICATION.md) defines
   the distinct object types and membership rules.
2. [Header and development-metadata indexes](HEADER-AND-METADATA-INDEXES.md)
   covers source-facing headers and metadata.
3. [Binary-to-DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md) covers
   static PE import/export facts.
4. [Reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
   explains qualified reverse navigation.

## Evidence boundary

The local-only isolated MSYS/UCRT64 collection provides direct bytes for a
bounded installed subset. The repository-wide file-index projection provides
broad ownership coverage with `present: false`. Neither observation proves a
logical library identity, a complete API, binary compatibility, dynamic loader
outcome, or repository-wide byte coverage without further evidence.

## Related volumes

- Volume 4: [Runtime environments](RUNTIME-ENVIRONMENTS.md)
- Volume 8: [Toolchain role model](TOOLCHAIN-ROLE-MODEL.md)
- Volume 11: [Package file inventory](PACKAGE-FILE-INVENTORY.md)
- Volume 13: [Reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
