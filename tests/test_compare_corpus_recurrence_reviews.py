import json
import unittest
from pathlib import Path

from scripts.compare_corpus_recurrence_reviews import compare

ROOT = Path(__file__).resolve().parents[1]


class CompareCorpusRecurrenceReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-recurrence-independent-review-workbook.json").read_text())

    def record(self, name: str, disagreement: bool = False) -> dict:
        responses = {"reviewer_name": name, "reviewer_role": "independent", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "none", "independent_attestation": True}
        vocab = self.workbook["decision_vocabulary"]
        for number, _item in enumerate(self.workbook["items"], 1):
            for key, allowed in vocab.items():
                responses[f"item_{number}_{key}"] = "exclude" if disagreement and key == "recurrence_include_decision" and number == 1 else allowed[0]
            responses[f"item_{number}_alternative_function"] = "Synthetic alternative"
            responses[f"item_{number}_reason"] = "Synthetic reason"
            responses[f"item_{number}_identity_or_duplicate_note"] = "Synthetic identity note"
        return {"record_type": "corpus_recurrence_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Recurrence review only; not phrase effectiveness or audience outcome evidence.", "responses": responses}

    def test_disagreement_is_preserved_and_not_promoted(self):
        report = compare([self.record("r1"), self.record("r2", True)], self.workbook)
        self.assertEqual(report["disagreement_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("Adjudicate", report["next_step"])

    def test_duplicate_reviewer_is_rejected(self):
        with self.assertRaises(ValueError):
            compare([self.record("same"), self.record("same")], self.workbook)


if __name__ == "__main__":
    unittest.main()
