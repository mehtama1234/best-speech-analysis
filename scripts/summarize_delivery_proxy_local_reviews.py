#!/usr/bin/env python3
"""Summarize validated local delivery reviews without promoting them."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts.validate_delivery_proxy_local_reviews import validate


ROOT = Path(__file__).resolve().parents[1]


def summarize(records: list[dict], atlas: dict | None = None) -> dict:
    if not records:
        raise ValueError("at least one local review record is required")
    errors = validate(records, atlas)
    if errors:
        raise ValueError("invalid local delivery review export: " + "; ".join(errors[:8]))
    by_job: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_job[record["job"]].append(record)
    rows = []
    for job, items in sorted(by_job.items()):
        rows.append({
            "job": job,
            "record_count": len(items),
            "unique_reviewer_count": len({item["reviewer"] for item in items}),
            "alignment_distribution": dict(sorted(Counter(item["alignment"] for item in items).items())),
            "identity_distribution": dict(sorted(Counter(item["identity"] for item in items).items())),
            "alternate_function_notes": sum(bool(item["alternate"].strip()) and item["alternate"].strip().lower() not in {"none", "not reviewed", "not available"} for item in items),
        })
    return {
        "schema_version": "1.0",
        "report_type": "delivery_proxy_local_review_summary",
        "status": "validated_local_observations_not_independent_validation",
        "record_count": len(records),
        "unique_clip_count": len({record["record_id"] for record in records}),
        "reviewer_codes": sorted({record["reviewer"] for record in records}),
        "by_job": rows,
        "claim_boundary": "This summarizes locally validated observation exports. Reviewer codes and complete fields do not establish reviewer independence, speaker identity, delivery meaning, effectiveness, teachability or listener outcomes.",
        "next_step": "Check reviewer conflict statements and independence separately; preserve disagreements and adjudicate only through the designated review process.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.records.read_text())
    summary = summarize(payload)
    rendered = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
