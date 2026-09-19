import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FullCorpusDeliveryInspectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/full-corpus-delivery-inspection.json").read_text())
        cls.html = (ROOT / "writeups/full-corpus-delivery-inspection.html").read_text()

    def test_all_videos_are_routed_with_missingness(self):
        self.assertEqual(self.data["video_count"], 395)
        self.assertEqual(len(self.data["rows"]), 395)
        self.assertEqual(self.data["feature_report_count"], 357)
        self.assertEqual(sum(self.data["inspection_status_counts"].values()), 395)
        self.assertIn("effectiveness evidence", self.data["claim_boundary"])
        self.assertEqual(self.html.count("class='video'"), 395)
        self.assertIn("All states", self.html)


if __name__ == "__main__":
    unittest.main()
