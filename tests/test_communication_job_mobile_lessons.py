import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobMobileLessonsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "research/communication-job-mobile-lessons.json").read_text())

    def test_mobile_payload_covers_all_jobs_and_keeps_capture_consent(self):
        self.assertEqual(self.payload["status"], "mobile_payload_provisional_not_validated")
        self.assertEqual(self.payload["lesson_count"], 18)
        for lesson in self.payload["lessons"]:
            self.assertEqual(len(lesson["steps"]), 6)
            self.assertEqual(lesson["capture_schema"]["consent"], "explicit_required_before_save")
            self.assertEqual(lesson["capture_schema"]["participant_code"], "pseudonymous_required")
            self.assertIn("not imitate", lesson["safety_boundary"])
            self.assertTrue(lesson["repeatable_form"])
            self.assertIn("phrase_form_coverage_status", lesson)
            self.assertEqual(len(lesson["exact_examples"]), 3)
            self.assertEqual(len(lesson["delivery_samples"]), 2)
            self.assertIn("manual observation", lesson["delivery_boundary"].lower())
            for example in lesson["exact_examples"]:
                self.assertTrue(example["segments"])

    def test_payload_does_not_claim_outcomes(self):
        self.assertIn("does not make a pattern effective", self.payload["claim_boundary"])
        self.assertTrue((ROOT / "writeups/communication-job-mobile-lessons.md").exists())


if __name__ == "__main__":
    unittest.main()
