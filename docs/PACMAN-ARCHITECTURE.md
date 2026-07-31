---
id: doc:volume-7:pacman-architecture
title: Pacman Architecture and Transaction Model
volume: 7
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs:
  - evidence:catalog:current
last_verified: 2026-07-30
---

# Pacman Architecture and Transaction Model

The linked [Level 2 runtime and package flow](../diagrams/level-2-runtime-package-flow.svg)
separates the repository and payload evidence path from runtime behavior.

```mermaid
flowchart LR
    C["pacman command"] --> D["local configuration and sync databases"]
    D --> R["configured repositories and mirrors"]
    R --> S["signed package metadata and archives"]
    S --> V["verification and dependency resolution"]
    V --> T["transaction"]
    T --> F["installed filesystem and local database"]
    T --> H["hooks and post-transaction actions"]
```

| Boundary | Responsibility | AKB evidence treatment |
| --- | --- | --- |
| Configuration | Enabled repositories, mirrors, keyring/trust settings | Observed snapshot; version-qualified |
| Sync databases | Repository package metadata and dependencies | Collector input with hashes/counts |
| Packages | Signed archives, file manifests, dependency metadata | Archive/installed evidence; never inferred bytes |
| Transaction | Resolution, install/remove/upgrade and local database update | Operational behavior requiring controlled observation |
| Hooks/cache | Policy actions and retained package payloads | Configuration and filesystem evidence |

## Trust and Recovery Rules

Repository metadata, mirrors, archives, and local databases are inputs with
separate provenance. A failed AKB import must not replace the prior generated
projection. Package ownership metadata does not establish binary behavior when
payload bytes are absent. Upgrade, repair, and rollback procedures remain
operations-guide work and must be tested against a version-qualified install.

## Controlled local state observation

On 2026-07-30, a read-only query of the isolated MSYS installation reported
pacman `6.1.0-25` with `msys2-keyring 1~20260214-1`. Its configured repository
order was CLANGARM64, MINGW32, MINGW64, UCRT64, CLANG64, and MSYS. The local
state contained 175 package-database directories and 170 cache archives; the
standard hook directory contained no hook files at that instant.

This is configuration and retained-state evidence only. It does not establish
mirror availability, signature verification outcomes, transaction behavior, or
the behavior of absent/custom hooks.

## Sync database hash evidence

`evidence:catalog:current`'s own manifest records the exact SHA-256 of each
of the six retrieved repository databases (`msys.db`, `ucrt64.db`,
`clang64.db`, `clangarm64.db`, `mingw64.db`, `mingw32.db`) at the retrieval
time this page's `evidence_refs` already cite — the "Sync databases" row's
"hash the exact database bytes" evidence, not previously cross-linked from
here. The same manifest records `pacman_version` as an empty string: the
collector did not capture the pacman version that produced these databases,
an honest, already-flagged gap rather than an inferred value.

## Related Views

- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Domain decomposition](DOMAIN-DECOMPOSITION.md)
