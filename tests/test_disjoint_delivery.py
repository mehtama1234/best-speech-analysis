import unittest
import json
import hashlib
from pathlib import Path
from scripts.compare_disjoint_delivery import compare_video


def row(eid, start, value, windows=1):
    return {"evidence_id": eid, "start_seconds": start, "end_seconds": start + 1,
            "audio_window_count": windows, "mean_rms_db": value}


class DisjointComparisonTests(unittest.TestCase):
    def test_excludes_target_context_and_guard_band(self):
        rows = [row("v:t", 10, 100), row("v:near", 13, 100),
                row("v:context", 30, 100), row("v:cnear", 34, 100)]
        rows += [row(f"v:c{i}", 50 + i * 2, 10) for i in range(5)]
        result = compare_video(rows, {"v:t"}, {"v:context"})
        self.assertEqual(result["control_ids"], [f"v:c{i}" for i in range(5)])
        self.assertEqual(result["metrics"]["mean_rms_db"]["delta"], 90)
        self.assertAlmostEqual(result["metrics"]["mean_rms_db"]["all_usable_delta_same_targets"], 50)
        self.assertIsNone(result["metrics"]["mean_pitch_hz_proxy"]["delta"])

    def test_missing_or_inadequate_controls_are_not_zero(self):
        result = compare_video([row("v:t", 0, 10)], {"v:t"}, set())
        self.assertIsNone(result["metrics"]["mean_rms_db"]["delta"])
        self.assertEqual(compare_video([], {"v:absent"}, set())["measured_target_ids"], [])

    def test_nonfinite_values_and_unmeasured_rows_excluded(self):
        rows = [row("v:t", 0, 10)] + [row(f"v:c{i}", 50+i*2, 1) for i in range(4)]
        rows += [row("v:nan", 80, float("nan")), row("v:noaudio", 90, 1, 0)]
        result = compare_video(rows, {"v:t"}, set())
        self.assertEqual(result["metrics"]["mean_rms_db"]["control_count"], 4)
        self.assertIsNone(result["metrics"]["mean_rms_db"]["delta"])

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            compare_video([row("v:t", 0, 1), row("v:t", 5, 2)], {"v:t"}, set())

    def test_saved_report_provenance_and_disjointness(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / "research/disjoint-delivery-comparison.json").read_text())
        for name, digest in report["source_sha256"].items():
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest)
        features = {}
        for path in (root / "data/features").glob("*.json"):
            data = json.loads(path.read_text())
            features[data["video_id"]] = {row["evidence_id"]: row for row in data["aligned_transcript"]}
        for pattern in report["patterns"].values():
            for video, result in pattern["per_video"].items():
                by_id = features.get(video, {})
                blocked = set(result["excluded_context_or_target_ids"]) | set(result["requested_target_ids"])
                self.assertFalse(blocked & set(result["control_ids"]))
                for eid in result["control_ids"]:
                    control = by_id[eid]
                    for excluded in blocked & set(by_id):
                        segment = by_id[excluded]
                        self.assertFalse(control["start_seconds"] < segment["end_seconds"] + 5 and
                                         control["end_seconds"] > segment["start_seconds"] - 5)


if __name__ == "__main__":
    unittest.main()
