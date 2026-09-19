import json
import unittest
from pathlib import Path

from scripts.compare_corpus_phrase_form_reviews import compare

ROOT = Path(__file__).resolve().parents[1]


class CompareCorpusPhraseFormReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-phrase-form-independent-review-workbook.json").read_text())

    def record(self, name: str, disagreement: bool = False) -> dict:
        responses = {"reviewer_name": name, "reviewer_role": "independent", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "none", "independent_attestation": True}
        for number, _item in enumerate(self.workbook["items"], 1):
            responses.update({f"item_{number}_form_match_decision": "confirmed", f"item_{number}_primary_function": "other", f"item_{number}_speaker_event_identity": "distinct_event", f"item_{number}_duplicate_or_compilation_risk": "low", f"item_{number}_recurrence_decision": "indeterminate" if disagreement and number == 1 else "admit_as_candidate", f"item_{number}_alternate_function": "Synthetic alternate.", f"item_{number}_reason": "Synthetic reason."})
        return {"record_type": "corpus_phrase_form_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Phrase-form review only; not delivery effectiveness or audience outcome evidence.", "responses": responses}

    def test_disagreement_is_preserved_and_not_promoted(self):
        report = compare([self.record("r1"), self.record("r2", True)], self.workbook)
        self.assertEqual(report["disagreement_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("Adjudicate", report["next_step"])

    def test_duplicate_reviewer_is_rejected(self):
        with self.assertRaises(ValueError):
            compare([self.record("same"), self.record("same")])


if __name__ == "__main__":
    unittest.main()
