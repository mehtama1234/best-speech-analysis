import json
import unittest
from pathlib import Path

from scripts.validate_communication_job_counterexample_review import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidateCommunicationJobCounterexampleReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-counterexample-workbook.json").read_text())

    def test_partial_export_is_rejected(self):
        errors = validate({"record_type": "communication_job_counterexample_review", "workbook_id": self.workbook["workbook_id"], "responses": {}}, self.workbook)
        self.assertTrue(errors)
        self.assertIn("independent_attestation must be true", errors)


if __name__ == "__main__":
    unittest.main()
