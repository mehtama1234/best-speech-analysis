import json
import unittest
from pathlib import Path

from scripts.build_external_review_gate_index import build

ROOT = Path(__file__).resolve().parents[1]


class ExternalReviewGateIndexTests(unittest.TestCase):
    def test_all_pending_operations_have_routing_and_boundaries(self):
        index = build()
        self.assertEqual(len(index["gates"]), 10)
        self.assertEqual({gate["gate_id"] for gate in index["gates"]}, {"identity", "function", "recurrence", "phrase_forms", "multimodal", "delivery", "counterexamples", "learner", "listener_stimuli", "listener_outcomes"})
        self.assertTrue(all(gate["source"] and gate["form"] and gate["validator"] and gate["comparator_or_summarizer"] and gate["claim_boundary"] for gate in index["gates"]))


if __name__ == "__main__":
    unittest.main()
