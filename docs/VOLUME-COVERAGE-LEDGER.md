---
id: doc:volume-20:volume-coverage-ledger
title: Twenty-Volume Coverage Ledger
volume: 20
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-30
---

# Twenty-Volume Coverage Ledger

This ledger audits the delivery structure defined in the
[project discussion record](PROJECT-DISCUSSION-RECORD.md). A volume is not
complete merely because a related page exists: its canonical material must
cover the stated subject with scoped evidence, and generated observations must
remain distinguishable from reviewed architecture.

| Volume | Canonical material | Coverage state | Remaining proof/work |
| ---: | --- | --- | --- |
| 1 Executive Architecture | [Ecosystem context](ECOSYSTEM-CONTEXT.md), [domain decomposition](DOMAIN-DECOMPOSITION.md), [eight-layer architecture](EIGHT-LAYER-ARCHITECTURE.md) | Partial | Per-layer evidence-qualified drill-downs |
| 2 Windows Platform | [Windows platform boundaries](WINDOWS-PLATFORM-BOUNDARIES.md) | Partial | Controlled, version-qualified observations for the listed host boundaries |
| 3 MSYS Runtime | [Runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md), [initialization](MSYS-RUNTIME-INITIALIZATION.md) | Partial | Controlled process, signal, fork/exec, filesystem, symlink, and PTY observations |
| 4 Runtime Environments | [Runtime environments](RUNTIME-ENVIRONMENTS.md) | Partial | Current evidence for every documented environment and compatibility/migration cases |
| 5 GNU Userland | [GNU userland role model](GNU-USERLAND-ROLE-MODEL.md) | Partial | Per-tool startup, configuration, dependency, and interaction pages |
| 6 Libraries | [Libraries architecture](LIBRARIES-ARCHITECTURE.md), [library family classification](LIBRARY-FAMILY-CLASSIFICATION.md), [header and metadata indexes](HEADER-AND-METADATA-INDEXES.md) | Partial | Observed family-level package/artifact coverage beyond the bounded installation |
| 7 Package Management | [Pacman architecture](PACMAN-ARCHITECTURE.md), [repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) | Partial | Version-qualified transaction, cache, hook, and repair observations |
| 8 Toolchains | [Toolchain role model](TOOLCHAIN-ROLE-MODEL.md) | Partial | Per-tool modules, executable workflows, configuration, and observed build outputs |
| 9 Git for Windows | [Distribution boundary](GIT-FOR-WINDOWS-BOUNDARY.md), [launcher/startup](GIT-FOR-WINDOWS-LAUNCHER-STARTUP.md), [transport boundaries](GIT-FOR-WINDOWS-TRANSPORT-BOUNDARIES.md) | Partial | Version-qualified installed artifact and launch evidence |
| 10 Interactive Architecture Explorer | [Explorer hierarchy](DIAGRAM-HIERARCHY.md), generated explorer routes | Partial | Zoomable graphical exploration and demonstrated populated deep-object views |
| 11 Package Catalog | [Repository package inventory](REPOSITORY-PACKAGE-INVENTORY.md), [package file inventory](PACKAGE-FILE-INVENTORY.md), [binary graph](BINARY-DLL-DEPENDENCY-GRAPH.md) | Partial | Direct artifact collection for more than the isolated installed subset |
| 12 Source Code Organization | [Source code organization](SOURCE-CODE-ORGANIZATION.md), recipe-tree collectors, and [Git for Windows package/source mappings](GIT-FOR-WINDOWS-PACKAGE-SOURCE-MAPPINGS.md) | Partial | Package-to-source-to-artifact proof |
| 13 Dependency Analysis | [Reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md) | Partial | Broader resolved binary/metadata dependency observations |
| 14 Build Systems | [Build-system role model](BUILD-SYSTEM-ROLE-MODEL.md), [artifact flow mappings](BUILD-ARTIFACT-FLOW-MAPPINGS.md) | Partial | Reproducible observed build pipeline and patch/output mapping |
| 15 Extension and Plugin Architecture | [Extension and plugin architecture](EXTENSION-AND-PLUGIN-ARCHITECTURE.md) | Partial | Concrete extension implementations and exercised compatibility/migration cases |
| 16 Security | [Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) | Partial | Reassigned canonical volume placement plus measured controls/verification history |
| 17 Performance | [Performance experiments](PERFORMANCE-EXPERIMENTS.md) | Partial | Reassigned canonical volume placement and retained benchmark history |
| 18 Developer Guide | [Developer/operator workflows](DEVELOPER-OPERATOR-WORKFLOWS.md) and explorer guidance | Partial | Canonical developer guide split from operations material |
| 19 Operations Guide | [Upgrade/rollback/repair/migration](UPGRADE-ROLLBACK-REPAIR-MIGRATION.md) | Partial | Canonical operations guide and observed operational exercises |
| 20 Reference Appendices | [Terminology](TERMINOLOGY-AND-BOUNDARIES.md), [requirements traceability](REQUIREMENTS-TRACEABILITY.md), local-retention and evidence documentation | Partial | Requirement-by-requirement completion evidence |

## Current evidence boundary

The local-only evidence includes full repository-file ownership plus a
hash-verified expanded installed-artifact snapshot across the isolated MSYS2
installation. Its standalone typed overlay contains 48,299 entities and
54,993 relationships; it remains separate from the multi-million-object
ownership projection to stay within workstation-safe memory limits. It does
not prove universal runtime behavior, source-to-payload byte identity, or
complete artifact coverage for every repository package. Those distinctions
are intentional and remain completion gates for the relevant rows above.

## Completion rule

Do not mark this ledger complete until every row has a canonical page or
generated view, direct evidence appropriate to its stated scope, and a
reproducible validation path. Cross-links alone do not close a gap.
