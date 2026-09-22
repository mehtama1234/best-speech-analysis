import unittest

from scripts.check_promotion_readiness import report


class PromotionReadinessCheckTests(unittest.TestCase):
    def test_current_checkpoint_fails_closed_with_open_human_gates(self):
        result = report()
        self.assertEqual(result["status"], "promotion_blocked")
        self.assertGreater(result["open_requirement_count"], 0)
        self.assertEqual(result["promotion_ready_count"], 0)
        self.assertGreater(result["open_gate_count"], 0)
        self.assertTrue(all(gate["form"] and gate["validator"] for gate in result["open_gates"]))
        self.assertIn("not human validation", result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
