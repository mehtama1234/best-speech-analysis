import unittest

from scripts.compare_recovered_pattern_reviews import compare
from scripts.validate_recovered_pattern_review_export import ITEM_IDS


def record(code: str, decision: str = "indeterminate") -> dict:
    return {
        "record_type": "recovered_pattern_independent_review",
        "workbook_id": "recovered-pattern-independent-review",
        "claim_boundary": "independent review; not effectiveness evidence",
        "reviewer": {
            "reviewer_code": code,
            "reviewer_role": "independent reviewer",
            "review_date": "2026-09-20",
            "conflict_statement": "none",
            "independent_attestation": True,
        },
        "responses": {
            item_id: {
                "decision": decision,
                "primary_function": "unclear",
                "alternate_explanation": "insufficient context",
                "context_note": "needs context",
                "identity_note": "not independently confirmed",
                "uncertainty_note": "candidate",
            }
            for item_id in ITEM_IDS
        },
    }


class CompareRecoveredPatternReviewsTests(unittest.TestCase):
    def test_preserves_disagreement_and_disables_promotion(self):
        first = record("R1")
        second = record("R2", decision="supports_candidate")
        report = compare([first, second])
        self.assertEqual(report["item_count"], len(ITEM_IDS))
        self.assertEqual(report["reviewer_count"], 2)
        self.assertEqual(report["disagreement_count"], len(ITEM_IDS))
        self.assertFalse(report["promotion_eligible"])
        self.assertEqual(report["adjudication_status"], "not_started")
        self.assertIn("source identity", report["claim_boundary"])

    def test_rejects_duplicate_reviewer_codes(self):
        with self.assertRaises(ValueError):
            compare([record("R1"), record("R1")])


if __name__ == "__main__":
    unittest.main()
