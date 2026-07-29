---
id: doc:volume-11:package-file-inventory
title: Package-to-File Inventory Model
volume: 11
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Package-to-File Inventory Model

The package-to-file inventory maps a package record to package-owned paths
within a verified inventory snapshot. It deliberately separates a declared
repository file manifest, a file found under a local installation root, and
bytes extracted from a package archive.

```mermaid
flowchart LR
    P["package record"] --> O["ownership manifest"]
    O --> R["repository-declared path"]
    O --> I["installed path observation"]
    A["package archive"] --> X["extracted payload path"]
    I --> H["hash and static analysis"]
    X --> H
    H --> G["artifact graph projection"]
```

| Evidence scope | What it establishes | Required fields | It does not establish |
| --- | --- | --- | --- |
| Repository file database | A package declares a path in that repository snapshot | Repository, package identity, normalized path, snapshot ID | Local presence, payload bytes, or current mirror availability |
| Installed-file observation | A package-owned path was observed beneath a specified MSYS2 root | Package identity, path, presence, observation time, snapshot ID | That every package file is locally present or unmodified |
| Archive payload observation | A path and bytes were extracted from a named archive | Archive digest, entry path, size/hash, extraction method | That the archive was installed by a transaction |
| Static artifact analysis | Observed properties of locally available bytes | Artifact hash, parser version, analysis result/warnings | Package ownership absent an independently resolved owner |

## Identity and Ownership Rules

1. Normalize package paths as MSYS-style absolute paths before creating the
   package `--installs-->` artifact relationship.
2. Qualify every ownership edge with the inventory snapshot. Ownership can
   change across package versions and repository snapshots.
3. Preserve `present: false` repository records without byte-derived fields;
   absence of local bytes is a collection fact, not a malformed artifact.
4. Do not collapse paths that share a basename. DLL identity, filesystem path,
   logical library identity, and package ownership are distinct objects.
5. Retain unresolved or ambiguous owners as reconciliation records rather than
   assigning a file to a plausible package.

## Inventory Sequence

1. Collect package file manifests for the selected installed or repository
   scope.
2. Validate JSONL stream hashes and record counts against the manifest.
3. Resolve package ownership and emit normalized artifact entities.
4. Analyze bytes only where local or archive extraction evidence makes them
   available; preserve warnings without fabricating metadata.
5. Atomically replace the current projection only after complete validation,
   retaining raw snapshots for reproducibility and diffing.

For broad, byte-free package-file coverage, import official pacman `.files`
databases and then run the deep-inventory importer. These records establish
package ownership only; their `present` property remains `false` and they do
not imply binary, export, or ABI observations.

```powershell
py -3 tools/import_repository_file_db.py C:\cache\msys.files `
    --repository msys --output work\files-inventory
py -3 tools/import_deep_inventory.py work\files-inventory --accumulate
```

## Related Views

- [Repository-to-package inventory](REPOSITORY-PACKAGE-INVENTORY.md)
- [Deep inventory evidence contract](DEEP-INVENTORY-CONTRACT.md)
- [Build artifact and flow mappings](BUILD-ARTIFACT-FLOW-MAPPINGS.md)
