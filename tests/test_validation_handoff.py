import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidationHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/validation-handoff.json").read_text())
        cls.markdown = (ROOT / "writeups/validation-handoff.md").read_text()

    def test_handoff_covers_all_human_gates_without_claiming_results(self):
        self.assertEqual(self.report["status"], "instruments_ready_no_human_records_received")
        self.assertEqual(len(self.report["review_gates"]), 8)
        self.assertEqual(len(self.report["learning_gates"]), 3)
        self.assertIn("No reviewer", self.report["claim_boundary"])
        for gate in self.report["review_gates"] + self.report["learning_gates"]:
            self.assertTrue(gate["validator"])
            self.assertTrue(gate["does_not_establish"])
        self.assertIn("Do not send credentials", self.markdown)


if __name__ == "__main__":
    unittest.main()
