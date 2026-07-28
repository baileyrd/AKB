---
id: doc:volume-7:pacman-architecture
title: Pacman Architecture and Transaction Model
volume: 7
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs: []
last_verified: 2026-07-28
---

# Pacman Architecture and Transaction Model

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

## Related Views

- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Domain decomposition](DOMAIN-DECOMPOSITION.md)
