# Master Volume Index

| Volume | Title | Primary questions |
| ---: | --- | --- |
| 1 | Executive Architecture | What is the ecosystem, why does it exist, and how is it partitioned? |
| 2 | Windows Platform | Which Windows services, APIs, formats, and constraints underpin it? |
| 3 | MSYS Runtime | How does POSIX emulation behave and interact with Windows? |
| 4 | Runtime Environments | How do MSYS, UCRT64, CLANG64, CLANGARM64, MINGW64, and MINGW32 differ? |
| 5 | GNU Userland | How do major userland tools start, execute, configure, and interact? |
| 6 | Libraries | Which library families, binary artifacts, APIs, and consumers exist? |
| 7 | Package Management | How do pacman, repositories, signing, transactions, and lifecycle work? |
| 8 | Toolchains | How do compilers, linkers, debuggers, and build tools produce artifacts? |
| 9 | Git for Windows | How does its distribution combine native Git and MSYS2-derived components? |
| 10 | Interactive Architecture Explorer | How are model objects searched, filtered, linked, and visualized? |
| 11 | Package Catalog | What packages and installed artifacts exist in each repository snapshot? |
| 12 | Source Code Organization | Where are architectural elements implemented upstream? |
| 13 | Dependency Analysis | What depends on what, why, and with what impact and centrality? |
| 14 | Build Systems | How are recipes, orchestration, flags, patches, and outputs organized? |
| 15 | Extension and Plugin Architecture | Where and how can the ecosystem be extended safely? |
| 16 | Security | What are the trust boundaries, threats, mitigations, and supply-chain controls? |
| 17 | Performance | Where are overhead, scale limits, hot paths, and tuning mechanisms? |
| 18 | Developer Guide | How should software be selected, built, debugged, packaged, and migrated? |
| 19 | Operations Guide | How is an installation configured, upgraded, repaired, audited, and observed? |
| 20 | Reference Appendices | Which terms, matrices, identifiers, variables, paths, and sources are canonical? |

## Standard volume structure

Each volume uses applicable portions of this structure:

1. Purpose and audience
2. Scope and boundaries
3. Conceptual architecture
4. Logical architecture
5. Component and package architecture
6. Runtime and process architecture
7. Data, filesystem, and configuration architecture
8. Build and deployment architecture
9. Interfaces and dependencies
10. Execution and sequence flows
11. Security and performance considerations
12. Compatibility, evolution, and migration
13. Operations and troubleshooting
14. Examples and scenarios
15. Object catalog and diagrams
16. Evidence, assumptions, gaps, and references

## Cross-volume rules

- A concept is defined once and referenced elsewhere by stable object ID.
- Package inventories belong to Volume 11; other volumes provide architectural
  interpretation and filtered views.
- Source details belong to Volume 12 and build mechanics to Volume 14.
- Security and performance concerns are summarized locally and analyzed fully
  in Volumes 16 and 17.
- Generated object pages may appear in multiple navigation paths without
  duplicating canonical model data.

## Delivery audit

The [Twenty-Volume Coverage Ledger](VOLUME-COVERAGE-LEDGER.md) records the
canonical material, evidence boundary, and remaining completion work for each
volume.

