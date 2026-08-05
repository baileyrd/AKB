---
id: doc:volume-6:library-category-video
title: Library Category — Video
volume: 6
status: partial
model_refs:
  - library:ffmpeg:ffmpeg
  - library:libsndfile:libsndfile
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:ffmpeg:about-2026-08-02
  - evidence:gstreamer:project-site-2026-08-02
  - evidence:recipe-dependencies:current
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Video

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:ffmpeg:ffmpeg` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | FFmpeg team |
| Environments | `ucrt64` |
| Upstream | <https://ffmpeg.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-ffmpeg` |
| Version (observed) | 8.1.2-2 |
| License (observed) | spdx:GPL-3.0-or-later |
| Architecture (observed) | any |
| Installed size (observed) | 81.37 MiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:ffmpeg:about-2026-08-02` — FFmpeg — About (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## The ranking

From the catalog snapshot (`20260729T113151Z`), dependents summed across
all environment variants:

| Library | Runtime | Build | Total | Version | License | Role |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `ffmpeg` (`library:ffmpeg:ffmpeg`) | 161 | 53 | **214** | 8.1.2-1 | GPL-3.0-or-later | everything |
| gstreamer | 85 | 12 | **97** | 1.28.5-1 | LGPL-2.1-or-later | pipeline framework |
| libtheora | 36 | 8 | **44** | 1.2.0-1 | BSD-3-Clause | codec |
| aom | 23 | 12 | **35** | 3.14.1-1 | BSD-2-Clause | AV1 reference codec |
| libass | 23 | 12 | **35** | 0.17.5-1 | ISC | subtitle rendering |
| x265 | 21 | 12 | **33** | 4.2-2 | GPL | HEVC encoder |
| dav1d | 32 | 0 | **32** | 1.5.4-1 | BSD-2-Clause | AV1 decoder |
| svt-av1 | 19 | 12 | **31** | 4.2.0-1 | BSD-3-Clause-Clear | AV1 encoder |
| libvpx | 21 | 0 | **21** | 1.16.0-1 | BSD-3-Clause | VP8/VP9 codec |

Recomputed 2026-08-02 against build-time edges read from the PKGBUILD
trees. Runtime figures from catalog snapshot `20260729T113151Z`. Check-time
edges are zero across this category.

`ffmpeg` and `gstreamer` hold first and second on either measure, and
`ffmpeg` gains 53 build edges. Below them the order rearranges modestly:
`libtheora`, `libass`, `aom`, and `x265` — eight to twelve build edges
each — rise past `dav1d` and `libvpx`, which have none.

Read that with the caveat below rather than as a usage claim. Almost every
codec here is declared in `depends` by the packages that use it, because a
codec needed to build is needed to run. The zeros on `dav1d` and `libvpx`
are not evidence of anything.

## FFmpeg is a dependency hub, not a leaf

The measured fact that shapes this whole category: **`ffmpeg` declares 53
runtime dependencies** in the UCRT64 variant — more than any other package
examined in this knowledge base. Among them are `aom`, `dav1d`, `libass`,
`libtheora`, `libvpx`, `svt-av1`, `x265`, `libx264`, `xvidcore`, `opus`,
`libvorbis`, `openal`, `SDL2`, `gnutls`, `libwebp`, `openjpeg2`, `zlib`,
and `vulkan`.

That single fact explains several others:

- **Most of the codecs in the table above are also FFmpeg's dependencies.**
  Their dependent counts are substantially FFmpeg-driven, and installing
  FFmpeg installs most of this category.
- **The category spans every other category on this page set.** FFmpeg's
  declared dependencies reach audio (`opus`, `libvorbis`, `openal`),
  imaging (`libwebp`, `openjpeg2`), graphics (`vulkan`, `SDL2`), and
  compression (`zlib`, `bzip2`).
- **FFmpeg is the ecosystem's widest single license surface.** It is
  GPL-3.0-or-later itself and composes 53 dependencies with their own
  terms, including `x265` under GPL. Anything redistributing it inherits
  that composition.

Upstream describes FFmpeg as a set of libraries — `libavcodec`,
`libavformat`, `libavfilter`, `libswscale`, `libswresample` — with
command-line drivers on top. So a program can link the libraries without
shipping the `ffmpeg` binary, and the license question differs between
those two uses.

## FFmpeg and GStreamer are structurally different

Both appear in the same ranking, and treating them as alternatives
obscures that they are different kinds of thing:

| | FFmpeg | GStreamer |
| --- | --- | --- |
| Shape | libraries plus drivers | pipeline framework with plugins |
| Composition | caller assembles calls | caller assembles a pipeline graph |
| Extension | contribute to the codebase | write a plugin |
| Catalog dependents | 161 | 85 |

GStreamer's plugin architecture means its capability set is distributed
across separate packages (`gst-plugins-base`, `-good`, `-bad`, `-ugly`),
so a dependent count for `gstreamer` alone understates what an
installation actually pulls in — the opposite of FFmpeg, where one package
declares everything.

## The AV1 cluster

Three separate AV1 packages appear: `aom` (the reference implementation,
both directions), `dav1d` (decoder only, optimised), and `svt-av1`
(encoder only, optimised). Their combined 74 dependents reflect a codec in
active transition, where the reference implementation and the
production-oriented ones coexist rather than one replacing the other.

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
- **`-devel` split packages on the MSYS side**, because the MSYS side ships
  headers as a separate package, so a recipe names `zlib-devel` at build
  time and `zlib` at run time.

Where a library *does* score build edges the signal is real — some recipes
do name libraries in `makedepends`, such as `gst-plugins-bad` declaring
`cairo` or `emacs` declaring `libpng`. But the convention is inconsistent
between recipes. Read the build column as evidence of use, and never read
its absence as evidence of non-use.

**Check-time edges are absent from this category**, as they are from every
category except testing: `check-depends-on` in this ecosystem is
overwhelmingly a Python-packaging phenomenon, concentrated on
`python-pytest` and its plugins. See
[Library Category — Testing](LIBRARY-CATEGORY-TESTING.md).

## Evidence and Gaps

- Build and check counts are **observed** from the six MSYS2 repository
  databases read 2026-08-02, projected additively into
  `model/recipe-dependencies/current.json`. They carry a later observation
  date than the runtime counts and versions above, which come from catalog
  snapshot `20260729T113151Z`; see `tools/import_build_dependencies.py` for
  why the two are separate.
- Dependent counts, versions, licenses, and FFmpeg's 53-item declared
  dependency list are **observed** from the catalog snapshot and are the
  strongest claims here.
- FFmpeg's About page and GStreamer's project site were retrieved
  2026-08-02 and verified 200.
- **Only `ffmpeg` is modelled as an entity.**
- **No media has been decoded or encoded by this knowledge base.** Nothing
  here states what any of these libraries does at runtime on Windows,
  which hardware acceleration paths resolve, or whether the packaged
  builds enable the codecs their dependencies suggest — build-time
  configuration is invisible in the catalog and no recipe analysis has
  been performed for these packages.
- No PE import analysis exists, so the actual DLL surface is unknown.

## Related Objects

- [Library Category — Audio](LIBRARY-CATEGORY-AUDIO.md)
- [Library Category — Imaging](LIBRARY-CATEGORY-IMAGING.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
