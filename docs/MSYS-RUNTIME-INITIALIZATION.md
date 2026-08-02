---
id: doc:volume-3:msys-runtime-initialization
title: MSYS Runtime Initialization Model
volume: 3
status: partial
model_refs:
  - runtime:msys2:msys-2.0.dll
  - environment:msys2:msys
evidence_refs: []
last_verified: 2026-07-28
---

# MSYS Runtime Initialization Model

## Purpose

This model describes the observable startup boundary for an MSYS-dependent
program. It distinguishes launcher/shell configuration from runtime DLL
initialization and from later application behavior.

```mermaid
sequenceDiagram
    participant L as Launcher or terminal
    participant E as Environment selection
    participant P as MSYS-dependent process
    participant R as msys-2.0.dll
    participant S as Shell or application
    L->>E: select MSYSTEM and startup options
    E->>P: create Windows process environment
    P->>R: load runtime dependency
    R->>R: initialize POSIX adaptation state
    R->>S: transfer to program entry/startup
```

## Responsibilities and Boundaries

- Launchers establish environment selection; they do not prove a program’s
  runtime dependency.
- `msys-2.0.dll` supplies the MSYS POSIX-compatibility boundary for programs
  that link to it.
- Native environment executables are outside that runtime dependency boundary.
- Shell profile processing is application-level behavior, not a substitute for
  runtime initialization analysis.

## Verification Gaps

Detailed ordering for mount setup, path conversion tables, signal machinery,
fork emulation, and pseudo-terminal setup requires version-qualified runtime
source analysis and controlled observations. Those are tracked as follow-on
runtime-model work rather than inferred here.

## Related Views

- [Ecosystem context](ECOSYSTEM-CONTEXT.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
- [Eight-layer architecture](EIGHT-LAYER-ARCHITECTURE.md)

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["msys-2.0.dll"]
    u0["bzip2"]
    u0 -->|uses-runtime| subject
    u1["curl"]
    u1 -->|uses-runtime| subject
    u2["Git (MSYS2 package)"]
    u2 -->|uses-runtime| subject
    u3["GNU Autoconf"]
    u3 -->|uses-runtime| subject
    u4["GNU Automake"]
    u4 -->|uses-runtime| subject
    u5["GNU Bash"]
    u5 -->|uses-runtime| subject
    u6["GNU Coreutils"]
    u6 -->|uses-runtime| subject
    u7["GNU Cpio"]
    u7 -->|uses-runtime| subject
    style subject stroke-width:3px
```

Dependencies and dependents of `runtime:msys2:msys-2.0.dll` in the composed graph: 70 dependents and 0 dependencies, of which 62 are omitted here for legibility.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->
