from __future__ import annotations

import hashlib
import unittest

from tools.verify_recipe_sources import verify_records


class RecipeSourceVerificationTests(unittest.TestCase):
    def test_verifies_aligned_checksum_and_source_alias(self):
        payload = b"source payload"
        records = verify_records(
            [{"path": "sample/PKGBUILD", "source": ["sample.tar.gz::https://example.test/sample.tar.gz"], "sha256sums": [hashlib.sha256(payload).hexdigest()]}],
            fetch=lambda url: payload,
        )
        self.assertEqual(records[0]["url"], "https://example.test/sample.tar.gz")
        self.assertTrue(records[0]["verified"])
        self.assertEqual(records[0]["outcome"], "verified")

    def test_preserves_mismatch_and_skip_as_explicit_outcomes(self):
        records = verify_records(
            [{"path": "sample/PKGBUILD", "source": ["https://example.test/a", "https://example.test/b"], "sha256sums": ["0" * 64, "SKIP"]}],
            fetch=lambda url: b"payload",
        )
        self.assertEqual(records[0]["outcome"], "checksum-mismatch")
        self.assertFalse(records[0]["verified"])
        self.assertEqual(records[1]["outcome"], "skipped-by-recipe")


if __name__ == "__main__":
    unittest.main()
