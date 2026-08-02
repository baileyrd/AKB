#!/usr/bin/env python3
"""Project build-time and check-time dependencies from the PKGBUILD trees.

`import_build_dependencies.py` reads `%MAKEDEPENDS%` and `%CHECKDEPENDS%` from
the pacman repository databases. That is what the *built package* records, and
it turned out to be an unreliable measure of what a package is built against:
a library needed at both build and run time is declared once, in `depends`, so
`SDL2_image` builds against SDL2 while recording zero build edges.

The recipe is the authority. This tool reads the same two fields from the
PKGBUILDs themselves, which is the declaration makepkg actually consumes, and
lets the two sources be compared rather than trusted.

Two things make recipe data harder than database data, and both are handled
here rather than papered over:

**Interpolation.** MINGW recipes name packages as
`${MINGW_PACKAGE_PREFIX}-python-${_realname}`. The prefix is expanded across
the five environment prefixes, pairing like with like -- a UCRT64 package
build-depends on UCRT64 packages, never on CLANG64 ones. Recipe-local `_`
scalars come from the `variables` field captured at collection time, so no
source tree is needed at import.

**Virtual provides.** Recipes name `cc`, not `gcc`. Roughly 8,800 edges point
at names no package carries but some package *provides*. Those resolve through
the catalog's `provides` metadata, and every edge records which route it took
in a `resolved_via` property, so a reader can discount them.

Names that still contain `$` after expansion, and names that resolve neither
directly nor through a provide, are dropped and counted. The counts are in the
snapshot manifest and in the projection's evidence record.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "model" / "catalog" / "current.json"
OUTPUT = ROOT / "model" / "recipe-dependencies" / "current.json"
SNAPSHOTS = ROOT / "evidence" / "recipe-dependency-snapshots"

SCHEMA_VERSION = "1.0.0"
EVIDENCE_ID = "evidence:recipe-dependencies:current"

# The five package-name prefixes MINGW_PACKAGE_PREFIX takes, one per
# environment. MSYS-side recipes use no prefix at all.
PREFIXES = (
    "mingw-w64-x86_64",
    "mingw-w64-i686",
    "mingw-w64-ucrt-x86_64",
    "mingw-w64-clang-x86_64",
    "mingw-w64-clang-aarch64",
)

FIELD_RELATIONS = (("makedepends", "build-depends-on"), ("checkdepends", "check-depends-on"))

PREFIX_REF = re.compile(r"\$\{?MINGW_PACKAGE_PREFIX\}?")
VAR_REF = re.compile(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?")
# A dependency entry that is really shell fragmentation from a conditional
# array. Recipes such as `makedepends=($([[ $CARCH == i686 ]] && echo foo))`
# defeat static parsing; the fragments are dropped, not guessed at.
SHELL_NOISE = re.compile(r"^[\[\]\(\)|&;<>!\\\"'`]+$|^(echo|test|if|then|else|fi)$")


class RecipeDependencyError(Exception):
    """Raised when a recipe collection is unusable."""


def clean(value: str) -> str:
    """Strip an optdepends description and any version constraint."""
    value = str(value).split(":", 1)[0]
    for char in "<=>":
        value = value.split(char)[0]
    return value.strip()


def expand(value: str, prefix: str | None, variables: dict[str, str]) -> str:
    """Substitute the environment prefix and recipe-local scalars."""
    if prefix is not None:
        value = PREFIX_REF.sub(prefix, value)
    for _ in range(4):  # bounded: recipe variables may reference each other
        replaced = VAR_REF.sub(lambda m: variables.get(m.group(1), m.group(0)), value)
        if replaced == value:
            break
        value = replaced
    return value


def catalog_index() -> tuple[dict[str, str], dict[str, str]]:
    """Return package-name -> id, and provide-name -> providing package id."""
    if not CATALOG.is_file():
        raise RecipeDependencyError("model/catalog/current.json is missing")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    packages: dict[str, str] = {}
    provides: dict[str, str] = {}
    for entity in catalog.get("entities", []):
        if entity.get("kind") != "package":
            continue
        packages[entity["name"]] = entity["id"]
    for entity in catalog.get("entities", []):
        if entity.get("kind") != "package":
            continue
        declared = (entity.get("properties") or {}).get("provides") or ""
        for item in declared.split(";"):
            name = item.split("=")[0].strip()
            # A real package always wins over a virtual name it shares.
            if name and name not in packages:
                provides.setdefault(name, entity["id"])
    return packages, provides


def load_recipes(sources: list[Path]) -> list[dict[str, Any]]:
    recipes: list[dict[str, Any]] = []
    for source in sources:
        path = source / "recipes.jsonl" if source.is_dir() else source
        if not path.is_file():
            raise RecipeDependencyError(f"no recipes.jsonl in {source}")
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                recipes.append(json.loads(line))
    if not recipes:
        raise RecipeDependencyError("no recipes collected")
    return recipes


def relationship_id(relation: str, source: str, target: str) -> str:
    key = f"{relation}|{source}|{target}".encode("utf-8")
    prefix = "build" if relation == "build-depends-on" else "check"
    return f"relationship:recipe-dependencies:{prefix}-{hashlib.sha256(key).hexdigest()[:20]}"


def project(recipes: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, int], collections.Counter]:
    packages, provides = catalog_index()
    edges: dict[str, dict[str, Any]] = {}
    stats: collections.Counter = collections.Counter()
    unresolved: collections.Counter = collections.Counter()

    for recipe in recipes:
        # Recipe-local `_` scalars, plus the standard PKGBUILD fields that
        # package names interpolate. `pkgname=("${pkgbase}" "lib${pkgbase}")`
        # is a common shape and resolves to nothing without pkgbase here.
        variables = dict(recipe.get("variables") or {})
        for field in ("pkgbase", "pkgver", "pkgrel"):
            value = recipe.get(field)
            if value and field not in variables:
                variables[field] = str(value)
        names = [clean(name) for name in recipe.get("pkgname", [])]
        if not names:
            continue
        for field, relation in FIELD_RELATIONS:
            declared = [clean(item) for item in recipe.get(field, [])]
            declared = [item for item in declared if item and not SHELL_NOISE.match(item)]
            if not declared:
                continue
            uses_prefix = "MINGW_PACKAGE_PREFIX" in " ".join(names + declared)
            for prefix in (PREFIXES if uses_prefix else (None,)):
                sources = [expand(name, prefix, variables) for name in names]
                targets = [expand(item, prefix, variables) for item in declared]
                for source_name in sources:
                    source_id = packages.get(source_name)
                    if source_id is None:
                        stats["source_unresolved"] += 1
                        continue
                    for target_name in targets:
                        stats["declared"] += 1
                        if "$" in target_name:
                            stats["target_uninterpolated"] += 1
                            unresolved[target_name] += 1
                            continue
                        target_id = packages.get(target_name)
                        route = "name"
                        if target_id is None:
                            target_id = provides.get(target_name)
                            route = "provides"
                        if target_id is None:
                            stats["target_absent"] += 1
                            unresolved[target_name] += 1
                            continue
                        stats[f"resolved_via_{route}"] += 1
                        identifier = relationship_id(relation, source_id, target_id)
                        if identifier in edges:
                            continue
                        edges[identifier] = {
                            "id": identifier,
                            "type": relation,
                            "source": source_id,
                            "target": target_id,
                            "status": "verified",
                            "confidence": "verified",
                            "scope": "package-recipe",
                            "condition": "",
                            "properties": {
                                "resolved_via": route,
                                "declared_as": target_name,
                                "recipe": str(recipe.get("path", "")),
                            },
                            "evidence_refs": [EVIDENCE_ID],
                        }

    stats["projected"] = len(edges)
    stats["build"] = sum(1 for e in edges.values() if e["type"] == "build-depends-on")
    stats["check"] = sum(1 for e in edges.values() if e["type"] == "check-depends-on")
    stats["recipes"] = len(recipes)

    observed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    digest = hashlib.sha256(
        "".join(sorted(edges)).encode("utf-8")
    ).hexdigest()[:12]
    snapshot_id = f"{observed_at.replace('-', '').replace(':', '').split('.')[0]}Z-{digest}"

    projection = {
        "schema_version": SCHEMA_VERSION,
        "snapshot": {
            "id": snapshot_id,
            "observed_at": observed_at,
            "description": (
                "Generated projection of build-time and check-time dependencies "
                "declared in MSYS2 and MinGW-w64 PKGBUILD recipes. Additive: "
                "relationships only, restricted to packages already present in "
                "the catalog projection."
            ),
            "upstream_versions": {"collector": "1.0.0"},
        },
        "entities": [],
        "relationships": sorted(edges.values(), key=lambda item: item["id"]),
        "claims": [],
        "evidence": [{
            "id": EVIDENCE_ID,
            "class": "observed",
            "title": "MSYS2 and MinGW-w64 recipe build-time and check-time dependencies",
            "locator": f"evidence/recipe-dependency-snapshots/{snapshot_id}/manifest.json",
            "retrieved_at": observed_at,
            "upstream_version": None,
            "integrity": digest,
            "notes": (
                f"Statically parsed from {stats['recipes']} PKGBUILD files without "
                "executing them. MINGW_PACKAGE_PREFIX is expanded across the five "
                "environment prefixes, pairing like with like; recipe-local scalars "
                "come from the parser's captured `variables`. "
                f"{stats.get('resolved_via_provides', 0)} edges resolve through a "
                "virtual provide rather than a package name and are marked "
                "`resolved_via: provides`. Dropped and counted: "
                f"{stats.get('target_uninterpolated', 0)} names still containing a "
                "shell expansion after substitution, and "
                f"{stats.get('target_absent', 0)} naming neither a package nor a "
                "provide in the catalog projection. Recipes are collected from the "
                "upstream trees at a later date than the catalog snapshot; edges "
                "whose endpoints are not both in the catalog are not emitted."
            ),
        }],
    }
    return projection, dict(stats), unresolved


def write_snapshot(projection: dict[str, Any], stats: dict[str, int],
                   unresolved: collections.Counter, sources: list[Path]) -> Path:
    snapshot = SNAPSHOTS / projection["snapshot"]["id"]
    snapshot.mkdir(parents=True, exist_ok=True)
    (snapshot / "manifest.json").write_text(
        json.dumps({
            "schema_version": SCHEMA_VERSION,
            "generated_at": projection["snapshot"]["observed_at"],
            "collector": "tools/import_recipe_dependencies.py",
            "sources": [str(item) for item in sources],
            "statistics": stats,
            "unresolved_top": unresolved.most_common(40),
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    return snapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", nargs="+", type=Path,
                        help="directories produced by tools/collect_recipe_tree.py")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)

    try:
        projection, stats, unresolved = project(load_recipes(args.source))
    except RecipeDependencyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    snapshot = write_snapshot(projection, stats, unresolved, args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(projection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"{stats['build']} build-depends-on and {stats['check']} check-depends-on "
        f"edges from {stats['recipes']} recipes; "
        f"{stats.get('resolved_via_provides', 0)} via provides, "
        f"{stats.get('target_absent', 0)} absent, "
        f"{stats.get('target_uninterpolated', 0)} uninterpolated"
    )
    print(snapshot.relative_to(ROOT))
    print(args.output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
