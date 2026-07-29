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
- [x] Architecture Decision Record template
- [x] Claim-level evidence implementation
- [x] Coverage metrics and quality gates

## Increment 1 — Evidence and inventory pipeline

- [x] Register official upstream sources
- [x] Discover and ingest enabled repository package metadata through pacman
- [x] Preserve content-addressed catalog snapshots and integrity manifests
- [x] Generate package dependency and reverse-navigation relationships
- [x] Produce package addition, removal, and version-change reports
- [x] Support on-demand and Windows Scheduled Task refresh
- [ ] Ingest repository database archives directly
- [x] Statically ingest package recipes without executing PKGBUILDs
- [x] Extract installed and repository package-file manifests
- [x] Extract PE imports, exports, subsystem, architecture, and debug metadata
- [x] Extract static/import archive members
- [x] Index headers, pkg-config files, and CMake metadata
- [x] Record artifact checksums, versions, retrieval dates, and licenses
- [x] Produce reproducible deep-inventory snapshot manifest
- [ ] Extract and analyze uninstalled binary payloads from package archives
- [ ] Resolve recipe source checksums against downloaded upstream payloads

## Increment 2 — Ecosystem baseline

- [x] L0 ecosystem context
- [x] L1 eight-layer architecture
- [x] L2 domain decomposition
- [x] Terminology and boundary decisions
- [x] MSYS2 versus MinGW-w64 role model
- [x] Bounded runtime observation and current-environment report
- [x] Environment comparison and migration matrix

## Increment 3 — Runtime and package management

- [x] MSYS runtime initialization
- [x] Process, fork, exec, signal, path, mount, filesystem, symlink, and PTY models
- [x] pacman architecture and transaction sequences
- [x] repository, mirror, signing, key, cache, hook, and database models

## Increment 4 — Toolchains and userland

- [x] GCC, LLVM, Binutils, Clang, LLD, GDB, and LLDB
- [x] CMake, Meson, Autotools, Make, Ninja, and pkg-config
- [x] GNU userland component deep dives
- [x] generated-artifact and build-flow mappings

## Increment 5 — Package and library catalog

- [x] Repository-to-package inventory
- [x] Package-to-file inventory
- [x] Binary-to-DLL dependency graph
- [x] Header and metadata indexes
- [x] Library family classification
- [ ] Reverse dependency and impact analysis

## Increment 6 — Git for Windows

- [x] Distribution boundary and divergence
- [x] Launcher, Git Bash, Mintty, and shell startup
- [x] Native Git, MSYS interaction, SSH, HTTP, credentials, crypto, and DLL loading
- [x] Package and source mappings

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
