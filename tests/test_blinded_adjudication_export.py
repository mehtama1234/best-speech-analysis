import unittest

from scripts.validate_blinded_adjudication_export import ITEM_COUNT, validate


class BlindedAdjudicationExportTests(unittest.TestCase):
    def test_rejects_missing_decisions(self):
        record = {"record_type": "blinded_review_adjudication", "claim_boundary": "not effectiveness evidence", "responses": {}}
        self.assertTrue(validate(record))

    def test_accepts_complete_bounded_decisions(self):
        responses = {"adjudicator_code": "A1", "adjudicator_role": "independent adjudicator", "adjudication_date": "2026-09-19", "conflict_statement": "none"}
        for number in range(1, ITEM_COUNT + 1):
            responses[f"item_{number}_final_decision"] = "indeterminate"
            responses[f"item_{number}_rationale"] = "Context is insufficient for promotion."
            responses[f"item_{number}_safety_note"] = "No additional note."
        record = {"record_type": "blinded_review_adjudication", "claim_boundary": "This does not establish effectiveness.", "responses": responses}
        self.assertEqual(validate(record), [])


if __name__ == "__main__":
    unittest.main()
