---
id: doc:volume-6:library-category-testing
title: Library Category — Testing
volume: 6
status: partial
model_refs:
  - library:google:googletest
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:googletest:project-site-2026-08-02
  - evidence:build-dependencies:current
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Testing

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:google:googletest` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Google |
| Environments | `ucrt64` |
| Upstream | <https://google.github.io/googletest/> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-gtest` |
| Version (observed) | 1.17.0-1 |
| License (observed) | spdx:BSD-3-Clause |
| Architecture (observed) | any |
| Installed size (observed) | 3.5 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:googletest:project-site-2026-08-02` — GoogleTest (official documentation site) (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Correction, 2026-08-02

This page previously reported that ten test frameworks across roughly 47
packages recorded **one** dependent between them, and correctly identified
the cause as a gap in this knowledge base's own data model rather than a
fact about MSYS2. **That gap is now closed**, and the numbers below are the
real ones.

The catalog projection carried four relationship types and none of them was
a build-time edge, because `tools/import_repository_db.py` read `%DEPENDS%`
and `%OPTDEPENDS%` from each package's `desc` record and dropped
`%MAKEDEPENDS%` and `%CHECKDEPENDS%`. Both fields were present in the
repository database the whole time — `%MAKEDEPENDS%` appears in 662 of the
798 `msys` records — and simply were not read.

`model/build-dependencies/current.json` now carries 54,035
`build-depends-on` and 3,428 `check-depends-on` edges. `build-depends-on`
is the largest single edge type in the composed graph, ahead of
`runtime-depends-on` at 41,061.

## The ranking

Dependents summed across all environment variants, now split by edge class.
Catalog and runtime figures are from snapshot `20260729T113151Z`; build and
check figures from the repository databases read 2026-08-02.

| Library | Runtime | Build | Check | Total | Version | License |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `gtest` (`library:google:googletest`) | 0 | 33 | 46 | **79** | 1.17.0-1 | BSD-3-Clause |
| cppunit | 0 | 46 | 13 | **59** | 1.15.1-3 | LGPL-2.1-or-later |
| catch (Catch2) | 0 | 21 | 0 | **21** | 3.15.3-1 | BSL-1.0 |
| cunit | 0 | 9 | 5 | **14** | 2.1.3-4 | LGPL2.1 |
| check | 0 | 11 | 0 | **11** | 0.15.2-4 | LGPL-2.1-or-later |
| cmocka | 0 | 4 | 5 | **9** | 1.1.8-3 | Apache-2.0 |
| doctest | 1 | 4 | 0 | **5** | 2.4.12-1 | MIT |
| unittest-cpp | 0 | 0 | 4 | **4** | 2.0.0-2 | MIT |
| cpputest | 0 | 0 | 0 | 0 | 4.0-2 | BSD-3-Clause |
| bcunit | 0 | 0 | 0 | 0 | 5.4.88-1 | LGPL-2.0-or-later |

The category totals 202 dependents rather than 1.

## The largest test framework in the catalog is not in that table

`python-pytest` has **1,262 dependents — 1,254 of them check-time**. It is
the most-depended-upon test framework in the ecosystem by more than an
order of magnitude, and it was entirely invisible before this fix, because
a Python test framework is a `checkdepends` of a Python package and never a
runtime dependency of anything.

The check-time leaders are all Python:

| Package | Check-time dependents |
| --- | ---: |
| python-pytest | 1,254 |
| python-pytest-cov | 142 |
| python-mock | 108 |
| python-coverage | 79 |
| python-pytest-mock | 64 |
| python-pytest-xdist | 63 |
| python-hypothesis | 60 |
| python-pytest-asyncio | 50 |

That is the shape of the category: a large, concentrated Python testing
stack, and a smaller, more evenly spread C and C++ one where `gtest` and
`cppunit` lead.

## What the build-time ranking looks like generally

The correction is not confined to testing. The top of the build-time
ranking shares almost nothing with the runtime ranking:

| Package | Build-time dependents |
| --- | ---: |
| ninja | 4,455 |
| cmake | 4,194 |
| python-installer | 4,187 |
| python-build | 4,132 |
| python-setuptools | 3,206 |
| autotools | 2,593 |
| pkgconf | 2,081 |
| python-pytest | 1,262 |
| git | 1,259 |
| python | 1,039 |
| meson | 1,023 |

Compare the runtime leaders — `python` at 999, `zlib` at 299, `libpng` at
471. **Not one of `ninja`, `cmake`, `python-installer`, `python-build`,
`setuptools`, `autotools`, or `pkgconf` appears anywhere in a runtime
ranking**, and between them they are declared by more packages than any
runtime dependency in the catalog. The build-time graph is a different
graph, and until now this knowledge base could not see it.

## Two generations, and what the split says

`cunit`, `bcunit`, `check`, `cppunit`, and `unittest-cpp` are older C and
C++ frameworks in the xUnit tradition. `gtest`, `catch` (Catch2),
`doctest`, `cmocka`, and `cpputest` are the current generation.

The build/check split within a framework is informative. `gtest` at 33
build and 46 check is used predominantly as intended — a check-time
dependency for running a suite. `cppunit` at 46 build and 13 check leans
the other way, which is consistent with packages linking it rather than
merely running against it. `catch` and `check` show no check-time
dependents at all despite build-time use.

`cpputest` and `bcunit` remain at zero on every edge class. Those two are
packaged and unused in this catalog, which is now a real finding rather
than an artifact.

The licensing is the most permissive of the seven categories: BSD, MIT,
Apache, and Boost dominate, with only the older `*unit` family under LGPL.
That is consistent with test frameworks being linked into software that is
not itself distributed.

## Evidence and Gaps

- Runtime counts, versions, and licenses are **observed** from catalog
  snapshot `20260729T113151Z`.
- Build and check counts are **observed** from the six MSYS2 repository
  databases read on 2026-08-02, projected additively — see
  `tools/import_build_dependencies.py` for why the two dates are separate
  and what that costs.
- **10,195 of 67,703 declared build and check edges were dropped** because
  one endpoint names a package absent from the 2026-07-29 catalog. Most are
  virtual provides and packages added since. The projection counts them
  rather than inventing entities for them.
- GoogleTest's documentation site was retrieved 2026-08-02 and verified 200.
- **Only `gtest` is modelled as an entity.**
- **No test framework has been built or run by this knowledge base**, and
  whether these work on the MSYS side, the native side, or both remains
  unestablished.

## Related Objects

- [Library Category — Logging](LIBRARY-CATEGORY-LOGGING.md)
- [Packaging for MSYS2](DEVELOPER-PACKAGING.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
