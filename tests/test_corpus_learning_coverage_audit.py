import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusLearningCoverageAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/corpus-learning-coverage-audit.json").read_text())
        cls.markdown = (ROOT / "writeups/corpus-learning-coverage-audit.md").read_text()
        cls.html = (ROOT / "writeups/corpus-learning-coverage-audit.html").read_text()

    def test_all_fixed_corpus_videos_reconcile(self):
        self.assertEqual(self.data["video_count"], 395)
        self.assertEqual(self.data["videos_with_transcript_lesson"], 395)
        self.assertEqual(self.data["videos_requiring_review"], 0)
        self.assertEqual(len(self.data["videos"]), 395)
        self.assertEqual(self.data["summary"]["function_cards"], 4016)
        self.assertEqual(self.data["summary"]["sequence_cards"], 2800)
        self.assertEqual(self.data["summary"]["learning_track_counts"], {"canonical_job_lesson": 207, "structural_bridge_lesson": 31, "transcript_exploration_lead": 157})
        self.assertEqual(self.data["summary"]["raw_audio_video_present"], 354)
        self.assertEqual(self.data["summary"]["feature_report_present"], 357)
        self.assertEqual(self.data["summary"]["full_proxy_index_video_count"], 364)
        self.assertEqual(self.data["summary"]["proxy_videos_without_itinerary_entry"], 7)
        self.assertIn("not validation evidence", self.data["claim_boundary"])
        self.assertIn("covered_with_transcript_lesson", self.markdown)
        self.assertEqual(self.html.count("class='video'"), 395)
        self.assertIn("Search video", self.html)
        self.assertIn("full-context", self.html)


if __name__ == "__main__":
    unittest.main()
