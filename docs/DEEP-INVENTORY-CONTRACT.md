# Deep Inventory Evidence Contract

## Purpose

The deep-inventory contract separates collection from architecture modeling.
Collectors describe observed bytes and metadata; the importer verifies and
normalizes those observations into graph entities and relationships.

## Files

| File | Record unit |
| --- | --- |
| `inventory-manifest.json` | Snapshot identity, schema, counts, and hashes |
| `artifacts.jsonl` | One package-owned filesystem artifact |
| `pe-imports.jsonl` | One importing binary and imported DLL pair |
| `pe-exports.jsonl` | One exported name or ordinal |
| `archive-members.jsonl` | One static/import archive member |
| `development-metadata.jsonl` | One parsed pkg-config or CMake file |
| `recipes.jsonl` | One statically parsed PKGBUILD |
| `warnings.jsonl` | One bounded analyzer warning |

The logical record schemas are defined in
`model/schema/deep-inventory.schema.json`. JSONL allows large observations to
be streamed and diffed without loading the full package universe into collector
memory. The importer presently performs the enforcement directly so it retains
its standard-library-only runtime.

## Invariants

1. Every stream listed in the manifest exists, including empty streams.
2. Every stream has a SHA-256 and exact record count.
3. Package paths are normalized MSYS-style absolute paths.
4. An artifact may be known through repository metadata while `present` is
   false; byte-derived fields must then be absent.
5. Analyzer failures become warning records and do not fabricate metadata.
6. PKGBUILDs are never executed by the collector.
7. Every graph fact derived from the inventory references its snapshot
   evidence object. Evidence IDs are snapshot-qualified, so accumulated
   projections preserve the observation that supports each retained fact.
8. Unknown or ambiguous targets remain unresolved records.
9. The current projection changes only after complete input verification.
10. Raw snapshots are immutable and current views are reproducible.

## Projection rules

| Observation | Entity or relationship |
| --- | --- |
| Package-owned path | `package --installs--> artifact` |
| PE import descriptor | `executable/dll --imports-dll--> dll` |
| PE export | `dll.properties.exports[]` |
| Archive member | `static/import-library.properties.members[]` |
| pkg-config or CMake file | Typed metadata entity plus parsed properties |
| Metadata requirement | `metadata --requires--> metadata` when unambiguous |
| PKGBUILD package output | `package --packaged-by--> build-recipe` |
| PKGBUILD dependency | Recipe dependency edge by dependency class |

Reverse dependencies are generated views over directional edges. They are not
duplicated in the canonical graph.
