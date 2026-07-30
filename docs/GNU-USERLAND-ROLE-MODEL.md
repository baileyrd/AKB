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
last_verified: 2026-07-30
---

# GNU Userland Role Model

The [Level 7 userland and applications view](../diagrams/level-7-userland-applications.svg)
connects this role model to shell, package, runtime, and Git for Windows paths.

| Component family | Role | Boundary | Per-tool page |
| --- | --- | --- | --- |
| Bash and shell startup | Command interpretation, environment/profile processing, script execution | Profile behavior is shell configuration, not global MSYS2 policy | [GNU Bash](GNU-BASH.md) |
| Coreutils, grep, sed, awk, find | POSIX-oriented command-line operations | Output and path behavior depend on active runtime/environment context | [GNU Coreutils](GNU-COREUTILS.md), [GNU Grep](GNU-GREP.md), [GNU Sed](GNU-SED.md), [GNU Awk (gawk)](GNU-AWK.md), [GNU Findutils](GNU-FINDUTILS.md) |
| Archive/compression tools | Package and developer workflow support | Archive contents require artifact evidence for ownership claims; not every tool in this family is a GNU project | [GNU Tar](GNU-TAR.md), [GNU Gzip](GNU-GZIP.md), [bzip2](BZIP2.md), [XZ Utils](XZ-UTILS.md) (zstd, zip/unzip, p7zip, lzip, cpio, lz4 pages not yet written) |
| Editors, pagers, terminals | Interactive development and operations | Terminal/PTY behavior crosses into runtime and Windows-console layers | Not yet written |
| SSH, curl, Git-adjacent tools | Network and source-control workflows | Transport/security details belong to dedicated architecture views | Not yet written |

[GNU Bash](GNU-BASH.md), [GNU Coreutils](GNU-COREUTILS.md),
[GNU Grep](GNU-GREP.md), [GNU Sed](GNU-SED.md), [GNU Awk (gawk)](GNU-AWK.md),
[GNU Findutils](GNU-FINDUTILS.md), [GNU Tar](GNU-TAR.md),
[GNU Gzip](GNU-GZIP.md), [bzip2](BZIP2.md), and [XZ Utils](XZ-UTILS.md) are
the per-tool pages written so far for this volume: each covers architectural
classification, responsibilities, boundaries, dependencies, configuration,
initialization and execution flow, runtime behavior, compatibility, security
considerations, failure modes, and evidence for its component, backed by
official upstream documentation and the pacman catalog snapshot. Bzip2 and
XZ Utils are documented as non-GNU projects despite sitting in this
GNU-userland volume's "Archive/compression tools" family — the family
groups by role, not by upstream. The remaining component families and
archive tools in the table above are still represented only at the shallow
role-table level and remain open work for this volume.

## Startup and Configuration

MSYS shell startup selects an environment and processes shell configuration.
Native programs launched from that shell may inherit variables but do not
thereby become MSYS-runtime-dependent. Capture effective startup files and
environment variables as controlled observations when diagnosing behavior.

## Related Views

- [MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [Runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
