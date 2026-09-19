import json
import unittest
from pathlib import Path

from scripts.summarize_corpus_function_review import summarize


ROOT = Path(__file__).resolve().parents[1]


class CorpusFunctionSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-function-independent-review-workbook.json").read_text())

    def test_synthetic_summary_preserves_labels_splits_and_boundary(self):
        responses = {
            "reviewer_name": "synthetic", "reviewer_role": "validator", "review_date": "2026-09-18",
            "review_modality": "synthetic", "conflict_statement": "structural test", "independent_attestation": True,
        }
        vocab = self.workbook["decision_vocabulary"]
        for number, _item in enumerate(self.workbook["items"], 1):
            for key, allowed in vocab.items():
                responses[f"item_{number}_{key}"] = allowed[0]
            responses[f"item_{number}_alternate_function"] = "synthetic alternative"
            responses[f"item_{number}_reason"] = "synthetic reason"
            responses[f"item_{number}_identity_or_duplicate_note"] = ""
        summary = summarize({"record_type": "corpus_function_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Function review only; not recurrence, effectiveness or listener outcome evidence.", "responses": responses}, self.workbook)
        self.assertEqual(summary["item_count"], 187)
        self.assertEqual(len(summary["by_candidate_function"]), 8)
        self.assertIn("train", summary["by_candidate_function"]["question"]["event_splits"])
        self.assertEqual(summary["status"], "validated_summary_non_promotional")
        self.assertIn("listener outcomes", summary["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
