import json
import unittest
from pathlib import Path

from scripts.build_communication_job_delivery_inventory import main


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobDeliveryInventoryTests(unittest.TestCase):
    def test_inventory_is_complete_and_bounded(self):
        main()
        report = json.loads((ROOT / "research/communication-job-delivery-inventory.json").read_text())
        self.assertEqual(report["job_count"], 18)
        self.assertEqual(report["sample_count"], 36)
        self.assertIn("does not identify a best vocal/nonverbal pattern", report["claim_boundary"])
        self.assertTrue(all(len(job["samples"]) == 2 for job in report["jobs"]))
        self.assertTrue(all(sample["observation_independence"] == "not_independent" for job in report["jobs"] for sample in job["samples"]))


if __name__ == "__main__":
    unittest.main()
