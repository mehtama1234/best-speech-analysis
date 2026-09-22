import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AutonomousDeliveryReconciliationTest(unittest.TestCase):
    def test_all_delivery_jobs_and_samples_reconcile(self):
        report = json.loads((ROOT / "research/autonomous-delivery-reconciliation.json").read_text(encoding="utf-8"))
        self.assertEqual(report["item_count"], 36)
        self.assertEqual(report["job_count"], 18)
        self.assertEqual(len(report["job_summaries"]), 18)
        self.assertTrue(all(item["practice_question"] for item in report["items"]))
        self.assertIn("effectiveness", report["claim_boundary"])

    def test_delivery_markdown_keeps_proxy_boundary(self):
        text = (ROOT / "writeups/autonomous-delivery-reconciliation.md").read_text(encoding="utf-8")
        self.assertIn("manual listening and independent review are not claimed", text)
        self.assertIn("## Safe use", text)


if __name__ == "__main__":
    unittest.main()
