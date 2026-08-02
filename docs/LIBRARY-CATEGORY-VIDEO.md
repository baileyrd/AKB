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
| Version (observed) | 8.1.2-1 |
| License (observed) | spdx:GPL-3.0-or-later |
| Architecture (observed) | any |
| Installed size (observed) | 81.4 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:ffmpeg:about-2026-08-02` — FFmpeg — About (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## The ranking

From the catalog snapshot (`20260729T113151Z`), dependents summed across
all environment variants:

| Library | Dependents | Version | License | Role |
| --- | ---: | --- | --- | --- |
| `ffmpeg` (`library:ffmpeg:ffmpeg`) | 161 | 8.1.2-1 | GPL-3.0-or-later | everything |
| gstreamer | 85 | 1.28.5-1 | LGPL-2.1-or-later | pipeline framework |
| libtheora | 36 | 1.2.0-1 | BSD-3-Clause | codec |
| dav1d | 32 | 1.5.4-1 | BSD-2-Clause | AV1 decoder |
| aom | 23 | 3.14.1-1 | BSD-2-Clause | AV1 reference codec |
| libass | 23 | 0.17.5-1 | ISC | subtitle rendering |
| x265 | 21 | 4.2-2 | GPL | HEVC encoder |
| libvpx | 21 | 1.16.0-1 | BSD-3-Clause | VP8/VP9 codec |
| svt-av1 | 19 | 4.2.0-1 | BSD-3-Clause-Clear | AV1 encoder |

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

## Evidence and Gaps

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
