---
id: doc:volume-7:pacman-package-signing
title: Pacman Package Signing
volume: 7
status: partial
model_refs:
  - package-manager:archlinux:pacman
  - layer:msys2:5-packages-and-repositories
evidence_refs:
  - evidence:pacman:pacman-8-2026-08-02
  - evidence:pacman:pacman-conf-5-2026-08-02
last_verified: 2026-08-02
---

# Pacman Package Signing

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `package-manager:archlinux:pacman` |
| Kind | `package-manager` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Arch Linux |
| Environments | `msys` |
| Upstream | <https://www.archlinux.org/pacman/> |
| Packaged as | `package:msys2:pacman` |
| Version (observed) | 6.1.0-25 |
| License (observed) | spdx:GPL-2.0-or-later |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 35.4 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:pacman:pacman-8-2026-08-02` — pacman(8) manual page (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Package signing is the mechanism by which pacman decides whether to trust
what a mirror delivered. It is configured by policy level rather than by a
single on/off switch, and the policy can differ per repository.

## Architectural Classification

`pacman.conf(5)` defines `SigLevel`, which sets the default signature
verification level, and `LocalFileSigLevel`, which sets the level for
installing packages from a local file rather than from a repository. Both
are documented under package and database signature checking.

The distinction matters: a `-U` install from a downloaded file is governed
by a different setting than a `-S` install from a repository, so a policy
that looks strict for repository installs may not be for file installs.

## Responsibilities

- Setting the verification level applied to packages and to databases.
- Allowing that level to be overridden per repository section, so
  repositories need not share a trust posture.
- Governing local-file installs separately through `LocalFileSigLevel`.

## Boundaries

Signature verification establishes that content matches a key the
installation trusts. It does not establish that the key should be trusted,
that the repository is authoritative, or that the package payload is
benign — three separate claims the
[trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) requires distinct evidence
for.

Keyring management — which keys are trusted and how they got there — is a
distinct concern from the verification level that consults them.

## Interfaces

`SigLevel` and `LocalFileSigLevel` in `pacman.conf`, at both the global and
per-repository level.

## Dependencies

A keyring supplying trusted keys, and the
[repository configuration](PACMAN-REPOSITORY-LAYOUT.md) that scopes policy
per section.

## Reverse Dependencies

Every [transaction](PACMAN-TRANSACTIONS.md) that installs anything.

## Configuration

Not captured for MSYS2. Which level is set globally, whether any repository
overrides it, and what the local-file level is are all unrecorded here —
which means this knowledge base cannot currently state MSYS2's effective
trust posture at all.

## Initialization and Execution Flow

Policy is read with the rest of the configuration and applied during
verification, before a package is installed.

## Runtime Behavior

Not observed. No controlled MSYS2 transaction with signature verification
has been recorded.

## Compatibility and Variants

Per-repository override means the six MSYS2 repositories may not share a
posture. Whether they do is unrecorded.

## Security Considerations

This is the security-critical page of Volume 7, and it is the one with the
least MSYS2-specific evidence — the configuration that would answer "is this
installation verifying signatures, and against whose keys" has not been
captured. Recorded as a gap rather than assumed favourably. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md).

## Failure Modes and Diagnostics

A signature failure during a transaction is the visible case. The invisible
case matters more: a permissive `SigLevel` produces no error at all, so the
absence of signature failures is not evidence that verification is
happening.

## Evidence, Assumptions, and Open Questions

Mechanism is backed by the pacman manual pages
(`evidence:pacman:pacman-8-2026-08-02`,
`evidence:pacman:pacman-conf-5-2026-08-02`).

The standing caveat for all of Volume 7: those are the **Arch Linux** pages.
MSYS2 ships pacman but places its root, database, and cache under the MSYS2
installation rather than at the Arch defaults, and enables its own six
repositories. Documented behavior establishes the mechanism, not MSYS2's
effective paths or configuration.

Open: no captured MSYS2 `pacman.conf`, no recorded effective path, and no
controlled observation of a transaction. The
[repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) states the
collection rules that would close this; they have not been executed.

## Related Objects

- [Repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md)
- [Repository layout](PACMAN-REPOSITORY-LAYOUT.md)
- [Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
