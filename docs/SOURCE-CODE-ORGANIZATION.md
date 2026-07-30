---
id: doc:volume-12:source-code-organization
title: Source Code Organization and Package Provenance
volume: 12
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-30
---

# Source Code Organization and Package Provenance

MSYS2 package source organization is represented as source repositories,
repository-relative recipe paths, declaratively parsed `PKGBUILD` records, and
their stated output-package/dependency expressions. These are source
provenance observations, not proof that a specific published archive was built
from the observed checkout.

```mermaid
flowchart LR
    R["official source repository commit"] --> T["checked-out recipe tree"]
    T --> P["PKGBUILD path and hash"]
    P --> O["declared package outputs"]
    P --> D["declared build/check/runtime inputs"]
    O -. "requires independent proof" .-> A["published package archive"]
```

| Object | Stable identity | Evidence supplied | Explicit limit |
| --- | --- | --- | --- |
| Source repository | Official repository URL and commit | Source provenance anchor | Package archive byte identity |
| Recipe tree | Repository-relative path plus checkout revision | Collection scope | Unchecked source execution |
| `PKGBUILD` | Relative path and SHA-256 | Declaratively parsed metadata | Arbitrary shell expansion or build result |
| Output package expression | Literal parsed package name/expression | Stated intended package relation | Published package ownership without matching evidence |
| Patch/source declaration | Literal recipe field | Declared upstream inputs | Retrieved source authenticity or application result |

## Collection boundary

The recipe collector never sources or executes `PKGBUILD` files. It records
their bytes, selected declarative fields, and dynamic expressions that cannot
be resolved safely. The compact local projection retains source-to-recipe and
unambiguous recipe-to-package links while keeping unresolved dynamic names
explicit.

## Navigation

1. Start with a snapshot-qualified package in the [package catalog](REPOSITORY-PACKAGE-INVENTORY.md).
2. Follow an observed `packaged-by` relationship only when its parsed output
   name uniquely matches the catalog.
3. Inspect the recipe path, commit, and hash before using any source field.
4. Use [build artifact flow mappings](BUILD-ARTIFACT-FLOW-MAPPINGS.md) for
   build-stage interpretation and [deep inventory](DEEP-INVENTORY-CONTRACT.md)
   for archive/installed-byte observations.

## Evidence boundary

The local snapshots from the official `MSYS2/MINGW-packages` and
`MSYS2/MSYS2-packages` trees demonstrate recipe provenance only. Establishing
an upstream-source → recipe → package archive → deployed artifact chain
requires matching source retrieval, patch application, build, and archive
evidence for the exact revision.

## Bounded provenance slice: zlib

On 2026-07-30, the retained MSYS2 `zlib/PKGBUILD` declared upstream
`zlib-1.3.2.tar.xz` and SHA-256
`d7a0654783a4da529d1bb793b7ad9c3318020af77667bcae35f95d0e42a792f3`.
A local retrieval of that exact URL matched the declared digest. The same
isolated installation contains `zlib 1.3.2-1` and `/usr/bin/msys-z.dll`.
The two recipe-local patches also matched their declared SHA-256 values.
This establishes recipe-declared source retrieval and installed ownership as
separate observations; it does not prove patch application, build execution,
or byte identity between the retrieved source and the installed DLL.

A controlled local build then applied both verified patches successfully but
failed under MSYS GCC `15.3.0` while compiling `gzlib.c`, which referenced
`lseek` without a visible declaration. This is a version-qualified failed
build observation, not evidence that the recipe or installed DLL is invalid.

## Related volumes

- Volume 11: [Repository package inventory](REPOSITORY-PACKAGE-INVENTORY.md)
- Volume 14: [Build artifact flow mappings](BUILD-ARTIFACT-FLOW-MAPPINGS.md)
- Volume 9: [Git for Windows package and source mappings](GIT-FOR-WINDOWS-PACKAGE-SOURCE-MAPPINGS.md)
