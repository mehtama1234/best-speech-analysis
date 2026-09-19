import json
import unittest
from pathlib import Path

from scripts.reduce_blinded_review_export import reduce


ROOT = Path(__file__).resolve().parents[1]


class BlindedReviewReducerTests(unittest.TestCase):
    def test_join_preserves_internal_reference_without_deciding(self):
        packet = json.loads((ROOT / "research/blinded-review-packet.json").read_text())
        key = json.loads((ROOT / "research/blinded-review-packet-key.json").read_text())
        responses = {"reviewer_code": "R1", "reviewer_role": "independent", "review_date": "2026-09-19", "conflict_statement": "none", "independent_attestation": True}
        number = 0
        for gate in ("function", "recurrence", "phrase_form"):
            for _item in packet["gates"][gate]["items"]:
                number += 1
                for field in ("decision", "primary_function", "alternate", "reason", "identity_note"):
                    responses[f"item_{number}_{field}"] = "indeterminate"
        export = {"record_type": "blinded_transcript_review", "packet_id": "blinded-corpus-transcript-review", "claim_boundary": "not effectiveness evidence", "responses": responses}
        result = reduce(export, key)
        self.assertEqual(len(result["items"]), 429)
        self.assertEqual(result["status"], "joined_for_adjudication_not_final_judgment")
        self.assertIn("internal_candidate_function", result["items"][0]["internal_reference"])
        self.assertEqual(result["items"][0]["reviewer_response"]["decision"], "indeterminate")


if __name__ == "__main__":
    unittest.main()
