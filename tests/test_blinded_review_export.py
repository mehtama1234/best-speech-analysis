import unittest

from scripts.validate_blinded_review_export import validate, ITEM_COUNT


class BlindedReviewExportTests(unittest.TestCase):
    def test_rejects_incomplete_or_nonindependent_export(self):
        record = {"record_type": "blinded_transcript_review", "packet_id": "blinded-corpus-transcript-review", "claim_boundary": "not effectiveness", "responses": {"independent_attestation": False}}
        errors = validate(record)
        self.assertIn("independent_attestation must be true", errors)
        self.assertGreater(len(errors), ITEM_COUNT)

    def test_accepts_complete_bounded_export(self):
        responses = {"reviewer_code": "R1", "reviewer_role": "independent reviewer", "review_date": "2026-09-19", "conflict_statement": "none", "independent_attestation": True}
        for number in range(1, ITEM_COUNT + 1):
            for field in ("decision", "primary_function", "alternate", "reason", "identity_note"):
                responses[f"item_{number}_{field}"] = "indeterminate"
        record = {"record_type": "blinded_transcript_review", "packet_id": "blinded-corpus-transcript-review", "claim_boundary": "not effectiveness evidence", "responses": responses}
        self.assertEqual(validate(record), [])


if __name__ == "__main__":
    unittest.main()
