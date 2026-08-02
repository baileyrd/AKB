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
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Testing

## The finding: this category is invisible to the model, not absent

From the catalog snapshot (`20260729T113151Z`):

| Library | Dependents | Variants | Version | License |
| --- | ---: | ---: | --- | --- |
| `gtest` (`library:google:googletest`) | **0** | 6 | 1.17.0-1 | BSD-3-Clause |
| catch (Catch2) | **0** | 5 | 3.15.3-1 | BSL-1.0 |
| cppunit | **0** | 5 | 1.15.1-3 | LGPL-2.1-or-later |
| cunit | **0** | 5 | 2.1.3-4 | LGPL2.1 |
| cmocka | **0** | 5 | 1.1.8-3 | Apache-2.0 |
| doctest | 1 | 5 | 2.4.12-1 | MIT |
| unittest-cpp | **0** | 4 | 2.0.0-2 | MIT |
| cpputest | **0** | 4 | 4.0-2 | BSD-3-Clause |
| check | **0** | 4 | 0.15.2-4 | LGPL-2.1-or-later |
| bcunit | **0** | 4 | 5.4.88-1 | LGPL-2.0-or-later |

Ten test frameworks, each packaged across four to six environment
variants — roughly 47 packages in total — and the entire category records
**one** dependent.

## The cause is this knowledge base's own data model

That is not a fact about the MSYS2 ecosystem. It is a gap in the catalog
projection, and naming it precisely is the most useful thing this page
does.

`model/catalog/current.json` carries four relationship types:
`runtime-depends-on`, `optional-depends-on`, `published-in`, and
`belongs-to-environment`. **It carries no build-time or check-time
dependency edges at all.**

A test framework is, almost by definition, never a runtime dependency. It
appears in a `PKGBUILD` as `checkdepends` or `makedepends` and is used
during `check()`. Those declarations exist in the recipes; they are simply
not projected into the model.

So the correct reading of the table is: **the catalog cannot see how these
packages are used**, and their zero counts measure the projection rather
than the ecosystem. Anyone using this knowledge base's dependency data to
rank library importance is systematically blind to the entire build-time
half of the graph.

The single `doctest` dependent is the exception that confirms the rule —
it is a runtime dependency somewhere, which the other nine happen not to
be.

## What this implies for the rest of the knowledge base

This is the sharpest finding of the seven category pages, and it is not
confined to testing:

- Build tools, code generators, and documentation tools are affected the
  same way. Anything used to *produce* a package rather than *run* it is
  under-counted or invisible.
- The whole-catalog rankings elsewhere in this knowledge base — including
  the ones on the other six category pages — measure runtime centrality
  specifically. That is a real property and a useful one, but it is not
  "importance", and the pages should be read with that qualifier.
- The remedy is a projection carrying `makedepends` and `checkdepends`
  from the recipes. The recipe ingestion pipeline exists
  (`Statically ingest package recipes without executing PKGBUILDs` is a
  closed roadmap item), so this is a modelling gap rather than a
  collection gap.

That remedy is not attempted here; it is recorded so that it is visible as
work rather than absent.

## The frameworks themselves

Two generations are represented. `cunit`, `bcunit`, `check`, `cppunit`,
and `unittest-cpp` are older C and C++ frameworks in the xUnit tradition.
`gtest`, `catch` (Catch2), `doctest`, `cmocka`, and `cpputest` are the
current generation, split between assertion-macro styles and
mock-supporting designs.

The licensing is more permissive than any other category on this page set:
BSD, MIT, Apache, and Boost dominate, with only the older `*unit` family
under LGPL. That is consistent with test frameworks being linked into
software that is not itself distributed.

`gtest` declares one runtime dependency (`gcc-libs` in the UCRT64
variant), so the packages themselves are thin.

## Evidence and Gaps

- Dependent counts, variant counts, versions, and licenses are
  **observed** from the catalog snapshot.
- The absence of build-time and check-time relationship types is
  **verified** by inspecting `model/catalog/current.json` directly: only
  four relationship types appear in it.
- GoogleTest's documentation site was retrieved 2026-08-02 and verified
  200.
- **Only `gtest` is modelled as an entity.**
- **No test framework has been built or run by this knowledge base.**
- Whether these frameworks work on the MSYS side, the native side, or both
  is unestablished. Given that they are C/C++ libraries with no host API
  requirement, both is the expected answer, and it is not verified.

## Related Objects

- [Library Category — Logging](LIBRARY-CATEGORY-LOGGING.md)
- [Packaging for MSYS2](DEVELOPER-PACKAGING.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
