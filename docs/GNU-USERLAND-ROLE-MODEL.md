---
id: doc:volume-5:gnu-userland-role-model
title: GNU Userland Role Model
volume: 5
status: partial
model_refs:
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs: []
last_verified: 2026-07-28
---

# GNU Userland Role Model

| Component family | Role | Boundary |
| --- | --- | --- |
| Bash and shell startup | Command interpretation, environment/profile processing, script execution | Profile behavior is shell configuration, not global MSYS2 policy |
| Coreutils, grep, sed, awk, find | POSIX-oriented command-line operations | Output and path behavior depend on active runtime/environment context |
| Archive/compression tools | Package and developer workflow support | Archive contents require artifact evidence for ownership claims |
| Editors, pagers, terminals | Interactive development and operations | Terminal/PTY behavior crosses into runtime and Windows-console layers |
| SSH, curl, Git-adjacent tools | Network and source-control workflows | Transport/security details belong to dedicated architecture views |

## Startup and Configuration

MSYS shell startup selects an environment and processes shell configuration.
Native programs launched from that shell may inherit variables but do not
thereby become MSYS-runtime-dependent. Capture effective startup files and
environment variables as controlled observations when diagnosing behavior.

## Related Views

- [MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [Runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
