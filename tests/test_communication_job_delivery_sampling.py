import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobDeliverySamplingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads((ROOT / "research/communication-job-delivery-sampling.json").read_text())

    def test_two_queue_items_per_shared_job_and_blank_observations(self):
        self.assertEqual(self.queue["status"], "queue_built_manual_observation_pending")
        self.assertEqual(self.queue["job_count"], 18)
        self.assertEqual(self.queue["item_count"], 36)
        by_job = {}
        for item in self.queue["items"]:
            by_job.setdefault(item["canonical_job"], []).append(item)
            self.assertIsNone(item["review"]["visual_observation"])
            self.assertIsNone(item["review"]["vocal_timing_observation"])
            self.assertTrue(item["transcript_segment_ids"])
        self.assertEqual(len(by_job), 18)
        self.assertTrue(all(len(items) == 2 for items in by_job.values()))

    def test_raw_media_boundary_is_visible(self):
        self.assertGreater(self.queue["coverage_summary"]["raw_audio_video_items"], 0)
        self.assertIn("Derived features are proxies", self.queue["claim_boundary"])
        self.assertTrue((ROOT / "writeups/communication-job-delivery-sampling.html").exists())


if __name__ == "__main__":
    unittest.main()
