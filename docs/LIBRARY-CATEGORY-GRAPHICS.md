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
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Graphics

## What is in the category

Graphics here means rendering primitives — 2D vector drawing and 3D API
access — as distinct from [imaging](LIBRARY-CATEGORY-IMAGING.md) (decoding
image formats) and [GUI](LIBRARY-CATEGORY-GUI.md) (widgets and event
loops). The boundary is not clean anywhere, and the dependency chain
below shows why.

From the catalog snapshot (`20260729T113151Z`), dependents summed across
all environment variants:

| Library | Dependents | Version | License | Role |
| --- | ---: | --- | --- | --- |
| `cairo` (`library:cairographics:cairo`) | 321 | 1.18.4-4 | LGPL-2.1-or-later OR MPL-1.1 | 2D vector rendering |
| vulkan-loader | 83 | 1~1.4.350.1-1 | Apache-2.0 | Vulkan ICD loading |
| glew | 77 | 2.3.1-4 | Modified BSD/MIT/GPL | OpenGL extension loading |
| freeglut | 47 | 3.8.0-1 | MIT | OpenGL windowing/input |
| glfw | 39 | 3.4-1 | Zlib | OpenGL/Vulkan windowing/input |
| libepoxy | 31 | 1.5.10-7 | MIT | OpenGL function dispatch |
| pixman | 30 | 0.46.4-3 | MIT | low-level pixel manipulation |
| angleproject | 19 | 2.1.r25748.890b5d8f-3 | BSD-3-Clause | OpenGL ES over other backends |
| mesa | 4 | 26.1.5-1 | MIT | software/driver GL implementation |

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

## Evidence and Gaps

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
