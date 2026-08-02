---
id: doc:volume-6:libarchive
title: libarchive
volume: 6
status: partial
model_refs:
  - library:libarchive:libarchive
  - package:msys2:mingw-w64-ucrt-x86_64-libarchive
  - component:cmake:cmake
  - library:libexpat:expat
  - library:gnu:libiconv
  - library:pcre:pcre2
  - library:gnu:zlib
  - library:facebook:zstd
  - library:tukaani:liblzma
  - library:openssl:openssl@ucrt64
  - library:bzip2:bzip2@ucrt64
  - library:lz4:lz4@ucrt64
  - library:blake2:libb2@ucrt64
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:libarchive:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# libarchive

## Purpose

libarchive is a multi-format archive and compression library, providing
a single API for reading and writing many archive formats (tar, zip, cpio,
and others) and compression filters rather than requiring a separate
implementation per format. This page documents its architectural role as
a directly-declared dependency of [CMake](CMAKE.md); see the
[official libarchive project site](https://www.libarchive.org/) for the
full API reference.

## Architectural Classification

`library:libarchive:libarchive` is packaged per native environment: this
page cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-libarchive` (version `3.8.8-2` in
the current catalog snapshot). It belongs to the UCRT64 environment and,
like [CMake](CMAKE.md#architectural-classification) itself and the rest
of Volume 8's toolchain components, does not depend on `msys-2.0.dll`,
per the [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).
This is a materially different tool from the individually documented
per-format archive/compression tools in Volume 5 ([GNU Tar](GNU-TAR.md),
[Info-ZIP Zip](INFO-ZIP-ZIP.md), [p7zip](P7ZIP.md), and others): those
are MSYS-environment command-line programs, each implementing (or
wrapping) a single archive format, while libarchive is a native UCRT64
library offering one API across many formats, consumed by other programs
such as CMake rather than invoked directly by end users in this
environment.

## Responsibilities

- Reading and writing multiple archive formats and compression filters
  through a single library API, consumed by [CMake](CMAKE.md)'s
  `file(ARCHIVE_CREATE)`/`file(ARCHIVE_EXTRACT)` commands and by CPack's
  archive-format packaging generator.

## Boundaries

libarchive provides archive/compression format handling as a library API
specifically; it is architecturally distinct from the individually
invoked archive/compression command-line tools documented in Volume 5
(see Architectural Classification) — those tools may themselves use
libarchive internally in other packaging ecosystems, but no such
relationship is recorded in this knowledge base's graph for the
MSYS-environment tools this page cross-references. libarchive already
appeared by package name in
[CMake's dependency table](CMAKE.md#dependencies) before this page
existed.

## Interfaces

- A C API (`archive_read_*`, `archive_write_*` function families) for
  format-agnostic archive reading and writing, per the documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-libarchive` declares
dependencies on ten packages. Seven are the same UCRT64-packaged
sibling libraries this knowledge base already documents, so this page
adds explicit `requires` edges for them: [Expat](EXPAT.md) (XML-format
handling for archive formats such as PAX/tar extended headers that embed
XML metadata), [GNU libiconv](GNU-LIBICONV.md) (character-set conversion
for archive entry filenames and metadata), [PCRE2](PCRE2.md)
(regular-expression matching for archive entry filtering),
[zlib](ZLIB.md) (DEFLATE-based archive formats such as zip and
gzip-compressed tar), [Zstandard (library)](LIBZSTD.md),
[liblzma (UCRT64)](LIBLZMA.md) (`.zst`- and `.xz`/LZMA-compressed
archive formats respectively), and [OpenSSL (UCRT64)](OPENSSL-UCRT64.md)
(cryptographic primitives for encrypted archive formats,
`relationship:toolchain:libarchive-requires-openssl-ucrt64`, added
2026-07-30). **Correction, 2026-07-30**: the zstd/xz/openssl edges were
originally declined here, reasoning that only their MSYS CLI-tool
siblings were modeled at the time; all three now have UCRT64-native
library-entity pages of their own, and the three missing edges
(`relationship:toolchain:libarchive-requires-zstd`,
`relationship:toolchain:libarchive-requires-liblzma`,
`relationship:toolchain:libarchive-requires-openssl-ucrt64`) are added.
Of the remaining three, **correction, 2026-08-02**: all three are now
individually modeled and their edges added — [bzip2 (UCRT64)](BZIP2-UCRT64.md)
(`relationship:foundation-libraries:libarchive-requires-bzip2-ucrt64`,
backing the bzip2 compression filter within libarchive's supported
archive formats), [LZ4 (UCRT64)](LZ4-UCRT64.md)
(`relationship:foundation-libraries:libarchive-requires-lz4-ucrt64`,
backing the LZ4 compression filter), and
[BLAKE2 (libb2) (UCRT64)](LIBB2-UCRT64.md)
(`relationship:foundation-libraries:libarchive-requires-libb2-ucrt64`,
backing BLAKE2-based checksum support) — reaching full 10/10 catalog
dependency coverage for this UCRT64 package.

## Reverse Dependencies

The catalog snapshot records 22 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-libarchive`, the widest
reverse-dependency footprint of any library added in this batch:
`package:msys2:mingw-w64-ucrt-x86_64-cmake`
(`relationship:toolchain:cmake-requires-libarchive` in this knowledge
base's graph), along with numerous unrelated UCRT64 GUI/desktop
applications (`akira`, `ark`, `evince`, `gimp`, and others) not
individually enumerated here, reflecting libarchive's role as a
broadly-used general-purpose archive library well beyond the
build-tooling context this page focuses on; see the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

libarchive has no persistent configuration file of its own; format and
filter selection are controlled entirely through its C API by the calling
program.

## Initialization and Execution Flow

As a library, libarchive has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [CMake](CMAKE.md) in this dependency chain, specifically
when `file(ARCHIVE_CREATE)`/`file(ARCHIVE_EXTRACT)` or CPack's archive
generators are used. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Which archive format and compression filter a given libarchive-backed
operation actually uses depends on the calling program's own choice
(explicit format selection or format auto-detection on read), not a
single fixed format across every consumer.

## Compatibility and Variants

Whether other native environments (CLANG64, i686) in this catalog package
libarchive separately was not confirmed while writing this page; this is
recorded as an open item rather than assumed either way.

## Security Considerations

Archive extraction from untrusted sources is a documented class of
security concern generally (path traversal via crafted archive entry
names, decompression-bomb resource exhaustion); this page does not assert
this specific package version's mitigation status for either. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `3.8.8-2` version.

## Failure Modes and Diagnostics

An archive-format-specific extraction or creation failure in
`file(ARCHIVE_CREATE)`/`file(ARCHIVE_EXTRACT)` or CPack should be checked
against libarchive's own format support for the target archive type
before being treated as a CMake defect.

## Evidence, Assumptions, and Open Questions

Multi-format archive handling scope is backed by the official libarchive
project site (`evidence:libarchive:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-libarchive` in the catalog. Package
identity, version, and the recorded dependency/dependent edges are backed
by the pacman catalog snapshot (`evidence:catalog:current`). **Update,
2026-08-02**: the MSYS environment does package libarchive separately —
see [libarchive (MSYS)](LIBARCHIVE-MSYS.md), a distinct catalog entity
now modeled in this knowledge base with its own, wider dependency set.
Also explicitly out of scope for this page: the six
UCRT64-native compression/crypto sub-dependencies not individually
modeled as separate components in this knowledge base, and header-level
API surface plus PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [CMake](CMAKE.md)
- [libarchive (MSYS)](LIBARCHIVE-MSYS.md)
- [libarchive (CLANG64)](LIBARCHIVE-CLANG64.md)
- [Expat](EXPAT.md)
- [GNU libiconv](GNU-LIBICONV.md)
- [PCRE2](PCRE2.md)
- [zlib](ZLIB.md)
- [Zstandard (library)](LIBZSTD.md)
- [liblzma (UCRT64)](LIBLZMA.md)
- [OpenSSL (UCRT64)](OPENSSL-UCRT64.md)
- [bzip2 (UCRT64)](BZIP2-UCRT64.md)
- [LZ4 (UCRT64)](LZ4-UCRT64.md)
- [BLAKE2 (libb2) (UCRT64)](LIBB2-UCRT64.md)
