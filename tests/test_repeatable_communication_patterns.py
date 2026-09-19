import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepeatableCommunicationPatternsTests(unittest.TestCase):
    def test_synthesis_keeps_evidence_boundary_and_learning_loop(self):
        guide = (ROOT / "writeups/repeatable-communication-patterns.md").read_text()
        self.assertIn("not a validated best-practice library", guide)
        self.assertIn("395 full-context transcript reviews", guide)
        self.assertIn("50 retrieved exact phrase forms", guide)
        self.assertIn("36-sample delivery-inspection", guide)
        self.assertIn("Delivery: what to inspect, not what to imitate", guide)
        self.assertIn("A repeatable practice cycle", guide)
        self.assertIn("Claim ladder", guide)
        self.assertIn("learner records and listener outcomes remain open", guide)


if __name__ == "__main__":
    unittest.main()
