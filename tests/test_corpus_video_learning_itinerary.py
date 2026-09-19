import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusVideoLearningItineraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/corpus-video-learning-itinerary.json").read_text())
        cls.html = (ROOT / "writeups/corpus-video-learning-itinerary.html").read_text()

    def test_one_entry_per_reviewed_video(self):
        self.assertEqual(self.data["video_count"], 395)
        self.assertEqual(len(self.data["entries"]), 395)
        self.assertGreater(self.data["entries_with_exact_evidence"], 390)
        self.assertIn("does not claim", self.data["claim_boundary"])
        self.assertIn("Exact evidence", self.html)


if __name__ == "__main__":
    unittest.main()
