import unittest
import json
from pathlib import Path
from scripts.review_evidence import load_annotations, label_supported, supported_labels, context_digest


class ContextualReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {row["annotation_id"]: row for row in
                    load_annotations(Path(__file__).resolve().parents[1])}

    def test_story_is_not_rejected_with_embedded_advice(self):
        row = self.rows["review-014"]
        self.assertFalse(row["candidate_label_supported"])
        self.assertEqual(supported_labels(row), ["story_or_personal_experience"])

    def test_question_does_not_imply_claim_qualification(self):
        row = self.rows["review-003"]
        self.assertTrue(label_supported(row, "question"))
        self.assertFalse(label_supported(row, "uncertainty_or_qualification"))

    def test_qualification_attribution_is_not_speaker_uncertainty(self):
        reported = self.rows["review-072"]["label_decisions"]["uncertainty_or_qualification"]
        self.assertTrue(reported["supported"])
        self.assertEqual(reported["view_attribution"], "reported_other_people_text")
        unresolved = self.rows["review-044"]["label_decisions"]["uncertainty_or_qualification"]
        self.assertEqual(unresolved["view_attribution"], "turn_attribution_unresolved")
        strong_advice = self.rows["review-073"]["label_decisions"]["uncertainty_or_qualification"]
        self.assertEqual(strong_advice["subtype"], "opinion_framed_advice_with_reinforcement")

    def test_example_subtypes_do_not_turn_illustration_into_proof(self):
        case = self.rows["review-031"]["label_decisions"]["example"]
        self.assertTrue(case["supported"])
        self.assertEqual(case["subtype"], "quantitative_before_after_case")
        self.assertIn("not fact-checked", case["reason"])
        detail = self.rows["review-030"]["label_decisions"]["example"]
        self.assertFalse(detail["supported"])
        self.assertIn("wig shop owner", detail["reason"])

    def test_contextual_contrast_can_revise_a_legacy_rejection(self):
        row = self.rows["review-080"]
        self.assertFalse(row["candidate_label_supported"])
        decision = row["label_decisions"]["contrast_or_disagreement"]
        self.assertTrue(decision["supported"])
        self.assertEqual(decision["view_attribution"], "scene_dialogue_text")
        self.assertIn("ten-second-gap", decision["reason"])

    def test_legacy_judgment_remains_distinguishable(self):
        row = {"candidate_labels": ["story_or_personal_experience"], "candidate_label_supported": True}
        self.assertNotIn("contextual_review_id", row)
        self.assertEqual(supported_labels(row), ["story_or_personal_experience"])

    def test_counterfactual_reaction_is_not_narrated_actual_event(self):
        row = self.rows["review-068"]
        self.assertTrue(row["candidate_label_supported"])
        decision = row["label_decisions"]["story_or_personal_experience"]
        self.assertFalse(decision["supported"])
        self.assertEqual(decision["subtype"], "autobiographically_anchored_counterfactual")
        self.assertTrue(label_supported(self.rows["review-013"], "story_or_personal_experience"))

    def test_question_boundary_is_not_nearby_question_presence(self):
        # These assertions preserve the recorded review distinctions, not
        # independent proof of their semantic correctness.
        row = self.rows["review-054"]
        self.assertTrue(label_supported(row, "question"))
        self.assertEqual(row["label_decisions"]["question"]["subtype"],
                         "interlocutor_question_spanning_captions")
        self.assertFalse(label_supported(self.rows["review-056"], "question"))

    def test_question_function_distinguishes_prompt_and_challenge(self):
        prompt = self.rows["review-053"]["label_decisions"]["question"]
        challenge = self.rows["review-019"]["label_decisions"]["question"]
        self.assertEqual(prompt["subtype"], "interviewer_narrative_prompt")
        self.assertEqual(challenge["subtype"], "question_form_challenge_to_repetition")

    def test_outro_attribution_reaches_reader_cards(self):
        root = Path(__file__).resolve().parents[1]
        outro = self.rows["review-049"]["label_decisions"]["call_to_action"]
        self.assertTrue(outro["supported"])
        self.assertEqual(outro["view_attribution"], "promotional_outro_text_not_featured_speaker_verified")
        self.assertIn(outro["reason"], (root / "writeups/reviewed-pattern-cards.md").read_text())
        for aid in ("review-022", "review-048", "review-052"):
            self.assertFalse(label_supported(self.rows[aid], "call_to_action"))

    def test_unclassified_has_context_without_silent_label_promotion(self):
        expected = {"review-045": "object_description_transition",
                    "review-046": "autobiographical_condition_detail",
                    "review-047": "habitual_action_with_reported_dialogue"}
        for aid, subtype in expected.items():
            row = self.rows[aid]
            self.assertEqual(row["candidate_labels"], ["unclassified"])
            self.assertEqual(row["label_decisions"]["unclassified"]["subtype"], subtype)
            self.assertEqual(supported_labels(row), [])

    def test_source_digest_changes_with_text_or_timing(self):
        row = {"evidence_id": "v:0", "start_seconds": 0, "end_seconds": 1, "text": "a"}
        original = context_digest([row])
        self.assertNotEqual(original, context_digest([{**row, "text": "b"}]))
        self.assertNotEqual(original, context_digest([{**row, "start_seconds": 0.5}]))

    def test_published_labels_follow_separate_decisions(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / "research/reviewed-delivery-patterns.json").read_text())
        patterns = report["patterns_by_candidate_label"]
        story_ids = {e["evidence_id"] for e in patterns["story_or_personal_experience"]["examples"]}
        qualification_ids = {e["evidence_id"] for e in patterns["uncertainty_or_qualification"]["examples"]}
        self.assertIn("S43F1BZfQKY:00011", story_ids)
        self.assertNotIn("-54zUwySKCg:00122", qualification_ids)
        practice = json.loads((root / "research/provisional-practice-patterns.json").read_text())
        for card in practice["patterns"]:
            label = card["candidate_label"]
            expected = sum(label in row["candidate_labels"] and label_supported(row, label)
                           for row in self.rows.values())
            self.assertEqual(card["eligibility"]["supported_count"], expected)

    def test_definition_is_not_any_use_of_means(self):
        for annotation_id in ("review-028", "review-029", "review-082", "review-085", "review-086"):
            self.assertFalse(label_supported(self.rows[annotation_id], "definition"))
        for annotation_id in ("review-006", "review-027", "review-083", "review-084"):
            self.assertTrue(label_supported(self.rows[annotation_id], "definition"))

    def test_failed_definition_card_is_retained_as_excluded(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / "research/provisional-practice-patterns.json").read_text())
        self.assertNotIn("definition", {card["candidate_label"] for card in report["patterns"]})
        excluded = {card["candidate_label"]: card for card in report["excluded_patterns"]}
        self.assertEqual(excluded["definition"]["supported_count"], 4)
        self.assertEqual(excluded["definition"]["reviewed_count"], 9)
        self.assertIn("support rate below 0.70", excluded["definition"]["reasons"])


if __name__ == "__main__":
    unittest.main()
