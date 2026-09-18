import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SharedLessonCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/shared-lesson-cards.json").read_text())

    def test_all_eight_cards_have_common_evidence_and_practice_contract(self):
        self.assertEqual(self.data["card_count"], 8)
        for card in self.data["cards"]:
            for key in ("communication_problem", "speech_function_hypothesis", "examples", "counterexamples", "delivery_evidence", "recurrence", "practice", "validation", "limits"):
                self.assertIn(key, card)
            self.assertTrue(card["examples"])
            self.assertTrue(all(example["exact_text"] for example in card["examples"]))
            self.assertTrue(all(example["source_url"] for example in card["examples"]))
            self.assertTrue(all(example["surrounding_context"] for example in card["examples"]))
            self.assertTrue(all(example["exact_text"] for example in card["counterexamples"]))
            self.assertTrue(card["practice"]["self_check"])
            self.assertIn("bounded_hypothesis", card["mechanism_status"])
            self.assertIn("speech_function", card)
            self.assertEqual(card["speech_function"]["candidate_family"], card["recurrence"]["phrase_family"])
            self.assertTrue(card["recurrence"]["phrase_forms"])
            self.assertIn("retrieval_samples", card["recurrence"])
            self.assertIn("observations", card["delivery_evidence"])
            self.assertEqual(card["recurrence"]["atlas_status"], "heuristic_retrieval_aid_requires_manual_review")

    def test_cards_preserve_provisional_boundaries(self):
        self.assertEqual(self.data["status"], "eight_draft_cards_not_validated")
        for card in self.data["cards"]:
            self.assertIn("causal effectiveness", card["limits"]["do_not_claim"])
            self.assertEqual(card["validation"]["listener_outcomes"], "not_tested")

    def test_cards_expose_the_full_evidence_chain_for_shared_clients(self):
        required = {
            "communication_problem", "exact_language_and_function", "delivery_evidence",
            "mechanism_hypothesis", "cross_talk_recurrence", "counterexamples_and_limits",
            "practice", "learner_check", "listener_outcome_check",
        }
        for card in self.data["cards"]:
            self.assertEqual(set(card["evidence_chain"]), required)
            self.assertEqual(card["evidence_chain"]["mechanism_hypothesis"]["status"], card["mechanism_status"])
            self.assertEqual(card["evidence_chain"]["listener_outcome_check"]["status"], "not_tested")
            self.assertEqual(card["evidence_chain"]["learner_check"]["status"], card["validation"]["learner_status"])
            self.assertEqual(
                card["evidence_chain"]["cross_talk_recurrence"]["video_hit_count"],
                card["recurrence"]["eligible_video_hit_count"],
            )


if __name__ == "__main__":
    unittest.main()
