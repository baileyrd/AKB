# AKB Bootstrap 0.2

This increment makes continuous package-catalog refresh an implemented AKB
capability.

## Added

- PowerShell collector for all enabled MSYS2 pacman repositories
- Complete, per-repository, installed-package, dependency, group, and summary outputs
- SHA-256 catalog manifest and collection metadata
- Portable Python catalog importer
- Historical evidence snapshots and current generated catalog projection
- Package addition, removal, and version-change analysis
- Unresolved dependency reporting
- Composed validation and index generation across authored and generated models
- On-demand refresh orchestrator
- Optional daily Windows Scheduled Task registration
- Self-updating architecture documentation
- Standard-library importer tests and end-to-end fixture

## Next refresh adapters

Package file manifests, PE/DLL analysis, libraries, headers, pkg-config and
CMake metadata, build recipes, upstream sources, runtime observations, and
official documentation remain planned.
