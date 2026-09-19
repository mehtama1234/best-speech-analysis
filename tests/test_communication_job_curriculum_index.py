import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobCurriculumIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "research/communication-job-curriculum-index.json").read_text())
        cls.html = (ROOT / "writeups/communication-job-curriculum.html").read_text()

    def test_integrates_all_evidence_layers_for_18_jobs(self):
        self.assertEqual(self.index["status"], "18_job_provisional_curriculum_not_validated")
        self.assertEqual(self.index["lesson_count"], 18)
        for lesson in self.index["lessons"]:
            self.assertEqual(len(lesson["counterexample_slots"]), 5)
            self.assertEqual(len(lesson["delivery_samples"]), 2)
            self.assertEqual(lesson["learner"]["task_count"], 4)
            self.assertIn("mechanism_hypothesis", lesson)
            self.assertIn("non_fit", lesson)

    def test_missing_validation_stays_visible(self):
        self.assertIn("not present any pattern as effective", self.index["claim_boundary"])
        self.assertIn("manual observation pending", self.html)
        self.assertIn("Counterexample and limit queue", self.html)


if __name__ == "__main__":
    unittest.main()
