---
id: doc:volume-11:binary-dll-dependency-graph
title: Binary-to-DLL Dependency Graph Model
volume: 11
status: partial
model_refs:
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:inventory:current
last_verified: 2026-08-05
---

# Binary-to-DLL Dependency Graph Model

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `runtime:msys2:msys-2.0.dll` |
| Kind | `runtime` |
| Status | `partial` |
| Confidence | `verified` |
| Authority | MSYS2 |
| Environments | `msys` |

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


The binary-to-DLL graph is derived from PE import descriptors in verified
artifact observations. It models static import declarations, not a claim that
the Windows loader resolved a particular DLL during a particular execution.

```mermaid
flowchart LR
    P["package-owned executable or DLL"] --> I["PE import descriptor"]
    I --> N["imported DLL name"]
    N --> R["unique observed DLL artifact"]
    N --> U["unresolved or ambiguous record"]
    R --> O["package ownership and snapshot evidence"]
```

| Graph object | Identity rule | Evidence rule | Excluded conclusion |
| --- | --- | --- | --- |
| Importing binary | Package-owned artifact path plus observed hash/snapshot | PE analysis of available bytes | Runtime execution or successful load |
| Imported DLL name | Case-normalized name from PE descriptor | Original descriptor retained in inventory | Unique filesystem target |
| DLL artifact target | Unique candidate artifact in the same qualified projection | Package ownership and byte observation | Loader selection across `PATH`, app-local, or system locations |
| `imports-dll` edge | Importing artifact to uniquely resolved DLL artifact | Source/target plus snapshot evidence | ABI compatibility, symbol availability, or transitive closure |
| Unresolved record | Descriptor that lacks a safe unique target | Snapshot, reason, and candidate set when applicable | A fabricated graph edge |

## Projection Rules

1. Emit `imports-dll` only when the importing artifact and a unique observed
   target can be resolved in the same qualified inventory projection.
2. Keep duplicate DLL basenames, API-set names, delay-load behavior, missing
   bytes, and targets outside the collected scope as explicit unresolved or
   ambiguous records.
3. Maintain directional import edges; generate reverse consumers at query time
   rather than storing duplicate inverse edges.
4. Keep PE imports separate from package dependencies, link inputs, and
   observed loader modules. Each answers a different compatibility question.
5. Bind all binary-derived metadata to the artifact hash and parser version;
   a package upgrade invalidates any unqualified binary assertion.

## Diagnostic Sequence

1. Identify the exact executable or DLL by path, package, snapshot, and hash.
2. Read its PE import descriptors without executing it.
3. Resolve candidate targets only within the qualified artifact projection.
4. Inspect unresolved records before reporting a missing or ambiguous DLL.
5. Use controlled runtime observation separately when the question is actual
   loader behavior rather than static dependency declaration.

## Observed at This Scale

A 2026-08-05 deep-inventory run across the 90 packages installed in this
host's `msys` environment populated this graph for real: 1,843 `imports-dll`
edges among 97 distinct imported-DLL identities, in
[`generated/binary-dependency-report.md`](../generated/binary-dependency-report.md).
The dominant structure is exactly what the runtime architecture predicts —
494 distinct binaries import `/usr/bin/msys-2.0.dll` directly, the single
highest fan-in target in the graph.

This is the MSYS side of the ecosystem only. No `ucrt64`, `clang64`,
`clangarm64`, `mingw64`, or `mingw32` package is installed on this host, so
the graph carries no native-toolchain binaries yet; see
[the deep-inventory blocker](DEEP-INVENTORY-BLOCKER.md) for what closing
that gap needs.

## Related Views

- [Package-to-file inventory](PACKAGE-FILE-INVENTORY.md)
- [Deep inventory evidence contract](DEEP-INVENTORY-CONTRACT.md)
- [Git for Windows transport boundaries](GIT-FOR-WINDOWS-TRANSPORT-BOUNDARIES.md)

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["msys-2.0.dll"]
    u0["bzip2"]
    u0 -->|uses-runtime| subject
    u1["curl"]
    u1 -->|uses-runtime| subject
    u2["Git (MSYS2 package)"]
    u2 -->|uses-runtime| subject
    u3["GNU Autoconf"]
    u3 -->|uses-runtime| subject
    u4["GNU Automake"]
    u4 -->|uses-runtime| subject
    u5["GNU Bash"]
    u5 -->|uses-runtime| subject
    u6["GNU Coreutils"]
    u6 -->|uses-runtime| subject
    u7["GNU Cpio"]
    u7 -->|uses-runtime| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `runtime:msys2:msys-2.0.dll` in the composed graph: 72 dependents and 0 dependencies, of which 64 are omitted here for legibility.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->
