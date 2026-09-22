import tempfile
import unittest
from pathlib import Path

from scripts.ingest_local_practice_records import forget_hash, ingest_records, record_hash


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


class LocalPracticeIngestionTests(unittest.TestCase):
    def test_valid_record_is_appended_and_duplicate_is_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "practice.jsonl"
            self.assertEqual(ingest_records([record()], ledger)["accepted"], 1)
            report = ingest_records([record()], ledger)
            self.assertEqual(report["accepted"], 0)
            self.assertEqual(report["duplicates"], 1)

    def test_invalid_record_is_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "practice.jsonl"
            invalid = record()
            invalid["consent"] = False
            report = ingest_records([invalid], ledger)
            self.assertEqual(report["accepted"], 0)
            self.assertEqual(len(report["rejected"]), 1)
            self.assertFalse(ledger.exists())

    def test_consent_withdrawal_removes_one_hashed_record(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "practice.jsonl"
            ingest_records([record()], ledger)
            self.assertEqual(forget_hash(ledger, record_hash(record())), 1)
            self.assertEqual(ledger.read_text(), "")

    def test_corrupted_existing_ledger_blocks_new_writes(self):
        import json

        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "practice.jsonl"
            ingest_records([record()], ledger)
            row = json.loads(ledger.read_text())
            row["step_responses"]["rehearse"] = "tampered"
            ledger.write_text(json.dumps(row) + "\n")
            report = ingest_records([record()], ledger)
            self.assertEqual(report["accepted"], 0)
            self.assertEqual(len(report["ledger_integrity_errors"]), 1)
            self.assertEqual(len(ledger.read_text().splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
