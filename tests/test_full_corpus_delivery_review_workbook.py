import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FullCorpusDeliveryReviewWorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/full-corpus-delivery-review-workbook.json").read_text())
        cls.html = (ROOT / "writeups/full-corpus-delivery-review-workbook.html").read_text()

    def test_blank_workbook_covers_all_videos(self):
        self.assertEqual(self.data["video_count"], 395)
        self.assertEqual(len(self.data["items"]), 395)
        self.assertEqual(self.data["completed_review_count"], 0)
        self.assertIn("Blank review infrastructure is not delivery evidence", self.data["claim_boundary"])
        self.assertEqual(self.html.count("data-state="), 395)
        self.assertIn("Download review JSON", self.html)


if __name__ == "__main__":
    unittest.main()
