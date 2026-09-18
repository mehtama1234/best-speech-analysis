import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MultimodalExpansionManualReview02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/multimodal-expansion-manual-review-02.json").read_text())

    def test_second_pass_has_ten_new_bounded_items(self):
        self.assertEqual(len(self.report["items"]), 10)
        self.assertEqual(self.report["independence"], "not_independent")
        self.assertEqual(self.report["status"], "internal_bounded_review_complete_independent_review_pending")

    def test_second_pass_links_existing_media_and_feature_records(self):
        for item in self.report["items"]:
            self.assertTrue((ROOT / item["video_source"]).exists())
            self.assertTrue((ROOT / item["audio_source"]).exists())
            self.assertTrue((ROOT / item["feature_source"]).exists())
            self.assertTrue(item["transcript_text"])

    def test_second_pass_preserves_non_aligned_cases(self):
        decisions = {item["alignment_decision"] for item in self.report["items"]}
        self.assertIn("visible_caption_overlap", decisions)
        self.assertTrue(any("not_aligned" in decision or "cutaway" in decision or "title_card" in decision or "fictional" in decision for decision in decisions))


if __name__ == "__main__":
    unittest.main()
