import unittest

from scripts.validate_recovered_pattern_review_export import ITEM_IDS, validate


class RecoveredPatternReviewExportTests(unittest.TestCase):
    def test_rejects_incomplete_or_nonindependent_export(self):
        record = {
            "record_type": "recovered_pattern_independent_review",
            "workbook_id": "recovered-pattern-independent-review",
            "claim_boundary": "not effectiveness evidence",
            "reviewer": {"independent_attestation": False},
            "responses": {},
        }
        errors = validate(record)
        self.assertIn("independent_attestation must be true", errors)
        self.assertGreater(len(errors), len(ITEM_IDS))

    def test_accepts_complete_bounded_export_without_internal_labels(self):
        responses = {
            item_id: {
                "decision": "indeterminate",
                "primary_function": "unclear",
                "alternate_explanation": "insufficient context",
                "context_note": "needs surrounding context",
                "identity_note": "identity not independently confirmed",
                "uncertainty_note": "machine transcript candidate",
            }
            for item_id in ITEM_IDS
        }
        record = {
            "record_type": "recovered_pattern_independent_review",
            "workbook_id": "recovered-pattern-independent-review",
            "claim_boundary": "independent review; not effectiveness evidence",
            "reviewer": {
                "reviewer_code": "R1",
                "reviewer_role": "independent reviewer",
                "review_date": "2026-09-20",
                "conflict_statement": "none",
                "independent_attestation": True,
            },
            "responses": responses,
        }
        self.assertEqual(validate(record), [])


if __name__ == "__main__":
    unittest.main()
