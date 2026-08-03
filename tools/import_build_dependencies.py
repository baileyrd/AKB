#!/usr/bin/env python3
"""Project build-time and check-time dependency edges from repository databases.

Why this exists as a separate projection rather than as part of the catalog:

`model/catalog/current.json` carried exactly four relationship types --
`runtime-depends-on`, `optional-depends-on`, `published-in`, and
`belongs-to-environment`. It had no build-time or check-time edges at all,
because `tools/import_repository_db.py` read `%DEPENDS%` and `%OPTDEPENDS%`
from each package's `desc` record and dropped `%MAKEDEPENDS%` and
`%CHECKDEPENDS%` on the floor.

The consequence was systematic. A test framework is a `checkdepends` and is
never a runtime dependency, so ten of them across roughly 47 packages recorded
**one** dependent between them -- a fact about the projection, not about the
ecosystem. Every dependency ranking in this knowledge base measured runtime
centrality specifically and was blind to the build-time half of the graph.

That is now fixed in `import_repository_db.py` for any future collection. This
tool exists because the *committed* catalog snapshot was collected on
2026-07-29 and its source archives are no longer byte-identical on the mirror:
in the four days since, 1,082 of 15,711 packages changed version. Re-collecting
the whole catalog to add build edges would silently invalidate every version
number quoted in prose across the documentation.

So this projection is deliberately **additive and narrow**. It contributes
build-time and check-time relationships only -- no entities, no versions, no
runtime edges -- and it emits an edge only when *both* endpoints already exist
in the catalog projection. Edges naming a package the catalog does not hold are
dropped and counted rather than inventing an entity at a second observation
date. The result is one date for packages and versions, another for build
edges, both recorded, neither overwriting the other.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import ctypes.util
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "model" / "catalog" / "current.json"
OUTPUT = ROOT / "model" / "build-dependencies" / "current.json"
SNAPSHOTS = ROOT / "evidence" / "build-dependency-snapshots"

SCHEMA_VERSION = "1.0.0"
EVIDENCE_ID = "evidence:build-dependencies:current"

FIELD_RELATIONS = (
    ("MAKEDEPENDS", "build-depends-on"),
    ("CHECKDEPENDS", "check-depends-on"),
)


class BuildDependencyError(Exception):
    """Raised when a repository database is unreadable or unsafe."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def zstd_decompress(raw: bytes) -> bytes:
    """Decompress a Zstandard frame using only the standard library.

    pacman databases are `.tar.zst` and Python's `tarfile` cannot read them.
    Three routes are tried in order and all of them are dependency-free in the
    sense that matters here (ADR 0002): no package needs installing.

    1. An external `zstd`/`unzstd`/`bsdtar`, which is what a Windows or MSYS2
       host has.
    2. `ctypes` against the system `libzstd`, which is what a Linux CI image
       typically has even without the command-line tool.

    If neither is available the error names both, because "cannot read archive"
    without saying what is missing wastes the reader's time.
    """
    for command in (["zstd", "-dc"], ["unzstd", "-c"], ["bsdtar", "-xOf", "-"]):
        try:
            done = subprocess.run(
                command, input=raw, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                check=False,
            )
        except (OSError, ValueError):
            continue
        if done.returncode == 0 and done.stdout:
            return done.stdout

    library = ctypes.util.find_library("zstd")
    if library:
        lib = ctypes.CDLL(library)
        lib.ZSTD_decompress.restype = ctypes.c_size_t
        lib.ZSTD_isError.restype = ctypes.c_uint
        # The frame header often omits the content size, so grow until it fits
        # rather than trusting ZSTD_getFrameContentSize.
        capacity = max(len(raw) * 8, 1 << 20)
        for _ in range(8):
            buffer = ctypes.create_string_buffer(capacity)
            written = lib.ZSTD_decompress(buffer, capacity, raw, len(raw))
            if not lib.ZSTD_isError(written):
                return buffer.raw[:written]
            capacity *= 4
        raise BuildDependencyError("libzstd could not decompress the archive")

    raise BuildDependencyError(
        "no Zstandard decoder available: install the 'zstd' command line tool "
        "or provide a system libzstd shared library"
    )


def open_archive(archive: Path) -> tarfile.TarFile:
    raw = archive.read_bytes()
    if raw[:4] == b"\x28\xb5\x2f\xfd":
        return tarfile.open(fileobj=io.BytesIO(zstd_decompress(raw)))
    try:
        return tarfile.open(archive, "r:*")
    except tarfile.TarError as exc:
        raise BuildDependencyError(f"cannot read repository database: {exc}") from exc


def parse_desc(payload: bytes) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    key: str | None = None
    for line in payload.decode("utf-8", "replace").splitlines():
        if line.startswith("%") and line.endswith("%") and len(line) > 2:
            key = line[1:-1]
            fields[key] = []
        elif line and key is not None:
            fields[key].append(line)
    return fields


def dependency_name(value: str) -> tuple[str, str]:
    """Split `name>=1.2` into its name and its version constraint."""
    value = value.split(":", 1)[0].strip()
    for index, char in enumerate(value):
        if char in "<=>":
            return value[:index], value[index:]
    return value, ""


def archive_edges(archive: Path, repository: str) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    with open_archive(archive) as bundle:
        members = [
            member for member in bundle.getmembers()
            if member.isfile() and member.name.endswith("/desc")
        ]
        if not members:
            raise BuildDependencyError(f"{archive.name} has no package desc records")
        for member in sorted(members, key=lambda item: item.name):
            if member.name.startswith("/") or ".." in PurePosixPath(member.name).parts:
                raise BuildDependencyError(f"unsafe archive member: {member.name}")
            stream = bundle.extractfile(member)
            if stream is None:
                raise BuildDependencyError(f"cannot read archive member: {member.name}")
            fields = parse_desc(stream.read())
            source = fields.get("NAME", [""])[0]
            if not source:
                raise BuildDependencyError(f"desc record without NAME: {member.name}")
            for field, relation in FIELD_RELATIONS:
                for declared in fields.get(field, []):
                    target, constraint = dependency_name(declared)
                    if target:
                        edges.append({
                            "source_repository": repository,
                            "source_package": source,
                            "relationship": relation,
                            "target_package": target,
                            "constraint": constraint,
                        })
    return edges


def package_id(name: str) -> str:
    return f"package:msys2:{name}"


def relationship_id(relation: str, source: str, target: str) -> str:
    key = f"{relation}|{source}|{target}".encode("utf-8")
    prefix = "build" if relation == "build-depends-on" else "check"
    return f"relationship:build-dependencies:{prefix}-{hashlib.sha256(key).hexdigest()[:20]}"


def catalog_package_ids() -> set[str]:
    if not CATALOG.is_file():
        raise BuildDependencyError("model/catalog/current.json is missing")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    return {
        entity["id"] for entity in catalog.get("entities", [])
        if entity.get("kind") == "package"
    }


def project(
    archives: list[Path], repositories: list[str], catalog_ids: set[str]
) -> tuple[dict[str, Any], list[dict[str, str]], dict[str, int]]:
    if not archives or len(archives) != len(repositories):
        raise BuildDependencyError("each archive requires exactly one repository")

    collected: list[dict[str, str]] = []
    source_archives: list[dict[str, str]] = []
    for archive, repository in zip(archives, repositories):
        if not archive.is_file():
            raise BuildDependencyError(f"archive is missing: {archive}")
        if not repository or repository != repository.lower():
            raise BuildDependencyError("repository must be a lowercase pacman name")
        collected.extend(archive_edges(archive, repository))
        source_archives.append({
            "repository": repository, "name": archive.name, "sha256": sha256(archive),
        })

    relationships: list[dict[str, Any]] = []
    seen: set[str] = set()
    dropped: list[dict[str, str]] = []
    counts = {"build-depends-on": 0, "check-depends-on": 0}

    for edge in sorted(
        collected,
        key=lambda item: (item["source_package"], item["relationship"], item["target_package"]),
    ):
        source, target = package_id(edge["source_package"]), package_id(edge["target_package"])
        # Both endpoints must already exist. Anything else would mint an entity
        # at a second observation date inside a projection whose whole point is
        # that it adds edges and nothing else.
        if source not in catalog_ids or target not in catalog_ids:
            dropped.append(edge)
            continue
        identifier = relationship_id(edge["relationship"], source, target)
        if identifier in seen:
            continue
        seen.add(identifier)
        counts[edge["relationship"]] += 1
        relationships.append({
            "id": identifier,
            "type": edge["relationship"],
            "source": source,
            "target": target,
            "status": "verified",
            "confidence": "verified",
            "scope": "package-catalog",
            "condition": edge["constraint"],
            "properties": {"source_repository": edge["source_repository"]},
            "evidence_refs": [EVIDENCE_ID],
        })

    observed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    digest = hashlib.sha256(
        "".join(sorted(entry["sha256"] for entry in source_archives)).encode("utf-8")
    ).hexdigest()[:12]
    snapshot_id = f"{observed_at.replace('-', '').replace(':', '').split('.')[0]}Z-{digest}"

    stats = {
        "collected": len(collected),
        "projected": len(relationships),
        "dropped": len(dropped),
        "build": counts["build-depends-on"],
        "check": counts["check-depends-on"],
    }

    projection = {
        "schema_version": SCHEMA_VERSION,
        "snapshot": {
            "id": snapshot_id,
            "observed_at": observed_at,
            "description": (
                "Generated projection of build-time and check-time package "
                "dependency edges. Additive: contributes relationships only, "
                "restricted to packages already present in the catalog "
                "projection."
            ),
            "upstream_versions": {"collector": "1.0.0"},
        },
        "entities": [],
        "relationships": relationships,
        "claims": [],
        "evidence": [{
            "id": EVIDENCE_ID,
            "class": "observed",
            "title": "MSYS2 repository database build-time and check-time dependencies",
            "locator": f"evidence/build-dependency-snapshots/{snapshot_id}/manifest.json",
            "retrieved_at": observed_at,
            "upstream_version": None,
            "integrity": digest,
            "notes": (
                "Read from the %MAKEDEPENDS% and %CHECKDEPENDS% fields of each "
                "package's desc record in the pacman repository databases. "
                "Collected separately from, and later than, the package catalog "
                "snapshot: its source archives are no longer byte-identical on "
                "the mirror, and re-collecting the catalog would have moved "
                f"package versions. {len(dropped)} declared edges name a package "
                "absent from the catalog projection and were dropped rather than "
                "minting an entity at a second observation date."
            ),
        }],
    }
    return projection, dropped, stats


def write_snapshot(
    projection: dict[str, Any], dropped: list[dict[str, str]],
    stats: dict[str, int], source_archives: list[dict[str, str]],
) -> Path:
    snapshot = SNAPSHOTS / projection["snapshot"]["id"]
    snapshot.mkdir(parents=True, exist_ok=True)
    if dropped:
        with (snapshot / "dropped-edges.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(dropped[0]))
            writer.writeheader()
            writer.writerows(dropped)
    (snapshot / "manifest.json").write_text(
        json.dumps({
            "schema_version": SCHEMA_VERSION,
            "generated_at": projection["snapshot"]["observed_at"],
            "collector": "tools/import_build_dependencies.py",
            "source_archives": source_archives,
            "statistics": stats,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    return snapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--archive", action="append", type=Path, required=True)
    parser.add_argument("--repository", action="append", required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)

    try:
        catalog_ids = catalog_package_ids()
        projection, dropped, stats = project(args.archive, args.repository, catalog_ids)
    except BuildDependencyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    source_archives = [
        {"repository": repository, "name": archive.name, "sha256": sha256(archive)}
        for archive, repository in zip(args.archive, args.repository)
    ]
    snapshot = write_snapshot(projection, dropped, stats, source_archives)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(projection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"{stats['build']} build-depends-on and {stats['check']} check-depends-on "
        f"edges projected from {stats['collected']} declared; {stats['dropped']} "
        f"dropped for an endpoint absent from the catalog"
    )
    print(snapshot.relative_to(ROOT))
    print(args.output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
