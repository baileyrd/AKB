---
id: doc:volume-18:building-software
title: Building Software on MSYS2
volume: 18
status: partial
model_refs:
  - environment:msys2:msys
  - environment:msys2:ucrt64
  - environment:msys2:clang64
evidence_refs:
  - evidence:msys2:cmake-2026-08-02
  - evidence:msys2:porting-2026-08-02
  - evidence:msys2:creating-packages-2026-08-02
  - evidence:cmake:documentation-2026-07-30
  - evidence:gnu:make-manual-2026-07-30
last_verified: 2026-08-02
---

# Building Software on MSYS2

Part 2 of the [Developer Guide](DEVELOPER-GUIDE.md). Assumes the
selection question — MSYS side or native side — is already answered.

## The prerequisite everyone hits

A fresh MSYS2 install has no build tools. Upstream states it and states
the trap in the same breath:

> In order to be able to compile a software or build a package you need to
> install basic packages by installing `base-devel`, as the MSYS2 install
> does not contain build tools. […] Note that — contrary to what you might
> expect — `base-devel` doesn't contain `gcc` nor `binutils`.

So `base-devel` is necessary and not sufficient. The compiler is a
separate install, and *which* compiler depends on the side chosen:

| Target | Install |
| --- | --- |
| MSYS side | `base-devel`, plus the MSYS `gcc` / `binutils` |
| UCRT64 | `base-devel`, plus `mingw-w64-ucrt-x86_64-toolchain` |
| CLANG64 | `base-devel`, plus the `mingw-w64-clang-x86_64-` toolchain |
| MINGW64 | `base-devel`, plus `mingw-w64-x86_64-toolchain` |

If the compiler is missing, upstream warns the failure will not be
obvious: "building might fail with unexpected errors."

## Which shell to build from

For an ordinary build of your own software, launch the shell for the
environment you are targeting — the launcher sets `PATH`, `MSYSTEM`, and
the toolchain prefix, so `gcc` resolves to the right one. This is what
[Runtime Environments](RUNTIME-ENVIRONMENTS.md) documents.

There is one documented exception, and it catches people:

> When building either `msys` or native software, you should use the MSYS
> shell, not the MINGW{32,64} shells.

That applies to building **packages** with `makepkg`/`makepkg-mingw`, not
to building your own source tree. `makepkg-mingw` arranges the target
environment itself. See [Packaging for MSYS2](DEVELOPER-PACKAGING.md).

## The two `make`s

MSYS2 ships two GNU Makes and they are not interchangeable:

| Package | Command | Nature |
| --- | --- | --- |
| `make` | `make` | MSYS-side; understands POSIX paths and shell constructs |
| `mingw-w64-*-make` | `mingw32-make` | fully native; no MSYS shell dependency |

Upstream's recommendation is unambiguous:

> The latter one is called `mingw32-make` on command line, is fully native
> and doesn't depend on msys2 shells. The downside is that it doesn't work
> with many Makefiles. Unless you know what you're doing, use the regular
> `make`.

The reason is the path and shell boundary: a Makefile that invokes shell
constructs or POSIX paths needs the MSYS side to interpret them. A
Makefile written to be run by `cmd.exe` does not.

To branch inside a Makefile, upstream publishes the detection snippet:

```make
msys_version := $(if $(findstring Msys, $(shell uname -o)),$(word 1, $(subst ., ,$(shell uname -r))),0)
```

It yields 1 or 2 under an MSYS shell and 0 elsewhere. Run through
`mingw32-make` from `cmd.exe` it will error, because `uname` is not on
`PATH` there — which is itself a useful signal about where you are.

## CMake

CMake has an MSYS-side package and native packages, and choosing the wrong
one is the most common CMake mistake on this platform. Upstream:

> When building projects for Windows with CMake (as opposed to building
> projects that are going to run in MSYS2 posix emulation runtime) make
> sure to install the MinGW version of CMake, i.e. installing e.g.
> `mingw-w64-x86_64-cmake`.

Pair it with a build tool. Upstream's current recommendation is Ninja
(`mingw-w64-x86_64-ninja`).

### Always name the generator

> it's recommended to explicitly specify the desired build file generator
> with the `-G` option. MSYS2 provided CMake defaults to Ninja (but this is
> not the default in upstream CMake, so it's safest to explicitly specify
> it).

That is a real portability hazard: the same `cmake` invocation behaves
differently under MSYS2's CMake than under an upstream CMake, because the
default generator differs. Name it.

```
cmake -G Ninja <path-to-source> -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

The three relevant generators, and what each implies:

| Generator | Build tool | Side |
| --- | --- | --- |
| `Ninja` | `ninja` | follows the CMake package you installed |
| `"MSYS Makefiles"` | `make` | MSYS side |
| `"MinGW Makefiles"` | `mingw32-make` | native |

`cmake --build .` works for all three, which is the portable form.

## Autotools

Autotools builds are the MSYS side's home ground: `configure` is a shell
script, and the MSYS shell is what runs it. The relevant hazard is the
host triplet rather than the tooling.

`configure` scripts that branch on `$host` must match **both** MSYS
triplet forms, because the triplet changed:

- `x86_64-pc-msys` / `i686-pc-msys` — older
- `x86_64-pc-cygwin` / `i686-pc-cygwin` — current
- `x86_64-w64-mingw32` / `i686-w64-mingw32` — native

A script that matches only `*-msys` will fall through to a generic branch
on a current MSYS2 install without any error, which makes the failure a
behavior difference rather than a build failure.

## Preprocessor branching

The identifier table is in the [Developer Guide](DEVELOPER-GUIDE.md#detecting-the-side-from-inside-the-build).
The one rule worth repeating here: `__CYGWIN__` is true on the MSYS side
**and** on Cygwin. `__MSYS__` is the one that distinguishes them, and the
distinction matters because MSYS2 diverges from Cygwin precisely in path
translation and mount behavior.

## Two filesystem namespaces

MSYS2 presents POSIX paths to MSYS-side programs and Windows paths to
native ones. A build that mixes the two — an MSYS-side `make` invoking a
native compiler, say — is crossing that boundary on every argument that
looks like a path.

`cygpath` converts explicitly in either direction and is the correct tool
when a native program must receive a Windows path. The mechanism is
[MSYS Path Conversion](MSYS-PATH-CONVERSION.md); the mount table that
drives it is [MSYS Mount Manager](MSYS-MOUNT-MANAGER.md).

## Build performance

A build dominated by process creation on the MSYS side pays the `fork`
emulation on every process. The analysis, including upstream's own
20–30% figure for removing `fork` from the compiler driver, is in
[Ecosystem Performance Architecture](ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md).
The short form: **a native build does not pay it at all.**

## What is not established here

- No build has been run on an MSYS2 host by this knowledge base. Every
  command above is from upstream documentation.
- The effective `makepkg.conf` compiler flags for MSYS2 are not captured,
  so nothing here states the default optimisation or hardening flags.
- Package names above are the documented forms; the installed set on any
  given host should be checked against `pacman -Ss` rather than assumed.

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
- [Packaging for MSYS2](DEVELOPER-PACKAGING.md)
- [Debugging on MSYS2](DEVELOPER-DEBUGGING.md)
- [MSYS Path Conversion](MSYS-PATH-CONVERSION.md)
- [Runtime Environments](RUNTIME-ENVIRONMENTS.md)
