---
id: doc:volume-6:library-category-graphics
title: Library Category — Graphics
volume: 6
status: partial
model_refs:
  - library:cairographics:cairo
  - library:libpng:libpng
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:cairo:project-site-2026-08-02
  - evidence:build-dependencies:current
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Graphics

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:cairographics:cairo` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | cairographics.org |
| Environments | `ucrt64` |
| Upstream | <https://www.cairographics.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-cairo` |
| Version (observed) | 1.18.4-4 |
| License (observed) | spdx:LGPL-2.1-or-later OR MPL-1.1 |
| Architecture (observed) | any |
| Installed size (observed) | 4.0 MB |

**Evidence on this object**

- `evidence:cairo:project-site-2026-08-02` — Cairo (official project site) (`primary`, retrieved 2026-08-02)
- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## What is in the category

Graphics here means rendering primitives — 2D vector drawing and 3D API
access — as distinct from [imaging](LIBRARY-CATEGORY-IMAGING.md) (decoding
image formats) and [GUI](LIBRARY-CATEGORY-GUI.md) (widgets and event
loops). The boundary is not clean anywhere, and the dependency chain
below shows why.

Recomputed 2026-08-02 against build-time edges. Dependents summed across
all environment variants; runtime figures from catalog snapshot
`20260729T113151Z`, build figures from the repository databases read
2026-08-02.

| Library | Runtime | Build | Total | Version | License | Role |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `cairo` (`library:cairographics:cairo`) | 321 | 185 | **506** | 1.18.4-4 | LGPL-2.1-or-later OR MPL-1.1 | 2D vector rendering |
| vulkan-loader | 83 | 30 | **113** | 1~1.4.350.1-1 | Apache-2.0 | Vulkan ICD loading |
| glew | 77 | 13 | **90** | 2.3.1-4 | Modified BSD/MIT/GPL | OpenGL extension loading |
| freeglut | 47 | 32 | **79** | 3.8.0-1 | MIT | OpenGL windowing/input |
| glfw | 39 | 8 | **47** | 3.4-1 | Zlib | OpenGL/Vulkan windowing/input |
| pixman | 30 | 6 | **36** | 0.46.4-3 | MIT | low-level pixel manipulation |
| libepoxy | 31 | 0 | **31** | 1.5.10-7 | MIT | OpenGL function dispatch |
| angleproject | 19 | 8 | **27** | 2.1.r25748.890b5d8f-3 | BSD-3-Clause | OpenGL ES over other backends |
| mesa | 4 | 3 | **7** | 26.1.5-1 | MIT | software/driver GL implementation |

The ordering is almost unchanged — `cairo` leads on either measure, and by
a wider margin on totals (506 against `vulkan-loader`'s 113). One pair
swaps: `pixman` at 36 now edges past `libepoxy` at 31, having led it by one
on runtime edges alone.

`cairo` gains 185 build edges, the largest absolute gain in the category,
from packages such as `gst-plugins-bad` that name it in `makedepends`.
`libepoxy` gains none — see the caveat below before reading that as
disuse.

## Two distinct sub-groups

The table splits cleanly, and the split is architecturally meaningful.

**2D rasterisation** — `cairo` and `pixman`. `cairo` is the API; `pixman`
is the pixel-level engine underneath it. `cairo` at 321 dependents is
tenfold above `pixman` at 30, because callers use the API and `pixman`
arrives as a transitive dependency.

**3D API plumbing** — `glew`, `libepoxy`, `vulkan-loader`, `angleproject`,
`mesa`, plus the windowing shims `glfw` and `freeglut`. None of these
draws anything. They exist because OpenGL and Vulkan entry points must be
resolved at runtime rather than linked, and because creating a
GL-capable window is platform-specific.

That second group is where Windows shows through. `angleproject` maps
OpenGL ES onto another backend — on Windows, typically Direct3D — and
`vulkan-loader` implements the ICD discovery mechanism that finds an
installed driver. Both exist because the platform does not provide the API
the caller wants in the form the caller wants it.

## The chain into GUI and imaging

Verified from declared dependencies in the catalog snapshot:

```
gtk3 ──requires──▶ cairo ──requires──▶ libpng ──requires──▶ zlib
                     │
                     └──requires──▶ pixman, freetype, fontconfig, glib2, lzo2
```

`cairo`'s nine declared dependencies span three of the seven categories
covered by this page set, which is the concrete reason the category
boundaries leak: a 2D rendering library needs font rasterisation
(freetype), font configuration (fontconfig), an object system (glib2), and
PNG output (libpng).

**This is also why `cairo` leads the category.** Its dependents are not
mostly graphics programs — they are GUI toolkits and document renderers
that need to draw.

## Variant multiplication

Every library in the table exists in four or five environment variants
(`mingw-w64-x86_64-`, `-ucrt-x86_64-`, `-clang-x86_64-`,
`-clang-aarch64-`, and in some cases `-i686-`). The dependent counts above
are summed across variants deliberately: counting one variant would
understate the library's structural position by a factor of four or five,
which is exactly the error that made `libpng` look like the tenth most
important library in the earlier candidates report rather than the fourth.

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
- Dependent counts, versions, licenses, and the declared-dependency chain
  are **observed** from the catalog snapshot.
- cairo's project site was retrieved 2026-08-02 and verified 200.
- **Only `cairo` is modelled as an entity**; the other eight are named
  from measured catalog data.
- **No rendering behavior has been observed.** Whether any of these
  libraries works on a given Windows host, which GL implementation
  resolves, and what a `vulkan-loader` ICD search finds are all
  unestablished — they require a Windows host with a display, which this
  knowledge base has never had.
- No PE import analysis exists for any package here, so the DLLs each one
  actually loads are unknown.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["Cairo"]
    u0["GTK 3"]
    u0 -->|requires| subject
    d0["libpng"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:cairographics:cairo` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [Library Category — GUI](LIBRARY-CATEGORY-GUI.md)
- [Library Category — Imaging](LIBRARY-CATEGORY-IMAGING.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
