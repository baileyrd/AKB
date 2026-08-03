---
id: doc:volume-10:explorer-domain-views
title: Explorer Domain Views
volume: 10
status: partial
model_refs:
  - layer:msys2:1-windows-kernel-services
  - layer:msys2:6-toolchains-and-build-systems
evidence_refs: []
last_verified: 2026-08-02
---

# Explorer Domain Views

## Purpose

The generated explorer provides stable typed views at `#/view/layers`,
`packages`, `artifacts`, `libraries`, `runtimes`, `toolchains`,
`repositories`, and `evidenced`. Each view projects the composed graph and
links back to canonical object routes.

## Projection rule

A view projects by entity **kind**, by **tag**, or by both. Tag projection
exists because some architectural groupings are modelled as a tag on an
existing kind rather than as a dedicated kind: the toolchain tools are
`component` and `library` entities carrying a `toolchain`, `compiler`,
`linker`, `debugger`, or `build-system` tag, not entities whose `kind` is
`toolchain`.

The authoritative definition is the `views` object in
`tools/build_explorer.py`, mirrored for testing in
`tests/test_roadmap_claims.py`.

## Correction, 2026-08-02

This page previously stated: *"Each view derives membership from entity
kinds in the composed projection... Empty views are intentional when the
current snapshot contains no matching typed objects."*

Both halves were wrong in a way that concealed a defect.

The `toolchains` view projected only by `kind`, and the graph emits no
entity of kind `toolchain` — so the view rendered zero objects while
seventeen matching entities existed under a `toolchain` or `build-system`
tag. Six shipped hyperlinks across four diagrams
(`level-0-ecosystem.svg`, `level-1-eight-layers.svg`,
`level-2-runtime-package-flow.svg`, and `level-6-toolchain-build-flow.svg`)
pointed into that empty view. The emptiness was not intentional and did not
reflect the snapshot.

The `layers` view was empty for a different reason: `layer` is a valid kind
in `model/vocabularies/entity-kinds.json`, but the eight layers documented
in [the eight-layer architecture](EIGHT-LAYER-ARCHITECTURE.md) had never
been authored as entities. They now exist as
`layer:msys2:1-windows-kernel-services` through
`layer:msys2:8-users-and-automation`, each `contains`-linked from
`ecosystem:msys2:msys2` and carrying representative members.

## Current membership

| View | Objects | Projection |
| --- | ---: | --- |
| layers | 8 | kind `layer` |
| packages | 15,711 | kinds `package`, `package-artifact` |
| artifacts | 549 | kinds `dll`, `executable`, `import-library`, `static-library`, `filesystem-path` |
| libraries | 171 | kinds `library`, `dll`, `import-library`, `static-library` |
| runtimes | 7 | kinds `runtime`, `environment`, `crt`, `abi` |
| toolchains | 17 | kinds above, plus tags `toolchain`, `compiler`, `linker`, `debugger`, `build-system` |
| repositories | 6 | kinds `repository`, `mirror`, `source-repository` |

## Enforcement

An empty view is now a build failure rather than a documented intention.
`tests/test_diagrams.py::test_every_view_a_diagram_links_to_resolves_to_objects`
scans every `#/view/` hyperlink in `diagrams/*.svg` and fails if any target
projection renders no objects, so a diagram cannot ship pointing at an empty
view. `tests/test_roadmap_claims.py` additionally gates the roadmap's
"Layer, package, library, runtime, toolchain, and repository views" item on
all six named views being non-empty.

If a view is genuinely expected to be empty in a future snapshot, that must
be recorded as a deliberate exception rather than asserted as a general
principle, because the general principle is what let this defect ship.

## Related Objects

- [Diagram hierarchy](DIAGRAM-HIERARCHY.md)
- [Eight-layer architecture](EIGHT-LAYER-ARCHITECTURE.md)
- [Explorer stable routes](EXPLORER-STABLE-ROUTES.md)
- [Charter drift assessment](CHARTER-DRIFT-ASSESSMENT.md)
