#!/usr/bin/env python3
"""Append validated local practice records to a consent-aware JSONL ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from .validate_practice_record import validate
except ImportError:
    from validate_practice_record import validate


def load_records(path: Path) -> list[dict]:
    payload = json.loads(path.read_text())
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
        return payload
    raise ValueError("input must be one practice record object or a list of objects")


def record_hash(record: dict) -> str:
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def source_record_from_ledger_row(row: dict) -> dict:
    """Recover the user-exported record before ingestion metadata was added."""
    return {key: value for key, value in row.items() if key not in {"record_hash", "ingested_at", "ingestion_boundary"}}


def ledger_row_integrity_errors(row: dict) -> list[str]:
    """Check the append-only hash envelope without judging the practice content."""
    if not isinstance(row, dict):
        return ["ledger row must be an object"]
    stored = row.get("record_hash")
    if not isinstance(stored, str) or not stored:
        return ["ledger row is missing record_hash"]
    expected = record_hash(source_record_from_ledger_row(row))
    return [] if stored == expected else ["ledger record hash does not match its content"]


def ingest_records(records: list[dict], ledger_path: Path | None = None, dry_run: bool = False) -> dict:
    accepted, rejected, duplicates = [], [], []
    existing_hashes: set[str] = set()
    ledger_integrity_errors: list[dict] = []
    if ledger_path and ledger_path.exists():
        for line_number, line in enumerate(ledger_path.read_text().splitlines(), 1):
            if line.strip():
                row = json.loads(line)
                row_errors = ledger_row_integrity_errors(row)
                if row_errors:
                    ledger_integrity_errors.append({"line": line_number, "errors": row_errors})
                if row.get("record_hash"):
                    existing_hashes.add(row["record_hash"])
    if ledger_integrity_errors:
        return {
            "accepted": 0,
            "rejected": [{"index": 0, "errors": ["existing ledger integrity check failed"]}],
            "duplicates": 0,
            "ledger_integrity_errors": ledger_integrity_errors,
            "dry_run": dry_run,
        }
    for number, record in enumerate(records, 1):
        errors = validate(record)
        if errors:
            rejected.append({"index": number, "errors": errors})
            continue
        digest = record_hash(record)
        if digest in existing_hashes:
            duplicates.append(digest)
            continue
        accepted.append({
            **record,
            "record_hash": digest,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "ingestion_boundary": "Practice log only; not independent review, learner validation, listener outcome or effectiveness evidence.",
        })
        existing_hashes.add(digest)
    if ledger_path and not dry_run and accepted:
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with ledger_path.open("a") as handle:
            for row in accepted:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {"accepted": len(accepted), "rejected": rejected, "duplicates": len(duplicates), "ledger_integrity_errors": [], "dry_run": dry_run}


def forget_hash(ledger_path: Path, digest: str) -> int:
    """Remove one record hash from the local ledger for consent withdrawal."""
    if not ledger_path.exists():
        return 0
    rows = [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()]
    kept = [row for row in rows if row.get("record_hash") != digest]
    removed = len(rows) - len(kept)
    if removed:
        ledger_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept))
    return removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, nargs="?")
    parser.add_argument("--ledger", type=Path, default=Path("data/local-practice-records.jsonl"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--forget-hash", help="Remove one record hash from the local ledger for consent withdrawal.")
    args = parser.parse_args()
    if args.forget_hash:
        print(json.dumps({"removed": forget_hash(args.ledger, args.forget_hash), "ledger": str(args.ledger)}))
        return 0
    if not args.input:
        parser.error("input is required unless --forget-hash is used")
    try:
        report = ingest_records(load_records(args.input), args.ledger, args.dry_run)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"invalid practice input: {error}")
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report["rejected"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
