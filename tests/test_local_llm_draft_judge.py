import json
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LocalLlmDraftJudgeTests(unittest.TestCase):
    def test_draft_screen_is_parsed_and_non_promotional(self):
        report = json.loads((ROOT / "research/local-llm-draft-judge.json").read_text())
        self.assertEqual(report["status"], "local_model_draft_screen_recorded_not_effectiveness_evidence")
        self.assertEqual(report["model_id"], "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertEqual(report["sequence_id"], "make_a_proposal")
        draft = (ROOT / "research/example-speech-draft.md").read_text()
        self.assertEqual(report["input_artifact"], "research/example-speech-draft.md")
        self.assertEqual(report["draft_sha256"], hashlib.sha256(draft.encode()).hexdigest())
        self.assertEqual(report["parsed_judgment_count"], 1)
        self.assertIn(report["judgment"]["overall"], {"draft_screen_clear", "draft_screen_revise", "draft_screen_incomplete"})
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("not", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
