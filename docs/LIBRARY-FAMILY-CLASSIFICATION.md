---
id: doc:volume-11:library-family-classification
title: Library Family Classification Model
volume: 11
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Library Family Classification Model

A library family groups related development and runtime artifacts around a
qualified logical API. The grouping is an evidence-backed classification, not
an equivalence claim based on a package name, filename stem, or one DLL import.

```mermaid
flowchart LR
    L["logical library family"] --> API["headers and documented API"]
    L --> PC["pkg-config and CMake metadata"]
    L --> S["static library"]
    L --> I["import library"]
    L --> D["runtime DLL"]
    L --> P["package ownership"]
```

| Member type | Classification evidence | Relationship to logical library | Must remain distinct |
| --- | --- | --- | --- |
| Header or header set | Package path, include layout, API metadata | Exposes source-facing interface | Binary implementation and ABI guarantee |
| `pkg-config`/CMake module | Parsed module identity and declared targets/requirements | Describes a consumption surface | Runtime dependency proof |
| Static library | Archive path and member inventory | Link-time implementation artifact | Import library and loaded DLL |
| Import library | Import-archive classification and member evidence | Link-time binding surface for a DLL | Static archive contents and runtime loader result |
| Runtime DLL | PE artifact identity, exports, imports, architecture | Deployable binary implementation | Logical API compatibility across versions |
| Package | Snapshot-qualified ownership and metadata | Distribution/deployment container | The library family itself |

## Classification Rules

1. Create a logical library-family association only when package, metadata,
   headers, archive, or binary evidence establishes a meaningful relationship.
   Filename similarity alone is insufficient.
2. Qualify classifications by environment, architecture, CRT/ABI, package
   version, and inventory snapshot wherever those properties are known.
3. Preserve many-to-many membership: one package can ship several libraries,
   and a family can span runtime, development, compatibility, or split
   packages.
4. Do not equate an import library with a static library, or either with its
   runtime DLL. Their file formats, linkage roles, and compatibility evidence
   differ.
5. Treat API/source compatibility, ABI compatibility, and loader resolution
   as separate claims requiring their own qualified evidence.

## Classification Sequence

1. Start with a snapshot-qualified package and owned artifact paths.
2. Collect headers, metadata modules, archives, and PE artifacts.
3. Compare declared names, imported targets, exports, and ownership evidence.
4. Record supported family membership plus confidence and unresolved ambiguity.
5. Use explicit ABI or runtime observations before making compatibility claims.

## Related Views

- [Header and development-metadata indexes](HEADER-AND-METADATA-INDEXES.md)
- [Binary-to-DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md)
- [Package-to-file inventory](PACKAGE-FILE-INVENTORY.md)
