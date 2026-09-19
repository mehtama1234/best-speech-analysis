import json
import unittest
from pathlib import Path

from scripts.compare_multimodal_independent_reviews import compare

ROOT = Path(__file__).resolve().parents[1]


class CompareMultimodalIndependentReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/multimodal-independent-review-workbook.json").read_text())

    def record(self, name: str, disagreement: bool = False) -> dict:
        responses = {"reviewer_name": name, "reviewer_role": "independent", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "none", "independent_attestation": True}
        values = {"boundary_decision": "aligned", "candidate_function_decision": "supported", "speaker_setting_decision": "supported", "audio_visual_decision": "supports", "safety_decision": "safe_as_written"}
        for number, _item in enumerate(self.workbook["items"], 1):
            for field, value in values.items():
                responses[f"item_{number}_{field}"] = "indeterminate" if disagreement and field == "audio_visual_decision" and number == 1 else value
            responses[f"item_{number}_alternative_explanation"] = "Synthetic alternative."
            responses[f"item_{number}_reason"] = "Synthetic reason."
        return {"schema_version": "1.0", "record_type": "independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Validation of evidence boundaries only; not delivery effectiveness or audience outcomes.", "responses": responses}

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
