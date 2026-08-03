---
id: doc:volume-13:reverse-dependency-impact-analysis
title: Reverse Dependency and Impact Analysis Model
volume: 13
status: partial
model_refs:
  - library:gnu:zlib
  - dll:gnu:zlib1.dll
  - package:msys2:mingw-w64-ucrt-x86_64-zlib
evidence_refs:
  - evidence:catalog:current
  - evidence:inventory:current
  - evidence:akb-process:zstd-recipe-import-exercise-2026-07-31
last_verified: 2026-07-31
---

# Reverse Dependency and Impact Analysis Model

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnu:zlib` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Jean-loup Gailly and Mark Adler |
| Environments | `ucrt64` |
| Upstream | <https://www.zlib.net/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-zlib` |
| Version (observed) | 1.3.2-2 |
| License (observed) | spdx:Zlib |
| Architecture (observed) | any |
| Installed size (observed) | 427.8 KB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:zlib:manual-2026-07-30` — zlib Manual (`primary`, retrieved 2026-07-30)

**Claims about this object**

- `claim:library:zlib:hub` (`observation`, `verified`) — zlib is the most-depended-upon package observed in this catalog snapshot among all components and libraries modeled in this knowledge base, with 299 recorded reverse dependents, exceeding gcc-libs' 167.

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


Impact analysis is a reproducible query over directional, snapshot-qualified
edges. It identifies observed consumers and changed objects; it does not by
itself prove breakage, load order, or compatibility after a package update.

```mermaid
flowchart LR
    C["changed package or artifact"] --> F["forward typed edges"]
    F --> R["derived reverse consumers"]
    R --> S["scope and environment filter"]
    S --> I["impact candidate report"]
    U["unresolved / ambiguous records"] --> I
```

| Edge family | Reverse query answers | Required qualification | Excluded conclusion |
| --- | --- | --- | --- |
| Package runtime dependency | Which catalog packages declare a requirement | Repository, environment, version, snapshot | Binary import or runtime load result |
| Optional dependency | Which packages declare an optional association | Dependency class and snapshot | Mandatory installation or execution path |
| Recipe build/check dependency | Which recipes use a build/test input | Recipe revision and parser evidence | Runtime deployment consumer |
| PE DLL import | Which analyzed binaries declare a DLL import | Artifact hash and inventory snapshot | Loader resolution or ABI compatibility |
| Metadata requirement | Which `.pc`/CMake modules declare a requirement | Metadata path, parser result, environment | A successful configured build |

## Analysis Rules

1. Derive reverse navigation from canonical forward edges at query time; do
   not store inverse duplicates that could diverge from their evidence.
2. Partition every report by edge type, snapshot, environment, architecture,
   and version constraints before calculating reachability or counts.
3. Include unresolved and ambiguous targets in the report as coverage limits,
   not as inferred relationships.
4. Report a change as an impact candidate when it intersects a qualified edge
   or artifact identity. Elevate it to a breakage conclusion only with API,
   ABI, build, or runtime verification evidence.
5. Keep catalog dependency changes and binary-import changes separately
   attributable so updates can be assessed at the correct architectural layer.

## Impact Workflow

1. Select two immutable snapshots or a single changed object identity.
2. Classify changes as package metadata, artifact bytes, metadata, recipe, or
   runtime observation changes.
3. Traverse only the applicable typed edges under matching scope qualifiers.
4. Include derived reverse consumers, unresolved records, and confidence.
5. Prioritize candidates for controlled rebuild, ABI comparison, or runtime
   validation rather than presenting graph reachability as a defect result.

## Generated Views

Two of the five edge families above are already backed by reproducible
generated views, previously produced but not linked from this page:

- [`generated/reverse-dependency-impact.json`](../generated/reverse-dependency-impact.json)
  — package runtime dependency edges, one entry per package with its
  `declared_consumers` list, snapshot-qualified via its own `snapshot`
  field. Built by `tools/build_catalog_views.py` from
  `evidence:catalog:current`.
- [`generated/binary-dependency-graph.json`](../generated/binary-dependency-graph.json)
  and [`generated/binary-dependency-report.md`](../generated/binary-dependency-report.md)
  — PE DLL import edges (3,058 as of this snapshot) with named-symbol and
  ordinal-import counts and derived reverse-importer counts per DLL. Built
  by `tools/import_deep_inventory.py` from a bounded installed-artifact
  snapshot (`evidence:inventory:current`, snapshot
  `20260729T122657Z-eac21b0c1bb8`); scope is
  that installation only, not every environment or package this knowledge
  base documents.

The Recipe build/check dependency and Metadata requirement edge families
have no corresponding generated view yet — not because the import logic
is missing, but because it has never resolved a real edge, as the
2026-07-31 controlled exercise below demonstrates.

### Controlled exercise: why the Recipe build/check edge family is still empty

`tools/import_deep_inventory.py`'s `build_projection()` already contains
working code to emit `build-depends-on` and `check-depends-on`
relationships from a recipe's `makedepends`/`checkdepends` fields (the
same function `tools/import_recipe_tree.py` calls). On 2026-07-31 this
was exercised end to end against one real recipe, not a synthetic
fixture: the current `mingw-w64-zstd/PKGBUILD` was downloaded from the
official `https://github.com/msys2/MINGW-packages` tree, run through
`tools/collect_recipe_tree.py`, then `tools/import_recipe_tree.py`.

The result was one `build-recipe` entity and **zero** relationships —
every one of its 5 package-name/dependency references (`pkgname`,
`depends`, and 3 `makedepends` entries) landed in `unresolved.json`
instead, because each one is the literal, unexpanded string
`${MINGW_PACKAGE_PREFIX}-...` in the source text. Per
[Package recipes never execute](THREAT-MODEL-AND-SUPPLY-CHAIN.md#measured-control-verification-package-recipes-never-execute),
`parse_pkgbuild()` deliberately never evaluates shell variables — the
same static-parsing-only property that makes recipe collection safe
also means `MINGW_PACKAGE_PREFIX` (`mingw-w64-ucrt-x86_64`, `mingw-w64-clang64`,
etc., normally substituted per target environment at build time) is
never resolved to a real package ID. This is the concrete, root-caused
reason the edge family has stayed empty: it is
[Package recipes](THREAT-MODEL-AND-SUPPLY-CHAIN.md)'s own documented
"Expanded dynamic-field coverage" assurance need surfacing here as a
missing generated view, not two independent gaps. This one-recipe,
local-only (per [Local-Only Evidence Retention](LOCAL-EVIDENCE-RETENTION.md),
not staged in this repository) result does not establish the outcome
for every recipe — a recipe with a literal (non-templated) dependency
name would resolve normally — only that this specific, common templating
pattern defeats resolution as designed.

## Worked Example: zlib

Querying [zlib](ZLIB.md)'s reverse dependents through three different edge
families in this table, on the same package, produces three different and
individually correct numbers — the concrete case Analysis Rules 2 and 5
describe:

- **299** — every edge in `work/official-catalog/dependency-edges.csv`
  targeting `mingw-w64-ucrt-x86_64-zlib`, the figure
  [zlib's own page](ZLIB.md#reverse-dependencies) cites. This mixes two
  dependency classes.
- **297** — the `declared_consumers` count in
  `generated/reverse-dependency-impact.json` for the same package,
  because that view's own stated scope is
  "declared runtime package dependencies only" and so excludes the
  catalog's 2 `optional-depends-on` edges. Partitioning by edge type (Rule
  2) recovers the difference: 297 `runtime-depends-on` + 2
  `optional-depends-on` = 299.
- **34** — the count of `imports-dll` edges in
  `generated/binary-dependency-graph.json` targeting
  `dll:gnu:zlib1.dll`'s installed-artifact counterpart
  (`dll:msys2:/ucrt64/bin/zlib1.dll`) — Binutils and GCC toolchain
  executables (`ld.exe`, `objdump.exe`, `cc1plus.exe`, and 31 others) on
  the one bounded installation this snapshot observed. This is
  byte-level PE import evidence, a categorically different and much
  narrower claim than a catalog-declared package dependency (per the
  table above): it proves an observed import table entry on this
  specific installation, not every UCRT64 install, and not that removing
  zlib would break these 34 binaries at load or run time (per Rule 4).

None of the three numbers is wrong; each answers a differently-scoped
question, which is why Rule 5 requires keeping catalog dependency changes
and binary-import changes separately attributable rather than collapsing
them into one "N things depend on zlib" figure.

## Related Views

- [Repository-to-package inventory](REPOSITORY-PACKAGE-INVENTORY.md)
- [Binary-to-DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md)
- [Build artifact and flow mappings](BUILD-ARTIFACT-FLOW-MAPPINGS.md)

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["zlib"]
    u0["CMake"]
    u0 -->|requires| subject
    u1["GNU Binutils"]
    u1 -->|requires| subject
    u2["GCC"]
    u2 -->|requires| subject
    u3["GDB"]
    u3 -->|requires| subject
    u4["curl (UCRT64)"]
    u4 -->|requires| subject
    u5["libxml2"]
    u5 -->|requires| subject
    u6["GnuTLS (UCRT64)"]
    u6 -->|requires| subject
    u7["libarchive"]
    u7 -->|requires| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnu:zlib` in the composed graph: 13 dependents and 0 dependencies, of which 5 are omitted here for legibility.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->
