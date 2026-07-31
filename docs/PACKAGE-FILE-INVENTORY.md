---
id: doc:volume-11:package-file-inventory
title: Package-to-File Inventory Model
volume: 11
status: partial
model_refs:
  - library:gnu:zlib
  - library:curl:libcurl
evidence_refs: []
last_verified: 2026-07-30
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

## Worked examples: archive payload observation beyond the installed subset

Two package archives (not the isolated installed subset) were statically
analyzed with `tools/analyze_package_archive.py` on 2026-07-29, each a
concrete instance of the "Archive payload observation" and "Static
artifact analysis" rows above:

- **zlib (UCRT64)**, `ucrt-zlib.pkg.tar.zst` — 11 owned artifacts (headers,
  pkg-config module, static/import libraries, and the runtime DLL), 114 PE
  exports, 9 PE-imported system DLLs; the full family-classification
  worked example on [zlib](ZLIB.md#family-classification).
- **curl (MSYS)**, `curl.pkg.tar.zst` — 532 owned artifacts (`/usr/bin/curl.exe`
  plus 531 documentation/support files, no `-devel` headers or static
  library in this base package), 0 PE exports (it is an executable, not
  a DLL), and 4 PE-imported DLLs: `kernel32.dll` (one symbol),
  `msys-2.0.dll` (79 symbols — confirming this build is MSYS-dependent,
  not native), `msys-curl-4.dll` (58 symbols — the split transfer
  library [libcurl](LIBCURL.md) documents), and `msys-z.dll` (`inflate`,
  `inflateEnd`, `inflateInit2_` — the MSYS build of
  [zlib](ZLIB.md), confirming a real, byte-level DEFLATE dependency
  distinct from the package-level `requires` edges elsewhere in this
  knowledge base).

Both are local-only per
[Local-Only Evidence Retention](LOCAL-EVIDENCE-RETENTION.md), not staged
as raw artifacts, and reproducible by re-running the collector against
the same archives. This is byte-level PE-import evidence for two
packages beyond the isolated installed subset; it does not establish
family-classification-level detail for curl (no `-devel` archive was
analyzed) or extend beyond these two packages.

## Related Views

- [Repository-to-package inventory](REPOSITORY-PACKAGE-INVENTORY.md)
- [Deep inventory evidence contract](DEEP-INVENTORY-CONTRACT.md)
- [Build artifact and flow mappings](BUILD-ARTIFACT-FLOW-MAPPINGS.md)
