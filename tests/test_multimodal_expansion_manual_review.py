import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MultimodalExpansionManualReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/multimodal-expansion-manual-review.json").read_text())

    def test_review_is_bounded_and_not_independent(self):
        self.assertEqual(len(self.report["items"]), 11)
        self.assertEqual(self.report["status"], "internal_bounded_review_complete_independent_review_pending")
        self.assertEqual(self.report["independence"], "not_independent")

    def test_every_item_links_existing_media_features_and_evidence(self):
        for item in self.report["items"]:
            self.assertTrue((ROOT / item["video_source"]).exists())
            self.assertTrue((ROOT / item["audio_source"]).exists())
            self.assertTrue((ROOT / item["feature_source"]).exists())
            self.assertRegex(item["evidence_id"], r"^[^:]+:\d{5}$")
            self.assertTrue(item["transcript_text"])
            self.assertIn("alignment_decision", item)
            self.assertIn("feature_limit", item)

    def test_alignment_decisions_include_counterexample_like_boundaries(self):
        decisions = {item["alignment_decision"] for item in self.report["items"]}
        self.assertIn("visible_caption_overlap", decisions)
        self.assertIn("setting_visible_caption_not_aligned", decisions)


if __name__ == "__main__":
    unittest.main()
