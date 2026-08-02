---
id: doc:volume-11:library-family-classification
title: Library Family Classification Model
volume: 11
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Library Family Classification Model

A library family groups related development and runtime artifacts around a
qualified logical API. The grouping is an evidence-backed classification, not
an equivalence claim based on a package name, filename stem, or one DLL import.

```mermaid
flowchart LR
    L["logical library family"] --> API["headers and documented API"]
    L --> PC["pkg-config and CMake metadata"]
    L --> S["static library"]
    L --> I["import library"]
    L --> D["runtime DLL"]
    L --> P["package ownership"]
```

| Member type | Classification evidence | Relationship to logical library | Must remain distinct |
| --- | --- | --- | --- |
| Header or header set | Package path, include layout, API metadata | Exposes source-facing interface | Binary implementation and ABI guarantee |
| `pkg-config`/CMake module | Parsed module identity and declared targets/requirements | Describes a consumption surface | Runtime dependency proof |
| Static library | Archive path and member inventory | Link-time implementation artifact | Import library and loaded DLL |
| Import library | Import-archive classification and member evidence | Link-time binding surface for a DLL | Static archive contents and runtime loader result |
| Runtime DLL | PE artifact identity, exports, imports, architecture | Deployable binary implementation | Logical API compatibility across versions |
| Package | Snapshot-qualified ownership and metadata | Distribution/deployment container | The library family itself |

## Classification Rules

1. Create a logical library-family association only when package, metadata,
   headers, archive, or binary evidence establishes a meaningful relationship.
   Filename similarity alone is insufficient.
2. Qualify classifications by environment, architecture, CRT/ABI, package
   version, and inventory snapshot wherever those properties are known.
3. Preserve many-to-many membership: one package can ship several libraries,
   and a family can span runtime, development, compatibility, or split
   packages.
4. Do not equate an import library with a static library, or either with its
   runtime DLL. Their file formats, linkage roles, and compatibility evidence
   differ.
5. Treat API/source compatibility, ABI compatibility, and loader resolution
   as separate claims requiring their own qualified evidence.

## Classification Sequence

1. Start with a snapshot-qualified package and owned artifact paths.
2. Collect headers, metadata modules, archives, and PE artifacts.
3. Compare declared names, imported targets, exports, and ownership evidence.
4. Record supported family membership plus confidence and unresolved ambiguity.
5. Use explicit ABI or runtime observations before making compatibility claims.

## Category Coverage

Seven categories are documented as categories rather than per library,
each ranked by dependents summed across all environment variants. All
seven were recomputed against build-time edges on 2026-08-02: runtime
figures come from catalog snapshot `20260729T113151Z`, build and check
figures from the repository databases read 2026-08-02.

| Category | Leader | Runtime | Build + check | Total |
| --- | --- | ---: | ---: | ---: |
| [GUI](LIBRARY-CATEGORY-GUI.md) | `qt6-base` | 637 | 458 | **1,095** |
| [Imaging](LIBRARY-CATEGORY-IMAGING.md) | `libpng` | 471 | 110 | **581** |
| [Graphics](LIBRARY-CATEGORY-GRAPHICS.md) | `cairo` | 321 | 185 | **506** |
| [Video](LIBRARY-CATEGORY-VIDEO.md) | `ffmpeg` | 161 | 54 | **215** |
| [Audio](LIBRARY-CATEGORY-AUDIO.md) | SDL2 | 158 | 0 | **158** |
| [Testing](LIBRARY-CATEGORY-TESTING.md) | `gtest` | 0 | 79 | **79** |
| [Logging](LIBRARY-CATEGORY-LOGGING.md) | `spdlog` | 27 | 0 | **27** |

**One category leader changed and four internal orderings moved:**

- **GUI**: `qt6-base` (1,095) displaces `glib2` (794). The page previously
  had to explain that its leader was not a GUI library at all; it now is.
  Qt 5 also overtakes GTK 3, 398 to 381.
- **Audio**: `libvorbis` (125) overtakes `libsndfile` (121), and `openal`
  climbs from fifth to fourth on 43 build edges.
- **Video**: `dav1d` falls from fourth to seventh with zero build edges
  while `aom`, `libass`, `x265`, and `svt-av1` rise past it.
- **Imaging**: `openjpeg2` rises from sixth to fifth past `lcms2`, at 99
  build against 119 runtime — the most build-weighted library in its
  category.
- **Graphics**: `pixman` edges past `libepoxy`. `cairo` leads on either
  measure.

### How to read the build column

**A nonzero build count is a floor, not a measure.** MSYS2 recipes declare
a library needed at both build and run time only once, in `depends` —
`SDL2_image` builds against SDL2 and lists it in `DEPENDS`, with
`MAKEDEPENDS` carrying only `cc` and `autotools`. What `makedepends`
reliably carries is build-*only* dependencies: toolchains and build
systems, header and code-generation packages, and `-devel` split packages
on the MSYS side (87 of them take 1,036 build edges between them; `zlib-devel`
alone has 111 against `zlib`'s 9 runtime).

So the build column is evidence of use, and its absence is not evidence of
non-use. Each category page repeats this where its own numbers depend on
it.

**Check-time edges are a Python phenomenon.** Outside testing they are
essentially zero across all six other categories — the only non-testing
entry anywhere is `gtk3` at 4.

**Corrected 2026-08-02.** The testing row previously read `0` and this
section said so was an artifact rather than a fact — the catalog projection
carried no build-time or check-time edges, because
`tools/import_repository_db.py` read `%DEPENDS%` and `%OPTDEPENDS%` from
each package's `desc` record and dropped `%MAKEDEPENDS%` and
`%CHECKDEPENDS%`.

That is fixed. `model/build-dependencies/current.json` carries 54,035
`build-depends-on` and 3,428 `check-depends-on` edges, and
`build-depends-on` is now the largest single edge type in the composed
graph — ahead of `runtime-depends-on` at 41,061.

Two results followed, in opposite directions:

- **Testing was an artifact.** The category goes from 1 dependent to 202,
  and `python-pytest` turns out to have 1,262 dependents — 1,254 of them
  check-time — making it the most-depended-upon test framework in the
  ecosystem by an order of magnitude, previously invisible.
- **Logging was not.** Every logging library records zero on both new edge
  classes. Its low counts are a fact about how logging is consumed.

The build-time graph is a genuinely different graph. Its leaders — `ninja`
(4,455), `cmake` (4,194), `python-installer` (4,187), `python-build`
(4,132), `python-setuptools` (3,206), `autotools` (2,593), `pkgconf`
(2,081) — do not appear anywhere in a runtime ranking, and between them
are declared by more packages than any runtime dependency in the catalog.

All seven category pages now carry both measures. No ranking in this
section is runtime-only any more.

## Related Views

- [Header and development-metadata indexes](HEADER-AND-METADATA-INDEXES.md)
- [Binary-to-DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md)
- [Package-to-file inventory](PACKAGE-FILE-INVENTORY.md)
