import json
from pathlib import Path
import unittest

from scripts.lock_listener_stimuli import build_lock


ROOT = Path(__file__).resolve().parents[1]


class ListenerStimulusLockTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-listener-stimulus-review-workbook.json").read_text())
        cls.draft = json.loads((ROOT / "research/communication-job-listener-stimuli-draft.json").read_text())

    def record(self, code):
        responses = {
            "reviewer_name": code, "reviewer_role": "independent reviewer", "review_date": "2026-09-18",
            "review_modality": "synthetic test", "conflict_statement": "synthetic test", "independent_attestation": True,
        }
        values = {
            "proposition_equivalence": "equivalent", "readability_match": "matched", "target_isolation": "isolated",
            "accessibility": "pass", "safety": "pass", "condition_order_or_blinding": "adequate", "lock_decision": "lock_for_pilot",
        }
        for number in range(1, 19):
            for field, value in values.items(): responses[f"item_{number}_{field}"] = value
            responses[f"item_{number}_reviewer_code"] = code
            responses[f"item_{number}_rationale_and_revision"] = "Synthetic review rationale."
        return {"record_type": "listener_stimulus_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Stimulus suitability review only; not listener outcome evidence.", "responses": responses}

    def adjudication(self, decision="lock_for_pilot"):
        responses = {}
        for number in range(1, 19):
            responses[f"item_{number}_final_decision"] = decision
            responses[f"item_{number}_accessibility_safety"] = "pass" if decision == "lock_for_pilot" else "revise"
            responses[f"item_{number}_rationale"] = "Synthetic adjudication rationale."
        return {"record_type": "listener_stimulus_adjudication", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Explicit stimulus lock decision after independent review; lock is pilot readiness only, not listener outcome or communication-effectiveness evidence.", "adjudicator_code": "adj-test", "adjudication_date": "2026-09-18", "review_a_code": "review-a", "review_b_code": "review-b", "source_review_a": "a.json", "source_review_b": "b.json", "responses": responses}

    def test_all_pairs_lock_only_after_all_gates(self):
        result = build_lock(self.record("review-a"), self.record("review-b"), self.adjudication(), self.workbook, self.draft)
        self.assertEqual(result["status"], "locked_for_pilot")
        self.assertEqual(result["locked_pair_count"], 18)
        self.assertEqual(len(result["locked_stimuli"]), 18)

    def test_one_hold_keeps_entire_set_unlocked(self):
        result = build_lock(self.record("review-a"), self.record("review-b"), self.adjudication("hold_for_revision"), self.workbook, self.draft)
        self.assertEqual(result["status"], "not_locked")
        self.assertEqual(result["locked_pair_count"], 0)
        self.assertNotIn("locked_stimuli", result)
