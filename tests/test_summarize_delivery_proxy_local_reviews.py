import json
import unittest
from pathlib import Path

from scripts.summarize_delivery_proxy_local_reviews import summarize


ROOT = Path(__file__).resolve().parents[1]


class SummarizeDeliveryProxyLocalReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads((ROOT / "research/delivery-proxy-candidate-atlas.json").read_text())
        cls.record_id = cls.atlas["candidates"][0]["record_id"]

    def test_summary_preserves_non_independence_boundary(self):
        record = {
            "record_id": self.record_id,
            "reviewer": "reviewer-1",
            "alignment": "clear",
            "identity": "uncertain",
            "updated_at": "2026-09-19T00:00:00Z",
            "conflict": "No conflict declared; independence requires separate adjudication.",
            "vocal": "pause not reviewed",
            "visual": "speaker visible; gesture not reviewed",
            "setting": "edited subtitles",
            "access": "captions available",
            "alternate": "not reviewed",
            "job": "humor_or_rapport",
        }
        result = summarize([record], self.atlas)
        self.assertEqual(result["record_count"], 1)
        self.assertIn("do not establish reviewer independence", result["claim_boundary"])
        self.assertEqual(result["by_job"][0]["alignment_distribution"], {"clear": 1})


if __name__ == "__main__":
    unittest.main()
