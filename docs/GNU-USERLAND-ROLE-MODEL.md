---
id: doc:volume-5:gnu-userland-role-model
title: GNU Userland Role Model
volume: 5
status: partial
model_refs:
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
  - component:gnu:bash
  - component:gnu:coreutils
  - component:gnu:grep
  - component:gnu:sed
  - component:gnu:gawk
  - component:gnu:findutils
  - component:gnu:tar
  - component:gnu:gzip
  - component:bzip2:bzip2
  - component:tukaani:xz
  - component:zstd:zstd
  - component:info-zip:zip
  - component:info-zip:unzip
  - component:p7zip:p7zip
  - component:lzip:lzip
  - component:gnu:cpio
  - component:lz4:lz4
  - component:gnu:ed
  - component:gnu:emacs
  - component:greenwood:less
  - component:mintty:mintty
  - component:gnu:nano
  - component:gnu:ncurses
  - component:vim:vim
evidence_refs:
  - evidence:gnu:bash-manual-2026-07-30
  - evidence:gnu:coreutils-manual-2026-07-30
  - evidence:gnu:grep-manual-2026-07-30
  - evidence:gnu:sed-manual-2026-07-30
  - evidence:gnu:gawk-manual-2026-07-30
  - evidence:gnu:findutils-manual-2026-07-30
  - evidence:gnu:tar-manual-2026-07-30
  - evidence:gnu:gzip-manual-2026-07-30
  - evidence:bzip2:project-site-2026-07-30
  - evidence:tukaani:xz-project-site-2026-07-30
  - evidence:zstd:project-site-2026-07-30
  - evidence:info-zip:zip-manual-2026-07-30
  - evidence:info-zip:unzip-manual-2026-07-30
  - evidence:p7zip:project-site-2026-07-30
  - evidence:lzip:manual-2026-07-30
  - evidence:gnu:cpio-manual-2026-07-30
  - evidence:lz4:manual-2026-07-30
  - evidence:gnu:ed-manual-2026-07-30
  - evidence:gnu:emacs-manual-2026-07-30
  - evidence:less:project-site-2026-07-30
  - evidence:mintty:project-site-2026-07-30
  - evidence:gnu:nano-manual-2026-07-30
  - evidence:gnu:ncurses-manual-2026-07-30
  - evidence:vim:documentation-2026-07-30
last_verified: 2026-07-30
---

# GNU Userland Role Model

The [Level 7 userland and applications view](../diagrams/level-7-userland-applications.svg)
connects this role model to shell, package, runtime, and Git for Windows paths.

| Component family | Role | Boundary | Per-tool page |
| --- | --- | --- | --- |
| Bash and shell startup | Command interpretation, environment/profile processing, script execution | Profile behavior is shell configuration, not global MSYS2 policy | [GNU Bash](GNU-BASH.md) |
| Coreutils, grep, sed, awk, find | POSIX-oriented command-line operations | Output and path behavior depend on active runtime/environment context | [GNU Coreutils](GNU-COREUTILS.md), [GNU Grep](GNU-GREP.md), [GNU Sed](GNU-SED.md), [GNU Awk (gawk)](GNU-AWK.md), [GNU Findutils](GNU-FINDUTILS.md) |
| Archive/compression tools | Package and developer workflow support | Archive contents require artifact evidence for ownership claims; not every tool in this family is a GNU project | [GNU Tar](GNU-TAR.md), [GNU Gzip](GNU-GZIP.md), [bzip2](BZIP2.md), [XZ Utils](XZ-UTILS.md), [Zstandard (zstd)](ZSTD.md), [Info-ZIP Zip](INFO-ZIP-ZIP.md), [Info-ZIP UnZip](INFO-ZIP-UNZIP.md), [p7zip](P7ZIP.md), [Lzip](LZIP.md), [GNU Cpio](GNU-CPIO.md), [LZ4](LZ4.md) |
| Editors, pagers, terminals | Interactive development and operations | Terminal/PTY behavior crosses into runtime and Windows-console layers; ncurses is the shared library underlying most of this family | [GNU Ed](GNU-ED.md), [GNU Nano](GNU-NANO.md), [Vim](VIM.md), [GNU Emacs](GNU-EMACS.md), [less](LESS.md), [mintty](MINTTY.md), [ncurses](NCURSES.md) |
| SSH, curl, Git-adjacent tools | Network and source-control workflows | Transport/security details belong to dedicated architecture views | Not yet written |

[GNU Bash](GNU-BASH.md), [GNU Coreutils](GNU-COREUTILS.md),
[GNU Grep](GNU-GREP.md), [GNU Sed](GNU-SED.md), [GNU Awk (gawk)](GNU-AWK.md),
[GNU Findutils](GNU-FINDUTILS.md), [GNU Tar](GNU-TAR.md),
[GNU Gzip](GNU-GZIP.md), [bzip2](BZIP2.md), [XZ Utils](XZ-UTILS.md),
[Zstandard (zstd)](ZSTD.md), [Info-ZIP Zip](INFO-ZIP-ZIP.md),
[Info-ZIP UnZip](INFO-ZIP-UNZIP.md), [p7zip](P7ZIP.md), [Lzip](LZIP.md),
[GNU Cpio](GNU-CPIO.md), [LZ4](LZ4.md), [GNU Ed](GNU-ED.md),
[GNU Nano](GNU-NANO.md), [Vim](VIM.md), [GNU Emacs](GNU-EMACS.md),
[less](LESS.md), [mintty](MINTTY.md), and [ncurses](NCURSES.md) are the
per-tool pages written so far for this volume: each covers architectural
classification, responsibilities, boundaries, dependencies, configuration,
initialization and execution flow, runtime behavior, compatibility,
security considerations, failure modes, and evidence for its component,
backed by official upstream documentation and the pacman catalog snapshot.
Bzip2, XZ Utils, Zstandard, Info-ZIP Zip/UnZip, p7zip, Lzip, LZ4, less,
mintty, and Vim are documented as non-GNU projects despite sitting in this
GNU-userland volume's role-based families — the families group by role, not
by upstream; only Bash, Coreutils, Grep, Sed, Awk, Findutils, Tar, Gzip,
Cpio, Ed, Nano, Emacs, and ncurses (GNU-hosted, though MIT-licensed rather
than GPL) are GNU-attributed. This completes every archive/compression tool
and every editor/pager/terminal tool identified for this volume. The
remaining component family (SSH/curl/Git-adjacent tools) is still
represented only at the shallow role-table level and remains open work for
this volume.

## Startup and Configuration

MSYS shell startup selects an environment and processes shell configuration.
Native programs launched from that shell may inherit variables but do not
thereby become MSYS-runtime-dependent. Capture effective startup files and
environment variables as controlled observations when diagnosing behavior.

## Related Views

- [MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [Runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
