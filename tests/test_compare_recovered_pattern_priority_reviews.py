import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.compare_recovered_pattern_priority_reviews import compare
from scripts.validate_recovered_pattern_priority_review_export import ITEM_IDS, main as validate_main


def record(code: str, decision: str = "indeterminate") -> dict:
    return {
        "record_type": "recovered_pattern_priority_review",
        "review_packet_id": "recovered-pattern-priority-review",
        "claim_boundary": "independent review; not effectiveness evidence",
        "reviewer": {
            "reviewer_code": code,
            "reviewer_role": "independent reviewer",
            "review_date": "2026-09-22",
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


class ComparePriorityReviewsTests(unittest.TestCase):
    def test_preserves_disagreement_and_disables_promotion(self):
        report = compare([record("R1"), record("R2", "supports_candidate")])
        self.assertEqual(report["item_count"], len(ITEM_IDS))
        self.assertEqual(report["disagreement_count"], len(ITEM_IDS))
        self.assertFalse(report["promotion_eligible"])
        self.assertEqual(report["adjudication_status"], "not_started")
        self.assertEqual(report["source_cluster_summary"]["linked_source_video_count"], 83)
        self.assertEqual(report["source_cluster_summary"]["maximum_items_per_linked_source_video"], 3)
        self.assertIn("not independent video-level replications", report["claim_boundary"])
        self.assertEqual(
            sum(len(cluster["blind_item_ids"]) for cluster in report["source_cluster_summary"]["linked_source_clusters"]),
            report["item_count"],
        )
        self.assertNotIn("pattern_id", json_text(report))

    def test_partial_returns_preserve_missingness_without_counting_it_as_agreement(self):
        item_id = sorted(ITEM_IDS)[0]
        first = record("R1")
        second = record("R2")
        first["responses"].pop(item_id)
        second["responses"][item_id] = {"decision": "", "context_note": "Source could not be accessed."}

        report = compare([first, second])

        self.assertEqual(report["decision_coverage_status"], "partial")
        self.assertEqual(report["items_with_missing_decisions"], 1)
        self.assertEqual(report["missing_decision_pairs"], 2)
        self.assertEqual(report["missing_decision_item_ids"], [item_id])
        self.assertEqual(report["agreement"]["decision"]["items_with_two_or_more_observations"], len(ITEM_IDS) - 1)
        self.assertEqual(report["agreement"]["decision"]["unanimous_items"], len(ITEM_IDS) - 1)
        self.assertFalse(report["promotion_eligible"])
        coverage_by_reviewer = {entry["reviewer_code"]: entry for entry in report["reviewer_coverage"]}
        self.assertEqual(coverage_by_reviewer["R1"]["missing_decision_item_ids"], [item_id])
        self.assertEqual(coverage_by_reviewer["R2"]["missing_fields_by_item"][0]["blind_item_id"], item_id)
        self.assertIn("Source could not be accessed.", json_text(report))
        item_report = next(item for item in report["responses_by_item"] if item["blind_item_id"] == item_id)
        self.assertIsNone(item_report["responses_by_reviewer"]["R1"])
        self.assertEqual(item_report["responses_by_reviewer"]["R2"]["context_note"], "Source could not be accessed.")
        self.assertTrue(item_report["linked_source_video_id"])
        self.assertTrue(item_report["catalog_video_id"])

    def test_rejects_duplicate_reviewer_codes(self):
        with self.assertRaises(ValueError):
            compare([record("R1"), record("R1")])

    def test_validator_cli_reports_partial_coverage_honestly(self):
        partial = record("R1")
        partial["responses"] = {sorted(ITEM_IDS)[0]: partial["responses"][sorted(ITEM_IDS)[0]]}
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path(temp_dir) / "partial-review.json"
            export_path.write_text(json.dumps(partial))
            output = io.StringIO()
            with patch.object(sys, "argv", ["validate_recovered_pattern_priority_review_export.py", str(export_path)]), redirect_stdout(output):
                result = validate_main()
        self.assertEqual(result, 0)
        self.assertIn("1/162 decisions; partial; missingness preserved", output.getvalue())


def json_text(value):
    import json
    return json.dumps(value)


if __name__ == "__main__":
    unittest.main()
