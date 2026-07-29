#!/usr/bin/env python3
"""Download declared HTTP(S) recipe sources and verify aligned SHA-256 sums."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import Request, urlopen


MAX_BYTES = 1024 * 1024 * 1024


class RecipeSourceError(Exception):
    """Raised when recipe-source verification input is invalid."""


def source_url(value: str) -> str:
    """Remove a pacman source alias without interpreting shell syntax."""
    return value.split("::", 1)[-1]


def download(url: str, max_bytes: int = MAX_BYTES) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise RecipeSourceError("only absolute HTTP(S) source URLs are eligible")
    request = Request(url, headers={"User-Agent": "msys2-akb-source-verifier/1"})
    with urlopen(request, timeout=60) as response:  # nosec B310: scheme is allow-listed above
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise RecipeSourceError(f"source exceeds {max_bytes} byte limit")
            chunks.append(chunk)
    return b"".join(chunks)


def verify_records(
    recipes: list[dict[str, Any]],
    fetch: Callable[[str], bytes] = download,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for recipe in recipes:
        sources = recipe.get("source", [])
        checksums = recipe.get("sha256sums", [])
        for index, source in enumerate(sources):
            expected = checksums[index] if index < len(checksums) else ""
            url = source_url(str(source))
            record: dict[str, Any] = {
                "recipe": recipe.get("path", ""), "source_index": index,
                "declared_source": source, "url": url, "expected_sha256": expected,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "verified": False,
            }
            if expected == "SKIP":
                record["outcome"] = "skipped-by-recipe"
            elif len(expected) != 64 or any(char not in "0123456789abcdefABCDEF" for char in expected):
                record["outcome"] = "unsupported-or-missing-sha256"
            else:
                try:
                    payload = fetch(url)
                    actual = hashlib.sha256(payload).hexdigest()
                    record.update({"actual_sha256": actual, "size": len(payload), "verified": actual.lower() == expected.lower(), "outcome": "verified" if actual.lower() == expected.lower() else "checksum-mismatch"})
                except (OSError, RecipeSourceError, ValueError) as exc:
                    record.update({"outcome": "download-failed", "error": str(exc)})
            records.append(record)
    return records


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    except json.JSONDecodeError as exc:
        raise RecipeSourceError(f"invalid recipes JSONL: {exc}") from exc


def verify(recipes_path: Path, output: Path) -> dict[str, int]:
    if not recipes_path.is_file():
        raise RecipeSourceError(f"recipes input is missing: {recipes_path}")
    records = verify_records(read_jsonl(recipes_path))
    output.mkdir(parents=True, exist_ok=True)
    result = output / "recipe-source-verification.jsonl"
    result.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    manifest = {
        "schema_version": "1.0.0", "collector": "tools/verify_recipe_sources.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": str(recipes_path), "records": len(records),
        "verified": sum(record["verified"] for record in records),
        "failures": sum(record["outcome"] in {"checksum-mismatch", "download-failed"} for record in records),
        "sha256": hashlib.sha256(result.read_bytes()).hexdigest(),
    }
    (output / "recipe-source-verification-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"records": manifest["records"], "verified": manifest["verified"], "failures": manifest["failures"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipes", type=Path, help="recipes.jsonl from deep inventory")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.recipes.resolve(), args.output.resolve())
    except (RecipeSourceError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Verified " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
