---
id: doc:volume-5:gnupg
title: GnuPG
volume: 5
status: partial
model_refs:
  - component:gnupg:gnupg
  - package:msys2:gnupg
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnupg:project-site-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GnuPG

## Purpose

GnuPG implements the OpenPGP standard for encryption, decryption, and
digital signing. This page documents its architectural role and its
deliberately independent cryptographic dependency stack; see the
[official GnuPG project site](https://gnupg.org/) for the full command
reference.

## Architectural Classification

`component:gnupg:gnupg` is packaged as `package:msys2:gnupg` (version
`2.4.9-1` in the current catalog snapshot, license `GPL`), authored by
Werner Koch and the GnuPG project. It belongs to the MSYS environment.
Despite sitting in the same "SSH, curl, Git-adjacent tools" family as
[OpenSSL](OPENSSL.md), GnuPG notably does **not** depend on OpenSSL in this
snapshot (see Dependencies) — a deliberate architectural separation between
the OpenPGP and TLS/X.509 cryptographic ecosystems.

## Responsibilities

- OpenPGP encryption, decryption, digital signing, and signature
  verification, plus key management (generation, import/export, the
  `dirmngr` component it also provides for key-server/OCSP network
  lookups).

## Boundaries

GnuPG implements the OpenPGP standard specifically, distinct from the X.509
certificate model [OpenSSL](OPENSSL.md) and [curl](CURL.md#dependencies)
use for TLS; the two are not interchangeable trust models despite both
appearing in this "security tools" grouping.

## Interfaces

- `gpg`/`gpg2` (core operations: `--encrypt`, `--decrypt`, `--sign`,
  `--verify`, key management), `dirmngr` (network key/certificate lookups,
  provided by this same package), per the project documentation.

## Dependencies

The catalog snapshot records fourteen `runtime-depends-on` edges for
`package:msys2:gnupg` — the widest dependency footprint of any component
documented in this volume, spanning its own independent cryptographic
stack plus archive, terminal, and database libraries:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Symmetric/public-key cryptography | `package:msys2:libgcrypt` | GnuPG's primary low-level cryptographic library, independent of OpenSSL's. |
| Low-level crypto primitives | `package:msys2:nettle` | Backs additional cryptographic primitives, the same Nettle library documented as a GnuTLS dependency for [GNU Emacs](GNU-EMACS.md#dependencies). |
| GnuPG error codes | `package:msys2:libgpg-error` | Shared error-code definitions used across the GnuPG project's own library stack. |
| IPC between GnuPG components | `package:msys2:libassuan` | Backs the Assuan IPC protocol GnuPG uses for communication between `gpg`, `dirmngr`, and other GnuPG-family helper processes. |
| Certificate/CMS handling | `package:msys2:libksba` | Backs X.509/CMS certificate parsing, used specifically by GnuPG's S/MIME support (`gpgsm`) despite GnuPG's primary focus being OpenPGP rather than X.509. |
| Threading | `package:msys2:libnpth` | GnuPG's own portable threading library (New/Nth Pth), used internally for concurrent operations. |
| TLS for network lookups | `package:msys2:libgnutls` | Backs `dirmngr`'s TLS-secured connections to key servers and OCSP responders — the network-facing exception to GnuPG's OpenSSL independence. Documented fully in [GnuTLS](GNUTLS.md). |
| HTTP transfer library | `package:msys2:libcurl` | Backs `dirmngr`'s HTTP-based key-server and certificate-revocation lookups. |
| Compression | `package:msys2:bzip2`, `package:msys2:libbz2`, `package:msys2:zlib` | Back compressed OpenPGP packet handling, per the OpenPGP standard's built-in compression support. |
| Character-set conversion | `package:msys2:libiconv` | Portable multibyte/character-set handling, matching the same rationale documented for [GNU Coreutils](GNU-COREUTILS.md). |
| Native-language messages | `package:msys2:libintl` | gettext-based message translation (NLS). |
| Interactive line editing | `package:msys2:libreadline` | Backs interactive prompts in GnuPG's command-line tools. |
| Key/passphrase database | `package:msys2:libsqlite` | Backs GnuPG's key- and trust-database storage. |
| Passphrase entry | `package:msys2:pinentry` | A separate, dedicated program GnuPG launches to securely prompt for passphrases, keeping passphrase entry isolated from the calling terminal/application. |

An optional dependency on `curl` (distinct from the `libcurl` runtime
dependency above) backs the `gpg2keys_curl` key-fetching helper.

## Reverse Dependencies

The snapshot records 4 relationships targeting `package:msys2:gnupg`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

`~/.gnupg/gpg.conf` and the GnuPG home directory (keyrings, trust database)
are a genuine, security-sensitive standing configuration and data store,
similar in sensitivity to [OpenSSH](OPENSSH.md#configuration)'s `~/.ssh`
directory.

## Initialization and Execution Flow

`gpg` is typically an invoke-run-exit process per operation, but may launch
`dirmngr` (for network lookups) and `pinentry` (for passphrase entry) as
separate child processes communicating over the Assuan IPC protocol
(backed by `libassuan`) — a materially more multi-process architecture than
most other tools documented in this volume. All are adapted from POSIX
semantics onto Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Passphrase entry is deliberately routed through the separate `pinentry`
process rather than read directly by `gpg`, a documented design choice
isolating secret entry from the calling context.

## Compatibility and Variants

GnuPG 2.x's split-process architecture (`gpg`, `gpg-agent`, `dirmngr`,
`pinentry` as cooperating processes) is a significant architectural
departure from the older GnuPG 1.x single-process model; scripts or
integrations written against 1.x assumptions may not map directly onto this
recorded `2.4.9-1` version's behavior.

## Security Considerations

GnuPG is itself security-critical infrastructure for encryption, signing,
and trust decisions; its explicit architectural separation of passphrase
entry (`pinentry`) from the main `gpg` process is a deliberate security
boundary. See [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture; no version-qualified CVE
review has been performed for the recorded `2.4.9-1` version.

## Failure Modes and Diagnostics

A passphrase prompt failing to appear (rather than a passphrase being
rejected) is commonly a `pinentry` configuration or terminal-integration
issue rather than a `gpg` defect, given the split-process architecture
described above.

## Evidence, Assumptions, and Open Questions

Command semantics and the split-process architecture are backed by the
official GnuPG project site (`evidence:gnupg:project-site-2026-07-30`),
matching the `project_url` already recorded for `package:msys2:gnupg` in
the catalog. Package identity, version, license, and all recorded
dependency edges are backed by the pacman catalog snapshot
(`evidence:catalog:current`). No open items beyond the general
version-qualified security review noted above.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [OpenSSL](OPENSSL.md)
- [curl](CURL.md)
- [GNU Emacs](GNU-EMACS.md)
- [GnuTLS](GNUTLS.md)
- [libgcrypt](LIBGCRYPT.md)
- [libassuan](LIBASSUAN.md)
- [libksba](LIBKSBA.md)
- [nPth](NPTH.md)
- [Nettle](NETTLE.md)
