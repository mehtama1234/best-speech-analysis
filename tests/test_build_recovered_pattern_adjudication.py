import unittest

from scripts.build_recovered_pattern_adjudication import build_adjudication
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


class RecoveredPatternAdjudicationTests(unittest.TestCase):
    def test_routes_only_disagreements_and_keeps_promotion_disabled(self):
        comparison = compare([record("R1"), record("R2", decision="supports_candidate")])
        packet = build_adjudication(comparison)
        self.assertEqual(packet["item_count"], comparison["disagreement_count"])
        self.assertTrue(packet["items"])
        self.assertTrue(all(item["final_decision"] is None for item in packet["items"]))
        self.assertFalse(packet["promotion_eligible"])
        self.assertIn("does not establish recurrence", packet["claim_boundary"])

    def test_rejects_promotion_eligible_comparison(self):
        comparison = compare([record("R1"), record("R2")])
        comparison["promotion_eligible"] = True
        with self.assertRaises(ValueError):
            build_adjudication(comparison)


if __name__ == "__main__":
    unittest.main()
