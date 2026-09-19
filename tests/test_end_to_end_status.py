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
        self.assertEqual(self.status["stages"]["transcript_lesson_inventory"]["review_count"], 395)
        self.assertGreater(self.status["stages"]["transcript_lesson_inventory"]["function_inventory_item_count"], 4000)
        self.assertEqual(self.status["stages"]["canonical_function_taxonomy"]["function_item_count"], 4016)
        self.assertGreater(self.status["stages"]["canonical_function_taxonomy"]["unclassified_item_count"], 0)
        self.assertEqual(self.status["stages"]["exact_caption_evidence_bank"]["function_record_count"], 4016)
        self.assertEqual(self.status["stages"]["exact_caption_evidence_bank"]["missing_evidence_id_count"], 0)
        self.assertEqual(self.status["stages"]["communication_job_cards"]["card_count"], 18)
        self.assertEqual(self.status["stages"]["communication_job_learner_check"]["task_count"], 72)
        self.assertEqual(self.status["stages"]["communication_job_learner_check"]["completed_records"], 0)
        self.assertEqual(self.status["stages"]["communication_job_listener_outcomes"]["pattern_count"], 18)
        self.assertFalse(self.status["stages"]["communication_job_listener_outcomes"]["stimulus_pairs_locked"])
        self.assertEqual(self.status["stages"]["listener_stimulus_preflight"]["manual_review_required"], 18)
        self.assertEqual(self.status["stages"]["exact_phrase_form_inventory"]["form_count"], 50)
        self.assertEqual(self.status["stages"]["exact_phrase_form_independent_review"]["queued_form_count"], 50)
        self.assertEqual(self.status["stages"]["exact_phrase_form_independent_review"]["completed_independent_reviews"], 0)
        self.assertEqual(self.status["stages"]["delivery_evidence_index"]["independent_observation_count"], 0)
        self.assertEqual(self.status["stages"]["shared_evidence_model"]["entity_type_count"], 11)
        self.assertEqual(self.status["stages"]["counterexample_library"]["queued_slot_count"], 90)
        self.assertEqual(self.status["stages"]["counterexample_library"]["completed_independent_reviews"], 0)
        self.assertEqual(self.status["stages"]["speech_function_candidate_review"]["completed_independent_reviews"], 0)
        self.assertEqual(self.status["stages"]["learner_check"]["completed_records"], 0)
        self.assertEqual(self.status["stages"]["listener_outcomes"]["completed_records"], 0)
        self.assertEqual(self.status["stages"]["delivery_evidence"]["raw_audio_video_without_transcript"], 8)
        self.assertEqual(self.status["stages"]["delivery_evidence"]["raw_only_visual_audit_items"], 8)
        self.assertGreaterEqual(len(self.status["next_required_gates"]), 5)
        self.assertIn("effectiveness", self.status["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
