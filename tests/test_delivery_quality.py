import unittest
import json
from pathlib import Path
from scripts.delivery_quality import rate_exclusion_reason, screened_value


class RateQualityTests(unittest.TestCase):
    def test_four_millisecond_artifact_is_missing_not_clamped(self):
        row = {"start_seconds": 1028.26, "end_seconds": 1028.264,
               "words_per_second_proxy": 750, "mean_rms_db": -20}
        self.assertIsNone(screened_value(row, "words_per_second_proxy"))
        self.assertEqual(row["words_per_second_proxy"], 750)
        self.assertEqual(screened_value(row, "mean_rms_db"), -20)

    def test_exact_floor_and_high_rates_remain_reviewable(self):
        row = {"start_seconds": 0, "end_seconds": .25, "words_per_second_proxy": 12}
        self.assertIsNone(rate_exclusion_reason(row))
        self.assertEqual(screened_value(row, "words_per_second_proxy"), 12)

    def test_missing_invalid_and_nonfinite_rates_rejected(self):
        for row in ({}, {"start_seconds": 1, "end_seconds": 0, "words_per_second_proxy": 1},
                    {"start_seconds": 0, "end_seconds": 1, "words_per_second_proxy": float("nan")}):
            self.assertIsNone(screened_value(row, "words_per_second_proxy"))

    def test_real_artifact_preserved_and_excluded_from_reference(self):
        root = Path(__file__).resolve().parents[1]
        feature = json.loads((root / "data/features/AwA0Jnfj3ao.json").read_text())
        target = next(row for row in feature["aligned_transcript"] if row["evidence_id"] == "AwA0Jnfj3ao:00238")
        self.assertEqual(target["words_per_second_proxy"], 750)
        self.assertIsNone(screened_value(target, "words_per_second_proxy"))
        report = json.loads((root / "research/disjoint-delivery-comparison.json").read_text())
        metric = report["patterns"]["conclusion_or_summary"]["per_video"]["AwA0Jnfj3ao"]["metrics"]["words_per_second_proxy"]
        self.assertEqual(metric["all_usable_reference_count"], 238)
