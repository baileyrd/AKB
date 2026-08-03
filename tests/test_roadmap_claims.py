"""Bind every ROADMAP.md checkbox to machine-checkable evidence.

A checked roadmap item removes work from the backlog, so a wrongly checked
box is more costly than a missing one. These tests enforce that:

1. every roadmap item has a claim entry in model/roadmap-claims.json;
2. every checked item's assertions currently hold;
3. every claim entry corresponds to a real roadmap item.

Unchecked items keep their assertions as the gate for ticking the box later.
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import akb  # noqa: E402

CLAIMS_PATH = ROOT / "model" / "roadmap-claims.json"
ROADMAP_PATH = ROOT / "ROADMAP.md"
ITEM_RE = re.compile(r"^\s*- \[([ xX])\]\s+(.+?)\s*$")

# Mirrors the view definitions in tools/build_explorer.py. A view projects by
# entity kind, by tag, or by both.
EXPLORER_VIEWS = {
    "layers": {"kinds": ["layer"]},
    "packages": {"kinds": ["package", "package-artifact"]},
    "artifacts": {"kinds": ["dll", "executable", "import-library", "static-library", "filesystem-path"]},
    "libraries": {"kinds": ["library", "dll", "import-library", "static-library"]},
    "runtimes": {"kinds": ["runtime", "environment", "crt", "abi"]},
    "toolchains": {
        "kinds": ["toolchain", "compiler", "linker", "debugger", "build-system"],
        "tags": ["toolchain", "compiler", "linker", "debugger", "build-system"],
    },
    "repositories": {"kinds": ["repository", "mirror", "source-repository"]},
}


def view_members(graph, view):
    spec = EXPLORER_VIEWS[view]
    kinds = set(spec.get("kinds", []))
    tags = set(spec.get("tags", []))
    return [
        entity
        for entity in graph["entities"]
        if entity["kind"] in kinds or (tags & set(entity.get("tags", [])))
    ]

# The drift assessment quotes absent terms verbatim; excluding it keeps a
# report *about* missing coverage from counting *as* coverage.
TERM_SCAN_EXCLUDE = {"CHARTER-DRIFT-ASSESSMENT.md"}


def parse_roadmap():
    items = []
    for line in ROADMAP_PATH.read_text(encoding="utf-8").splitlines():
        match = ITEM_RE.match(line)
        if match:
            items.append((match.group(2), match.group(1).lower() == "x"))
    return items


def docs_in_volume(volume):
    matches = []
    for path in sorted((ROOT / "docs").glob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines()[:20]:
            if line.strip() == f"volume: {volume}":
                matches.append(path)
                break
    return matches


def docs_containing(term, paths=None):
    needle = term.lower()
    hits = []
    for path in paths if paths is not None else sorted((ROOT / "docs").glob("*.md")):
        if path.name in TERM_SCAN_EXCLUDE:
            continue
        if needle in path.read_text(encoding="utf-8").lower():
            hits.append(path)
    return hits


def check(assertion, graph, inventory_kinds):
    """Return (ok, detail) for one assertion."""
    kind = assertion["type"]

    if kind == "path_exists":
        target = ROOT / assertion["path"]
        return target.exists(), f"{assertion['path']} exists={target.exists()}"

    if kind == "doc_exists":
        target = ROOT / "docs" / assertion["doc"]
        return target.exists(), f"docs/{assertion['doc']} exists={target.exists()}"

    if kind == "min_lines":
        target = ROOT / assertion["path"]
        if not target.exists():
            return False, f"{assertion['path']} missing"
        actual = len(target.read_text(encoding="utf-8").splitlines())
        return actual >= assertion["lines"], f"{assertion['path']} has {actual} lines, need {assertion['lines']}"

    if kind == "term_in_path":
        target = ROOT / assertion["path"]
        if not target.exists():
            return False, f"{assertion['path']} missing"
        found = assertion["term"] in target.read_text(encoding="utf-8")
        return found, f"{assertion['path']} contains {assertion['term']!r}={found}"

    if kind == "min_docs_in_volume":
        actual = len(docs_in_volume(assertion["volume"]))
        return actual >= assertion["count"], (
            f"volume {assertion['volume']} has {actual} pages, need {assertion['count']}"
        )

    if kind == "term_in_volume":
        scope = docs_in_volume(assertion["volume"])
        actual = len(docs_containing(assertion["term"], scope))
        return actual >= assertion["min_files"], (
            f"'{assertion['term']}' in {actual} volume-{assertion['volume']} pages, "
            f"need {assertion['min_files']}"
        )

    if kind == "no_three_segment_claim_ids":
        import json as _json
        graph_raw = _json.loads((ROOT / "model" / "graph.json").read_text(encoding="utf-8"))
        offenders = [c["id"] for c in graph_raw.get("claims", []) if len(c["id"].split(":")) < 4]
        return not offenders, (
            f"{len(offenders)} claim ids still use three segments"
            + (f" (e.g. {offenders[0]})" if offenders else "")
        )

    if kind == "term_in_docs":
        actual = len(docs_containing(assertion["term"]))
        return actual >= assertion["min_files"], (
            f"'{assertion['term']}' in {actual} pages, need {assertion['min_files']}"
        )

    if kind == "min_graph_entities_of_kind":
        actual = sum(1 for e in graph["entities"] if e["kind"] == assertion["kind"])
        return actual >= assertion["count"], (
            f"graph has {actual} '{assertion['kind']}' entities, need {assertion['count']}"
        )

    if kind == "min_inventory_entities_of_kind":
        actual = inventory_kinds.get(assertion["kind"], 0)
        return actual >= assertion["count"], (
            f"inventory has {actual} '{assertion['kind']}' entities, need {assertion['count']}"
        )

    if kind == "explorer_view_nonempty":
        actual = len(view_members(graph, assertion["view"]))
        return actual > 0, f"explorer view '{assertion['view']}' resolves to {actual} objects"

    if kind == "min_observed_packages":
        report = json.loads((ROOT / "generated" / "coverage-assessment.json").read_text(encoding="utf-8"))
        actual = report.get("package_payload_coverage", {}).get("observed_packages", 0)
        return actual >= assertion["count"], (
            f"deep inventory covers {actual} packages, need {assertion['count']}"
        )

    raise AssertionError(f"unknown assertion type: {kind}")


class RoadmapClaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
        cls.claims = cls.document["items"]
        cls.items = parse_roadmap()
        cls.graph = akb.load_composed_graph()
        inventory = json.loads((ROOT / "model" / "inventory" / "current.json").read_text(encoding="utf-8"))
        cls.inventory_kinds = {}
        for entity in inventory.get("entities", []):
            cls.inventory_kinds[entity["kind"]] = cls.inventory_kinds.get(entity["kind"], 0) + 1

    def test_roadmap_has_items(self):
        self.assertGreaterEqual(len(self.items), 60)

    def test_every_roadmap_item_has_a_claim(self):
        """An item with no checkable definition of done cannot sit on the roadmap."""
        missing = [text for text, _ in self.items if text not in self.claims]
        self.assertEqual(
            missing,
            [],
            "roadmap items with no entry in model/roadmap-claims.json:\n  " + "\n  ".join(missing),
        )

    def test_every_claim_matches_a_roadmap_item(self):
        """Claims must not outlive the items they describe."""
        texts = {text for text, _ in self.items}
        orphaned = sorted(set(self.claims) - texts)
        self.assertEqual(
            orphaned,
            [],
            "claims with no matching roadmap item:\n  " + "\n  ".join(orphaned),
        )

    def test_every_checked_item_is_supported_by_evidence(self):
        """The load-bearing test: a ticked box must be backed by what it claims."""
        failures = []
        for text, checked in self.items:
            if not checked:
                continue
            for assertion in self.claims.get(text, []):
                ok, detail = check(assertion, self.graph, self.inventory_kinds)
                if not ok:
                    failures.append(f"[x] {text}\n      {detail}")
        self.assertEqual(
            failures,
            [],
            "roadmap items are checked but their evidence does not exist:\n    "
            + "\n    ".join(failures),
        )

    def test_unchecked_items_state_what_done_means(self):
        """An unchecked item still needs its gate, or ticking it later is unguarded."""
        bare = [text for text, checked in self.items if not checked and not self.claims.get(text)]
        self.assertEqual(
            bare,
            [],
            "unchecked roadmap items with no assertions:\n  " + "\n  ".join(bare),
        )

    def test_every_declared_assertion_type_is_implemented(self):
        """A declared type with no evaluator would gate nothing.

        Deriving the known-type set from the claims file means declaring a
        type is now enough to make it accepted. Only assertions on `[x]`
        items are ever evaluated, so an unimplemented type used solely on
        an unchecked item would sit here silently until the day someone
        ticked the box. Probing `check` closes that gap: a probe with the
        wrong keys raises KeyError, which still proves the dispatch matched
        — only the fallthrough means nothing implements it.
        """
        unimplemented = []
        for name in self.document["assertion_types"]:
            try:
                check({"type": name}, self.graph, self.inventory_kinds)
            except AssertionError as error:
                if "unknown assertion type" in str(error):
                    unimplemented.append(name)
            except Exception:  # pylint: disable=broad-except
                pass  # dispatch matched; missing probe keys are expected
        self.assertEqual(
            unimplemented,
            [],
            "assertion types declared in model/roadmap-claims.json but not "
            f"implemented in check(): {unimplemented}",
        )

    def test_assertion_types_are_known(self):
        """Types are declared once, in the claims file, and used from there.

        This set used to be duplicated here as a literal, so adding a type
        meant editing it in two places and forgetting one made the failure
        look like a bad claim rather than a stale test.
        """
        declared = set(self.document["assertion_types"])
        for text, assertions in self.claims.items():
            for assertion in assertions:
                self.assertIn(
                    assertion["type"],
                    declared,
                    f"{text}: unknown assertion type {assertion['type']}",
                )


if __name__ == "__main__":
    unittest.main()
