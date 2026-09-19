import json
import unittest
from pathlib import Path

from scripts.compare_corpus_identity_reviews import compare

ROOT = Path(__file__).resolve().parents[1]


class CompareCorpusIdentityReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-identity-review-workbook.json").read_text())

    def record(self, name: str, disagreement: bool = False) -> dict:
        responses = {"reviewer_name": name, "reviewer_role": "independent", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "none", "independent_attestation": True}
        values = {"speaker_identity": "verified", "event_identity": "verified_distinct_event", "upload_event_match": "confirmed", "duplicate_or_compilation_status": "distinct_for_counting", "source_provenance_status": "official_or_primary"}
        for number, _item in enumerate(self.workbook["items"], 1):
            for field, value in values.items():
                responses[f"item_{number}_{field}"] = "unclear" if disagreement and field == "event_identity" and number == 1 else value
            responses[f"item_{number}_reviewer_code"] = name
            responses[f"item_{number}_rationale_or_uncertainty"] = "Synthetic rationale."
        return {"record_type": "corpus_identity_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Identity and duplication review only; not recurrence or effectiveness evidence.", "responses": responses}

    def test_disagreement_is_preserved_and_never_promoted(self):
        report = compare([self.record("r1"), self.record("r2", True)], self.workbook)
        self.assertEqual(report["disagreement_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("adjudicator", report["next_step"])

    def test_duplicate_reviewer_is_rejected(self):
        with self.assertRaises(ValueError):
            compare([self.record("same"), self.record("same")], self.workbook)


if __name__ == "__main__":
    unittest.main()
