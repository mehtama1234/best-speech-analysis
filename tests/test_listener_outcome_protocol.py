import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ListenerOutcomeProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((ROOT / "research/listener-outcome-protocol.json").read_text())

    def test_protocol_is_separate_from_learner_teachability(self):
        self.assertEqual(self.protocol["status"], "design_complete_not_run")
        self.assertEqual(len(self.protocol["patterns"]), 8)
        self.assertIn("trust", self.protocol["claim_boundary"])
        self.assertIn("learner", self.protocol["purpose"])

    def test_protocol_has_matched_controls_and_accessibility(self):
        self.assertIn("randomized matched control", self.protocol["design"]["comparison"])
        self.assertTrue(self.protocol["consent_and_accessibility"])
        self.assertEqual(len(self.protocol["listener_tasks"]), 6)
        self.assertIn("pattern_informed", self.protocol["record_schema"]["condition_values"])
        self.assertEqual(self.protocol["record_form"], "writeups/listener-outcome-record.html")


if __name__ == "__main__":
    unittest.main()
