---
id: doc:volume-8:toolchain-role-model
title: MSYS2 Toolchain Role Model
volume: 8
status: partial
model_refs:
  - environment:msys2:ucrt64
  - environment:msys2:clang64
evidence_refs: []
last_verified: 2026-07-28
---

# MSYS2 Toolchain Role Model

| Role | GCC-oriented environments | LLVM-oriented environments | Boundary |
| --- | --- | --- | --- |
| Compiler driver | GCC | Clang | Source-language translation only; not full ABI identity |
| Linker | GNU binutils/ld by default | LLD by default | Linker features and output behavior are target-specific |
| C++ library | libstdc++ | libc++ | Do not mix object/static-library assumptions across C++ ABI boundaries |
| Debugger | GDB | LLDB where provided | Debugger selection does not change program ABI |
| CRT/target | Determined by selected environment | Determined by selected environment | UCRT/MSVCRT and architecture remain independent dimensions |

## Decision Rules

1. Select the target environment before selecting packages or compiler flags.
2. Rebuild objects and static libraries when changing architecture, CRT, or
   C++ library family.
3. Treat imported DLL interfaces as separate from static-link and object-file
   compatibility; validate ownership and CRT crossings at each API boundary.
4. Generated inventory identifies installed tool artifacts; it does not prove
   a project’s effective flags or link order.

## Related Views

- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
- [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)
