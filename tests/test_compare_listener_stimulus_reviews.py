import copy
import json
import unittest
from pathlib import Path

from scripts.compare_listener_stimulus_reviews import compare

ROOT = Path(__file__).resolve().parents[1]


class CompareListenerStimulusReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-listener-stimulus-review-workbook.json").read_text())

    def record(self, name: str, disagreement: bool = False) -> dict:
        responses = {"reviewer_name": name, "reviewer_role": "independent", "review_date": "2026-09-18", "review_modality": "text", "conflict_statement": "none", "independent_attestation": True}
        values = {
            "proposition_equivalence": "equivalent", "readability_match": "matched", "target_isolation": "isolated", "accessibility": "pass", "safety": "pass", "condition_order_or_blinding": "adequate", "lock_decision": "lock_for_pilot",
        }
        for n, _item in enumerate(self.workbook["items"], 1):
            for field, value in values.items(): responses[f"item_{n}_{field}"] = "hold_for_revision" if disagreement and field == "lock_decision" and n == 1 else value
            responses[f"item_{n}_reviewer_code"] = name
            responses[f"item_{n}_rationale_and_revision"] = "synthetic rationale"
        return {"record_type": "listener_stimulus_independent_review", "workbook_id": self.workbook["workbook_id"], "responses": responses}

    def test_disagreement_is_preserved_and_never_promoted(self):
        report = compare([self.record("r1"), self.record("r2", disagreement=True)], self.workbook)
        self.assertEqual(report["status"], "agreement_report_not_lock_evidence")
        self.assertEqual(report["disagreement_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("adjudicator", report["next_step"])

    def test_duplicate_reviewer_is_rejected(self):
        with self.assertRaises(ValueError):
            compare([self.record("same"), self.record("same")], self.workbook)


if __name__ == "__main__":
    unittest.main()
