---
id: doc:volume-18:packaging
title: Packaging for MSYS2
volume: 18
status: partial
model_refs:
  - package-manager:archlinux:pacman
  - environment:msys2:msys
  - repository:msys2:msys
evidence_refs:
  - evidence:msys2:creating-packages-2026-08-02
  - evidence:msys2:package-management-2026-08-02
  - evidence:arch:pkgbuild-5-2026-08-02
  - evidence:arch:makepkg-8-2026-08-02
  - evidence:pacman:pacman-8-2026-08-02
last_verified: 2026-08-02
---

# Packaging for MSYS2

Part 4 of the [Developer Guide](DEVELOPER-GUIDE.md).

## What a package is here

MSYS2 uses a port of pacman, so a package is an archive plus metadata,
and the format follows Arch's:

> A package is an archive containing a piece of software. This normally
> means executable files, runtime libraries, data, shared and static link
> libraries, header files, config files, and manual pages. Packages also
> contain metadata, such as the software's name, description of its
> purpose, version number, vendor, checksum, and a list of dependencies.

The output artifact is a `.pkg.tar.zst`, optionally accompanied by a
`.sig`.

## Recipes

> Packages are built from programmatic recipes to ensure builds are
> reproducible. A recipe is a set of files which describe how to build,
> package and install a given piece of software; these are often specific
> to MSYS2.

In the simplest case a recipe is a single `PKGBUILD` — a bash script of
variables and functions. Complex recipes add install scripts and patch
files. Each recipe lives in its own directory, which doubles as the build
working directory.

Two conventions upstream states explicitly:

- **Indentation is two spaces.** Upstream even gives the fixer:
  `expand -t 2 PKGBUILD > PKGBUILD.new && mv PKGBUILD.new PKGBUILD`.
- **Patch files are named `###-target-Purpose.patch`** — a sequence number
  from 001, the package name and version the patch was first written for,
  and a description of what it fixes.

## PKGBUILD essentials

From `PKGBUILD(5)`:

> The mandatory fields for a minimally functional PKGBUILD are `pkgname`,
> `pkgver`, `pkgrel` and `arch`.

and a convention that prevents a whole class of confusing failures:

> If you need to create any custom variables for use in your build
> process, it is recommended to prefix their name with an `_`
> (underscore). This will prevent any possible name clashes with internal
> makepkg variables.

`pkgname` may be an array, which is how one recipe produces several
packages:

> makepkg supports building multiple packages from a single PKGBUILD.
> This is achieved by assigning an array of package names to the `pkgname`
> directive. Each split package uses a corresponding packaging function
> with name `package_foo()`.

Split-package options default to the global values, and a documented
subset — `pkgdesc`, `arch`, `url`, `license`, `groups`, `depends`,
`optdepends`, `provides`, `conflicts`, `replaces`, `backup`, `options`,
`install`, `changelog` — can be overridden per split package.

Integrity fields (`sha256sums`, `sha512sums`, `b2sums`, and others) are
arrays parallel to `source`. Which algorithms are used and generated is
governed by `INTEGRITY_CHECK` in `makepkg.conf(5)` — **and MSYS2's
effective `makepkg.conf` is not captured by this knowledge base**, so do
not assume Arch's defaults apply.

## The build phases

`makepkg` runs a fixed sequence. Upstream lists it:

1. **download, verify, extract** — sources fetched if needed, checked
   against checksums and PGP signatures where specified, extracted into a
   working directory (`src` by default).
2. **`prepare()`** — apply patches and source modifications here.
3. **`build()`** — run the build tools, e.g. `./configure && make`.
4. **`check()`** — optional; run the software's test suite.
5. **`package()`** — given a temporary directory, place the final package
   contents into it, e.g. `make install`.
6. **tidy, archive, sign** — contents scanned for issues, tidied, packaged
   into `.tar.zst` with an optional `.sig`.

Getting each step into the right function matters for more than
tidiness: `makepkg` can skip and resume phases, and that only works if the
phases are honest.

## `makepkg` versus `makepkg-mingw`

This is the MSYS2-specific part, and it is the thing an Arch packager
will get wrong:

| Building | Command |
| --- | --- |
| `msys` package | `makepkg` |
| `mingw` package | `makepkg-mingw` |

> The actual build and packaging is done by running `makepkg` or
> `makepkg-mingw`. The former is used to build `msys` packages and the
> latter for `mingw` packages. […] When building either `msys` or native
> software, you should use the MSYS shell, not the MINGW{32,64} shells.

**Use the MSYS shell for both.** `makepkg-mingw` sets up the target
environment itself; launching it from a MINGW shell is the common mistake.

Typical invocations, per upstream:

- `makepkg -sCLf` — full build.
- `makepkg -RdLf` — repackage. "useful when the process failed in
  `package()` and you don't want to run the long build part again."

`makepkg-mingw` takes the same arguments.

## Rebuilding an existing package

The documented worked examples, which are also the fastest route to
debug symbols:

```sh
git clone "https://github.com/msys2/MSYS2-packages"
cd MSYS2-packages/flex
makepkg -sCLf
pacman -U flex-*.pkg.tar.zst
```

```sh
git clone "https://github.com/msys2/MINGW-packages"
cd MINGW-packages/mingw-w64-python3
makepkg-mingw -sCLf
pacman -U mingw-w64-*-python3-*-any.pkg.tar.zst
```

Two recipe repositories, one per side. That split is the packaging-level
expression of the same `msys-2.0.dll` boundary that runs through the whole
ecosystem.

## Naming

Upstream states the scheme:

> The packages in `msys2` are named just like on a Linux distribution, the
> packages in the others are prefixed by either `mingw-w64-i686-` for
> 32-bit packages, or `mingw-w64-x86_64-` for 64-bit packages with a
> secondary prefix `clang` or `ucrt` where applicable.

So `bash` is MSYS-side; `mingw-w64-ucrt-x86_64-python` is the UCRT64
build of Python. The prefix is not cosmetic — it is what keeps six
environments' worth of the same upstream software distinguishable in one
catalog. The catalog measured by this knowledge base contains four
`python` builds among its six most-depended-on packages, which is that
scheme in action.

## Which repository

Five repositories are documented: `msys2`, `mingw32`, `mingw64`, and the
newer `ucrt64` and `clang64`. The recipe decides which by which side it
targets and which environment it is built for.

The decision rule for the side is in the
[Developer Guide](DEVELOPER-GUIDE.md#choosing-a-side). Short version:
default to `mingw`; choose `msys` only for POSIX infrastructure, the
toolchain, hard-to-port build dependencies, or gap-bridging tools.

## Contributing upstream

Upstream publishes the intended flow: build in the target subsystem, test,
patch, write the recipe, build the package, install locally, test again,
commit to your fork of the target repository, open a pull request, respond
to CI and review, and — the step people skip —

> Offer your fixes to the software's developers (upstream).

One prohibition is stated flatly, and it is a policy rather than a
technical constraint:

> Please do not create pull requests for PKGBUILDs that just repackage
> binary releases from other projects. This is contrary to the goals of
> MSYS2. If the software cannot be built for some reason then try to fix
> the cause of that.

## What is not established here

- **MSYS2's effective `makepkg.conf` has never been captured.** Default
  compiler flags, `INTEGRITY_CHECK` algorithms, compression settings, and
  `PACKAGER` are all unknown to this knowledge base. Anywhere this page
  cites Arch's `PKGBUILD(5)` or `makepkg(8)`, MSYS2-specific divergence is
  possible and unverified.
- **`makepkg-mingw` has no manual page cited here**, because Arch's
  `makepkg(8)` does not describe it. Its exact behavior beyond "takes the
  same arguments" is not established.
- **No package has been built by this knowledge base.** The commands are
  quoted from upstream, not run.
- The repository signing posture for MSYS2 remains unestablished; see
  [pacman Package Signing](PACMAN-PACKAGE-SIGNING.md).

## Related Objects

- [Developer Guide](DEVELOPER-GUIDE.md)
- [Building Software on MSYS2](DEVELOPER-BUILDING-SOFTWARE.md)
- [pacman Architecture](PACMAN-ARCHITECTURE.md)
- [pacman Transactions](PACMAN-TRANSACTIONS.md)
- [pacman Repository Layout](PACMAN-REPOSITORY-LAYOUT.md)
