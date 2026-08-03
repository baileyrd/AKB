---
id: doc:volume-6:library-category-gui
title: Library Category — GUI
volume: 6
status: partial
model_refs:
  - library:gnome:gtk3
  - library:cairographics:cairo
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gtk:project-site-2026-08-02
  - evidence:recipe-dependencies:current
  - evidence:qt:framework-2026-08-02
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — GUI

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnome:gtk3` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | The GNOME Project |
| Environments | `ucrt64` |
| Upstream | <https://www.gtk.org/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-gtk3` |
| Version (observed) | 3.24.52-1 |
| License (observed) | spdx:LGPL-2.1-or-later |
| Architecture (observed) | any |
| Installed size (observed) | 73.5 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:gtk:project-site-2026-08-02` — GTK (official project site) (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## The ranking

Recomputed 2026-08-02 against build-time edges, which this knowledge base
could not see until `model/recipe-dependencies/current.json` was added.
Dependents summed across all environment variants. Runtime figures from
catalog snapshot `20260729T113151Z`; build and check from the repository
databases read 2026-08-02.

| Library | Runtime | Build | Check | Total | Version | License |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| qt6-base | 637 | 422 | 0 | **1,059** | 6.11.1-1 | LGPL-3.0-only WITH Qt-GPL-exception |
| glib2 | 735 | 59 | 0 | **794** | 2.88.1-1 | LGPL |
| qt5-base | 223 | 159 | 0 | **382** | 5.15.19+kde+r96-1 | LGPL-3.0-only WITH Qt-GPL-exception |
| `gtk3` (`library:gnome:gtk3`) | 234 | 143 | 4 | **381** | 3.24.52-1 | LGPL-2.1-or-later |
| pango | 235 | 92 | 0 | **327** | 1.58.0-1 | LGPL-2.1 |
| gdk-pixbuf2 | 204 | 28 | 0 | **232** | 2.44.7-1 | LGPL-2.1-or-later |
| gtk4 | 88 | 37 | 0 | **125** | 4.22.4-1 | LGPL-2.1-or-later |
| atk | 37 | 0 | 0 | **37** | 2.60.5-1 | LGPL-2.1-or-later |
| libadwaita | 23 | 0 | 0 | **23** | 1.9.1-1 | LGPL-2.1-or-later |
| fltk | 16 | 4 | 0 | **20** | 1.4.5-1 | LGPL-2.0-or-later WITH FLTK-exception |

**The leader changed.** On runtime edges alone `glib2` topped this table at
735, and this page previously had to explain that its leader was not a GUI
library at all — `glib2` is an object system, main-loop implementation, and
portability layer that everything in the GTK stack requires and much
outside it requires too.

With build-time edges included, `qt6-base` leads at 1,059 and the ranking
finally means what a reader expects it to mean. `qt6-base` gains 422 build
edges against `glib2`'s 59, which is the difference between a framework
packages are *built against* and infrastructure they merely link.

The `glib2` qualification still holds where it is cited, and the milder
version applies to `pango` (text layout) and `gdk-pixbuf2` (image loading
for GTK): both are GTK-stack infrastructure rather than widget toolkits.

## Two toolkits, three generations

Stripping out infrastructure leaves the actual toolkits:

| Toolkit | Total | Runtime | Build | Nature |
| --- | ---: | ---: | ---: | --- |
| Qt 6 | 1,059 | 637 | 422 | full application framework |
| Qt 5 | 382 | 223 | 159 | previous Qt generation, still heavily depended on |
| GTK 3 | 381 | 234 | 143 | widget toolkit over the GLib stack |
| GTK 4 | 125 | 88 | 37 | current GTK generation |
| FLTK | 20 | 16 | 4 | small self-contained toolkit |

Three observations follow.

**Qt is ahead of GTK, and the gap is wider than runtime edges showed.**
Qt 5 and Qt 6 together reach 1,441 against GTK 3 and GTK 4's 506 — a ratio
of roughly 2.8:1, against 2.7:1 on runtime edges alone. Part of that is
scope: Qt is documented upstream as a full cross-platform application
framework — networking, threading, and more — rather than a widget set, so
packages depend on `qt6-base` for non-GUI reasons.

**Qt 5 overtakes GTK 3 once build edges count, barely.** On runtime alone
GTK 3 led Qt 5, 234 to 223. On totals Qt 5 leads by a single edge, 382 to
381, because Qt 5 is declared as a build dependency 159 times against
GTK 3's 143. A margin that thin is not a finding; it is a tie.

**Both families carry their previous generation at scale.** Qt 5 at 382
and GTK 3 at 381 each exceed the newer generation alongside them — GTK 4 at
125, and Qt 6 aside. A migration to the newer major version is still in
progress across the catalog, and a build environment realistically needs
both.

## License asymmetry

This is the one category where licensing differs structurally between the
options. The GTK stack is LGPL-2.1-or-later throughout. Qt is
`LGPL-3.0-only WITH Qt-GPL-exception`, which is a different and more
constrained obligation, and Qt's commercial licensing exists alongside it.
For a project choosing a toolkit, that difference is often decisive and it
is visible directly in the catalog's `licenses` field.

## The rendering path

Verified from declared dependencies in the catalog snapshot, GTK 3
declares twelve runtime dependencies including `cairo`, `atk`,
`gdk-pixbuf2`, `glib2`, `pango`, and `json-glib`. So:

```
gtk3 ──requires──▶ cairo ──requires──▶ libpng ──requires──▶ zlib
```

A GUI application on this platform pulls in the graphics category, which
pulls in the imaging category, which pulls in compression. That chain is
the structural reason `zlib` and `libpng` top the whole-catalog and
imaging rankings respectively.

Qt 6 declares seventeen runtime dependencies and does not sit on the GLib
stack, which is the other half of why the two families rarely mix in one
process.

## What Windows changes

Nothing on this page has been observed running. The relevant open
questions, all unestablished here:

- Which windowing backend each toolkit uses on Windows, and whether it
  goes through the Win32 API directly or through an abstraction.
- How each interacts with the console/ConPTY boundary — see
  [Windows Console and ConPTY Boundary](WINDOWS-CONSOLE-CONPTY-BOUNDARY.md).
- Whether any of them are usable from the MSYS side at all, or only from
  the native environments. Given the `msys-2.0.dll` boundary, native is
  the expected answer, but it is not verified here.

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
- Dependent counts, versions, licenses, and dependency declarations are
  **observed** from the catalog snapshot.
- GTK's and Qt's project pages were retrieved 2026-08-02 and verified 200.
- **Only `gtk3` is modelled as an entity.**
- **No GUI program has been built or run by this knowledge base.** Every
  behavioral statement above is either a dependency fact from the catalog
  or explicitly marked as an open question.
- No PE import analysis exists for any package here.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["GTK 3"]
    d0["Cairo"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnome:gtk3` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [Library Category — Graphics](LIBRARY-CATEGORY-GRAPHICS.md)
- [Library Category — Imaging](LIBRARY-CATEGORY-IMAGING.md)
- [Windows Console and ConPTY Boundary](WINDOWS-CONSOLE-CONPTY-BOUNDARY.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
