import json
import unittest
from pathlib import Path

from scripts.validate_corpus_identity_review import validate
from scripts.summarize_corpus_identity_reviews import summarize

ROOT = Path(__file__).resolve().parents[1]


class ValidateCorpusIdentityReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-identity-review-workbook.json").read_text())

    def test_partial_export_is_rejected(self):
        errors = validate({"record_type": "corpus_identity_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Identity and duplication review only; not recurrence or effectiveness evidence.", "responses": {}}, self.workbook)
        self.assertTrue(errors)
        self.assertIn("independent_attestation must be true", errors)

    def synthetic(self):
        responses = {"reviewer_name": "synthetic", "reviewer_role": "reviewer", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "synthetic", "independent_attestation": True}
        for number, _item in enumerate(self.workbook["items"], 1):
            responses.update({f"item_{number}_speaker_identity": "verified", f"item_{number}_event_identity": "verified_distinct_event", f"item_{number}_upload_event_match": "confirmed", f"item_{number}_duplicate_or_compilation_status": "distinct_for_counting", f"item_{number}_source_provenance_status": "official_or_primary", f"item_{number}_reviewer_code": "synthetic", f"item_{number}_rationale_or_uncertainty": "Synthetic test decision."})
        return {"record_type": "corpus_identity_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Identity and duplication review only; not recurrence or effectiveness evidence.", "responses": responses}

    def test_summary_preserves_identity_boundary(self):
        report = summarize([self.synthetic()], self.workbook)
        self.assertEqual(report["reviewed_item_count_per_export"], self.workbook["item_count"])
        self.assertFalse(report["promotion_eligible"])
        self.assertEqual(report["decision_distributions"]["speaker_identity"]["verified"], self.workbook["item_count"])


if __name__ == "__main__":
    unittest.main()
