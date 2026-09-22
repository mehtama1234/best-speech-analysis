import unittest
from pathlib import Path

from scripts.ingest_local_practice_records import ingest_records
from scripts.summarize_local_practice_ledger import summarize


def record():
    return {
        "record_type": "local_communication_practice_record",
        "schema_version": "1.0",
        "lesson_id": "mobile:provisional-job-opening",
        "pattern_id": "provisional-job-opening",
        "canonical_job": "opening",
        "source_evidence_ids": ["dgkxN6RASpg:00000"],
        "delivery_sample_ids": ["delivery:opening:01"],
        "participant_code": "synthetic-local-user",
        "consent": True,
        "accessibility_or_modality": "typed",
        "step_responses": {"rehearse": "synthetic"},
        "claim_boundary": "Local practice log only; not learner-validation evidence or effectiveness evidence.",
        "saved_at": "2026-09-19T00:00:00Z",
    }


class LocalPracticeLedgerSummaryTests(unittest.TestCase):
    def test_summary_preserves_metadata_only_boundary(self):
        report = summarize([record()])
        self.assertEqual(report["record_count"], 1)
        self.assertEqual(report["canonical_job_counts"], {"opening": 1})
        self.assertEqual(report["modality_counts"], {"typed": 1})
        self.assertIn("does not score performance", report["claim_boundary"])

    def test_invalid_records_are_reported(self):
        invalid = record()
        invalid["consent"] = False
        report = summarize([invalid])
        self.assertEqual(report["record_count"], 0)
        self.assertEqual(report["invalid_record_count"], 1)

    def test_tampered_ingested_row_is_not_counted(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "practice.jsonl"
            ingest_records([record()], ledger)
            row = __import__("json").loads(ledger.read_text())
            row["step_responses"]["rehearse"] = "modified after ingestion"
            report = summarize([row])
        self.assertEqual(report["record_count"], 0)
        self.assertEqual(report["invalid_record_count"], 1)
        self.assertIn("hash", report["invalid_records"][0]["errors"][0])


if __name__ == "__main__":
    unittest.main()
