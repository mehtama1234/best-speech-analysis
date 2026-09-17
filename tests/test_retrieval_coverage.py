import unittest
from scripts.audit_retrieval_coverage import census


class RetrievalCoverageTests(unittest.TestCase):
    def test_multilabel_counts_and_context_union(self):
        rows = [dict(video_id="a", evidence_id="a:0", candidate_speech_functions=["question", "example"]),
                dict(video_id="a", evidence_id="a:1", candidate_speech_functions=["unclassified"]),
                dict(video_id="b", evidence_id="b:0", candidate_speech_functions=["example"])]
        result = census(rows, {"a:0"}, {"a:0", "a:1"})
        self.assertEqual(result["totals"], {"segments": 3, "unclassified_segments": 1,
                         "contextual_target_segments": 1, "inspected_context_segments": 2})
        self.assertEqual(result["stored_label_occurrences"]["example"], 2)
        self.assertEqual(result["videos_with_segments"], 2)
        self.assertEqual(result["by_video"]["b"]["contextual_target_segments"], 0)
