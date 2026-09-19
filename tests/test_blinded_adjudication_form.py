import unittest

from scripts.build_blinded_adjudication_form import render


class BlindedAdjudicationFormTests(unittest.TestCase):
    def test_render_keeps_reference_and_requires_decision(self):
        html = render({"record_type": "blinded_review_adjudication_input", "items": [{"gate": "function", "blind_item_id": "blind-1", "source_review_item_id": "function:x", "internal_reference": {"internal_candidate_function": "opening"}, "reviewer_response": {"decision": "indeterminate"}}]})
        self.assertIn("internal_candidate_function", html)
        self.assertIn("item_1_final_decision", html)
        self.assertIn("adjudicator_record_not_effectiveness_evidence", html)


if __name__ == "__main__":
    unittest.main()
