import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EndToEndStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.status = json.loads((ROOT / "research/end-to-end-status.json").read_text())

    def test_dashboard_preserves_broad_scope_and_incomplete_gates(self):
        self.assertEqual(self.status["status"], "research_checkpoint_not_complete")
        self.assertEqual(self.status["stages"]["transcript_context"]["video_count"], 395)
        self.assertEqual(self.status["stages"]["speech_function_candidate_review"]["completed_independent_reviews"], 0)
        self.assertEqual(self.status["stages"]["learner_check"]["completed_records"], 0)
        self.assertEqual(self.status["stages"]["listener_outcomes"]["completed_records"], 0)
        self.assertEqual(self.status["stages"]["delivery_evidence"]["raw_audio_video_without_transcript"], 8)
        self.assertEqual(self.status["stages"]["delivery_evidence"]["raw_only_visual_audit_items"], 8)
        self.assertGreaterEqual(len(self.status["next_required_gates"]), 5)
        self.assertIn("effectiveness", self.status["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
