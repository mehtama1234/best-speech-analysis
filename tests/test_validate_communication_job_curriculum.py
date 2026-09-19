import copy
import json
import unittest
from pathlib import Path

from scripts.validate_communication_job_curriculum import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidateCommunicationJobCurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "research/communication-job-curriculum-index.json").read_text())

    def test_current_curriculum_joins_all_required_layers(self):
        self.assertEqual(validate(self.index), [])

    def test_missing_delivery_sample_is_rejected(self):
        broken = copy.deepcopy(self.index)
        broken["lessons"][0]["delivery_samples"].pop()
        self.assertTrue(any("two delivery samples" in error for error in validate(broken)))


if __name__ == "__main__":
    unittest.main()
