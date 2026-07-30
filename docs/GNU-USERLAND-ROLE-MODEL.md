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
evidence_refs:
  - evidence:gnu:bash-manual-2026-07-30
  - evidence:gnu:coreutils-manual-2026-07-30
last_verified: 2026-07-30
---

# GNU Userland Role Model

The [Level 7 userland and applications view](../diagrams/level-7-userland-applications.svg)
connects this role model to shell, package, runtime, and Git for Windows paths.

| Component family | Role | Boundary | Per-tool page |
| --- | --- | --- | --- |
| Bash and shell startup | Command interpretation, environment/profile processing, script execution | Profile behavior is shell configuration, not global MSYS2 policy | [GNU Bash](GNU-BASH.md) |
| Coreutils, grep, sed, awk, find | POSIX-oriented command-line operations | Output and path behavior depend on active runtime/environment context | [GNU Coreutils](GNU-COREUTILS.md) (grep/sed/awk/find pages not yet written) |
| Archive/compression tools | Package and developer workflow support | Archive contents require artifact evidence for ownership claims | Not yet written |
| Editors, pagers, terminals | Interactive development and operations | Terminal/PTY behavior crosses into runtime and Windows-console layers | Not yet written |
| SSH, curl, Git-adjacent tools | Network and source-control workflows | Transport/security details belong to dedicated architecture views | Not yet written |

[GNU Bash](GNU-BASH.md) and [GNU Coreutils](GNU-COREUTILS.md) are the first
per-tool pages for this volume: each covers architectural classification,
responsibilities, boundaries, dependencies, configuration, initialization and
execution flow, runtime behavior, compatibility, security considerations,
failure modes, and evidence for its component, backed by the official GNU
manuals and the pacman catalog snapshot. The remaining component families in
the table above are still represented only at the shallow role-table level
and remain open work for this volume.

## Startup and Configuration

MSYS shell startup selects an environment and processes shell configuration.
Native programs launched from that shell may inherit variables but do not
thereby become MSYS-runtime-dependent. Capture effective startup files and
environment variables as controlled observations when diagnosing behavior.

## Related Views

- [MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [Runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
