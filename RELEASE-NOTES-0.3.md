# AKB Bootstrap 0.3

Bootstrap 0.3 adds authoritative deep inventory to the self-updating MSYS2
Architecture Knowledge Base.

## Added

- package-owned file inventory from installed or repository pacman databases;
- SHA-256, size, presence, package ownership, and artifact classification;
- bounded PE32/PE32+ metadata, import, export, and debug-directory analysis;
- GNU/BSD archive-member analysis for static and import libraries;
- header, pkg-config, and CMake development-metadata analysis;
- static PKGBUILD extraction without evaluating untrusted shell code;
- typed artifact, DLL, package, library, metadata, and recipe relationships;
- content-addressed deep-inventory snapshots and integrity manifests;
- artifact-level additions, removals, and content-change reports;
- explicit warnings, ambiguities, and unresolved-reference reports;
- unit fixtures for PE, archive, metadata, recipe, projection, and change logic.

## Operational boundary

Repository-wide pacman file databases identify all packaged paths. Deep binary
inspection requires the corresponding files to exist locally. Automated
package-archive extraction and upstream source retrieval remain planned because
they require separate storage, trust, retention, and execution-boundary rules.
