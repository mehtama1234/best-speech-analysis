import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeliveryLearningGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = (ROOT / "writeups/delivery-learning-guide.md").read_text()

    def test_guide_covers_delivery_dimensions_and_boundaries(self):
        for heading in (
            "Timing and silence",
            "Pace and density",
            "Vocal emphasis and effort",
            "Turn, orientation and visible action",
            "Setting, edit and access",
        ):
            self.assertIn(heading, self.guide)
        for job in (
            "Opening", "Closing", "Question", "Answer or response",
            "Story or personal experience", "Example or case",
            "Contrast or disagreement", "Correction or reframe",
            "Repair or self-correction", "Qualification or boundary",
            "Definition or explanation", "Transition or structure",
            "Callback or repetition", "Humor or rapport",
            "Credit or acknowledgment", "Call to action or audience role",
            "Persuasion or advocacy", "Reflection or value frame",
        ):
            self.assertIn(f"| {job} |", self.guide)
        self.assertIn("354 videos have local audio/video", self.guide)
        self.assertIn("cannot yet prove", self.guide)
        self.assertIn("accessible equivalent", self.guide.lower())


if __name__ == "__main__":
    unittest.main()
