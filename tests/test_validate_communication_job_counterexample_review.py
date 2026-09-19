import json
import unittest
from pathlib import Path

from scripts.validate_communication_job_counterexample_review import validate
from scripts.summarize_communication_job_counterexamples import summarize

ROOT = Path(__file__).resolve().parents[1]


class ValidateCommunicationJobCounterexampleReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-counterexample-workbook.json").read_text())

    def test_partial_export_is_rejected(self):
        errors = validate({"record_type": "communication_job_counterexample_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Counterexample review only; not outcome evidence.", "responses": {}}, self.workbook)
        self.assertTrue(errors)
        self.assertIn("independent_attestation must be true", errors)

    def synthetic(self, status="no_candidate_found"):
        responses = {"reviewer_name": "synthetic", "reviewer_role": "reviewer", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "synthetic", "independent_attestation": True}
        for number, _item in enumerate(self.workbook["items"], 1):
            responses.update({f"item_{number}_evidence_status": status, f"item_{number}_function_decision": "not_decidable", f"item_{number}_identity_status": "unclear", f"item_{number}_context_note": "No candidate was forced.", f"item_{number}_alternative_explanation": "Insufficient evidence.", f"item_{number}_safety_or_accessibility_note": "No added risk assessed.", f"item_{number}_reviewer_code": "synthetic"})
        return {"record_type": "communication_job_counterexample_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Counterexample and limitation review only; not delivery effectiveness or audience outcomes.", "responses": responses}

    def test_no_candidate_slots_are_summarized_without_promotion(self):
        report = summarize([self.synthetic()], self.workbook)
        self.assertEqual(report["record_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertEqual(report["by_job_and_type"][0]["status_counts"]["no_candidate_found"], 1)

    def test_confirmed_candidate_requires_source_fields(self):
        errors = validate(self.synthetic("confirmed_counterexample"), self.workbook)
        self.assertTrue(any("missing candidate source field" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
