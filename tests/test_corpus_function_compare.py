import json
import unittest
from pathlib import Path

from scripts.compare_corpus_function_reviews import compare


ROOT = Path(__file__).resolve().parents[1]


class CorpusFunctionCompareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-function-independent-review-workbook.json").read_text())

    def make_record(self, reviewer, alternate_first=False):
        responses = {
            "reviewer_name": reviewer, "reviewer_role": "validator", "review_date": "2026-09-18",
            "review_modality": "synthetic", "conflict_statement": "structural test", "independent_attestation": True,
        }
        vocab = self.workbook["decision_vocabulary"]
        for number, _item in enumerate(self.workbook["items"], 1):
            for key, allowed in vocab.items():
                responses[f"item_{number}_{key}"] = allowed[0]
            if alternate_first and number == 1:
                responses["item_1_candidate_label_decision"] = "indeterminate"
            responses[f"item_{number}_alternate_function"] = "synthetic alternative"
            responses[f"item_{number}_reason"] = "synthetic reason"
            responses[f"item_{number}_identity_or_duplicate_note"] = ""
        return {"record_type": "corpus_function_independent_review", "workbook_id": self.workbook["workbook_id"], "responses": responses}

    def test_compare_preserves_agreement_and_disagreement_without_promotion(self):
        report = compare([self.make_record("r1"), self.make_record("r2", alternate_first=True)], self.workbook)
        self.assertEqual(report["reviewer_count"], 2)
        self.assertEqual(report["item_count"], 187)
        self.assertEqual(report["agreement"]["context"]["unanimous_fraction"], 1.0)
        self.assertEqual(report["disagreement_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("listener outcomes", report["claim_boundary"])

    def test_compare_rejects_duplicate_reviewer_codes(self):
        with self.assertRaises(ValueError):
            compare([self.make_record("same"), self.make_record("same")], self.workbook)


if __name__ == "__main__":
    unittest.main()
