import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_refresh_policy import ValidationError, validate


ROOT = Path(__file__).resolve().parents[1]


class RefreshPolicyTests(unittest.TestCase):
    def test_policy_covers_each_registered_source(self):
        counts = validate()
        registry = json.loads((ROOT / "evidence" / "source-registry.json").read_text())
        self.assertEqual(counts["sources"], len(registry["sources"]))

    def test_unknown_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            policy_path = Path(directory) / "policy.json"
            policy = json.loads((ROOT / "evidence" / "refresh-policy.json").read_text())
            policy["sources"][0]["source_id"] = "source:unknown"
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "unknown source policy"):
                validate(policy_path=policy_path)


if __name__ == "__main__":
    unittest.main()
