import unittest

from scripts.build_end_to_end_acceptance_matrix import build


class EndToEndAcceptanceMatrixTests(unittest.TestCase):
    def test_matrix_preserves_open_gates_and_requirement_evidence(self):
        matrix = build()
        self.assertEqual(matrix["status"], "research_checkpoint_not_complete")
        self.assertEqual(len(matrix["rows"]), 12)
        self.assertGreater(matrix["open_requirement_count"], 0)
        by_id = {row["requirement_id"]: row for row in matrix["rows"]}
        self.assertEqual(by_id["full_context_transcript"]["status"], "complete_for_fixed_corpus")
        self.assertEqual(by_id["learner_validation"]["status"], "protocol_ready_not_run")
        self.assertEqual(by_id["listener_outcome_separation"]["status"], "protocol_ready_not_run")
        self.assertTrue(all(row["evidence"] and row["remaining"] for row in matrix["rows"]))


if __name__ == "__main__":
    unittest.main()
