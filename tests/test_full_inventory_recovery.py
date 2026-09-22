import collections
import json
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FullInventoryRecoveryTest(unittest.TestCase):
    def test_coverage_layers_are_explicit_and_non_overlapping(self):
        coverage = json.loads((ROOT / "research/corpus-coverage-audit.json").read_text())
        self.assertEqual(coverage["inventory_count"], 480)
        self.assertEqual(coverage["canonical_full_context_review_count"], 395)
        self.assertEqual(coverage["recovered_machine_transcript_candidate_count"], 71)
        self.assertEqual(coverage["alternate_source_machine_transcript_candidate_count"], 11)
        self.assertEqual(coverage["unique_text_bearing_video_count"], 477)
        self.assertEqual(coverage["external_source_lead_count"], 3)
        self.assertEqual(coverage["external_transcript_candidate_count"], 1)
        self.assertEqual(coverage["unique_text_bearing_video_count_including_external"], 478)
        self.assertEqual(coverage["unresolved_after_media_recovery_count"], 14)
        canonical = set(coverage["layers"]["canonical_full_context"])
        recovered = set(coverage["layers"]["machine_transcript_candidates"])
        self.assertTrue(canonical.isdisjoint(recovered))

    def test_every_recovered_audio_row_is_a_candidate(self):
        rows = [
            json.loads(line)
            for line in (ROOT / "research/recovered-audio-transcripts.jsonl").read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 71)
        self.assertTrue(all(row["status"] == "machine_transcript_candidate" for row in rows))
        self.assertTrue(all(row["review_status"] == "not_human_reviewed" for row in rows))

    def test_full_inventory_pattern_layer_has_all_core_themes(self):
        payload = json.loads((ROOT / "research/full-inventory-pattern-candidates.json").read_text())
        self.assertEqual(len(payload["patterns"]), 22)
        self.assertEqual(payload["alternate_source_machine_transcript_count"], 11)
        self.assertEqual(payload["external_transcript_candidate_count"], 1)
        self.assertTrue(all(row["recovered_machine_video_count"] >= 0 for row in payload["patterns"]))
        self.assertIn("not semantic validation", payload["claim_boundary"])

    def test_all_55_pattern_matrix_reconciles_every_taxonomy_row(self):
        payload = json.loads((ROOT / "research/all-55-pattern-evidence.json").read_text())
        self.assertEqual(payload["pattern_count"], 55)
        self.assertEqual({row["category"] for row in payload["patterns"]}, {"core_theme", "structural_subtheme", "additional_subtheme"})
        self.assertTrue(all(row["candidate_form"] for row in payload["patterns"]))
        self.assertTrue(all("direct_recovered_flagged_video_count" in row for row in payload["patterns"]))
        self.assertTrue(all(row["direct_recovered_flagged_video_count"] <= row["direct_recovered_video_count"] for row in payload["patterns"]))

    def test_recovered_transcript_quality_audit_preserves_candidate_boundary(self):
        payload = json.loads((ROOT / "research/recovered-transcript-quality-audit.json").read_text())
        self.assertEqual(payload["candidate_count"], 83)
        self.assertEqual(payload["counts_by_evidence_layer"]["direct_audio"], 71)
        self.assertEqual(payload["counts_by_evidence_layer"]["alternate_source"], 11)
        self.assertEqual(payload["counts_by_evidence_layer"]["external_transcript"], 1)
        self.assertIn("does not establish semantic accuracy", payload["claim_boundary"])
        self.assertTrue(all(row["disposition"] for row in payload["rows"]))

    def test_recovered_pattern_rule_audit_covers_all_patterns(self):
        payload = json.loads((ROOT / "research/recovered-pattern-rule-audit.json").read_text())
        self.assertEqual(payload["pattern_count"], 55)
        self.assertEqual(len(payload["patterns"]), 55)
        self.assertGreaterEqual(payload["broad_density_pattern_count"], 1)
        self.assertIn("not a semantic match", payload["claim_boundary"])

    def test_local_model_triage_keeps_nonpromotion_boundary(self):
        payload = json.loads((ROOT / "research/local-llm-recovered-pattern-screen.json").read_text())
        self.assertEqual(payload["pattern_count"], 55)
        self.assertEqual(payload["candidate_card_count"], 2431)
        self.assertEqual(payload["batch_count"], 11)
        self.assertLessEqual(payload["parsed_judgment_count"], 55)
        self.assertFalse(payload["promotion_eligible"])
        self.assertIn("not human semantic validation", payload["claim_boundary"])

    def test_local_model_triage_schema_audit_preserves_unresolved_output(self):
        payload = json.loads((ROOT / "research/local-llm-recovered-pattern-screen-audit.json").read_text())
        self.assertEqual(payload["expected_pattern_count"], 55)
        self.assertEqual(payload["model_entry_count"], 55)
        self.assertEqual(payload["unique_model_pattern_count"], 55)
        self.assertEqual(payload["complete_schema_count"], 49)
        self.assertEqual(payload["field_variant_count"], 6)
        self.assertEqual(payload["unresolved_pattern_count"], 0)
        self.assertFalse(payload["promotion_eligible"])
        self.assertIn("schema-completeness audit", payload["claim_boundary"])
        self.assertIn("does not validate semantic accuracy", payload["claim_boundary"])

    def test_recovered_pattern_cards_retain_exact_evidence_and_boundaries(self):
        payload = json.loads((ROOT / "research/recovered-pattern-candidate-cards.json").read_text())
        self.assertEqual(payload["source_transcript_row_count"], 83)
        self.assertEqual(payload["candidate_card_count"], 2431)
        self.assertEqual(payload["patterns_with_cards"], 55)
        self.assertTrue(all(card["evidence"] for card in payload["cards"]))
        self.assertTrue(all(card["claim_status"] == "recovery_candidate_not_human_validated" for card in payload["cards"]))
        self.assertIn("source identity", payload["claim_boundary"])

    def test_recovered_pattern_review_workbook_is_blinded_and_complete(self):
        packet = json.loads((ROOT / "research/recovered-pattern-independent-review-workbook.json").read_text())
        key = json.loads((ROOT / "research/recovered-pattern-independent-review-key.json").read_text())
        self.assertEqual(packet["item_count"], 2431)
        self.assertEqual(len(packet["items"]), len(key["items"]))
        self.assertNotIn("pattern_id", packet["items"][0])
        self.assertTrue(all(item["pattern_id"] for item in key["items"]))
        self.assertIn("does not establish semantic accuracy", packet["claim_boundary"])

    def test_recovered_pattern_priority_packet_spans_all_patterns_without_promotion(self):
        packet = json.loads((ROOT / "research/recovered-pattern-priority-review.json").read_text())
        key = json.loads((ROOT / "research/recovered-pattern-priority-review-key.json").read_text())
        self.assertEqual(packet["pattern_count"], 55)
        self.assertEqual(packet["item_count"], 162)
        self.assertNotIn("patterns_covered", packet)
        self.assertEqual(len({item["pattern_id"] for item in key["items"]}), 55)
        self.assertEqual(len(packet["items"]), len(key["items"]))
        packet_text = json.dumps(packet)
        pattern_ids = {item["pattern_id"] for item in key["items"]}
        self.assertTrue(all(pattern_id not in packet_text for pattern_id in pattern_ids))
        self.assertEqual(
            {item["blind_item_id"] for item in packet["items"]},
            {item["blind_item_id"] for item in key["items"]},
        )
        self.assertFalse(packet.get("promotion_eligible", False))
        self.assertIn("does not establish semantic accuracy", packet["claim_boundary"])
        for forbidden in ("pattern_id", "candidate_form", "card_id", "category", "quality_flags", "quality_disposition"):
            self.assertNotIn(forbidden, json.dumps(packet))
        key_by_id = {item["blind_item_id"]: item for item in key["items"]}
        self.assertTrue(all(item.get("proposed_move") for item in packet["items"]))
        self.assertTrue(all(item["proposed_move"] == key_by_id[item["blind_item_id"]]["candidate_form"] for item in packet["items"]))
        self.assertTrue(all("proposed move" in item["review_prompt"] for item in packet["items"]))
        self.assertEqual(key["status"], "internal_priority_key_do_not_send_with_packet")

    def test_priority_review_batch_maximizes_source_coverage_with_bounded_reuse(self):
        packet = json.loads((ROOT / "research/recovered-pattern-priority-review.json").read_text())
        key = json.loads((ROOT / "research/recovered-pattern-priority-review-key.json").read_text())
        cards = json.loads((ROOT / "research/recovered-pattern-candidate-cards.json").read_text())["cards"]
        from scripts.build_recovered_pattern_priority_review import select

        selected = select(cards)
        selected_card_ids = {card["card_id"] for card in selected}
        linked_sources = [item["source_url"].rsplit("=", 1)[-1] for item in packet["items"]]
        catalog_sources = [item["video_id"] for item in packet["items"]]
        self.assertEqual(len(selected), 162)
        self.assertEqual(selected_card_ids, {item["card_id"] for item in key["items"]})
        self.assertEqual(len(set(linked_sources)), 83)
        self.assertEqual(len(set(catalog_sources)), 83)
        self.assertLessEqual(max(collections.Counter(linked_sources).values()), 3)
        self.assertLessEqual(max(collections.Counter(catalog_sources).values()), 3)
        self.assertEqual(packet["source_coverage"]["selected_linked_source_count"], 83)
        self.assertEqual(packet["source_coverage"]["candidate_linked_source_count"], 83)
        self.assertEqual(packet["source_coverage"]["maximum_items_per_linked_source"], 3)
        self.assertEqual(sum(packet["source_coverage"]["selected_evidence_layer_counts"].values()), 162)
        self.assertIn("Source reuse remains clustered evidence", packet["selection_rule"])

    def test_recovered_pattern_priority_browser_shows_target_but_hides_internal_labels(self):
        html = (ROOT / "writeups/recovered-pattern-priority-review.html").read_text()
        packet = json.loads((ROOT / "research/recovered-pattern-priority-review.json").read_text())
        self.assertIn("recovered_pattern_priority_review_draft_v1", html)
        self.assertIn("Download review export", html)
        self.assertIn("partial review", html)
        self.assertNotIn('"pattern_id"', html)
        self.assertIn("Proposed move to check:", html)
        self.assertIn("Yes — the excerpt shows this move", html)
        self.assertIn("did not create these candidate cards or labels", html)
        self.assertIn("have not seen the internal key or another reviewer’s decisions", html)
        embedded = re.search(r"<script id='items' type='application/json'>(.*?)</script>", html, re.DOTALL)
        self.assertIsNotNone(embedded)
        self.assertEqual(json.loads(embedded.group(1)), packet["items"])

    def test_priority_review_export_validator_preserves_missingness_and_rejects_bad_exports(self):
        from scripts.validate_recovered_pattern_priority_review_export import ITEM_IDS, validate

        responses = {
            item_id: {
                "decision": "indeterminate",
                "primary_function": "unclear",
                "alternate_explanation": "insufficient context",
                "context_note": "needs surrounding context",
                "identity_note": "identity requires review",
                "uncertainty_note": "machine candidate",
            }
            for item_id in ITEM_IDS
        }
        record = {
            "record_type": "recovered_pattern_priority_review",
            "review_packet_id": "recovered-pattern-priority-review",
            "claim_boundary": "independent review; not effectiveness evidence",
            "reviewer": {
                "reviewer_code": "R1",
                "reviewer_role": "independent reviewer",
                "review_date": "2026-09-22",
                "conflict_statement": "none",
                "independent_attestation": True,
            },
            "responses": responses,
        }
        self.assertEqual(validate(record), [])
        # A decided item must carry its requested context, while an undecided
        # item may remain entirely missing in a partial return.
        decided_id = sorted(ITEM_IDS)[0]
        record["responses"][decided_id]["context_note"] = "   "
        self.assertTrue(any("has a decision but is missing context_note" in error for error in validate(record)))
        record["responses"][decided_id]["context_note"] = "needs surrounding context"
        record["responses"].pop(sorted(ITEM_IDS)[0])
        self.assertEqual(validate(record), [])  # Valid partial exports retain missing item coverage.
        record["responses"]["unknown-blind-item"] = {"decision": "indeterminate"}
        self.assertTrue(validate(record))
        record["responses"].pop("unknown-blind-item")
        record["responses"][sorted(ITEM_IDS)[1]]["decision"] = "invalid_decision"
        self.assertTrue(validate(record))
        record["responses"][sorted(ITEM_IDS)[1]]["decision"] = ["indeterminate"]
        self.assertTrue(validate(record))

    def test_second_model_comparison_is_explicitly_non_corroborating(self):
        payload = json.loads((ROOT / "research/second-model-recovered-pattern-comparison-audit.json").read_text())
        self.assertEqual(payload["requested_pattern_count"], 55)
        self.assertEqual(payload["parsed_output_count"], 53)
        self.assertEqual(payload["complete_schema_count"], 47)
        self.assertEqual(payload["malformed_output_count"], 4)
        self.assertEqual(payload["missing_output_count"], 2)
        self.assertFalse(payload["use_for_corroboration"])
        self.assertFalse(payload["promotion_eligible"])
        self.assertIn("not independent human evidence", payload["claim_boundary"])

    def test_presentation_pattern_review_priorities_cover_all_patterns_without_ranking_effectiveness(self):
        payload = json.loads((ROOT / "research/presentation-pattern-review-priorities.json").read_text())
        self.assertEqual(payload["pattern_count"], 55)
        self.assertEqual(sum(payload["priority_tier_counts"].values()), 55)
        self.assertIn("not an effectiveness ranking", payload["claim_boundary"])
        self.assertTrue(all(row["review_action"] for row in payload["patterns"]))

    def test_recovered_pattern_review_browser_hides_candidate_labels(self):
        html = (ROOT / "writeups/recovered-pattern-independent-review.html").read_text()
        self.assertIn("recovered_pattern_review_draft_v1", html)
        self.assertIn("Download review export", html)
        self.assertNotIn('"pattern_id"', html)
        self.assertNotIn('"candidate_form"', html)


if __name__ == "__main__":
    unittest.main()
