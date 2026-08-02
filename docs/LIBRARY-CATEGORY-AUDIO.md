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

| Library | Dependents | Version | License | Layer |
| --- | ---: | --- | --- | --- |
| SDL2 | 158 | 2.32.10-1 | Zlib | output + input abstraction |
| `libsndfile` (`library:libsndfile:libsndfile`) | 100 | 1.2.2-1 | LGPL-2.1-or-later | file I/O across formats |
| libvorbis | 98 | 1.3.7-2 | custom | codec |
| libogg | 75 | 1.3.6-1 | BSD-3-Clause | container |
| openal | 70 | 1.25.2-1 | GPL-2.0-or-later | 3D audio output |
| flac | 67 | 1.5.0-1 | custom Xiph/LGPL/GPL/FDL | codec |
| opus | 63 | 1.6.1-1 | BSD-3-Clause | codec |
| portaudio | 57 | 1~19.7.0-5 | custom | output abstraction |
| mpg123 | 32 | 1.33.5-1 | LGPL-2.1-or-later | codec (MP3) |

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

## Evidence and Gaps

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
