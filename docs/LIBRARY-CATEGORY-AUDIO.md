---
id: doc:volume-6:library-category-audio
title: Library Category — Audio
volume: 6
status: partial
model_refs:
  - library:libsndfile:libsndfile
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:libsndfile:project-site-2026-08-02
  - evidence:libsdl:project-site-2026-08-02
  - evidence:build-dependencies:current
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Audio

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:libsndfile:libsndfile` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Erik de Castro Lopo |
| Environments | `ucrt64` |
| Upstream | <https://libsndfile.github.io/libsndfile/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-libsndfile` |
| Version (observed) | 1.2.2-1 |
| License (observed) | spdx:LGPL-2.1-or-later |
| Architecture (observed) | any |
| Installed size (observed) | 2.4 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:libsndfile:project-site-2026-08-02` — libsndfile (official project site) (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## The ranking

From the catalog snapshot (`20260729T113151Z`), dependents summed across
all environment variants:

| Library | Runtime | Build | Total | Version | License | Layer |
| --- | ---: | ---: | ---: | --- | --- | --- |
| SDL2 | 158 | 0 | **158** | 2.32.10-1 | Zlib | output + input abstraction |
| libvorbis | 98 | 27 | **125** | 1.3.7-2 | custom | codec |
| `libsndfile` (`library:libsndfile:libsndfile`) | 100 | 21 | **121** | 1.2.2-1 | LGPL-2.1-or-later | file I/O across formats |
| openal | 70 | 43 | **113** | 1.25.2-1 | GPL-2.0-or-later | 3D audio output |
| libogg | 75 | 8 | **83** | 1.3.6-1 | BSD-3-Clause | container |
| opus | 63 | 12 | **75** | 1.6.1-1 | BSD-3-Clause | codec |
| flac | 67 | 5 | **72** | 1.5.0-1 | custom Xiph/LGPL/GPL/FDL | codec |
| portaudio | 57 | 14 | **71** | 1~19.7.0-5 | custom | output abstraction |
| mpg123 | 32 | 10 | **42** | 1.33.5-1 | LGPL-2.1-or-later | codec (MP3) |

Recomputed 2026-08-02 against build-time edges. Runtime figures from
catalog snapshot `20260729T113151Z`; build figures from the repository
databases read 2026-08-02. Check-time edges are zero across this category.

Two positions change. **`libvorbis` overtakes `libsndfile`** (125 to 121),
having trailed it 98 to 100 on runtime edges alone. And **`openal` climbs
from fifth to fourth**, past `libogg`, on the strength of 43 build edges —
the highest build-to-runtime ratio in the category at roughly 0.6:1, which
fits a library games and engines compile against.

**SDL2 leads with zero build edges**, and that is the clearest illustration
of the caveat below: `mingw-w64-ucrt-x86_64-SDL2_image` builds against SDL2
and declares it in `depends`, not `makedepends`. Its zero means "declared
as a runtime dependency", not "not used at build time".

SDL2 is listed first by count but belongs to more than one category — it
abstracts audio, input, and rendering together, which is why it also
appears in the video ranking. Reading it as "the leading audio library"
would overstate the audio-specific part of what it does.

## Three layers, and they are cleanly separated

Unlike the graphics and GUI categories, this one decomposes neatly:

**Containers** — `libogg`. A container carries encoded streams without
knowing how they were encoded.

**Codecs** — `libvorbis`, `flac`, `opus`, `mpg123`. Each is one encoding.

**Abstractions** — `libsndfile` over file formats, `portaudio` and
`openal` over output devices, SDL2 over everything.

`libsndfile` is the interesting one architecturally, and its declared
dependencies show why: it requires `flac`, `lame`, `libogg`, `libvorbis`,
`mpg123`, and `opus`. It is a **facade over the codec layer** — a caller
uses one API and gets six encodings, at the cost of pulling all six in.
That is the reason a package needing only WAV support still installs a
Vorbis decoder.

## The Ogg family

`libogg` at 75 and `libvorbis` at 98 sit close together because Vorbis is
almost always carried in Ogg. `opus` at 63 and `flac` at 67 likewise
commonly use it. The Xiph stack accounts for four of the nine entries.

`libvorbis` and `flac` carry custom licenses rather than SPDX
identifiers in the catalog metadata — `flac` specifically as
`custom:Xiph;LGPL;GPL;FDL`, a four-way combination. Anything redistributing
statically-linked audio support has a license-composition question here
comparable to the imaging category's.

## Output on Windows

`portaudio`, `openal`, and SDL2 all exist to hide the platform's audio
output API. What each of them targets on Windows — WASAPI, DirectSound,
WinMM — is **not established by this knowledge base**. That question needs
either PE import analysis or a runtime observation, and neither exists:
the deep-inventory pipeline has run against 2 of 15,711 packages.

The MSYS/native boundary applies as everywhere else: audio output is a
Windows API, so these are native-environment libraries. Whether any is
usable from the MSYS side is not verified here.

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
- Dependent counts, versions, licenses, and `libsndfile`'s declared
  dependency set are **observed** from the catalog snapshot.
- libsndfile's and SDL's project sites were retrieved 2026-08-02 and
  verified 200.
- **Only `libsndfile` is modelled as an entity.**
- **No audio has been played, encoded, or decoded by this knowledge base.**
  The layering above is read from declared dependencies and upstream
  descriptions, not from behavior.
- Which host audio API each abstraction uses is unknown, and is the
  sharpest specific gap in this category.

## Related Objects

- [Library Category — Video](LIBRARY-CATEGORY-VIDEO.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
