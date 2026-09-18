import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SharedLearnerCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((ROOT / "research/shared-learner-check.json").read_text())
        cls.html = (ROOT / "writeups/shared-learner-check.html").read_text()

    def test_unifies_both_slices_without_promoting_lessons(self):
        self.assertEqual(self.protocol["pattern_count"], 8)
        self.assertEqual(self.protocol["task_count"], 32)
        self.assertEqual(self.protocol["status"], "protocol_drafted_not_run")
        self.assertEqual(len({task["source_task_bank"] for task in self.protocol["tasks"]}), 2)
        self.assertTrue(all(pattern["status"] == "draft_not_validated" for pattern in self.protocol["patterns"]))

    def test_form_contains_consent_and_all_pattern_sections(self):
        self.assertIn('name="consent"', self.html)
        self.assertIn("shared-learner-check", self.html)
        for number in range(1, 9):
            self.assertIn(f'p{number}_listener_restatement', self.html)
            self.assertIn(f'p{number}_boundary_note', self.html)


if __name__ == "__main__":
    unittest.main()
