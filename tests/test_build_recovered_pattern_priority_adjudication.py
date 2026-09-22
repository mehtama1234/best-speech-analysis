import unittest

from scripts.build_recovered_pattern_priority_adjudication import build_adjudication
from scripts.compare_recovered_pattern_priority_reviews import compare
from scripts.validate_recovered_pattern_priority_review_export import ITEM_IDS


def record(code, decision="indeterminate"):
    return {
        "record_type": "recovered_pattern_priority_review",
        "review_packet_id": "recovered-pattern-priority-review",
        "claim_boundary": "independent review; not effectiveness evidence",
        "reviewer": {"reviewer_code": code, "reviewer_role": "reviewer", "review_date": "2026-09-22", "conflict_statement": "none", "independent_attestation": True},
        "responses": {item_id: {"decision": decision, "primary_function": "unclear", "alternate_explanation": "insufficient", "context_note": "needs context", "identity_note": "unknown", "uncertainty_note": "candidate"} for item_id in ITEM_IDS},
    }


class PriorityAdjudicationTests(unittest.TestCase):
    def test_routes_disagreements_without_labels_or_promotion(self):
        comparison = compare([record("R1"), record("R2", "supports_candidate")])
        packet = build_adjudication(comparison)
        self.assertEqual(packet["item_count"], comparison["disagreement_count"])
        self.assertTrue(packet["items"])
        self.assertTrue(all(item["final_decision"] is None for item in packet["items"]))
        self.assertFalse(packet["promotion_eligible"])
        self.assertEqual(packet["items"][0]["reviewer_responses"]["R1"]["decision"], "indeterminate")
        self.assertTrue(packet["items"][0]["linked_source_video_id"])
        self.assertTrue(packet["items"][0]["proposed_move"])
        self.assertNotIn("pattern_id", str(packet))

    def test_preserves_partial_review_coverage_without_turning_it_into_disagreement(self):
        item_id = sorted(ITEM_IDS)[0]
        first, second = record("R1"), record("R2")
        first["responses"].pop(item_id)
        second["responses"][item_id] = {"decision": "", "context_note": "Source unavailable."}
        comparison = compare([first, second])
        packet = build_adjudication(comparison)

        self.assertEqual(packet["item_count"], 0)
        self.assertEqual(packet["status"], "no_structured_disagreement_missingness_preserved_no_promotion")
        self.assertEqual(packet["source_missingness"]["decision_coverage_status"], "partial")
        self.assertEqual(packet["source_missingness"]["missing_decision_item_ids"], [item_id])
        retained = packet["source_missingness"]["item_reviews_with_missing_decisions"][0]
        self.assertIsNone(retained["responses_by_reviewer"]["R1"])
        self.assertEqual(retained["responses_by_reviewer"]["R2"]["context_note"], "Source unavailable.")

    def test_rejects_promotable_comparison(self):
        comparison = compare([record("R1"), record("R2")])
        comparison["promotion_eligible"] = True
        with self.assertRaises(ValueError):
            build_adjudication(comparison)


if __name__ == "__main__":
    unittest.main()
