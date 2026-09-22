import copy
import json
import unittest
from pathlib import Path

from scripts.validate_external_review_launch_manifest import validate


ROOT = Path(__file__).resolve().parents[1]


class ExternalReviewLaunchManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "research/external-review-launch-manifest.json").read_text())
        cls.gates = json.loads((ROOT / "research/external-review-gate-index.json").read_text())

    def test_current_launch_manifest_is_structurally_ready(self):
        self.assertEqual(validate(self.manifest, self.gates, ROOT), [])

    def test_completed_operation_is_rejected_without_records(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["operations"][0]["status"] = "completed"
        errors = validate(manifest, self.gates, ROOT)
        self.assertTrue(any("cannot be marked completed" in error for error in errors))

    def test_missing_instrument_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["operations"][0]["validator"] = "scripts/not-a-validator.py"
        errors = validate(manifest, self.gates, ROOT)
        self.assertTrue(any("references missing validator" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
