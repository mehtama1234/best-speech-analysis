import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Corpus30DayRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.route = json.loads((ROOT / "research/corpus-30-day-study-route.json").read_text())
        cls.markdown = (ROOT / "writeups/corpus-30-day-study-route.md").read_text()

    def test_route_covers_every_video_once(self):
        ids = [video_id for day in self.route["days"] for video_id in day["video_ids"]]
        self.assertEqual(self.route["video_count"], 395)
        self.assertEqual(self.route["day_count"], 29)
        self.assertEqual(len(ids), 395)
        self.assertEqual(len(set(ids)), 395)
        self.assertEqual(self.route["max_videos_per_day"], 14)
        self.assertIn("not validation evidence", self.route["claim_boundary"])
        self.assertIn("Daily loop", self.markdown)


if __name__ == "__main__":
    unittest.main()
