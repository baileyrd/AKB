---
id: doc:volume-9:git-for-windows-package-source-mappings
title: Git for Windows Package and Source Mappings
volume: 9
status: partial
model_refs: []
evidence_refs:
  - source:git-for-windows:git
  - source:git-for-windows:build-extra
  - source:git-for-windows:git-sdk-64
last_verified: 2026-07-28
---

# Git for Windows Package and Source Mappings

Git for Windows release artifacts are assembled distribution outputs, not a
pacman inventory.  AKB therefore maps a release-qualified artifact to the
source and build surfaces used to investigate it, while preserving the fact
that a component's presence must be proven from that specific artifact.

| Mapping surface | Primary source | Role | Required qualifier |
| --- | --- | --- | --- |
| Windows-specific Git implementation | `git-for-windows/git` | Windows port and buildable Git source tree | Commit, tag, or build-options revision |
| Distribution assembly support | `git-for-windows/build-extra` | Additional build files and scripts for Git for Windows on MSYS2 | Commit referenced by the release/build process |
| SDK observation surface | `git-for-windows/git-sdk-64` | Mirror of the current 64-bit Git for Windows SDK | Snapshot commit and SDK release/date |
| Installed Git for Windows artifact | Release installer or portable archive | The deployable files, executables, DLLs, and launchers under analysis | Filename, version, retrieval date, and checksum |

## Mapping Rules

1. Do not equate a source repository's file list with a release artifact's
   installed file list. Extract the latter from the installer or portable
   archive being examined.
2. Record all source mappings as many-to-many: a distribution artifact can
   combine multiple source revisions, and a source revision can appear in
   multiple releases.
3. Treat the SDK mirror as an observation and build environment, not proof
   that every SDK file ships in an end-user installer.
4. Preserve release artifact checksums and source commit identifiers together
   before asserting provenance, patches, or bundled component versions.
5. Keep upstream and vendored dependency provenance separate from the Git for
   Windows source mapping until the release's build metadata proves the link.

## Collection Sequence

1. Acquire the selected release artifact without execution and record its
   immutable identity.
2. Extract its file manifest and identify the relevant executable, launcher,
   DLL, or helper.
3. Record the associated Git for Windows source and assembly revisions from
   release-qualified build metadata.
4. Create component-level mappings only where both the artifact and source
   evidence identify the relationship.

## Related Views

- [Git for Windows boundary](GIT-FOR-WINDOWS-BOUNDARY.md)
- [Git for Windows transport boundaries](GIT-FOR-WINDOWS-TRANSPORT-BOUNDARIES.md)
- [Deep inventory evidence contract](DEEP-INVENTORY-CONTRACT.md)
