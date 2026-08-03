---
id: doc:volume-18:migration
title: Migrating Between MSYS2 Environments
volume: 18
status: partial
model_refs:
  - environment:msys2:msys
  - environment:msys2:ucrt64
  - environment:msys2:mingw64
  - environment:msys2:clang64
  - environment:msys2:clangarm64
evidence_refs:
  - evidence:msys2:environments-2026-07-28
  - evidence:msys2:porting-2026-08-02
  - evidence:msys2:creating-packages-2026-08-02
last_verified: 2026-08-02
---

# Migrating Between MSYS2 Environments

Part 5 of the [Developer Guide](DEVELOPER-GUIDE.md).

## Two kinds of migration, with very different costs

| Move | Cost |
| --- | --- |
| Between native environments (MINGW64 → UCRT64, → CLANG64) | Recompile; audit CRT-visible behavior |
| Across the MSYS boundary (MSYS ↔ native) | **Port.** The POSIX API you were using does not exist on the other side |

The second is not a migration in the ordinary sense. Nothing carries over
automatically, because the two sides do not share libraries at all:

> You also can't link a `mingw` program against an `msys` library.

Plan them differently. The rest of this page treats them separately.

## Migrating between native environments

### What actually changes

The environments differ in C runtime, compiler, C++ standard library,
linker, and exception model. The full eleven-attribute comparison is
[Runtime Environments](RUNTIME-ENVIRONMENTS.md); the per-environment
pages are linked from the [Developer Guide](DEVELOPER-GUIDE.md#choosing-among-the-native-environments).

The changes that bite, in order of how often they bite:

1. **Every dependency must exist in the target environment.** Packages are
   per-environment; `mingw-w64-x86_64-foo` and
   `mingw-w64-ucrt-x86_64-foo` are different packages. A dependency
   present in one repository may be absent from another.
2. **C++ ABI does not cross toolchains.** A libstdc++ object and a libc++
   object are not interchangeable. Moving GCC → Clang means rebuilding
   every C++ dependency for the target, not relinking.
3. **The C runtime changes what `printf` and friends do.** `msvcrt.dll`
   and the UCRT differ in format-specifier and locale behavior. This is
   the classic MINGW64 → UCRT64 surprise, and it is a behavior change
   rather than a compile error.
4. **Linker differences surface as link errors, not runtime bugs** — which
   is the good case. LLD and BFD `ld` differ in how they handle some
   flags and script constructs.

### The migration sequence

1. Install the target environment's toolchain package.
2. Resolve dependencies in the target repository first, before touching
   code. A missing dependency ends the migration; better to find it in
   step 2 than step 5.
3. Rebuild clean. Do not reuse object files or a configured build tree
   from the source environment — stale configure caches are a reliable
   source of confusing failures.
4. Fix compile and link errors.
5. **Run the test suite and read the formatted output**, not just the exit
   code. Runtime differences of the `printf` kind pass compilation
   silently.
6. Check the produced binary's imports against expectations. This is where
   a stale dependency on the previous CRT shows up.

Step 6 is exactly the analysis this knowledge base cannot yet perform on
any binary — the PE import extraction pipeline exists but has been run
against 2 of 15,711 packages.

### 32-bit and ARM64

MINGW32 is a distinct target, not a flag on MINGW64: a separate
environment, separate packages, separate prefix (`mingw-w64-i686-`).
CLANGARM64 likewise targets a different architecture entirely. Both are
recompilation-plus-porting exercises, and the pointer-size assumptions in
the source are the usual obstacle for the 64→32 direction.

## Migrating across the MSYS boundary

### MSYS → native: a port

You are removing a POSIX runtime the program depends on. What has to be
replaced:

| The program used | It must now |
| --- | --- |
| `fork` | Use process creation directly, or `posix_spawn`-style APIs |
| POSIX signals | Use Windows mechanisms; `SIGUSR1` has no native equivalent |
| POSIX paths, mounts, `/dev/*` | Use Windows paths; no mount table exists |
| PTYs | Use ConPTY or a wrapper; see [Windows Console and ConPTY Boundary](WINDOWS-CONSOLE-CONPTY-BOUNDARY.md) |
| `msys-2.0.dll` symlink semantics | Windows-native link behavior, which differs |

The compensation is that the emulation cost disappears entirely — see
[Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md)
— and the result ships as an ordinary Windows program with no runtime to
carry.

### Native → MSYS: rare, and usually wrong

Moving native code onto the MSYS side is unusual and upstream discourages
it by implication: the `msys` repository is for POSIX infrastructure, the
toolchain, hard-to-port build dependencies, and gap-bridging tools. If the
motivation is "I need a POSIX API", check first whether the native
environments already provide what is needed. If the motivation is "it
builds more easily there", the cost is that the result is no longer a
normal Windows program.

### Making source work on both sides

The identifiers are documented and listed in the
[Developer Guide](DEVELOPER-GUIDE.md#detecting-the-side-from-inside-the-build).
Three practical rules:

- Branch on `__MSYS__`, not `__CYGWIN__`, when MSYS2 specifically is
  meant. `__CYGWIN__` is also true on Cygwin.
- In `configure`-style scripts, match **both** `*-pc-msys` and
  `*-pc-cygwin`. The MSYS host triplet changed, and a script matching only
  the old form falls through silently.
- In Python, the MSYS side reports `sys.platform == "cygwin"` and the
  native side reports `"win32"`.

## Migrating from other Windows development setups

### From Cygwin

The MSYS side is closest to Cygwin — it is a fork of it — and much source
carries over. The divergence is concentrated exactly where it hurts:
**path translation and mount behavior**. Anything relying on Cygwin's
specific mount configuration, `cygdrive` prefix, or path-conversion
behavior for native child processes must be re-verified rather than
assumed. That caveat is standing across this entire knowledge base.

### From MSVC

This is a toolchain and ABI change, not a POSIX question. The C++ ABI
differs, debug-information formats differ, and the import-library
conventions differ. Nothing in this knowledge base characterises the MSVC
side, so this page notes the direction exists and stops rather than
guessing.

### From WSL

WSL is a different mechanism entirely — a Linux environment rather than a
Windows-native or emulation-layer one — and produces Linux binaries.
Moving from WSL to MSYS2 native is a port to Windows, not a migration.
This knowledge base holds no WSL material.

## What is not established here

- **No migration has been performed or observed by this knowledge base.**
  The sequences above are derived from the documented differences between
  environments, not from executed migrations.
- **The CRT behavior differences between `msvcrt.dll` and the UCRT are
  asserted at the level of "they differ", not enumerated.** No
  specifier-by-specifier comparison exists here.
- **No PE import analysis exists for any binary**, so step 6 of the
  migration sequence is a recommendation this knowledge base cannot
  currently demonstrate.
- MSVC and WSL are named as directions, not documented.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["MSYS"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `environment:msys2:msys` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [Developer Guide](DEVELOPER-GUIDE.md)
- [Runtime Environments](RUNTIME-ENVIRONMENTS.md)
- [Building Software on MSYS2](DEVELOPER-BUILDING-SOFTWARE.md)
- [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)
- [Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md)
