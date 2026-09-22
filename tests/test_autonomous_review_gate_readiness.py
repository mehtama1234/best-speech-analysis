import unittest

from scripts.validate_autonomous_review_gate_readiness import validate


class AutonomousReviewGateReadinessTest(unittest.TestCase):
    def test_all_external_gates_are_runnable_and_uncompleted(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
