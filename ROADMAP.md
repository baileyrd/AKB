# Architecture Knowledge Base Roadmap

Every item below is bound to a machine-checkable claim in
[`model/roadmap-claims.json`](model/roadmap-claims.json), enforced by
`tests/test_roadmap_claims.py`.

The rules that test enforces:

1. Every roadmap item must have a claim entry. An item with no stated,
   checkable definition of done cannot appear here.
2. Every `[x]` item's assertions must currently hold. A box cannot be
   ticked while the evidence for it does not exist.
3. `[ ]` items carry their assertions too — that is what "done" will mean
   when the box is ticked.

**Correction, 2026-08-02**: this file previously recorded 66 of 66 items
complete. A charter audit ([Charter Drift Assessment](docs/CHARTER-DRIFT-ASSESSMENT.md))
found that fifteen of those checkmarks covered work that was not written,
and that several charter deliverables had no roadmap entry at all and so
were invisible as work. The false checkmarks are cleared below with their
disproving evidence, and the missing work is added as Increments 9–12.
A checked box removes an item from the backlog, so a wrong one is more
costly than a missing one.

## Increment 0 — Foundation

- [x] Governing charter
- [x] Information architecture
- [x] Twenty-volume master index
- [x] Documentation standard
- [x] Typed graph schema
- [x] Entity and relationship vocabularies
- [x] Bootstrap graph
- [x] Source registry
- [x] Validation and index generation
- [x] Architecture Decision Record template
- [x] Claim-level evidence implementation
- [x] Coverage metrics and quality gates

## Increment 1 — Evidence and inventory pipeline

The collection *pipeline* is built and tested. Its *coverage* is 2 of
15,711 packages (`generated/coverage-assessment.json` →
`package_payload_coverage.percent` = 0.013), so the extraction items below
are cleared: the capability exists, the extraction has not been performed.

**BLOCKED — needs a Windows host with MSYS2 installed.** The six unchecked
items in this increment, and the three in Increment 5 that project their
output, are not undone work in the ordinary sense. They are the only items
on this roadmap that cannot be closed from this environment at all.
`tools/Collect-AkbDeepInventory.ps1` asks `<Msys2Root>\usr\bin\pacman.exe`
which files each installed package owns and then reads those files' PE
headers. That needs a Windows machine with MSYS2 actually installed and the
packages of interest present — properties of a host, not dependencies that
could be added. Every session this knowledge base has run in has been a
Linux container.

[The Deep-Inventory Blocker](docs/DEEP-INVENTORY-BLOCKER.md) states this
once, names the six statements elsewhere in the knowledge base that are
currently qualified by it, and gives the single command that would close
it. The nine items stay unchecked deliberately: ticking them would remove
the largest remaining gap here from the backlog while it is entirely open.

- [x] Register official upstream sources
- [x] Discover and ingest enabled repository package metadata through pacman
- [x] Preserve content-addressed catalog snapshots and integrity manifests
- [x] Generate package dependency and reverse-navigation relationships
- [x] Produce package addition, removal, and version-change reports
- [x] Support on-demand and Windows Scheduled Task refresh
- [x] Ingest repository database archives directly
- [x] Statically ingest package recipes without executing PKGBUILDs
- [x] Build the deep-inventory collection pipeline
- [ ] Extract installed and repository package-file manifests
- [ ] Extract PE imports, exports, subsystem, architecture, and debug metadata
- [ ] Extract static/import archive members
- [ ] Index headers, pkg-config files, and CMake metadata
- [x] Record artifact checksums, versions, retrieval dates, and licenses
- [x] Produce reproducible deep-inventory snapshot manifest
- [ ] Extract and analyze uninstalled binary payloads from package archives
- [x] Resolve recipe source checksums against downloaded upstream payloads
- [ ] Run deep inventory across the installed package set

## Increment 2 — Ecosystem baseline

- [x] L0 ecosystem context
- [x] L1 eight-layer architecture
- [x] L2 domain decomposition
- [x] Terminology and boundary decisions
- [x] MSYS2 versus MinGW-w64 role model
- [x] Bounded runtime observation and current-environment report
- [x] Environment comparison and migration matrix
- [x] Per-environment architecture pages for MSYS, UCRT64, CLANG64, CLANGARM64, MINGW64, and MINGW32

**Closed 2026-08-02.** The charter requires each environment documented
separately against eleven attributes; the matrix satisfied the roadmap item
as worded but not the charter requirement. Six pages now cover ABI, compiler,
runtime, CRT, linker, executable format, package repository, strengths,
weaknesses, compatibility, and migration strategy per environment. Volume 4
goes from 1 page to 7.

## Increment 3 — Runtime and package management

- [x] MSYS runtime initialization
- [x] Process, fork, exec, signal, path, mount, filesystem, symlink, and PTY models
- [x] pacman architecture and transaction sequences
- [x] repository, mirror, signing, key, cache, hook, and database models
- [x] msys-2.0.dll subsystem architecture pages

**Partly closed 2026-08-02.** Volume 3 goes from 2 pages to 11: the runtime
itself now has a page, and each of its eight documented subsystems has one,
modeled as `subsystem:msys2:*` entities under `runtime:msys2:msys-2.0.dll`.
The pages carry the five bounded 2026-07-30 probes where they apply and
state plainly where they do not — path conversion, the mount table, and
environment conversion have no observation at all.

**Volume 7 closed 2026-08-02** to the same standard: 2 pages to 7, covering
the transaction model, sync/local database split, repository sections and
precedence, signature policy, and the alpm hook format — each grounded in
the pacman manual pages rather than recalled. `pacman` itself is now modeled
as `package-manager:archlinux:pacman`; it had no entity at all. Every page
carries the standing caveat that the manual pages are Arch's and MSYS2's
effective paths and configuration remain uncaptured.

## Increment 4 — Toolchains and userland

- [x] GCC, LLVM, Binutils, Clang, LLD, GDB, and LLDB
- [x] CMake, Meson, Autotools, Make, Ninja, and pkg-config
- [x] GNU userland component deep dives
- [x] generated-artifact and build-flow mappings
- [x] GNU Diffutils and GNU Patch pages
- [x] LLVM umbrella page covering IR, codegen, and the llvm-* tool family

**Closed 2026-08-02.** `diffutils` and `patch` had catalog packages but no
component entities and no pages, despite being the mechanism every MSYS2
package recipe uses to carry source modifications. Both pages converge on
the same ecosystem-specific finding: `patch(1)` states that "on Windows,
reads and writes do transform line endings by default, and patches should
be generated by `diff --binary` when line endings are significant". Three
layers can each independently mangle a patch — how it was generated, the
CRLF heuristic `patch` applies on read, and the MSYS mount options. The
third is uncaptured here, so both pages stop at documented tool behavior
rather than claiming composed behavior on a real install.

`LLVM.md` is the umbrella Clang, LLD, and LLDB had been sitting under
without one: the SSA-based typed IR in its three equivalent forms, the
seven-stage code generator, and the `llvm-*` tool family split as upstream
splits it — tools that work on LLVM's own representation, and the ones
upstream itself calls "GNU binutils replacements". The measured part is
the MSYS2 packaging, which shows `llvm` to be a metapackage pinning
`llvm-libs` and `llvm-tools` at an exact version, the MSYS and native
sides on different major versions (21.1.8 against 22.1.8), and a 3.4 GB
side-by-side `llvm-21`.

Both pages state that no package file manifest exists, so what the
`llvm-tools` package actually installs is listed from upstream rather than
observed.

gnu.org returned 403 through this environment's proxy, so the diff and
patch manual pages were read from man7.org's mirror. Both evidence records
say so.

## Increment 5 — Package and library catalog

- [x] Repository-to-package inventory
- [ ] Package-to-file inventory
- [ ] Binary-to-DLL dependency graph
- [ ] Header and metadata indexes
- [x] Library family classification
- [x] Reverse dependency and impact analysis
- [x] Library coverage for the graphics, GUI, audio, video, imaging, logging, and testing categories
- [x] Carry build-time and check-time dependency edges from the PKGBUILD recipes

**The three cleared items are BLOCKED behind Increment 1's extraction
work**, which needs a Windows host with MSYS2 installed — see
[The Deep-Inventory Blocker](docs/DEEP-INVENTORY-BLOCKER.md). They are
projections of data that collection would produce, so closing them first
would mean generating reports over two packages and calling the ecosystem
covered. `generated/binary-dependency-report.md` is 22 lines and
`generated/development-artifact-catalog.md` is 11 lines, both covering the
same two packages.

**Library categories closed 2026-08-02.** Seven pages, one per category,
each ranked from the catalog snapshot by dependents summed across
environment variants — which is the correction that matters, because
`generated/library-candidates.md` counted variants separately and so
ranked `libpng` tenth when it is fourth.

The sharpest result was the testing page. Ten test frameworks across
roughly 47 packages recorded **one** dependent between them — not a fact
about the ecosystem but a gap in the projection, which carried no
build-time or check-time edges at all.

**That gap is closed, 2026-08-02.** `tools/import_repository_db.py` read
`%DEPENDS%` and `%OPTDEPENDS%` from each package's `desc` record and
dropped `%MAKEDEPENDS%` and `%CHECKDEPENDS%`. Both were in the repository
database the whole time — `%MAKEDEPENDS%` appears in 662 of the 798 `msys`
records. `model/recipe-dependencies/current.json` now carries 60,703
`build-depends-on` and 3,383 `check-depends-on` edges, and
`build-depends-on` is the largest single edge type in the composed graph,
ahead of `runtime-depends-on` at 41,061.

It is an **additive** projection rather than a catalog refresh, and
deliberately so: the committed catalog snapshot's source archives are no
longer byte-identical on the mirror, and in four days 1,082 of 15,711
packages changed version. Re-collecting to add build edges would have
silently invalidated every version quoted in prose across the
documentation. So the projection contributes relationships only, emits an
edge only when both endpoints already exist in the catalog, and drops and
counts the rest — 10,195 of 67,703 declared. Two dates, both recorded,
neither overwriting the other.

What it revealed:

- **Testing goes from 1 dependent to 202**, and `python-pytest` turns out
  to have 1,262 — 1,254 of them check-time — making it the ecosystem's
  most-depended-upon test framework by an order of magnitude while being
  completely invisible.
- **The build-time graph is a different graph.** Its leaders — `ninja`
  4,455, `cmake` 4,194, `python-installer` 4,187, `python-build` 4,132,
  `python-setuptools` 3,206, `autotools` 2,593, `pkgconf` 2,081 — appear
  nowhere in any runtime ranking, and between them are declared by more
  packages than any runtime dependency in the catalog.
- **Logging was not an artifact.** Every logging library records zero on
  both new edge classes, so that category's low counts are a real fact
  about how logging is consumed. One of the logging page's three candidate
  explanations is ruled out by measurement rather than left open.

## Increment 6 — Git for Windows

- [x] Distribution boundary and divergence
- [x] Launcher, Git Bash, Mintty, and shell startup
- [x] Native Git, MSYS interaction, SSH, HTTP, credentials, crypto, and DLL loading
- [x] Package and source mappings

**Closed 2026-08-02.** Volume 9 goes from 4 pages to 8. The three terms that
appeared nowhere — `MSYS interaction`, `HTTP transport`, `credential
manager` — each now have a page, and mintty is named as the terminal host
rather than parenthesised in a diagram label. Facts come from
gitforwindows.org, gitcredentials(7), and git-config, fetched this session.

Two things the batch did not resolve and says so: Git Credential Manager's
own repository was unreachable from this environment, so its internals are
not independently verified; and no PE import analysis of any Git for Windows
binary exists, which is what the DLL-loading page would need to move past
mechanism.

## Increment 7 — Explorer

- [x] Stable object routes and deep links
- [x] Search, filters, breadcrumbs, and cross-references
- [x] Progressive graph expansion and collapse
- [x] Forward and reverse dependency navigation
- [x] Layer, package, library, runtime, toolchain, and repository views
- [x] Accessible SVG and textual fallbacks
- [x] Large-graph performance tests
- [ ] Graphical zoomable graph rendering in the explorer page

**Closed 2026-08-02.** The `layers` and `toolchains` views had resolved to
zero objects: `toolchains` projected only by an entity `kind` the graph
never emits, and the eight layers documented in
[the eight-layer architecture](docs/EIGHT-LAYER-ARCHITECTURE.md) had never
been authored as entities despite `layer` being a valid kind. Views now
project by kind, tag, or both, and the eight layers are modelled. All seven
views resolve — `toolchains` to 17 objects, `layers` to 8 — and the six
diagram hyperlinks that dead-ended in `toolchains` are live.
`tests/test_diagrams.py` now fails the build if any diagram links to a view
that renders nothing.

**Withdrawn from this branch 2026-08-02.** A zoomable `#/graph/<id>` view
was built here, then dropped: `main` had independently gained a real
interactive graph view in the explorer (#142) while this branch was in
flight, and shipping two implementations of the same feature would be worse
than shipping one. `main`'s is the one kept.

The box stays unticked here because this branch no longer implements it.
It is satisfied on `main`, and merging resolves it there rather than being
asserted from a branch that does not carry the code.

## Increment 8 — Assurance and operations

- [x] Threat model and supply-chain analysis
- [x] Performance experiments and hot-path analysis
- [x] Upgrade, rollback, repair, and migration guides
- [x] Developer and operator workflows
- [x] Initial continuous refresh, difference reports, and historical snapshots
- [x] Multi-source refresh orchestration, retention policy, and alerting

**Closed 2026-08-02.** `docs/PERFORMANCE-EXPERIMENTS.md` benchmarked this
repository's own `validate`/`generate-indexes`/`build-explorer` operations
while filed under Volume 17, which made the volume look covered. It is now
Volume 20 and says so at the top.
[Ecosystem Performance Architecture](docs/ECOSYSTEM-PERFORMANCE-ARCHITECTURE.md)
covers the four hot paths the item names: fork emulation, path translation,
mount-table lookup, and pacman transaction cost.

It contains no MSYS2 timings and says so in its first paragraph, because no
Windows host was available. What it does contain: the published `fork`
algorithm with the cost properties that follow from it, the one quantified
figure upstream stands behind (substituting `spawn` for `fork`/`exec`
"increased compilation speeds by twenty to thirty percent"), the documented
longest-prefix mount-table rule, the executability-probe I/O cost, and the
pacman transaction shape measured from this repository's own catalog
projection — 44,683 dependency edges over 15,711 packages, mean out-degree
2.84, `python` at 999 dependents.

## Increment 9 — Windows platform

**Closed 2026-08-02.** The charter's Scope section names eight Windows
subsystems; none had a roadmap entry, so none was visible as work. Volume 2
goes from 1 page to 8 — one boundary page per subsystem, plus the existing
table now linking to each.

They are deliberately *boundary* pages, not Windows internals: what MSYS2
depends on, where the claim stops, what evidence an exact claim needs, and
what this knowledge base holds. ADR 0001 records that narrowing, which
`PROJECT-CHARTER.md` had made without one.

The filesystem page carries the sharpest finding: WMI volume queries were
denied by host policy, so volume type — the leading candidate explanation
for Volume 3's unexplained `ln -s` / `test -L` discrepancy — is precisely
what this volume was prevented from collecting.

- [x] NT Kernel, Win32, and Console/ConPTY boundaries
- [x] Filesystem, Registry, Security, and Networking boundaries
- [x] ADR recording the contextual-scope narrowing for Windows internals

## Increment 10 — Diagram generation

The charter's Diagram Hierarchy section required Level 0 through Level 7
drill-down with every diagram hyperlinking to related diagrams. No roadmap
item mentioned diagrams, and the eight hand-authored SVGs had zero
hyperlinks to each other on level semantics that did not match the charter.

**Largely closed 2026-08-02.** `tools/build_diagrams.py` generates the ladder
from the composed model, emitting SVG, PlantUML, and Graphviz per level on
the charter's own semantics, with parent/child navigation and a link to each
level's canonical page. The hand-authored set is retired. Per-object
subgraphs remain outstanding.

- [x] Generate diagrams from the composed model
- [x] Emit PlantUML and Graphviz alongside SVG
- [x] Renumber levels to the charter ladder and link parent, child, and sibling
- [x] Per-object dependency subgraphs on documentation pages

## Increment 11 — Documentation as code

The companion objective requires diagrams, indexes, reports, and repetitive
object pages to be generated from the model. When this increment opened, no
tool in `tools/` wrote into `docs/` and all 253 pages were hand-authored.
Three now do: `build_object_diagrams.py`, `build_object_facts.py`, and
`build_volume_ledger.py`, each owning only what lies between its markers.

- [x] Generate mechanical object-page sections from the composed model
- [x] Validate documentation pages in `tools/akb.py`
- [x] Enforce the model schemas in CI
- [x] Enforce roadmap claims against evidence
- [x] Normalise the nine three-segment claim identifiers

**Schema enforcement closed 2026-08-02.** The item read "with jsonschema";
that package is unavailable here and the repository has no dependency
manifest and no CI install step. `tools/schema_check.py` implements the
measured subset of JSON Schema the three schemas actually use and rejects
anything outside it, so the deliverable — schemas enforced on every push —
is unchanged while the zero-dependency property is kept. Recorded as
[ADR 0002](charter/adr/0002-dependency-free-schema-checking.md) rather than
silently reworded. Running the schemas for the first time found that 30
claim identifiers use four segments and 9 use three; the nine are the
outliers and normalising them is added above rather than blessed.

**Mechanical sections closed 2026-08-02.** `tools/build_object_facts.py`
writes a facts block into 233 object pages, placed after the H1 and before
the first authored section: the subject's model ID, kind, status,
confidence, authority, applicable environments, upstream project, and
packaging — with version, license, architecture, and installed size read
from the catalog snapshot — plus every evidence record on the object with
its class and retrieval date, and every claim whose subject it is.

The defect this fixes is drift rather than absence. Each page restated
those fields in prose by hand, and nothing checked they still matched:
`validate_docs` verifies that a `model_ref` resolves, not that the sentence
beside it is still true after a catalog refresh. The generated fields are
now correct by construction and the prose around them is untouched.

It deliberately generates no prose. Purpose, boundaries, and analysis stay
hand-authored; only fields with one right answer in the model are
generated, and only for entity kinds that name an object rather than a
topic.

**Claim identifiers normalised 2026-08-02.** All nine three-segment
identifiers now use the four-segment `claim:<kind>:<subject>:<aspect>`
form, together with every citation of them in documentation prose — ten
pages carried them by name, which is why the rename was deferred when the
inconsistency was first found rather than done on the spot.

The schema was tightened at the same time: `$defs/claimId` previously
accepted both forms with a description explaining why. Its pattern now
requires four segments, so the short form cannot return. That was verified
by reintroducing `claim:library:zlib-hub` and confirming `schema_check.py`
rejects it.

## Increment 12 — Volume balance

Volume 6 holds 157 of 253 pages and 66.9% of all prose; Volume 18 has none.
Eleven volumes hold fourteen pages between them.

- [x] Volume 17 performance architecture for the ecosystem
- [x] Volume 18 developer guide

**Volume 18 closed 2026-08-02.** The volume had zero pages; the ledger
pointed at `DEVELOPER-WORKFLOW.md`, which is about this
repository's own tooling and stays in Volume 20. Five pages now answer the
charter's question in its own five parts — select, build, debug, package,
migrate — sourced from MSYS2's own wiki and documentation rather than
inherited from Arch or Cygwin. The load-bearing facts: the `msys-2.0.dll`
link test as the one decision everything follows from, the `base-devel`
trap (it contains neither `gcc` nor `binutils`), the `makepkg` versus
`makepkg-mingw` split with the MSYS shell used for both, the three
just-in-time debugging cases including the inherited `SetErrorMode` flag
that silently suppresses the debugger for native children of MSYS
processes, and the host-triplet change from `*-pc-msys` to `*-pc-cygwin`
that makes old `configure` matches fall through without error.

No command on any of the five pages has been run by this knowledge base,
and each page says so.

`tests/test_doc_links.py` was added alongside them: nothing had ever
checked that a Markdown link points at a file that exists. All 290 pages
pass, and the test was verified to fail on an introduced break.
- [x] Per-volume page and heading metrics in the coverage ledger
- [x] Replace the ledger's uniform "Partial" with the charter's eight coverage states

**Both closed 2026-08-02.** The ledger reported "Partial" for all twenty
volumes, so a volume of 164 pages and a volume of 596 words across two
stubs read identically. `tools/build_volume_ledger.py` now measures pages,
`##` headings, words, words per page, and distinct evidence and model
references per volume, writing them into a marker-delimited block. The
coverage state is *not* computed — it is a judgment, authored in
`model/volume-coverage.json` with a rationale per volume so a change to it
appears in a diff beside its reasoning.

Generated blocks are excluded from the prose counts, so a volume cannot
inflate its word count by carrying more diagrams.

What the measurement then showed, none of which was visible before:

- Volume 6 holds 164 of 300 pages and 55.2% of all prose.
- **Nine volumes cite no evidence record on any page** — 1, 10, 11, 12,
  13, 14, 15, 16, 19. Their claims are authored rather than sourced, and
  that is now stated on the ledger rather than hidden behind a uniform
  label.
- Volume 10 has the lowest prose density in the knowledge base at 179
  words per page, while documenting an explorer that is itself built and
  tested.
- Three of the charter's eight states are in use: `partial`, `inferred`,
  and `planned`. `inferred` marks Volumes 2, 7, 17, and 18 — sound
  material reasoned from documentation rather than observed, which is a
  gap in evidence class rather than in extent. Volume 12 is `planned`.

`tests/test_volume_ledger.py` parses `charter/PROJECT-CHARTER.md` and
fails if the declared state vocabulary drifts from the charter's, so the
eight states cannot quietly become seven or nine.
