---
id: doc:volume-6:libksba
title: libksba
volume: 6
status: partial
model_refs:
  - library:gnupg:libksba
  - package:msys2:mingw-w64-ucrt-x86_64-libksba
  - library:gnupg:libgpg-error
  - library:gnupg:libksba@msys
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnupg:libksba-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# libksba

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnupg:libksba` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | GnuPG project |
| Environments | `ucrt64` |
| Upstream | <https://www.gnupg.org/related_software/libksba/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-libksba` |
| Version (observed) | 1.6.8-1 |
| License (observed) | GPL |
| Architecture (observed) | any |
| Installed size (observed) | 820.87 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:gnupg:libksba-manual-2026-07-30` — libksba (official project page) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Libksba is a CMS and X.509 certificate access library, used to back
GnuPG's S/MIME support (`gpgsm`) despite GnuPG's primary focus being
OpenPGP. This page documents the **UCRT64**-packaged build specifically;
the MSYS-packaged `package:msys2:gnupg` component GnuPG.md documents
actually depends on a separately versioned MSYS sibling package,
corrected 2026-07-30 and documented on
[libksba (MSYS)](LIBKSBA-MSYS.md) — this page no longer claims a direct
GnuPG dependency for that reason. See the
[official libksba project page](https://www.gnupg.org/related_software/libksba/)
for the API reference shared by both packages.

## Architectural Classification

`library:gnupg:libksba` is packaged per native environment: this page
cites the UCRT64 build, `package:msys2:mingw-w64-ucrt-x86_64-libksba`
(version `1.6.8-1` in the current catalog snapshot, license `GPL`).

## Responsibilities

- Parsing and generating CMS (Cryptographic Message Syntax) and X.509
  certificate structures, the data formats GnuPG's `gpgsm` component uses
  for S/MIME email encryption and signing, a materially different trust
  model from OpenPGP's web-of-trust.

## Boundaries

Libksba handles CMS/X.509 data structures; it does not perform the
underlying cryptographic operations on that data — that remains
[libgcrypt](LIBGCRYPT.md)'s role. Libksba is also distinct from
[libxml2](LIBXML2.md) and [Expat](EXPAT.md) in this volume: it parses
ASN.1-based binary certificate formats, not XML.

## Interfaces

- A C API for parsing and constructing X.509 certificates and CMS
  messages (`ksba_cert_new`, `ksba_cms_new`), per the documentation.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-libksba`:
`mingw-w64-ucrt-x86_64-libgpg-error`, the shared error-code vocabulary
documented fully in [libgpg-error](LIBGPG-ERROR.md).

## Reverse Dependencies

The snapshot records 1 relationship targeting
`package:msys2:mingw-w64-ucrt-x86_64-libksba` (its own `-devel`
subpackage). [GnuPG](GNUPG.md) is **not** among them — that was a
pre-2026-07-30 modeling error, corrected in favor of
[libksba (MSYS)](LIBKSBA-MSYS.md#reverse-dependencies), which GnuPG's own
MSYS-packaged catalog dependency actually targets. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list of this UCRT64 package's actual dependents.

## Configuration

Libksba has no persistent configuration file; it is a parsing/generation
library configured entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, libksba has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it. [GnuPG's](GNUPG.md) own `gpgsm` component links against
[libksba (MSYS)](LIBKSBA-MSYS.md) instead of this UCRT64 package.

## Runtime Behavior

Libksba is exercised only when S/MIME functionality in a program linking
against this UCRT64 build is actually used; a purely OpenPGP-based
workflow does not meaningfully exercise this dependency despite it being
installed.

## Compatibility and Variants

Libksba implements CMS/X.509 per the relevant IETF/ITU-T standards; this
page does not enumerate specific standard-conformance details, deferring
to the project's own documentation.

## Security Considerations

Parsing untrusted X.509 certificates and CMS messages is a documented
general risk class for certificate-parsing libraries (malformed ASN.1
structures triggering parser defects); this is directly relevant given
libksba's role processing externally supplied certificates. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.6.8-1` version.

## Failure Modes and Diagnostics

Libksba itself has no user-facing CLI; S/MIME-related failures should be
checked against certificate validity and format before being treated as
a libksba defect.

## Evidence, Assumptions, and Open Questions

The CMS/X.509 parsing role is backed by the official libksba project page
(`evidence:gnupg:libksba-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:mingw-w64-ucrt-x86_64-libksba` in the
catalog. Package identity, version, license, and the dependency edge are
backed by the pacman catalog snapshot (`evidence:catalog:current`).
Correction (2026-07-30): this page previously claimed a direct
`component:gnupg:gnupg` dependency and cited
`relationship:ssh-curl-git:gnupg-requires-libksba` as evidence; that
relationship's target has since been corrected to
[libksba (MSYS)](LIBKSBA-MSYS.md), since `package:msys2:gnupg` is an
MSYS-environment package and this page's UCRT64 package was never its
actual catalog-recorded dependency. Open, and explicitly out of scope for
this page: header-level API surface and PE import/export-level evidence,
per the [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["libksba"]
    d0["libgpg-error"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnupg:libksba` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [libgpg-error](LIBGPG-ERROR.md)
- [libksba (MSYS)](LIBKSBA-MSYS.md)
- [libksba (CLANG64)](LIBKSBA-CLANG64.md)
