import unittest

from scripts.build_communication_job_promotion_readiness import build


class CommunicationJobPromotionReadinessTests(unittest.TestCase):
    def test_all_cards_remain_explicitly_blocked_by_open_gates(self):
        report = build()
        self.assertEqual(report["card_count"], 18)
        self.assertEqual(report["promotion_ready_count"], 0)
        self.assertTrue(all(row["status"] == "provisional_not_promotion_ready" for row in report["cards"]))
        self.assertTrue(all(row["blockers"] for row in report["cards"]))
        self.assertTrue(all(set(row["blockers"]) == set(row["blocker_routes"]) for row in report["cards"]))
        self.assertTrue(all(route["form"] and route["validator"] for route in report["routes"].values()))


if __name__ == "__main__":
    unittest.main()
