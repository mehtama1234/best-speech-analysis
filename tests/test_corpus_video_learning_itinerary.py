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
        self.assertGreater(self.data["entries_with_phrase_handles"], 150)
        self.assertGreater(self.data["phrase_handle_count"], 400)
        self.assertEqual(self.data["learning_track_counts"], {"canonical_job_lesson": 207, "structural_bridge_lesson": 31, "transcript_exploration_lead": 157})
        self.assertTrue(all("phrase_handles" in row and "phrase_handle_status" in row for row in self.data["entries"]))
        self.assertTrue(all("learning_note" in row and "learning_form" in row for row in self.data["entries"]))
        self.assertIn("does not claim", self.data["claim_boundary"])
        self.assertIn("Exact evidence", self.html)
        self.assertIn("Exact phrase handles", self.html)
        self.assertIn("Learning track", self.html)
        self.assertIn("structural_bridge_lesson", self.html)
        self.assertIn("Recorded structural relation", self.html)


if __name__ == "__main__":
    unittest.main()
