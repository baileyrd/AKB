---
id: doc:volume-20:requirements-traceability
title: Handoff Requirement Traceability
volume: 20
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-31
---

# Handoff Requirement Traceability

This matrix evaluates the original project handoff against current evidence.
`Complete` means the stated scope has direct repository evidence; a tool or
template alone is not sufficient.

| Requirement | State | Current evidence | Remaining proof/work |
| --- | --- | --- | --- |
| Machine-readable architecture model | Partial | Typed graph plus official package snapshot | Model runtime, source, binary, and file objects at observed scale |
| Full package catalog | Partial | 15,711 snapshot-bound package records | Refresh cadence, all configured repos, and signed-source provenance |
| Package, library, binary, headers, metadata relationships | Partial | Package and declared dependency views plus a local-only, hash-verified isolated installed-artifact projection (package ownership, PE imports/exports, archives, headers, and metadata) | Extend direct collection beyond the bounded installed set and resolve dependencies absent from that observation |
| MSYS runtime and environment architecture | Partial | Runtime/environment role models and Level 0/1 links; six verified, evidence-qualified environment claims in the [claim/evidence index](../generated/claim-evidence-index.md) | Subsystem objects, flows, and tested evidence for each behavior |
| GNU, toolchain, pacman, Git for Windows documentation | Partial | Dedicated role and boundary documents; per-component pages with responsibilities, boundaries, interfaces, dependencies, and primary evidence now exist for every GNU-userland tool (29, Volume 5), every toolchain tool (14, Volume 8), and every documented library (104, Volume 6, one — zlib — additionally carrying full family-classification evidence); Git for Windows' three canonical pages (Volume 9) now carry controlled local launcher, PATH-resolution, and PE-import observations rather than methodology text alone | Per-component pages of the same depth for pacman/repository internals (Volume 7) remain undone (no pacman installation is available in the current authoring environment to observe); Git for Windows still lacks per-component pages of the GNU-userland/toolchain depth, only page-level controlled observations |
| Interactive Explorer | Partial | Stable routes, search, filters, dependency navigation | Zoomable graphical exploration and complete populated object categories |
| Level 0–7 linked diagram hierarchy | Partial | Eight linked, route-tested SVGs spanning Levels 0–7 and generated dossiers for every composed object | Diagrams and dossiers are navigation aids; substantive per-object evidence-qualified drill-down coverage remains incomplete |
| Every major claim traceable to evidence | Partial | Source registry, snapshot manifest, and [generated claim/evidence index](../generated/claim-evidence-index.md), now covering 39 claims (fact/observation/inference-classified) and 115 evidence records — the original 6 bounded environment facts, per-component dependency-to-feature claims across Volumes 5, 6, and 8, and controlled local observations now covering Volumes 2, 3, 9, 11, 16, 17, and 18 as well | Claim coverage for authored narrative outside those volumes, and per-object citations for Volumes 4, 7, and beyond |
| Security, performance, upgrade, and operations | Partial | Dedicated authored documents and refresh policy | Measured operational history and requirement-specific evidence |

## Acceptance rule

Do not change a state to `Complete` until the linked evidence covers the full
stated scope and the generation/validation path is reproducible from the
repository.
