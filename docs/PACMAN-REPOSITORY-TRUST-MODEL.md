---
id: doc:volume-7:pacman-repository-trust-model
title: Pacman Repository, Mirror, and Trust Model
volume: 7
status: partial
model_refs:
  - ecosystem:msys2:msys2
evidence_refs:
  - evidence:akb-process:zstd-signature-verification-2026-07-31
last_verified: 2026-07-31
---

# Pacman Repository, Mirror, and Trust Model

Pacman combines local policy, repository metadata, mirror delivery, signature
verification, and retained local state. These boundaries must be recorded
separately: successful download from a mirror is not evidence of repository
trust, and a local cache is not proof that a package remains available upstream.

```mermaid
flowchart LR
    C["pacman.conf and include files"] --> R["enabled repositories"]
    R --> M["mirror URLs"]
    M --> D["sync databases and package archives"]
    K["keyring and signature policy"] --> V["verification"]
    D --> V
    V --> T["transaction"]
    T --> L["local package database"]
    T --> H["hooks"]
    D --> A["package cache"]
```

| Boundary | Responsibility | AKB collection rule |
| --- | --- | --- |
| Repository configuration | Selects repository names, order, and policy inputs | Snapshot effective configuration and included files with redaction where required |
| Mirrors | Deliver repository databases and archives | Record selected URL and retrieval time; do not treat availability as authority |
| Keyring and signatures | Bind trusted keys and policy to signed metadata/artifacts | Capture keyring package/version and verification result, never private key material |
| Sync databases | Provide the package universe used by dependency resolution | Hash the exact database bytes and record repository/mirror provenance |
| Package cache | Retains previously fetched package archives locally | Inventory cached bytes separately from enabled repositories |
| Hooks | Run configured pre/post-transaction actions | Capture hook definitions and execution outcome as version-qualified operational evidence |
| Local database | Records installed-package state and ownership metadata | Snapshot before/after a controlled transaction; do not infer payload behavior |

## Trust and Recovery Rules

1. Repository authority, mirror transport, signature verification, and package
   payload integrity are distinct claims requiring distinct evidence.
2. A refresh may update only a staging snapshot. Promote it only after hashes,
   schema validation, and generation checks pass; preserve the prior projection
   on failure.
3. Record package cache retention and cleanup policy before relying on an
   archive for rollback or binary analysis.
4. Model hooks as executable policy with their own provenance and failure
   handling; a completed transaction does not by itself prove every hook's
   intended effect.
5. Repair, keyring reset, and rollback steps must remain version- and
   environment-qualified procedures, not generic assertions in the graph.

## Diagnostic Sequence

1. Capture effective repository and mirror configuration.
2. Identify the retrieved sync database and package archive bytes.
3. Record the signature/keyring verification outcome.
4. Observe local database, cache, and hooks before and after a controlled
   transaction.

## Controlled local signature verification

On 2026-07-31, the "Keyring and signatures" row's "verification result"
collection rule was exercised directly, independent of a pacman
installation (none is available in the current authoring environment):
`mingw-w64-ucrt-x86_64-zstd-1.5.7-2-any.pkg.tar.zst` and its detached
`.sig` file were downloaded from the official mirror
(`https://mirror.msys2.org/mingw/ucrt64/`), and `gpg --verify` against
that pair reported `gpg: Signature made ... using RSA key
5F944B027F7FE2091985AA2EFA11531AA0AA7F57` and `gpg: Good signature from
"Christoph Reiter (MSYS2 development key) <reiter.christoph@gmail.com>"`
after fetching that key ID from `hkps://keyserver.ubuntu.com`.

This is genuine cryptographic verification that the archive's bytes
match a signature made by a real, named MSYS2 packager's private key —
not a simulation or a documentation-only claim. It is explicitly
**not** the same trust chain pacman itself uses: `gpg` reported
`WARNING: This key is not certified with a trusted signature! There is
no indication that the signature belongs to the owner`, because the key
was fetched ad hoc from a public keyserver rather than through pacman's
own `msys2-keyring` package and its local trust database. This
establishes archive-signature validity for one package/version against
one keyserver-sourced key on one date; it does not establish pacman's
own keyring-trust chain, key provenance beyond the keyserver's own
claims, or signature verification for any other package.

## Related Views

- [Pacman architecture and transaction model](PACMAN-ARCHITECTURE.md)
- [Deep inventory evidence contract](DEEP-INVENTORY-CONTRACT.md)
- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
