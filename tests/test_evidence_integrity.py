"""Retained evidence payloads must still match the hashes they were sealed with.

Every collection writes a manifest recording a SHA-256 per payload file, and
`tools/import_deep_inventory.py` refuses to import a snapshot whose files do
not match. That gate protects a real import — but nothing checked the payloads
already in the repository, so corruption sat undetected until someone tried to
re-import.

It had. Twelve of twenty-three files failed their own manifest: committed from
a Windows host with CRLF endings and normalised to LF on checkout, which made
every retained snapshot unimportable while looking untouched in a diff.
`.gitattributes` now marks them `-text`, and this test is what notices if that
protection is removed or a payload is edited in place.

`import_deep_inventory.py --verify-only` does the same check for one directory
and is the manual equivalent; this runs it over everything the repository
retains, in the suite, so it runs wherever the suite does.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOTS = ("evidence/inventory-snapshots", "evidence/snapshots")


def snapshots() -> list[tuple[Path, dict]]:
    """Return every retained snapshot directory paired with its manifest."""
    found = []
    for base in EVIDENCE_ROOTS:
        root = ROOT / base
        if not root.is_dir():
            continue
        for directory in sorted(p for p in root.iterdir() if p.is_dir()):
            manifest = next(iter(sorted(directory.glob("*manifest*.json"))), None)
            if manifest and manifest.is_file():
                found.append((directory, json.loads(manifest.read_text(encoding="utf-8"))))
    return found


class EvidenceIntegrityTests(unittest.TestCase):
    def test_retained_payloads_match_their_manifests(self) -> None:
        mismatched, checked = [], 0
        for directory, manifest in snapshots():
            for name, expected in manifest.get("sha256", {}).items():
                payload = directory / name
                if not payload.is_file():
                    mismatched.append(f"{directory.name}/{name}: missing")
                    continue
                checked += 1
                actual = hashlib.sha256(payload.read_bytes()).hexdigest()
                if actual != expected:
                    crlf = payload.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
                    hint = (
                        " (the CRLF form matches — line-ending normalisation, check .gitattributes)"
                        if hashlib.sha256(crlf).hexdigest() == expected
                        else ""
                    )
                    mismatched.append(f"{directory.name}/{name}: {actual[:12]} != {expected[:12]}{hint}")
        self.assertEqual(
            mismatched,
            [],
            "retained evidence payloads no longer match their manifests, so "
            "tools/import_deep_inventory.py would refuse to import them:\n  "
            + "\n  ".join(mismatched),
        )
        self.assertGreater(checked, 0, "no retained payloads were found to verify")

    def test_manifest_counts_match_payload_line_counts(self) -> None:
        """A hash match with a wrong count would mean the manifest is stale."""
        wrong = []
        for directory, manifest in snapshots():
            for name, count in manifest.get("counts", {}).items():
                payload = directory / name
                if not payload.is_file() or not name.endswith(".jsonl"):
                    continue
                actual = len(payload.read_text(encoding="utf-8").splitlines())
                if actual != count:
                    wrong.append(f"{directory.name}/{name}: {actual} lines, manifest says {count}")
        self.assertEqual(wrong, [], "manifest record counts disagree with payloads:\n  " + "\n  ".join(wrong))


if __name__ == "__main__":
    unittest.main()
