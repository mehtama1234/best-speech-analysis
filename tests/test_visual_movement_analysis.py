import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VisualMovementAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/visual-movement-analysis.json").read_text())

    def test_local_feature_reports_and_detector_missingness_are_preserved(self):
        self.assertEqual(len(self.report["video_summary"]), 364)
        self.assertIn("scene-pixel", self.report["measurement_policy"])
        for row in self.report["video_summary"].values():
            self.assertIn("face_observable_frames", row)
            self.assertLessEqual(row["face_present_frames"], row["face_observable_frames"])


if __name__ == "__main__":
    unittest.main()
