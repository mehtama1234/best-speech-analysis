import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PoseProxyCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports = [json.loads(path.read_text()) for path in (ROOT / "data/pose-features").glob("*.json")]
        cls.geometry = json.loads((ROOT / "research/pose-geometry-analysis.json").read_text())
        cls.movement = json.loads((ROOT / "research/pose-movement-analysis.json").read_text())

    def test_full_local_feature_coverage_and_bounded_policy(self):
        self.assertEqual(len(self.reports), 364)
        self.assertEqual(self.geometry["pose_video_count"], 364)
        self.assertEqual(self.movement["video_count"], 364)
        self.assertIn("no gesture", self.geometry["measurement_policy"])
        self.assertIn("no gesture", self.movement["measurement_policy"])

    def test_landmark_records_are_observable_geometry_only(self):
        for report in self.reports:
            self.assertIn("MediaPipe Pose", report["model"])
            self.assertIn("no gesture", report["measurement_policy"])
            for frame in report["frames"]:
                self.assertIn("person_detected", frame)
                if frame["person_detected"]:
                    self.assertIn("keypoints", frame)
                    self.assertIn("visible_keypoint_count", frame)


if __name__ == "__main__":
    unittest.main()
