import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PresentationBuilderTest(unittest.TestCase):
    def test_builder_has_all_architectures_and_patterns(self):
        html = (ROOT / "writeups/presentation-builder.html").read_text()
        sequences = json.loads((ROOT / "research/presentation-sequence-library.json").read_text())["sequences"]
        patterns = json.loads((ROOT / "research/presentation-pattern-playbook.json").read_text())["cards"]
        self.assertEqual(len(sequences), 6)
        self.assertEqual(len(patterns), 55)
        self.assertIn("Download Markdown outline", html)
        for sequence in sequences:
            self.assertIn(sequence["sequence_id"], html)
        for pattern in patterns:
            self.assertIn(pattern["pattern_id"], html)


if __name__ == "__main__":
    unittest.main()
