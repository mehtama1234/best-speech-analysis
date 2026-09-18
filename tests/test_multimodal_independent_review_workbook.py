import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MultimodalIndependentReviewWorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads(
            (ROOT / "research/multimodal-independent-review-workbook.json").read_text()
        )

    def test_workbook_covers_both_internal_review_passes(self):
        self.assertEqual(self.workbook["item_count"], 21)
        self.assertEqual(len(self.workbook["items"]), 21)
        self.assertEqual(
            self.workbook["source_reviews"],
            [
                "research/multimodal-expansion-manual-review.json",
                "research/multimodal-expansion-manual-review-02.json",
            ],
        )
        self.assertEqual(
            {item["internal_review_source"] for item in self.workbook["items"]},
            set(self.workbook["source_reviews"]),
        )

    def test_workbook_contains_no_independent_judgments(self):
        for item in self.workbook["items"]:
            self.assertTrue(item["review_item_id"])
            self.assertTrue(all(value is None for value in item["review"].values()))


if __name__ == "__main__":
    unittest.main()
