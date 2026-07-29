# Repository Database Archive Import

`tools/import_repository_db.py` reads pacman repository database archives
directly without extracting files to the filesystem. It accepts tar formats
handled by Python's standard library and parses only regular `*/desc` records.
It rejects traversal-shaped member names, missing package identity, duplicate
package names, malformed descriptions, and archives with no package records.

Convert one downloaded database into the existing catalog-import contract:

```powershell
py -3 tools/import_repository_db.py C:\cache\msys.db `
    --repository msys --output work\catalog-from-db
py -3 tools/import_package_catalog.py work\catalog-from-db
```

The conversion writes `all-packages.csv`, `dependency-edges.csv`, and a
catalog manifest. The manifest records the source archive name and SHA-256;
the normal importer then verifies the generated inputs, snapshots them, and
atomically promotes the resulting catalog projection.

Archive collection and trust verification remain separate responsibilities:
obtain repository databases through the configured pacman mirror and its
signature/key policy before passing a local archive to this tool.
