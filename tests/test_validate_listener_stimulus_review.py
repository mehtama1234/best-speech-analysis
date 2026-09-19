import json
import unittest
from pathlib import Path

from scripts.validate_listener_stimulus_review import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidateListenerStimulusReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-listener-stimulus-review-workbook.json").read_text())

    def test_partial_export_is_rejected(self):
        errors = validate({"record_type": "listener_stimulus_independent_review", "workbook_id": self.workbook["workbook_id"], "responses": {}}, self.workbook)
        self.assertTrue(errors)
        self.assertIn("independent_attestation must be true", errors)


if __name__ == "__main__":
    unittest.main()
