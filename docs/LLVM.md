---
id: doc:volume-8:llvm
title: LLVM
volume: 8
status: partial
model_refs:
  - component:llvm:llvm
  - component:llvm:clang
  - component:llvm:lld
  - component:llvm:lldb
  - library:llvm:llvm-libs
  - environment:msys2:clang64
evidence_refs:
  - evidence:llvm:langref-2026-08-02
  - evidence:llvm:codegen-2026-08-02
  - evidence:llvm:command-guide-2026-08-02
  - evidence:llvm:llvm-libs-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-08-02
---

# LLVM

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `component:llvm:llvm` |
| Kind | `component` |
| Status | `partial` |
| Confidence | `high` |
| Authority | LLVM Project |
| Environments | `clang64`, `clangarm64`, `mingw64`, `msys`, `ucrt64` |
| Upstream | <https://llvm.org/> |
| Packaged as | `package:msys2:llvm` |
| Version (observed) | 21.1.8-2 |
| License (observed) | spdx:Apache-2.0 WITH LLVM-exception |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 348.7 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:llvm:codegen-2026-08-02` — The LLVM Target-Independent Code Generator (`primary`, retrieved 2026-08-02)
- `evidence:llvm:command-guide-2026-08-02` — LLVM Command Guide (`primary`, retrieved 2026-08-02)
- `evidence:llvm:langref-2026-08-02` — LLVM Language Reference Manual (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

LLVM is the umbrella this ecosystem's Clang-based environments rest on.
[Clang](CLANG.md) is a front end that produces LLVM IR; [LLD](LLD.md) is a
linker built on LLVM's object libraries; [LLDB](LLDB.md) is a debugger
built on the same infrastructure. This page covers what sits underneath
all three: **the intermediate representation, the code generator, and the
`llvm-*` tool family**.

The organising fact is that LLVM is a *library set with drivers on top*,
not a compiler with libraries attached. That is why the MSYS2 packaging
splits it the way it does, and why the same infrastructure appears in a
linker and a debugger as well as a compiler.

## The Intermediate Representation

Upstream's own definition:

> LLVM is a Static Single Assignment (SSA) based representation that
> provides type safety, low-level operations, flexibility, and the
> capability of representing 'all' high-level languages cleanly. It is the
> common code representation used throughout all phases of the LLVM
> compilation strategy.

Two properties in that sentence do the work.

**SSA.** Each value is assigned exactly once, so def-use chains are
explicit in the representation rather than recovered by analysis. Most
LLVM optimisations are stated over that structure.

**Typed.** Upstream gives the motivating example:

> By providing type information, LLVM can be used as the target of
> optimizations: for example, through pointer analysis, it can be proven
> that a C automatic variable is never accessed outside of the current
> function, allowing it to be promoted to a simple SSA value instead of a
> memory location.

### Three equivalent forms

This is the fact that makes the tool family below make sense:

> The LLVM code representation is designed to be used in three different
> forms: as an in-memory compiler IR, as an on-disk bitcode
> representation (suitable for fast loading by a Just-In-Time compiler),
> and as a human readable assembly language representation. […] The three
> different forms of LLVM are all equivalent.

So `.ll` (text) and `.bc` (bitcode) hold the same program, and
`llvm-as`/`llvm-dis` move between them losslessly. Nothing analogous
exists in the GCC pipeline as a stable, documented, user-facing artifact,
and that difference is why LLVM's tooling can inspect and transform
half-compiled programs.

Upstream also draws a distinction worth carrying into any tooling that
generates IR:

> There is a difference between what the parser accepts and what is
> considered [well formed].

Parse success is not validity.

## The Code Generator

The target-independent code generator takes IR to machine code in a
documented sequence of stages:

| Stage | What it does |
| --- | --- |
| Instruction Selection | Maps IR onto target instructions, producing a DAG |
| Scheduling and Formation | Orders that DAG and emits `MachineInstr`s |
| SSA-based Machine Code Optimizations | Optional; works on the SSA form the selector produced (modulo scheduling, peephole) |
| Register Allocation | Transforms an **infinite virtual register file in SSA form** into the target's concrete registers; introduces spill code |
| Prolog/Epilog Code Insertion | Emits frame setup once stack size is known; eliminates abstract stack references; frame-pointer elimination and stack packing live here |
| Late Machine Code Optimizations | Operates on final machine code — spill-code scheduling, peephole |
| Code Emission | Emits target assembly or machine code |

Targets may insert their own passes anywhere in that flow, which is how
architecture-specific behavior enters a target-independent pipeline.

The design rationale upstream states is worth quoting because it explains
why LLVM is usable both in a JIT and in an offline optimising compiler:

> The code generator is based on the assumption that the instruction
> selector will use an optimal pattern matching selector to create
> high-quality sequences of native instructions. Alternative code
> generator designs based on pattern expansion and aggressive iterative
> peephole optimization are much slower. This design permits efficient
> compilation (important for JIT environments) and aggressive
> optimization (used when generating code offline) by allowing components
> of varying levels of sophistication to be used for any step of
> compilation.

The register-allocation row is the one with the most visible consequence
for anyone reading generated code: before that stage, the program uses
unlimited virtual registers. Spill code — and therefore a large part of
the difference between `-O0` and `-O2` output — is created there.

## The `llvm-*` Tool Family

Upstream divides the tools into two groups, and the division is
architecturally meaningful.

### Tools that operate on LLVM's own representation

| Tool | Role |
| --- | --- |
| `opt` | LLVM optimizer — runs passes over IR |
| `llc` | LLVM static compiler — IR to target assembly or object |
| `lli` | Directly executes programs from LLVM bitcode |
| `llvm-as` / `llvm-dis` | Assembler and disassembler between `.ll` and `.bc` |
| `llvm-link` | Bitcode linker |
| `llvm-diff` | Structural diff of two IR modules |
| `llvm-extract` | Pulls functions or globals out of a module |
| `llvm-config` | Prints LLVM compilation options |
| `llvm-mc` | Machine-code playground — assemble/disassemble at the MC layer |
| `llvm-mca` | Machine-code analyzer — static throughput estimation |
| `llvm-reduce` | Automatic testcase reducer |
| `llvm-profdata` / `llvm-cov` | Profile data and coverage |
| `llvm-symbolizer` | Addresses to source locations |
| `llvm-dwarfdump` | Dump and verify DWARF |

`opt` and `llc` together are the compiler pipeline with the front end
removed, which is why they are the tools for investigating *whether the
optimiser or the code generator* produced a given result.

### Tools upstream calls "GNU binutils replacements"

| LLVM tool | GNU counterpart |
| --- | --- |
| `llvm-ar` | `ar` |
| `llvm-ranlib` | `ranlib` |
| `llvm-nm` | `nm` |
| `llvm-objdump` | `objdump` |
| `llvm-objcopy` | `objcopy` |
| `llvm-strip` | `strip` |
| `llvm-readelf` | `readelf` |
| `llvm-addr2line` | `addr2line` |
| `llvm-cxxfilt` | `c++filt` |
| `llvm-size`, `llvm-strings` | `size`, `strings` |

Plus `llvm-readobj`, LLVM's own object reader, and `llvm-lib`, described
upstream as an "`lib.exe` compatible library tool" — the MSVC-facing one,
which is the tool in this list most specific to Windows.

**This is where the LLVM environments and the GCC environments diverge in
practice.** A CLANG64 build can use the `llvm-*` tools throughout and
never invoke [GNU Binutils](GNU-BINUTILS.md); a UCRT64 or MINGW64 build
uses Binutils. Build systems that hardcode `ar` or `nm` rather than
respecting `AR`/`NM` will pull the GNU tools into an otherwise-LLVM build,
which usually works and occasionally does not.

## How MSYS2 Packages It

The packaging reflects the library/driver split directly. From the catalog
snapshot (`20260729T113151Z`):

| Package | Version | Installed size | Depends on |
| --- | --- | --- | --- |
| `mingw-w64-clang-x86_64-llvm` | 22.1.8-2 | 440 MB | `llvm-libs=22.1.8`, `llvm-tools=22.1.8` |
| `mingw-w64-clang-x86_64-llvm-libs` | 22.1.8-2 | 156 MB | `cc-libs`, `libffi`, `libxml2`, `zlib`, `zstd` |
| `mingw-w64-clang-x86_64-llvm-tools` | 22.1.8-2 | 131 MB | `llvm-libs=22.1.8` |
| `mingw-w64-clang-x86_64-llvm-openmp` | 22.1.8-1 | 2.7 MB | — |
| `mingw-w64-clang-x86_64-llvm-21` | 21.1.8-5 | **3.4 GB** | `cc-libs` |
| `llvm` (MSYS side) | 21.1.8-2 | 366 MB | `llvm-libs=21.1.8` |
| `llvm-libs` (MSYS side) | 21.1.8-2 | 78 MB | `gcc-libs`, `libzstd`, `zlib`, `libxml2`, `libedit` |

Four observations follow from that table, all from measured catalog data:

1. **`llvm` is a metapackage.** It pulls in `llvm-libs` and `llvm-tools`
   at an exact pinned version (`=22.1.8`). The libraries and the drivers
   are separately installable, which is what lets a program link LLVM
   without installing the tool family.
2. **The MSYS side and the native side are on different major versions**
   — 21.1.8 versus 22.1.8 in this snapshot. They are different packages
   for different sides, so this is expected rather than broken, but any
   claim of "the LLVM version on MSYS2" has to say which side.
3. **A versioned side-by-side package exists** (`llvm-21`) at 3.4 GB —
   roughly eight times the size of the current `llvm` package, which is
   consistent with an unsplit build that includes what the split packages
   separate out.
4. **`llvm-libs` dependencies differ by side.** The MSYS build links
   `libedit`; the native build does not, and links `libffi` instead. That
   is the MSYS/native boundary showing up as a dependency difference in
   the same upstream project.

`llvm` is in the `mingw-w64-clang-x86_64-toolchain` group, so it arrives
with the CLANG64 toolchain rather than being an optional add-on. License
is `Apache-2.0 WITH LLVM-exception` throughout.

## Relationship to Clang, LLD, and LLDB

| Component | What it is | Page |
| --- | --- | --- |
| Clang | C/C++/Objective-C front end producing LLVM IR | [Clang](CLANG.md) |
| LLD | Linker built on LLVM's object libraries | [LLD](LLD.md) |
| LLDB | Debugger built on the same infrastructure | [LLDB](LLDB.md) |
| `libc++` | LLVM's C++ standard library | [libc++](LIBCXX.md) |
| `llvm-libs` | The infrastructure libraries themselves | [LLVM libraries](LLVM-LIBS.md) |
| `clang-libs` | Clang's libraries, usable independently of the driver | [Clang libraries](CLANG-LIBS.md) |

They share a release train — the version numbers move together — but MSYS2
packages them separately, so an installation can hold one without the
others.

## Evidence and Gaps

- IR properties, the code-generation stages, and the tool inventory come
  from LLVM's own documentation, retrieved 2026-08-02 and verified 200
  before citation. **They describe LLVM upstream, not the MSYS2 build.**
- Package versions, sizes, dependencies, licenses, and group membership
  are observed from the catalog snapshot and are the strongest claims on
  this page.
- **Which `llvm-*` tools the MSYS2 `llvm-tools` package actually
  installs is not established.** No package file manifest has been
  collected for it — the deep-inventory pipeline exists but has covered 2
  of 15,711 packages. The table above lists what LLVM ships, not what
  MSYS2 installs.
- No PE analysis of any LLVM binary exists here, so nothing states which
  DLLs the MSYS2 builds import.
- The LLVM 21 versus 22 split between sides is a snapshot observation from
  2026-07-29 and will drift.

## Related Objects

- [Clang](CLANG.md)
- [LLD](LLD.md)
- [LLDB](LLDB.md)
- [LLVM libraries](LLVM-LIBS.md)
- [GNU Binutils](GNU-BINUTILS.md)
