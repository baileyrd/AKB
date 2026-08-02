---
id: doc:volume-6:library-category-logging
title: Library Category — Logging
volume: 6
status: partial
model_refs:
  - library:gabime:spdlog
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:catalog:current
last_verified: 2026-08-02
---

# Library Category — Logging

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gabime:spdlog` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Gabi Melman |
| Environments | `ucrt64` |
| Upstream | <https://github.com/gabime/spdlog> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-spdlog` |
| Version (observed) | 1.17.0-3 |
| License (observed) | spdx:MIT |
| Architecture (observed) | any |
| Installed size (observed) | 1.2 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## The finding: this category is genuinely small

From the catalog snapshot (`20260729T113151Z`), dependents summed across
all environment variants:

| Library | Dependents | Variants | Version | License |
| --- | ---: | ---: | --- | --- |
| `spdlog` (`library:gabime:spdlog`) | 27 | 5 | 1.17.0-3 | MIT |
| glog | 18 | 4 | 0.7.1-10 | BSD-3-Clause |
| ng-log | 4 | 4 | 0.8.2-4 | BSD-3-Clause |
| log4cpp | 3 | 3 | 1.1.4-4 | LGPL-2.1-or-later |
| log4cxx | 0 | 3 | 1.7.0-1 | Apache-2.0 |

The leader has 27 dependents. Every other category's leader is in the
hundreds — `libpng` at 471, `glib2` at 735, `cairo` at 321, `ffmpeg` at
161, `libsndfile` at 100. **Logging's leader is an order of magnitude
below the next-smallest category's**, and the whole category totals 52
dependents.

That is a measured result and it is worth stating rather than padding.
Three explanations are consistent with it, and this knowledge base cannot
currently distinguish between them:

1. **C and C++ projects commonly write their own logging** rather than
   taking a dependency, so the libraries exist without accumulating
   dependents.
2. **Header-only usage is invisible here.** `spdlog` is usable
   header-only. A project that vendors or `#include`s it without declaring
   a package dependency contributes nothing to this count. The catalog
   records declared package dependencies, not source-level usage.
3. **Logging is often provided by a framework** rather than a dedicated
   library. Qt, GLib, and Boost all carry logging facilities, and a
   project using those does not appear in this table.

Explanation 2 is the one this knowledge base could test and has not: it
needs header inventories, which the deep-inventory pipeline produces and
which have been collected for 2 of 15,711 packages.

## What the category contains

`spdlog` and `glog` are modern C++ loggers; `log4cpp` and `log4cxx` are
ports of the log4j model; `ng-log` is a `glog` successor. The `log4*`
family's near-zero dependent counts (3 and 0) suggest the log4j-derived
model has not carried into this ecosystem, though see the caveats above
before treating a low count as evidence of disuse.

`spdlog`'s single declared runtime dependency is `fmt`, which is a
formatting library rather than a logging one — the dependency is real and
narrow.

## Why there is no MSYS2-specific logging story

Unlike audio (which needs a host output API) or GUI (which needs a
windowing system), logging is largely platform-neutral: it formats strings
and writes to files or streams. The Windows-specific questions that would
apply — Event Log integration, `OutputDebugString`, ETW — are not
addressed by any package in this table according to its metadata, and
this knowledge base has no evidence either way.

One boundary question does apply and is unresolved here: a logger writing
to a file path crosses the MSYS/native path boundary like anything else,
so a library configured with a POSIX path from an MSYS-side process and
linked into a native program is in the territory described by
[MSYS Path Conversion](MSYS-PATH-CONVERSION.md). No observation exists.

## Evidence and Gaps

- Dependent counts, variant counts, versions, and licenses are
  **observed** from the catalog snapshot.
- **`spdlog`'s upstream project page was not retrievable**: github.com
  returned 403 through this environment's proxy. The entity records the
  project URL from package metadata, which is observed, but no primary
  upstream source is cited for it. This is the only category page in the
  set without a verified upstream citation, and it is recorded here rather
  than papered over.
- **Only `spdlog` is modelled as an entity.**
- The three candidate explanations for the low counts are stated as
  candidates. Distinguishing them requires header and file inventories
  that do not exist yet.

## Related Objects

- [Library Category — Testing](LIBRARY-CATEGORY-TESTING.md)
- [Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
