---
id: doc:volume-6:library-category-imaging
title: Library Category — Imaging
volume: 6
status: partial
model_refs:
  - library:libpng:libpng
  - library:gnu:zlib
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:libpng:project-site-2026-08-02
  - evidence:build-dependencies:current
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Imaging

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:libpng:libpng` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | PNG Development Group |
| Environments | `ucrt64` |
| Upstream | <http://www.libpng.org/pub/png/libpng.html> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-libpng` |
| Version (observed) | 1.6.58-1 |
| License (observed) | custom |
| Architecture (observed) | any |
| Installed size (observed) | 2.5 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:libpng:project-site-2026-08-02` — libpng (official project page) (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Why this category leads

Imaging is the heaviest of the seven categories this page set covers, and
it is not close. From the catalog snapshot (`20260729T113151Z`), counting
dependents across all environment variants of each project:

| Library | Runtime | Build | Total | Version | License |
| --- | ---: | ---: | ---: | --- | --- |
| `libpng` (`library:libpng:libpng`) | 471 | 110 | **581** | 1.6.58-1 | custom |
| libjpeg-turbo | 310 | 117 | **427** | 3.2.0-1 | custom BSD-like |
| libtiff | 266 | 95 | **361** | 4.7.2-1 | MIT |
| libwebp | 163 | 71 | **234** | 1.6.0-1 | BSD-3-Clause |
| openjpeg2 | 119 | 99 | **218** | 2.5.4-2 | BSD-2-Clause |
| lcms2 | 114 | 12 | **126** | 2.19.1-1 | MIT AND GPL-3.0-or-later |
| libheif | 62 | 11 | **73** | 1.23.1-1 | LGPL-3.0 AND MIT |
| giflib | 61 | 4 | **65** | 6.1.3-1 | MIT |
| libraw | 32 | 3 | **35** | 0.22.2-1 | LGPL-2.1 OR CDDL-1.0 |

Recomputed 2026-08-02 against build-time edges. Runtime figures from
catalog snapshot `20260729T113151Z`; build figures from the repository
databases read 2026-08-02. Check-time edges are zero across this category.

The order holds at the top — `libpng`, `libjpeg-turbo`, `libtiff` in the
same sequence — and one entry moves: **`openjpeg2` rises from sixth to
fifth**, passing `lcms2`. It is the most build-weighted library in the
category at 99 build against 119 runtime, close to one-to-one, which fits a
codec pulled in by media packages at compile time.

`lcms2`, by contrast, gains only 12 build edges against 114 runtime — it is
a colour-management engine consumed at runtime rather than built against.

`libpng` at 471 dependents is the fourth most-depended-upon library of any
kind in this catalog, behind only the `python` and `zlib` families. That
is a measured fact, not an impression: the earlier
[library candidates report](../generated/library-candidates.md) ranked it
tenth, which undercounted it by treating each environment variant
separately.

**The reason imaging leads is that image decoding is a dependency of
things that are not about images.** A GUI toolkit needs icons; a document
renderer needs embedded figures; a browser engine needs everything. So the
imaging libraries accumulate dependents from every category below.

## The layering

Verified from declared dependencies in the catalog snapshot:

```
gtk3  ──requires──▶  cairo  ──requires──▶  libpng  ──requires──▶  zlib
```

Each arrow is a declared runtime dependency, not an inference. The chain
matters because it explains the dependent counts: `zlib`'s position at the
top of the whole-catalog ranking and `libpng`'s at the top of this
category are the same phenomenon one layer apart.

`libpng` is the reference PNG implementation and PNG's compression *is*
DEFLATE, so the `zlib` dependency is structural rather than incidental.

## Format coverage and what it implies

Each library in the table corresponds to a format family, and the
presence of all of them is why "imaging support" is rarely one package:

| Library | Formats |
| --- | --- |
| libpng | PNG |
| libjpeg-turbo | JPEG |
| libtiff | TIFF |
| libwebp | WebP |
| openjpeg2 | JPEG 2000 |
| libheif | HEIF/AVIF container |
| giflib | GIF |
| libraw | camera raw formats |
| lcms2 | not a format — colour management (ICC profiles) |

`lcms2` at 114 dependents is the odd one out and worth naming: it is a
colour-management engine, so it appears wherever colour correctness
matters rather than wherever a specific format is read.

## License spread

This category has the most heterogeneous licensing of the seven:
`libpng` and `libjpeg-turbo` carry custom licenses, `libheif` combines
LGPL-3.0 with MIT, `lcms2` combines MIT with GPL-3.0-or-later, and
`libraw` is dual LGPL-2.1/CDDL-1.0. Anything statically linking across
this category has a real license-composition question, and the catalog's
`licenses` field is the observed starting point for answering it.

## What the build column does and does not mean

**A nonzero build count is a floor, not a measure.** MSYS2 recipes declare
a library needed at *both* build and run time only once, in `depends`.
`mingw-w64-ucrt-x86_64-SDL2_image` builds against SDL2 and lists it in
`DEPENDS`; its `MAKEDEPENDS` carries only `cc` and `autotools`. So a
library can be built against by hundreds of packages and still score zero
in the build column.

What `makedepends` reliably carries is build-*only* dependencies:

- toolchains and build systems — `cc`, `cmake`, `ninja`, `meson`,
  `autotools`, `pkgconf`;
- header-only and code-generation packages — `vulkan-headers`, `nasm`,
  `gtk-doc`, `gobject-introspection`;
- **`-devel` split packages on the MSYS side.** 87 of them receive 1,036
  build edges between them; `zlib-devel` alone has 111, against `zlib`'s 9
  runtime, because the MSYS side ships headers as a separate package.

Where a library *does* score build edges the signal is real — some recipes
do name libraries in `makedepends`, such as `gst-plugins-bad` declaring
`cairo` or `emacs` declaring `libpng`. But the convention is inconsistent
between recipes. Read the build column as evidence of use, and never read
its absence as evidence of non-use.

**Check-time edges are near-absent from this category**, as they are from
every category except testing: `check-depends-on` in this ecosystem is
overwhelmingly a Python-packaging phenomenon, concentrated on
`python-pytest` and its plugins. See
[Library Category — Testing](LIBRARY-CATEGORY-TESTING.md).

## Evidence and Gaps

- Build and check counts are **observed** from the six MSYS2 repository
  databases read 2026-08-02, projected additively into
  `model/build-dependencies/current.json`. They carry a later observation
  date than the runtime counts and versions above, which come from catalog
  snapshot `20260729T113151Z`; see `tools/import_build_dependencies.py` for
  why the two are separate.
- Dependent counts, versions, and licenses are **observed** from the
  catalog snapshot and are the strongest claims here.
- The three-link dependency chain is **verified** against declared
  dependencies in the same snapshot.
- libpng's project page was retrieved 2026-08-02 and verified 200.
- **No page in this category has PE import analysis, header inventory, or
  file manifests behind it.** The deep-inventory pipeline has run against
  2 of 15,711 packages. So nothing here states which DLL a given package
  actually installs, or what its exported surface is.
- Only `libpng` is modelled as an entity. The other eight are named from
  measured catalog data without individual pages.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libpng"]
    u0["Cairo"]
    u0 -->|requires| subject
    d0["zlib"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:libpng:libpng` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [Library Category — Graphics](LIBRARY-CATEGORY-GRAPHICS.md)
- [Library Category — GUI](LIBRARY-CATEGORY-GUI.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
