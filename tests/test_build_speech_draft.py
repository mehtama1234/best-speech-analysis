import unittest

from scripts.build_speech_draft import build


class SpeechDraftTests(unittest.TestCase):
    def test_draft_uses_sequence_stems_and_boundaries(self):
        text = build("make_a_proposal", "A safer launch", "the product team", "choose one next experiment")
        self.assertIn("# Speech worksheet: A safer launch", text)
        self.assertIn("Sentence stem:", text)
        self.assertIn("Listener check:", text)
        self.assertIn("Boundary check:", text)
        self.assertIn("Source examples:", text)
        self.assertIn("evidence `", text)
        self.assertIn("  > ", text)
        self.assertIn("Claim boundary", text)


if __name__ == "__main__":
    unittest.main()
