# Architecture Knowledge Base Roadmap

## Increment 0 — Foundation

- [x] Governing charter
- [x] Information architecture
- [x] Twenty-volume master index
- [x] Documentation standard
- [x] Typed graph schema
- [x] Entity and relationship vocabularies
- [x] Bootstrap graph
- [x] Source registry
- [x] Validation and index generation
- [ ] Architecture Decision Record template
- [ ] Claim-level evidence implementation
- [ ] Coverage metrics and quality gates

## Increment 1 — Evidence and inventory pipeline

- [ ] Register official upstream sources
- [x] Discover and ingest enabled repository package metadata through pacman
- [x] Preserve content-addressed catalog snapshots and integrity manifests
- [x] Generate package dependency and reverse-navigation relationships
- [x] Produce package addition, removal, and version-change reports
- [x] Support on-demand and Windows Scheduled Task refresh
- [ ] Ingest repository database archives directly
- [ ] Ingest package recipes
- [ ] Extract package archives and file manifests
- [ ] Extract PE imports, exports, subsystem, architecture, and debug metadata
- [ ] Extract static/import archive members
- [ ] Index headers, pkg-config files, and CMake metadata
- [ ] Record checksums, versions, retrieval dates, and licenses
- [ ] Produce reproducible snapshot manifest

## Increment 2 — Ecosystem baseline

- [ ] L0 ecosystem context
- [ ] L1 eight-layer architecture
- [ ] L2 domain decomposition
- [ ] Terminology and boundary decisions
- [ ] MSYS2 versus MinGW-w64 role model
- [ ] Environment comparison and migration matrix

## Increment 3 — Runtime and package management

- [ ] MSYS runtime initialization
- [ ] Process, fork, exec, signal, path, mount, filesystem, symlink, and PTY models
- [ ] pacman architecture and transaction sequences
- [ ] repository, mirror, signing, key, cache, hook, and database models

## Increment 4 — Toolchains and userland

- [ ] GCC, LLVM, Binutils, Clang, LLD, GDB, and LLDB
- [ ] CMake, Meson, Autotools, Make, Ninja, and pkg-config
- [ ] GNU userland component deep dives
- [ ] generated-artifact and build-flow mappings

## Increment 5 — Package and library catalog

- [ ] Repository-to-package inventory
- [ ] Package-to-file inventory
- [ ] Binary-to-DLL dependency graph
- [ ] Header and metadata indexes
- [ ] Library family classification
- [ ] Reverse dependency and impact analysis

## Increment 6 — Git for Windows

- [ ] Distribution boundary and divergence
- [ ] Launcher, Git Bash, Mintty, and shell startup
- [ ] Native Git, MSYS interaction, SSH, HTTP, credentials, crypto, and DLL loading
- [ ] Package and source mappings

## Increment 7 — Explorer

- [ ] Stable object routes and deep links
- [ ] Search, filters, breadcrumbs, and cross-references
- [ ] Progressive graph expansion and collapse
- [ ] Forward and reverse dependency navigation
- [ ] Layer, package, library, runtime, toolchain, and repository views
- [ ] Accessible SVG and textual fallbacks
- [ ] Large-graph performance tests

## Increment 8 — Assurance and operations

- [ ] Threat model and supply-chain analysis
- [ ] Performance experiments and hot-path analysis
- [ ] Upgrade, rollback, repair, and migration guides
- [ ] Developer and operator workflows
- [x] Initial continuous refresh, difference reports, and historical snapshots
- [ ] Multi-source refresh orchestration, retention policy, and alerting
