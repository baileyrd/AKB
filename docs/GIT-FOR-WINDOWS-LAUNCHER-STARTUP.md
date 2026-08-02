---
id: doc:volume-9:git-for-windows-launcher-startup
title: Git for Windows Launcher and Shell Startup Model
volume: 9
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Git for Windows Launcher and Shell Startup Model

```mermaid
flowchart LR
    A["Start-menu shortcut or terminal invocation"] --> B["Git for Windows launcher"]
    B --> C["Terminal host — mintty"]
    B --> D["Bash process and environment"]
    D --> E["Shell startup files"]
    D --> F["Git and supporting executables"]
```

| Component | Responsibility | Boundary |
| --- | --- | --- |
| Launcher | Selects executable, arguments, working directory, and initial environment | Installation-specific launch details require observed evidence |
| Terminal host | Provides interactive terminal/session behavior | Console/PTY integration is distinct from Git process behavior. The terminal host is [mintty](MINTTY.md); PTY behavior is documented on [PTY and console](MSYS-PTY-AND-CONSOLE.md) |
| Bash | Interprets commands and processes startup configuration | Shell profiles are user/site configuration, not package metadata |
| Git executable | Performs Git operations and invokes configured helpers | Transport, credentials, SSH, and DLL loading are separate domains |

## Diagnostic Rules

Capture the actual launcher command, environment, startup files, terminal host,
and resolved executable path before attributing a failure to Git Bash. A native
Git invocation outside Git Bash may follow different startup and DLL-resolution
paths.

## Related Views

- [Git for Windows boundary](GIT-FOR-WINDOWS-BOUNDARY.md)
- [Git Bash and MSYS interaction](GIT-FOR-WINDOWS-GIT-BASH.md)
- [DLL loading](GIT-FOR-WINDOWS-DLL-LOADING.md)
- [mintty](MINTTY.md)
- [GNU userland role model](GNU-USERLAND-ROLE-MODEL.md)
