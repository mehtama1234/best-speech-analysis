#!/usr/bin/env python3
"""Validate local JSON exports from the delivery proxy review browser."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "research/delivery-proxy-candidate-atlas.json"
ALIGNMENTS = {"indeterminate", "clear", "partial", "misaligned"}
IDENTITIES = {"not_reviewed", "uncertain", "supported"}
TEXT_FIELDS = ("vocal", "visual", "setting", "access", "alternate", "conflict")


def validate(payload: object, atlas: dict | None = None) -> list[str]:
    atlas = atlas or json.loads(ATLAS.read_text())
    allowed = {
        row["record_id"] or row["evidence_id"]: row["canonical_job"]
        for row in atlas["candidates"]
    }
    if not isinstance(payload, list):
        return ["export must be a JSON list"]
    errors: list[str] = []
    seen: set[str] = set()
    for number, row in enumerate(payload, 1):
        prefix = f"record {number}"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        record_id = str(row.get("record_id", "")).strip()
        if record_id not in allowed:
            errors.append(f"{prefix} references an unknown atlas record_id")
        elif row.get("job") != allowed[record_id]:
            errors.append(f"{prefix} job does not match atlas record")
        if record_id in seen:
            errors.append(f"{prefix} duplicates record_id")
        seen.add(record_id)
        if not str(row.get("reviewer", "")).strip():
            errors.append(f"{prefix} is missing reviewer code")
        if row.get("alignment") not in ALIGNMENTS:
            errors.append(f"{prefix} has invalid transcript alignment")
        if row.get("identity") not in IDENTITIES:
            errors.append(f"{prefix} has invalid identity status")
        if not str(row.get("updated_at", "")).strip():
            errors.append(f"{prefix} is missing updated_at")
        for field in TEXT_FIELDS:
            if not str(row.get(field, "")).strip():
                errors.append(f"{prefix} is missing {field}; write not reviewed/not available when appropriate")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_delivery_proxy_local_reviews.py EXPORT.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid delivery proxy local review export:\n" + "\n".join(f"- {error}" for error in errors[:60]))
        return 1
    print("delivery proxy local review export valid: local bounded observations only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
