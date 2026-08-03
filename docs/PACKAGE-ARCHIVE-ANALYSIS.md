---
id: doc:volume-11:package-archive-analysis
title: Uninstalled Package Archive Analysis
volume: 11
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-08-02
---

# Uninstalled Package Archive Analysis

`tools/analyze_package_archive.py` statically analyzes a downloaded package
archive without installing it or executing package scripts. It reads regular
archive members in-stream, rejects traversal-shaped paths, records checksums,
and applies the same PE, archive-member, pkg-config, and CMake metadata
parsers used for installed inventory. It also preserves safe symbolic and hard
links as path records, so library aliases can be projected as explicit
`links-to` relationships rather than being silently omitted.

The [Level 6 executable and DLL diagram](../diagrams/level-6.svg)
shows the deliberate boundary between declared repository metadata and
observed package-payload artifacts.

```powershell
py -3 tools/analyze_package_archive.py C:\cache\sample.pkg.tar `
    --package sample --output work\sample-archive
py -3 tools/import_deep_inventory.py work\sample-archive
```

For a directory of downloaded package archives, the batch importer reads each
archive's `.PKGINFO` package name, analyzes it independently, and accumulates
only verified snapshots:

```powershell
py -3 tools/import_package_archives.py C:\cache\msys2-packages
```

The generated JSONL and manifest use the established deep-inventory importer
contract. The manifest records the source package archive hash and labels its
scope `package-archive`, preserving the distinction from files installed in a
local MSYS2 root. Standard archive formats are read directly by Python. For
the `.zst` packages published by MSYS2, the tool first lists and validates
every path, then expands the archive with the host `tar` implementation into a
temporary directory before reading regular files and safe links. Decompression
and analysis never execute package payloads.
