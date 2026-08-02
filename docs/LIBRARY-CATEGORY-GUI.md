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
  - evidence:qt:framework-2026-08-02
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — GUI

## The ranking, and why its top entry is misleading

From the catalog snapshot (`20260729T113151Z`), dependents summed across
all environment variants:

| Library | Dependents | Version | License |
| --- | ---: | --- | --- |
| glib2 | 735 | 2.88.1-1 | LGPL |
| qt6-base | 637 | 6.11.1-1 | LGPL-3.0-only WITH Qt-GPL-exception |
| pango | 235 | 1.58.0-1 | LGPL-2.1 |
| `gtk3` (`library:gnome:gtk3`) | 234 | 3.24.52-1 | LGPL-2.1-or-later |
| qt5-base | 223 | 5.15.19+kde+r96-1 | LGPL-3.0-only WITH Qt-GPL-exception |
| gdk-pixbuf2 | 204 | 2.44.7-1 | LGPL-2.1-or-later |
| gtk4 | 88 | 4.22.4-1 | LGPL-2.1-or-later |
| atk | 37 | 2.60.5-1 | LGPL-2.1-or-later |
| libadwaita | 23 | 1.9.1-1 | LGPL-2.1-or-later |
| fltk | 16 | 1.4.5-1 | LGPL-2.0-or-later WITH FLTK-exception |

**`glib2` at 735 is not a GUI library.** It is an object system, main-loop
implementation, and portability layer. It tops this table because
everything in the GTK stack requires it and a great deal outside the GTK
stack requires it too. Reading it as "the most popular GUI library" would
be wrong; it is listed here because it is inseparable from the GTK family
in the dependency graph, not because it draws anything.

The same qualification applies more weakly to `pango` (text layout) and
`gdk-pixbuf2` (image loading for GTK) — both are GTK-stack infrastructure
rather than widget toolkits.

## Two toolkits, three generations

Stripping out infrastructure leaves the actual toolkits:

| Toolkit | Dependents | Nature |
| --- | ---: | --- |
| Qt 6 | 637 | full application framework |
| GTK 3 | 234 | widget toolkit over the GLib stack |
| Qt 5 | 223 | previous Qt generation, still heavily depended on |
| GTK 4 | 88 | current GTK generation |
| FLTK | 16 | small self-contained toolkit |

Two observations follow directly from those numbers.

**Qt is ahead of GTK in this catalog**, and by a wide margin once Qt 5 and
Qt 6 are considered together (860 combined) against GTK 3 and GTK 4 (322
combined). Part of that is scope: Qt is documented upstream as a full
cross-platform application framework — networking, threading, and more —
rather than a widget set, so packages depend on `qt6-base` for
non-GUI reasons.

**Both families carry their previous generation at scale.** Qt 5 at 223
and GTK 3 at 234 each have more dependents than the newer generation
alongside them (GTK 4 at 88). A migration to the newer major version is
still in progress across the catalog, and a build environment realistically
needs both.

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

## Evidence and Gaps

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
