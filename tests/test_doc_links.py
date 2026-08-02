"""Fail the build on a Markdown link that points at a file which is not there.

Nothing checked this before. `akb.validate()` reads the composed graph and
never opens a page; `akb.validate_docs()` opens pages but reads only their
frontmatter. A page could therefore link to `FOO.md` forever without anyone
noticing, and a renamed page could silently orphan every reference to it.

Scope is deliberately narrow: relative links between repository files.
External URLs are not fetched — that would make the test suite depend on the
network, and URL verification belongs to the evidence-registration discipline
instead, where a fetch is recorded once with a retrieval date.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LINK = re.compile(r"\]\(([^)]+)\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")

SEARCH_DIRS = ("docs", "charter", ".")


def markdown_files():
    seen = set()
    for name in SEARCH_DIRS:
        base = ROOT / name
        pattern = "*.md" if name == "." else "**/*.md"
        for path in sorted(base.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


class DocumentationLinkTests(unittest.TestCase):
    def test_every_relative_link_resolves(self):
        broken = []
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            for match in LINK.finditer(text):
                target = match.group(1).strip()
                if not target or target.startswith(EXTERNAL):
                    continue
                # Strip a fragment; anchors are not validated, only files.
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    rel = path.relative_to(ROOT)
                    broken.append(f"{rel} -> {target}")
        self.assertEqual(
            broken,
            [],
            "Markdown links point at files that do not exist:\n      "
            + "\n      ".join(broken),
        )


if __name__ == "__main__":
    unittest.main()
