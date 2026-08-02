---
id: doc:volume-20:charter-drift-assessment
title: Charter Drift Assessment
volume: 20
status: partial
model_refs: []
evidence_refs:
  - evidence:repo:self-audit-2026-08-02
last_verified: 2026-08-02
---

# AKB Drift Assessment

## 1. Verdict

Yes — the project drifted, and the direction is unambiguous: **it went depth-first on one volume instead of breadth-first across twenty, and then marked itself finished.** Volume 6 (Libraries) holds 157 of 252 pages and 113,429 of 169,664 words — 66.9% of the entire corpus — while the five charter-peer volumes it was supposed to sit alongside (Volume 2 Windows Platform, Volume 3 MSYS Runtime, Volume 4 Runtime Environments, Volume 7 Package Management, Volume 9 Git for Windows) total 10 pages and 3,883 words between them: 2.29%, a 29:1 ratio. The single most striking fact: **of the 96 documentation pages added in the last 40 docs-touching commits, 96 went to Volume 6 and zero went anywhere else** — and all 28 commits made on 2026-08-02 are per-library dependency-closure commits ("Add GMP (CLANG64)", "Close curl (CLANG64)", "Add BLAKE2 (libb2) (UCRT64)"). Meanwhile `ROADMAP.md` carries 66 `- [x]` and 0 `- [ ]`, reporting the project as 100% delivered, while `docs/VOLUME-COVERAGE-LEDGER.md` marks all 20 volumes "Partial", `docs/REQUIREMENTS-TRACEABILITY.md` marks all 9 requirements "Partial", 241 of 243 pages self-declare `status: partial`, and `generated/coverage-assessment.md` reports 0.013% package payload coverage. Three instruments, three irreconcilable pictures of the same project.

Critically, this was **not** authorized by the repo's own charter restatement. I read `charter/PROJECT-CHARTER.md` in full: it narrows exactly two things (Windows internals to "contextual scope"; third-party packages to "selectively at source-internal level according to architectural significance, dependency centrality, security criticality"). It preserves the L0–L7 drill-down ladder verbatim in its "Architecture depths" table, preserves the eight-state coverage vocabulary, and preserves "provide drill-down navigation from ecosystem to source unit." It never mentions the 20 volumes at all — so nothing at charter level defends volume balance — and `charter/adr/` contains only `README.md` and `TEMPLATE.md`: **zero ADRs**, despite governance stating "Architecture Decision Records govern irreversible or cross-cutting choices." The narrowings that did happen were never recorded as decisions.

---

## 2. The Drift, Ranked

### 1. Nineteen volumes are starved to feed one (critical)

**Charter:** Twenty co-equal volumes, adopted verbatim in `docs/MASTER-VOLUME-INDEX.md`.

**Actual:** v6: 157 pages / 113,429 words. v5: 30 / 22,593. v8: 15 / 12,311. Then the cliff — v1: 6, v10: 8, v11: 5, v9: 4, v20: 4, v3: 2, v7: 2, v14: 2, and v2/v4/v12/v13/v15/v16/v17/v19 at exactly **one page each**. Volume 18 (Developer Guide) has **zero** pages: `grep -rn 'volume: 18' docs/` returns nothing repo-wide, and the ledger's Volume 18 row cites `docs/DEVELOPER-WORKFLOW.md`, which is `volume: 20` and documents the AKB's own git workflow, not MSYS2 development. Eleven volumes hold 14 pages / 936 lines combined — 2.6% of prose. Every thin volume's last touch is 2026-07-29 or 07-30; HEAD is 2026-08-02, ~40 commits later.

Three volumes are not merely thin but **about the wrong system or wrong shape**: Volume 17 (Performance) is `docs/PERFORMANCE-EXPERIMENTS.md`, 34 lines, benchmarking `tools/benchmark_akb.py`'s own `validate`/`generate-indexes`/`build-explorer` operations — zero mention of fork() emulation cost, path translation, mount-table lookup, or pacman transaction cost. Volume 4 collapses six environments the charter said to "document each separately" into one 82-line matrix missing 4 of the 11 required attributes entirely (executable format: 0 hits, package repository: 0, strengths: 0, weaknesses: 0). Volume 10's eight explorer pages total 160 lines with **zero `##` headings on any of them**.

**Remedy:** Impose a per-volume quota before any further Volume 6 page. Split `RUNTIME-ENVIRONMENTS.md` into six per-environment pages against the 11 attributes — highest leverage in the entire audit, because Volume 6 is generating dozens of pages of per-environment ABI detail with no canonical environment page to reference. Re-file `PERFORMANCE-EXPERIMENTS.md` under Volume 20 and author a real Volume 17. Author Volume 18 fresh; do **not** re-key `DEVELOPER-WORKFLOW.md`, which is genuinely Volume 20 material.

### 2. ROADMAP.md reports 66/66 complete, including work that was never written (critical enabler)

This is the root cause, not a symptom. Verified false completions:

- `ROADMAP.md:50` `[x] Process, fork, exec, signal, path, mount, filesystem, symlink, and PTY models` → Volume 3 is **2 pages / 675 words**, one 6-row responsibility table. No page anywhere is titled for `msys-2.0.dll`. `mount manager`, `environment manager`, `process manager`: **0 hits across all 252 docs**.
- `ROADMAP.md:52` `[x] repository, mirror, signing, key, cache, hook, and database models` → 2 pages / 784 words. `repository layout`: 0 hits repo-wide. `package signing`: 0 hits repo-wide.
- `ROADMAP.md:73` `[x] Launcher, Git Bash, Mintty, and shell startup` → Mintty's only Volume 9 appearance is a parenthetical inside a Mermaid node: `C["Terminal host (for example Mintty)"]`.
- `ROADMAP.md:45` `[x] Environment comparison and migration matrix` — the roadmap **substituted a matrix for the charter's "Document each environment separately"** and then checked its own substitution.
- `ROADMAP.md:83` `[x] Layer, package, library, runtime, toolchain, and repository views` — the `layers` and `toolchains` views resolve to **0 objects**.
- Increment 1's `[x] Extract PE imports, exports…` and `[x] Index headers, pkg-config files, and CMake metadata` → run against **2 packages**.

Volume 2's eight named Windows subsystems (NT Kernel, Win32, Console, ConPTY, Filesystem, Registry, Security, Networking) appear **nowhere in ROADMAP.md as planned work** — `grep -ni "windows\|registry\|conpty\|console\|win32\|kernel" ROADMAP.md` returns only lines 12, 25, 70, none of them scope. `grep -ci diagram ROADMAP.md` = **0**: not one roadmap item concerns diagrams.

**Remedy:** Uncheck Increments 2 (environments), 3 (runtime + pacman), 6 (Git for Windows components), 7 (views), and Increment 1/5's inventory items. Restore the charter's "Document each environment separately" wording. Add a missing Increment for Volume 2. Then adopt the ledger's own rule as the checkbox criterion — *"Cross-links alone do not close a gap"* — and add a test in `tests/` that **fails if a roadmap item is checked while its ledger row is still Partial**. That last step is what stops this recurring.

### 3. The deep-inventory pipeline exists, works, and was run on 2 of 15,711 packages (critical — highest leverage)

The charter's per-library field list (DLLs, import libraries, static libraries, headers, pkg-config, CMake metadata, exported APIs) is unimplemented on all 157 Volume 6 pages: the only DLL filenames in all 252 docs are `msys-2.0.dll` (278×) and `msys-z.dll` (1×); **zero** `.dll.a` or `.lib` filenames repo-wide; pkg-config on 4 pages, CMake on 19, "import librar" on 1, exported-API/dumpbin/objdump on **0**; and 75 pages carry an identical disclaimer deferring exactly this. Four of ten charter fields delivered, six not.

The root cause is not missing tooling. `tools/deep_inventory.py` (603 lines), `tools/import_deep_inventory.py` (666 lines), and `tools/Collect-AkbDeepInventory.ps1` exist, are tested (`tests/test_deep_inventory.py`), and demonstrably work end to end — **they were run on `curl` and `mingw-w64-ucrt-x86_64-zlib` and never again**. `model/inventory/current.json` holds 552 entities of which 13 are `dll`, 2 `header`, 1 `import-library`, 1 `pkg-config-module`, 1 `static-library`; `generated/development-artifact-catalog.md` is 11 lines covering one package. `generated/coverage-assessment.json`: `"observed_packages": 2, "percent": 0.013`.

**Remedy:** Batch the existing collector across the installed package set, then add a generated `## Artifacts` block to the library page template. This single action populates six missing charter fields on all 157 pages **from data rather than authoring**, mechanically fills the missing `## Files and Directory Structure` heading, and populates the hollow Interfaces/Compatibility sections on the environment-variant pages. Nothing else in this audit converts so much existing asset into charter compliance.

### 4. The Diagram Hierarchy — an entire charter section — is delivered at roughly zero (critical)

**Charter:** "Every diagram must support drill-down. Level 0 → … → Level 7… Every diagram should hyperlink to related diagrams." Restated verbatim in `charter/PROJECT-CHARTER.md`'s Architecture depths table and `docs/PROJECT-DISCUSSION-RECORD.md:320-339`.

**Actual, all reproduced:**
- `grep -o 'href="[^"]*\.svg[^"]*"' diagrams/*.svg` → **empty**. Not one of the 8 SVGs links to any other SVG. All 51 hrefs point into `../generated/explorer/index.html#/`. There is no L0→L7 chain; there are 8 independent pictures that dead-end in the same flat page. `tests/test_diagrams.py:22` asserts `assertIn("generated/explorer/index.html#/", href)` — **the test suite would fail a sibling-diagram link**, locking the drift in.
- Levels 4–7 contradict the repo's *own* charter ladder. level-4 is an environment matrix (charter L2/L3), level-5 is package-to-artifact flow (charter L4), level-6 is a toolchain role flow, level-7 is an application landscape. **Zero diagrams exist for the Library, Executable/DLL, or Source-unit levels.** All eight viewBoxes are 960 wide with 5–9 nodes each: peer overviews, not zooms.
- Nothing generates them. `grep -rn 'diagrams' tools/ .github/` → two hits, both read-only counts in `assess_akb_coverage.py`. The 8 SVGs were committed Jul 29–30 and never touched again, while `model/graph.json` gained 2,398 lines across 28 commits since Aug 1.
- `docs/DIAGRAM-HIERARCHY.md` — the page README sends readers to — embeds all 8 SVGs with markdown `![]()` image syntax. **Hyperlinks inside an SVG loaded as `<img>` are inert in every browser**, so all 51 hrefs are unreachable from the primary presentation surface.
- `README.md:26` describes `diagrams/` as "Diagram specifications and generated visual outputs." It contains 8 hand-written final SVGs, no specs, no generator. The same README table lists an `explorer/` top-level directory that doesn't exist.
- PlantUML and Graphviz: **zero artifacts, zero generators**. The single `plantuml` match repo-wide is the sentence requiring it.

**Remedy:** Write `tools/build_diagrams.py` emitting `diagrams/level-*.svg` plus `.puml` and `.dot` from `load_composed_graph()`, reusing `build_explorer.py`'s existing `route_for()`. Renumber to the charter's ladder (do **not** amend the charter — it is already correct). Add parent/child navigation to each SVG. Relax `tests/test_diagrams.py:22` to accept sibling `level-*.svg` targets and add a test asserting each level links to N−1 and N+1. Replace the `![]()` embeds with `<object type="image/svg+xml">`.

### 5. The repo's own 21-heading standard is 15-heading in practice, and the missing 6 are the charter-shaped ones (critical)

`docs/DOCUMENTATION-STANDARD.md` lists 21 required object-page headings with the explicit rule: *"record `Not applicable` with a reason instead of silently omitting an expected concern."* Six are on **zero of 252 pages**: Build and Packaging (#11), Files and Directory Structure (#12), Performance Considerations (#15), Extension and Migration (#17), Examples (#18), and **Diagrams (#19)**. Only 3 of 252 pages contain the string "not applicable," so 249 pages omit six concerns silently — a self-inflicted, self-documented violation requiring no interpretation of the original charter at all.

The charter's five diagram headings (Sequence, Component, Class, Package, Deployment) are on **0/252** pages, while the sibling heading Execution Flow is on 199 — the docs follow their own standard on everything *except* the diagram one. Total embedded diagrams: 20 mermaid blocks in 20 files (7.9%), of which 19 are generic flowcharts and exactly **one** is a typed `sequenceDiagram` (`docs/MSYS-RUNTIME-INITIALIZATION.md`). 226 of 252 pages contain zero code fences of any kind — no command examples, no config snippets, no directory listings anywhere. And `grep -l 'diagrams/' $(grep -l '^volume: 6$' docs/*.md)` → **0**: not one of the 157 library pages links to any diagram.

**Remedy:** Either add the six sections to the template or amend the standard to 15 and record the reduction as a dated deviation — then wire the choice into the validator so it cannot drift again. Generate a per-object Mermaid dependency/reverse-dependency subgraph from the 76,105 package edges already in the model; that is a pure generator change in `tools/akb.py`. Promote the existing `sequenceDiagram` into the template. **Do not add a References section** — `## Evidence, Assumptions, and Open Questions` (200/252) plus populated `evidence_refs:` (204/252) is a better, machine-readable citation apparatus; just alias it so the charter mapping is explicit.

### 6. Nothing validates a documentation page (major)

`tools/akb.py`'s `validate()` (lines 51–117) operates exclusively on the composed JSON graph. **It never opens a Markdown file.** Exactly one tool in the repo touches `docs/` at all — `tools/assess_akb_coverage.py:14` — and it only counts files. None of the 20 test modules opens a `docs/*.md`. There is no heading check, no frontmatter-completeness check, and no check that a page's `model_refs` resolve. Two live defects this already permits: 9 pages have **no `status:` line at all**, and 2 pages have body text a naive frontmatter parse misreads as `volume:`.

Relatedly, the three JSON Schemas in `model/schema/` are inert — `jsonschema` is imported nowhere. Because `validate()` ignores `properties`, the `packaged_as` package reference carried by all 156 library entities is completely unvalidated; a typo would pass CI silently.

**Remedy:** Add `validate_docs()` asserting required frontmatter keys, the ordered required-heading set (allowing `Not applicable — reason` bodies), and that every `model_refs`/`evidence_refs` entry resolves. Add a `jsonschema` pass over `graph.json` and each projection. Wire both into the same exit code.

### 7. The explorer ships without the graph (major)

`generated/explorer/index.html` is 46,779,848 bytes and contains **zero `<svg>` substrings and zero references to `overview.svg`**. The 43.8 MB inline `<script>` has zoom=0, `scale(`=0, viewBox=0. The charter's "interactive HTML/SVG explorer… expand/collapse, zoom" ships as HTML-only; "expand/collapse" is a `Show N more` toggle on flat lists (`build_explorer.py:80`, `const limit = 25`). Two of eight views resolve to **0 objects** — `layers` and `toolchains` — while 6 shipped diagram hyperlinks point at them, `README.md:80` tells users toolchains works, and `tests/test_diagrams.py:44-47` **asserts the dead link is present**. The toolchain data exists: 10 components carry a `toolchain` tag and 8 more carry `build-system`; the view simply filters on a `kind` that is never emitted. `docs/EXPLORER-DOMAIN-VIEWS.md` rationalizes it — "Empty views are intentional when the current snapshot contains no matching typed objects" — which is false here.

`overview.svg` renders 80 of 16,477 entities (0.49%) and 78 of 77,331 edges (0.10%), selected by **alphabetical ID order** and placed on a modulo-8 grid with no layout algorithm. The resulting census: 43 components, 16 filesystem-paths, 13 DLLs, 6 environments, 1 ecosystem, 1 executable — **zero packages, zero libraries, zero repositories**, and 16 of 80 nodes are man-page file paths.

**Remedy (one-line first):** redefine `layers`/`toolchains` as tag projections; make `build_explorer.py` fail the build when any view route referenced by a checked-in diagram resolves to 0 members; change the test from asserting the link exists to asserting its target is non-empty; fix `README.md:80`. Then embed `overview.svg` in `index.html`, replace alphabetical truncation with degree-ranked selection, shard the 43 MB inline literal to a fetched data file, paginate and debounce.

### 8. Seven charter-named library categories have zero coverage — and the repo's own ranking says to fix them first (critical)

Graphics, GUI, Audio, Video, Imaging, Logging, and Testing have **no page and no graph entity**. All 39 representative names I tested (cairo, gtk, qt5/qt6, freetype, harfbuzz, libpng, libjpeg, libtiff, webp, sdl, gstreamer, ffmpeg, opus, vorbis, flac, mesa, vulkan, imagemagick, log4c, spdlog, gtest, catch2, fftw, blas, lapack…) return **0 hits in `model/graph.json`**; in `docs/` they appear only inside boilerplate disclaimers. The 42-tag histogram over 208 entities contains no graphics/gui/audio/video/imaging/logging/testing tag.

The aggravating fact: `generated/library-candidates.md` — the repo's own centrality ranking — puts **`libpng` at #10 with 117 declared runtime dependents**, `libtiff` at 66, `libwebp` at 42, **above most libraries that do have pages**. So this violates even the narrowed selection rule in `charter/PROJECT-CHARTER.md` ("dependency centrality"). `model/catalog/current.json` already contains cairo, gtk3, qt6-base, libpng, ffmpeg, freetype, sdl2 — the data is there; only the authoring is absent.

**Remedy:** One representative page per missing category before any further per-environment sibling of an already-documented crypto/compression library. Start with libpng, libtiff, libwebp — your own ranking already nominates them ahead of everything in the current queue.

### 9. Named-subsystem gaps in Volumes 2, 3, 7, 9 (major)

- **Volume 9 (Git for Windows):** 4 pages / 1,356 words for 13 named components. `MSYS interaction`: 0 hits repo-wide. `HTTP transport`: 0 hits in Volume 9. Git Credential Manager never named as a product. Mintty appears once, in a Mermaid parenthetical. `docs/MINTTY.md` exists but is `volume: 5` (the MSYS2 package) and Volume 9 doesn't link it. For scale: `docs/GNU-BASH.md` alone (1,035 words) is 76% of all of Volume 9.
- **Volume 3 (MSYS Runtime):** 2 pages / 675 words for 12 named subsystems. No page titled for `msys-2.0.dll`; the 173 files mentioning it are boilerplate `uses-runtime` rows. It does carry real controlled evidence (MSYS 3.6.10 probes for process lifecycle, USR1 trap, symlink classification, `/dev/tty`) — it is not vacuous, it is two pages where thirteen subsystem architectures were asked for.
- **Volume 7 (Package Management):** 2 pages / 784 words for 13 topics, 11 of them existing as single rows in boundary tables whose third columns are headed "AKB evidence treatment." No pacman operation semantics, no sync-db/local-db formats, no dependency-resolution or transaction algorithm. Most of this is desk-researchable from upstream pacman docs and does **not** require the controlled observations the ledger gates the whole volume on.
- **Volume 2 (Windows Platform):** 1 page / 485 words for 8 subsystems. NT Kernel: 1 hit repo-wide, in the pasted charter transcript. The mechanism of drift is visible here: `charter/PROJECT-CHARTER.md` reclassified this to "Contextual scope" — defensible in isolation, but a unilateral narrowing of a charter Scope bullet with **no ADR**, in a repo whose governance says ADRs govern cross-cutting choices and whose `charter/adr/` is empty.

**Smaller, cheap:** `GNU-DIFFUTILS.md` and `GNU-PATCH.md` are the only two of the charter's 15 named GNU tools without pages, while Volume 5 authored 8 pages for tools the charter never named. Both are already modeled (`package:msys2:diffutils`, `package:msys2:patch` confirmed present). An LLVM umbrella page is missing (only `LLVM-LIBS.md`, filed `volume: 6`), so LLVM IR, the backend/codegen pipeline, and the `llvm-*` tool family have no home.

The mechanism behind both: completeness is measured against the project's **internally-derived role model** ("Every component family identified in the role model now has evidence-backed per-tool pages") rather than against the charter's explicit lists — so charter items that fell outside the role model never surfaced as gaps.

### 10. Documentation is not documentation-as-code (major)

**Charter:** *"All diagrams, indexes, reports, and repetitive object pages should be generated from the model"* — the repo's own words at `docs/PROJECT-DISCUSSION-RECORD.md:433`. No tool in `tools/` writes into `docs/`. All 252 pages, including ~157 repetitive per-library object pages, are hand-written. `README.md:56-65` publishes a "Model-first workflow" mermaid chart asserting `V["Validate"] --> D["Documentation"]` — an edge that exists in no tool. `model/graph.json` (208 entities / 670 relationships) is hand-edited: 180 of its 351 authored `requires` edges re-transcribe pairs the catalog already derives automatically as `runtime-depends-on`.

The ledger flattens this too: all 20 rows read "Partial" — one of the **eight** states `charter/PROJECT-CHARTER.md` requires coverage reports to distinguish. Volume 6 (157 pages) and Volume 18 (0 pages) carry the identical label, and 4 ledger citations point at pages whose frontmatter assigns them to a different volume. 241 of 252 pages are `status: partial`; a value applied to 96% of pages carries no signal.

Finally, `tools/Update-Akb.ps1` — the scheduled Windows refresh — runs `akb.py all` but never `build_catalog_views.py`, `build_explorer.py`, or `assess_akb_coverage.py`, all three of which CI runs before `git diff --exit-code`. Latent today (the catalog snapshot hasn't changed since Jul 30); divergent on the next real refresh.

---

## 3. What's Actually On Plan

Preserve these. They are genuinely strong and several exceed the charter.

**The model is the asset, and it is excellent.** `load_composed_graph()` produces **16,477 entities / 77,331 relationships**, composed from a hand-authored graph plus four generated projections. It honors the hard modeling distinctions most projects collapse: separate kinds for `library` vs `dll` vs `import-library` vs `static-library` vs `header` vs `pkg-config-module`; `upstream-project` vs `package` vs `package-artifact` vs `filesystem-path`; and separate edge types for `build-depends-on` / `runtime-depends-on` / `check-depends-on` / `optional-depends-on`, plus packaged dependency vs binary import (`imports-dll`). Reverse dependencies are **derived, never stored as duplicate edges** — exactly right.

**Validation and reproducibility are real, not decorative.** `validate()` enforces duplicate IDs, kind/type vocabulary membership, relationship endpoint resolution, evidence-ref resolution, and claim-subject resolution; `.github/workflows/validate.yml` runs it on every push and re-runs four generators before `git diff --exit-code`. **65 tests across 19 modules run green in 55s.** Catalog and inventory snapshots are content-addressed with `observed_at` timestamps and snapshot-to-snapshot change reports — the exact mechanism a rolling-release distribution needs.

**Evidence discipline exceeds the charter.** Every page carries `model_refs`/`evidence_refs`/`last_verified`; `DOCUMENTATION-STANDARD.md` defines a five-class evidence taxonomy and five-level confidence scale the charter never asked for. All **1,463 `model_refs` across 242 pages resolve** to real entity IDs — zero unresolved. 89 pages explicitly flag out-of-scope items rather than bluffing.

**Intellectual honesty is the project's best trait.** `generated/coverage-assessment.json` publishes its own `0.013%` payload coverage. `library-candidates.md` labels its output "package-name candidate; not a logical library identity." `WINDOWS-PLATFORM-BOUNDARIES.md` records that WMI queries were denied by host policy and declines to claim filesystem type. The ledger states the correct rule: *"Cross-links alone do not close a gap."* This is better practice than most enterprise architecture references. **The problem is that ROADMAP.md contradicts all of it.**

**Volume 8 (Toolchains) is the template to copy everywhere else.** 12 of 13 charter-named tools with dedicated pages, 15 pages / 12,311 words, at real depth (`GNU-GCC.md` 1,014 words across 15 standard headings; `CLANG.md` 850). **Volume 5 (GNU Userland)** is 13 of 15 covered and over-delivers with 15 tools the charter never named.

**Volume 6's quality per page has not degraded as volume grew** — `docs/ZLIB.md` and the most recently added `docs/LIBB2-UCRT64.md` carry the identical 15 standard headings. Template consistency is 197 of 252 pages byte-identical in heading sequence. And the per-environment sibling pages are **not clones**: measured across all 72 sibling pairs, median textual similarity is 0.215 and the maximum is 0.781 — they encode genuinely different package identities, dependency sets, and non-interchangeability prose. **The environment-variant strategy is correct and charter-aligned; only its monopoly on effort is the problem.**

**Explorer fundamentals that do work:** all 16,477 entities emit stable, percent-encoded, ID-based `#/object/` routes (regression-tested); search matches id/name/aliases/tags; forward *and* reverse dependency navigation is first-class via a typed `isDependency` predicate; breadcrumbs exist on every route; `overview.txt` is a complete 93,813-line textual fallback for the entire graph; every SVG carries `role="img"`, `aria-labelledby`, and substantive `<title>`/`<desc>`. Zero dependencies, fully offline-regenerable.

---

## 4. Why It Drifted

The git history explains it mechanically, without needing anyone to have made a bad decision.

**181 commits total: 101 on 2026-07-29, 52 on 2026-07-30, 28 on 2026-08-02.** The first two days built everything — the charter, the 20-volume index, the documentation standard, the schema, the vocabularies, the validator, the catalog importer, the deep-inventory pipeline, the explorer, all 8 diagrams, and one-page sketches for most volumes — and then checked off all 66 roadmap items. The scaffold was declared done. Every one of the 28 commits since is a Volume 6 library page: *"Add GMP (CLANG64); scope a new MSYS/UCRT64/CLANG64 audit vector"*, *"Close the libarchive (CLANG64) dependency cluster"*, *"Add BLAKE2 (libb2) (UCRT64), closing libarchive's last declined edge."*

Three forces then locked it in:

**The per-library workflow is a closed loop that generates its own backlog.** Adding a library page surfaces its declared dependencies, each of which becomes a new "open edge," each of which justifies another page, in each of three environments. It is tractable, it produces a clean commit message every time, and it **structurally cannot terminate** — it creates edges as fast as it closes them. Nothing bounds it. The other 18 volumes require different and harder work: writing a diagram generator, engineering SVG zoom into a 46 MB page, running a Windows-host collector at scale, or desk-researching pacman's transaction algorithm. None of those produce a satisfying commit every twenty minutes.

**The roadmap removed the alternatives from view.** With 66/66 checked and zero unchecked items, there is literally no open work item in the repo. Volume 6 dependency closure is not competing against Volume 3 subsystem pages on a backlog — it is the only visible work, because everything else is marked done. `grep -ci diagram ROADMAP.md` = 0. This is why "marked done but not done" is worse than "not done": it deletes the item from the backlog.

**Completeness was measured against internally-derived models rather than the charter.** The Volume 5 ledger row says "Every component family identified in the role model now has evidence-backed per-tool pages" — true against the role model, and that is exactly why Diffutils and Patch never surfaced. The Volume 8 row says the same, which is why the LLVM umbrella dissolved into its constituent tools unnoticed. The charter's explicit lists (15 GNU tools, 13 toolchain tools, 19 library categories, 13 runtime subsystems, 8 Windows subsystems, 13 Git-for-Windows components, 11 environment attributes) were never encoded as checklists anywhere a tool could see them.

`charter/PROJECT-CHARTER.md` is a contributing factor only in what it *omits*: it never mentions the 20 volumes or per-page structure, so nothing at governing-document level enforces volume balance. And with zero ADRs written, the two real scope narrowings that did occur (Windows → contextual, LLVM → decomposed) exist as prose in a charter rather than as recorded, reviewable decisions.

---

## 5. Course Correction

### (a) Stop doing

1. **Stop adding Volume 6 per-environment sibling pages.** Freeze net-new `-CLANG64` / `-UCRT64` / `-MSYS` variants of already-documented libraries until Volumes 2/3/4/7/9 each reach Volume 8's per-page depth. The marginal architectural value of the 97th variant page is far below the first Volume 3 subsystem page.
2. **Stop running the "close the next dependency edge" loop as the default work item.** It is unbounded by construction.
3. **Stop checking roadmap boxes for work that has a Partial ledger row.** Make it mechanically impossible (see below).
4. **Stop hand-authoring mechanical content** — dependency lists, reverse-dependency lists, artifact inventories — that `load_composed_graph()` can emit.

### (b) Start doing

1. **Generate docs from the model.** Emit the mechanical per-object sections (Dependencies, Reverse Dependencies, Package, DLLs, Headers, Artifacts, Mermaid subgraph) into per-page include blocks from `load_composed_graph()`.
2. **Generate diagrams from the model** in three formats (`.svg`, `.puml`, `.dot`), at the charter's actual L0–L7 semantics, with sibling and parent/child links.
3. **Enforce the standard in code** — `validate_docs()` for frontmatter and headings, `jsonschema` for the model, a roadmap/ledger consistency test, and a build failure when a diagram-referenced view route resolves to 0 members.
4. **Write the ADRs** for the two narrowings already in effect (Windows contextual scope; LLVM decomposed into its tools). Cheap, and it is what your own governance section requires.
5. **Encode the charter's explicit lists as machine-checkable checklists** in the ledger rows, so "complete per the role model" can never again read as "complete per the charter."

### (c) Keep doing

The evidence discipline, the `status: partial` honesty, the derived-not-stored reverse dependencies, the content-addressed snapshots, the CI reproducibility gate, the 65 green tests, the Volume 8 page template, and the per-environment variant *strategy* (just not its monopoly on effort).

### Top 3 next actions, in priority order

**1. Run the deep-inventory collector at scale. (~1 day of Windows-host runtime + ~2 days of template/generator work.)**
`tools/Collect-AkbDeepInventory.ps1` → `tools/import_deep_inventory.py` already emit `dll` / `import-library` / `static-library` / `header` / `pkg-config-module` / PE-export entities and are covered by `tests/test_deep_inventory.py`. They have been run against 2 packages. Batch them across the installed package set, then add a generated `## Artifacts` and `## Files and Directory Structure` block to the object template. **This one action closes six of the charter's ten per-library fields on all 157 pages, fills two of the six missing standard headings, populates the hollow Interfaces/Compatibility sections, moves payload coverage off 0.013%, and unblocks the L5/L6 diagrams — all from data already collectible with code already written.** Highest leverage in the audit by a wide margin.

**2. Write `tools/build_diagrams.py` and fix the roadmap/validator gates. (~3–4 days.)**
Emit `diagrams/level-*.svg` plus `.puml` and `.dot` from `load_composed_graph()` at the charter's own ladder (L4 Package, L5 Library, L6 Executable/DLL, L7 Source unit), with per-diagram parent/child/sibling links and a link to the owning doc page; add per-object Mermaid subgraphs to the page template from the 76,105 existing dependency edges. In the same change: relax `tests/test_diagrams.py:22`, add `validate_docs()`, add the roadmap-vs-ledger consistency test, make `build_explorer.py` fail on empty diagram-referenced views, and redefine `layers`/`toolchains` as tag projections (a one-line fix that makes 6 shipped dead links live). Wire `build_diagrams.py` into `validate.yml` and append the three missing generators to `Update-Akb.ps1`. This converts the model into the charter's most conspicuously missing artifact class and makes the drift self-detecting.

**3. Rebalance the volumes against a quota, starting with Volume 4. (~2 weeks of authoring, sequenced.)**
In order: (i) split `RUNTIME-ENVIRONMENTS.md` into six per-environment pages against all 11 charter attributes — Volume 6 is producing dozens of pages of per-environment ABI detail with nothing canonical to reference; (ii) `msys-2.0.dll` plus one page per Volume 3 subsystem on the 15-heading template, even if evidence-thin; (iii) one library page per missing category, starting with libpng/libtiff/libwebp, which your own `library-candidates.md` already ranks above most of what is documented; (iv) Volume 7 repository-layout and pacman-transaction pages (desk-researchable, not gated on observations); (v) Volume 9 per-component split; (vi) Volume 2 — either eight pages or the ADR; (vii) `GNU-DIFFUTILS.md`, `GNU-PATCH.md`, LLVM umbrella, real Volume 17, real Volume 18. Before any of it: **uncheck ROADMAP Increments 2, 3, 6, and 7's false items and replace the ledger's twenty "Partial" labels with your own eight-state vocabulary plus per-row page/line/heading metrics**, so progress becomes a burn-down instead of a claim.
---

## Audit Provenance

Produced 2026-08-02 by a 13-agent adversarial audit: six parallel dimension
auditors compared the original project charter against the repository, and an
independent verifier attempted to refute each finding by re-deriving its
evidence from source. Only findings that survived refutation appear above.

- **54 findings confirmed**, 4 refuted, 57 charter requirements found honored
- 13 agents, 425 tool calls, 1,110,076 tokens

| Dimension | Verdict | Confirmed | Refuted |
| --- | --- | --- | --- |
| Volume coverage and balance | severe-drift | 9 | 1 |
| Per-page documentation standards compliance | severe-drift | 9 | 1 |
| Diagrams and the Level 0-7 drill-down hierarchy | severe-drift | 10 | 1 |
| Volume 10 — Interactive Architecture Explorer | partial-drift | 9 | 0 |
| Machine-readable model and documentation-as-code | partial-drift | 8 | 1 |
| Named-subsystem scope coverage (charter "Scope" section, groups A–G) | severe-drift | 9 | 0 |

Headline claims were re-verified by hand after the audit completed:
`ROADMAP.md` 66 checked / 0 unchecked; Volume 18 zero pages; zero
diagram-to-diagram hyperlinks against 51 diagram-to-explorer hyperlinks;
`generated/explorer/index.html` 46,779,848 bytes containing zero `<svg>`
elements; zero tools writing into `docs/`; `package_payload_coverage`
2 of 15,711 packages (0.013%).
