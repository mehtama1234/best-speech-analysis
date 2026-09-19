import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobDeliveryMeasurementPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/communication-job-delivery-measurement-preflight.json").read_text())

    def test_all_queue_samples_have_measurement_records_and_boundaries(self):
        self.assertEqual(self.report["status"], "reproducible_proxy_measurements_attached_manual_review_pending")
        self.assertEqual(self.report["item_count"], 36)
        self.assertEqual(len(self.report["items"]), 36)
        self.assertGreater(self.report["matched_sample_count"], 0)
        for item in self.report["items"]:
            self.assertIn("audio_measurements", item)
            self.assertIn("measurement_limits", item)
            self.assertIsInstance(item["measurement_limits"], list)

    def test_proxy_boundary_is_explicit(self):
        self.assertIn("does not convert proxies", self.report["claim_boundary"])
        self.assertIn("coarse spectral pitch", self.report["metric_definitions"]["mean_pitch_hz_proxy"])
        self.assertTrue((ROOT / "writeups/communication-job-delivery-measurement-preflight.md").exists())


if __name__ == "__main__":
    unittest.main()
