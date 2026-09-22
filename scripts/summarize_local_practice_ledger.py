#!/usr/bin/env python3
"""Summarize local practice-ledger metadata without scoring outcomes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from .ingest_local_practice_records import ledger_row_integrity_errors
    from .validate_practice_record import validate
except ImportError:
    from ingest_local_practice_records import ledger_row_integrity_errors
    from validate_practice_record import validate


def read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def summarize(records: list[dict]) -> dict:
    valid, invalid = [], []
    for index, record in enumerate(records, 1):
        # Raw records are accepted by this pure helper for callers that are
        # preparing a summary. Actual ingested ledger rows carry a hash and
        # must pass the tamper check before their metadata is counted.
        integrity_errors = ledger_row_integrity_errors(record) if "record_hash" in record or "ingested_at" in record else []
        errors = integrity_errors + validate(record)
        if errors:
            invalid.append({"index": index, "errors": errors})
        else:
            valid.append(record)
    jobs = Counter(record["canonical_job"] for record in valid)
    modalities = Counter(record["accessibility_or_modality"] for record in valid)
    response_counts = [len(record.get("step_responses", {})) for record in valid]
    return {
        "schema_version": "1.0",
        "status": "local_practice_metadata_only",
        "record_count": len(valid),
        "invalid_record_count": len(invalid),
        "invalid_records": invalid,
        "canonical_job_counts": dict(sorted(jobs.items())),
        "modality_counts": dict(sorted(modalities.items())),
        "response_count_total": sum(response_counts),
        "response_count_min": min(response_counts) if response_counts else 0,
        "response_count_max": max(response_counts) if response_counts else 0,
        "claim_boundary": "This summarizes local practice activity metadata only. It does not score performance, prove teachability, measure listener outcomes or establish effectiveness.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = summarize(read_ledger(args.ledger))
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
    return 1 if report["invalid_record_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
