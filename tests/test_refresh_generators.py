"""The refresh script and CI must regenerate the same artifacts.

`Update-Akb.ps1` carries a comment telling the next editor to keep its
generator list in step with the CI workflow, because CI regenerates
everything and then runs `git diff --exit-code` — so a refresh that skips a
generator leaves the working tree in a state CI rejects. Nothing enforced
that, and the list drifted: `build_object_facts.py` and
`build_volume_ledger.py` were added to CI and never to the script. Both
write into `docs/` between markers, so the drift was invisible until a
Windows host ran a refresh and found CI red for reasons it did not cause.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
REFRESH = ROOT / "tools" / "Update-Akb.ps1"
STEP = "Verify generated indexes are reproducible"


def ci_generators() -> list[str]:
    """Generators CI runs before `git diff --exit-code`."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert STEP in text, f"{STEP!r} step is gone from the workflow"
    return re.findall(r"python tools/(\w+\.py)", text.split(STEP, 1)[1])


def refresh_generators() -> list[str]:
    """Generators the refresh script runs, including ones invoked by name."""
    text = REFRESH.read_text(encoding="utf-8")
    loop = text.split("foreach ($generator in", 1)[1].split(")", 1)[0]
    named = re.findall(r'"(\w+\.py)"', loop)
    direct = re.findall(r'Join-Path \$PSScriptRoot "(\w+\.py)"', text)
    return named + direct


class RefreshGeneratorTests(unittest.TestCase):
    def test_refresh_runs_every_generator_ci_regenerates(self) -> None:
        missing = sorted(set(ci_generators()) - set(refresh_generators()))
        self.assertEqual(
            missing,
            [],
            "tools/Update-Akb.ps1 does not run generators that CI regenerates, so a "
            f"refresh on a Windows host would leave CI red: {missing}",
        )

    def test_refresh_accumulates_the_inventory_projection(self) -> None:
        """A refresh must not discard evidence it cannot re-collect.

        `model/inventory/current.json` is three accumulated
        `scope=package-archive` snapshots — downloaded payloads analysed byte
        by byte. A refresh collects `scope=installed` through pacman, a
        different modality rather than a newer version of the same
        observation. Importing without `--accumulate` replaces 552 entities
        with that run's handful and drops `evidence:inventory:current`, which
        two documentation pages cite, so `akb.py validate-docs` then fails on
        a tree the operator has no obvious way to repair.

        `merge_projection` is unit-tested in tests/test_deep_inventory.py.
        What nothing checked was that the refresh path actually reaches it.
        """
        text = REFRESH.read_text(encoding="utf-8")
        call = re.search(r'^.*import_deep_inventory\.py.*$', text, re.M)
        self.assertIsNotNone(call, "Update-Akb.ps1 no longer imports the deep inventory")
        self.assertIn(
            "--accumulate",
            call.group(0),
            "tools/Update-Akb.ps1 imports the deep inventory without --accumulate, so a "
            "refresh would discard the retained package-archive projection and the "
            "evidence record two documentation pages cite",
        )

    def test_every_named_generator_exists(self) -> None:
        missing = sorted(
            name for name in set(ci_generators()) | set(refresh_generators())
            if not (ROOT / "tools" / name).is_file()
        )
        self.assertEqual(missing, [], f"generators named but absent from tools/: {missing}")


if __name__ == "__main__":
    unittest.main()
