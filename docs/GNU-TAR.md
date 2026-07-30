---
id: doc:volume-5:gnu-tar
title: GNU Tar
volume: 5
status: partial
model_refs:
  - component:gnu:tar
  - package:msys2:tar
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:tar-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Tar

## Purpose

Tar stores a tree of files, with their metadata, as a single archive stream.
This page documents its architectural role, its composition with separate
compression tools, and its metadata-preservation and extraction-safety
behavior; see the
[official GNU Tar manual](https://www.gnu.org/software/tar/manual/tar.html)
for the full option and format reference.

## Architectural Classification

`component:gnu:tar` is a GNU-userland component packaged as
`package:msys2:tar` (version `1.35-3` in the current catalog snapshot,
license `GPL3`), belonging to the MSYS environment. Tar is an archiving
tool, not a compression tool: the ubiquitous `.tar.gz`/`.tar.bz2`/`.tar.xz`
formats are tar's archive stream piped through a separate single-file
compressor, not a single unified format.

## Responsibilities

- Serializing a directory tree — including permissions, ownership,
  timestamps, symlinks, and sparse-file layout, where supported — into one
  archive stream, and reversing that process on extraction.
- Streaming to and from stdin/stdout, enabling pipelines with
  [GNU Gzip](GNU-GZIP.md), [bzip2](BZIP2.md), or [XZ Utils](XZ-UTILS.md)
  without an intermediate archive file.

## Boundaries

Tar does not itself compress data beyond invoking a paired compressor via
`-z`/`-j`/`-J`/`--zstd` or the general `--use-compress-program`. It also does
not resolve which specific compressor package is installed; that is a
package-dependency concern, addressed below.

## Interfaces

- Mode selection: `-c` (create), `-x` (extract), `-t` (list).
- Compression-filter selection: `-z` (gzip), `-j` (bzip2), `-J` (xz),
  `--zstd`, or an arbitrary external filter via `--use-compress-program`;
  `-a`/`--auto-compress` selects a filter from the archive's file extension.
- `-g` (incremental archives) and `-M` (multi-volume archives) for backup
  workflows, per the manual.

## Dependencies

The catalog snapshot records two `runtime-depends-on` edges for
`package:msys2:tar`: `package:msys2:libiconv` and `package:msys2:libintl`,
matching the same character-set-conversion and NLS rationale documented for
[GNU Coreutils](GNU-COREUTILS.md). Notably, no dependency edge is recorded
against `zlib`, `libbz2`, or `liblzma` — the codec libraries behind `-z`,
`-j`, and `-J`. This is consistent with this build of tar invoking the
external `gzip`/`bzip2`/`xz` programs as separate processes for those
filters rather than linking the codecs in directly, but it could also
reflect a limitation of this metadata-only extraction; PE import analysis
against the installed binary would be needed to distinguish the two and is
open work. Tar's declared dependencies also list `sh`, a virtual capability
provided by `package:msys2:bash` rather than an actual package name; it is
retained in `generated/unresolved-dependencies.json` rather than asserted as
a relationship, per the same explanation given for
[GNU Grep](GNU-GREP.md#dependencies).

## Reverse Dependencies

The snapshot records 3 relationships targeting `package:msys2:tar`. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Tar has no persistent configuration file. Command-line flags control
behavior per invocation; the historical `TAPE` environment variable sets a
default archive device, per the manual.

## Initialization and Execution Flow

Tar is an invoke-run-exit process. When a compression filter is requested
and not linked in directly (see Dependencies), tar forks and execs the
corresponding external compressor as a child process — an MSYS-runtime
process-creation event adapted by `msys-2.0.dll`, per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md); this page
does not restate that mechanism.

## Runtime Behavior

Metadata preservation (permissions, ownership, timestamps, symlinks) during
extraction is subject to the underlying filesystem's support for those
concepts. On this environment's MSYS/NTFS boundary, symlink handling is
directly affected by the same discrepancy already flagged in the
[MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md#controlled-local-observation):
`ln -s` succeeded and the target was readable, but `test -L` returned
non-zero. That discrepancy is relevant to tar's symlink-archiving and
extraction fidelity in this environment and is not re-derived here.

## Compatibility and Variants

GNU tar's default output uses GNU-specific format extensions unless
`--format=pax` or `--format=ustar` is specified; archives intended for
strict POSIX or BSD `tar` (`bsdtar`/libarchive) compatibility should pin an
explicit `--format`, per the manual's format-compatibility notes.

## Security Considerations

The manual documents that GNU tar strips leading `/` from archive member
names and refuses to extract absolute paths or `..`-traversal entries
outside the extraction directory unless `-P`/`--absolute-names` is given —
a default protection against path-traversal and symlink-redirection attacks
from untrusted archives. Piping an untrusted archive through `-z`/`-j`/`-J`
also inherits the general decompression-bomb risk of the paired compressor;
see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for
the project's general supply-chain posture.

## Failure Modes and Diagnostics

Extracting an archive with the wrong or no compression flag (for example,
`tar -xf archive.tar.xz` without `-J` or `-a`) is a common usage error; the
`-a`/`--auto-compress` flag's extension-based detection is the documented
mitigation. Metadata-preservation surprises (permissions, symlinks) on this
environment should first be checked against the runtime behavior map
discrepancy noted above before being treated as a tar-specific defect.

## Evidence, Assumptions, and Open Questions

Archive format, filter selection, and extraction-safety defaults are backed
by the official GNU Tar manual (`evidence:gnu:tar-manual-2026-07-30`).
Package identity, version, license, and dependency edges are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open: whether this
build links compression codecs directly or forks external programs is
unconfirmed pending PE import analysis, and the symlink-fidelity discrepancy
already flagged in the runtime behavior map remains open.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Gzip](GNU-GZIP.md)
- [bzip2](BZIP2.md)
- [XZ Utils](XZ-UTILS.md)
- [MSYS Runtime Behavior Map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
- [MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md)
