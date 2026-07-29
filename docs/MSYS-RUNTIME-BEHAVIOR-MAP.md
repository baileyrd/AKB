---
id: doc:volume-3:msys-runtime-behavior-map
title: MSYS Runtime Behavior Architecture Map
volume: 3
status: partial
model_refs:
  - runtime:msys2:msys-2.0.dll
evidence_refs: []
last_verified: 2026-07-28
---

# MSYS Runtime Behavior Architecture Map

The [Level 3 runtime-boundary diagram](../diagrams/level-3-msys-runtime-boundary.svg)
is the navigation companion to this map. It distinguishes MSYS-dependent
execution from native environment execution before drilling into individual
adaptation concerns.

| Concern | MSYS runtime responsibility | Windows-facing boundary | Required deep evidence |
| --- | --- | --- | --- |
| Process creation | Present POSIX process semantics where supported | Windows process creation and handles | Runtime source and controlled probes |
| `fork()` / `exec()` | Adapt POSIX lifecycle expectations | Process image, inheritance, loader | Version-qualified implementation analysis |
| Signals | Map POSIX signal behavior to available host mechanisms | Threads, processes, console control | Behavioral test matrix |
| Paths and mounts | Translate MSYS paths and virtual mount rules | Drive/UNC/filesystem namespaces | Mount table and path-conversion observations |
| Filesystem and symlinks | Present POSIX-like file operations | NTFS/ReFS/Win32 semantics | Filesystem probes by host/version |
| PTY and console | Provide terminal-facing abstractions | Console, ConPTY, pipes | Terminal integration tests |

## Boundary Rule

These services apply to MSYS-dependent processes. Native UCRT64, CLANG64, and
MinGW programs use Windows-facing runtime behavior directly unless they
explicitly load the MSYS runtime.

## Evidence Gaps

This is a responsibility map, not a claim of exact implementation ordering or
feature parity. Each row requires source revision, Windows version, and
reproducible observation evidence before being elevated beyond `partial`.

## Related Views

- [Runtime initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
