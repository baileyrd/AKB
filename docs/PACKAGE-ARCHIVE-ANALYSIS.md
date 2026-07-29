# Uninstalled Package Archive Analysis

`tools/analyze_package_archive.py` statically analyzes a downloaded package
archive without installing it or executing package scripts. It reads regular
archive members in-stream, rejects traversal-shaped paths, records checksums,
and applies the same PE, archive-member, pkg-config, and CMake metadata
parsers used for installed inventory.

The [Level 5 evidence flow](../diagrams/level-5-package-artifact-evidence.svg)
shows the deliberate boundary between declared repository metadata and
observed package-payload artifacts.

```powershell
py -3 tools/analyze_package_archive.py C:\cache\sample.pkg.tar `
    --package sample --output work\sample-archive
py -3 tools/import_deep_inventory.py work\sample-archive
```

The generated JSONL and manifest use the established deep-inventory importer
contract. The manifest records the source package archive hash and labels its
scope `package-archive`, preserving the distinction from files installed in a
local MSYS2 root. Standard archive formats are read directly by Python. For
the `.zst` packages published by MSYS2, the tool first lists and validates
every path, then expands the archive with the host `tar` implementation into a
temporary directory before reading only regular files. Decompression and
analysis never execute package payloads.
