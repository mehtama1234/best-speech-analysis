import copy
import json
import unittest
from pathlib import Path

from scripts.validate_end_to_end_status import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateEndToEndStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/end-to-end-status.json").read_text())

    def test_current_dashboard_reconciles(self):
        self.assertEqual(validate(self.report), [])

    def test_validator_catches_stale_count_and_premature_completion(self):
        report = copy.deepcopy(self.report)
        report["stages"]["transcript_context"]["video_count"] = 10
        report["stages"]["learner_check"]["completed_records"] = 1
        errors = validate(report)
        self.assertTrue(any("transcript_context.video_count" in error for error in errors))
        self.assertTrue(any("learner records" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
