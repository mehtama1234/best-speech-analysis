#!/usr/bin/env python3
"""Validate exported local reviews from the full timing candidate atlas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "research/full-corpus-timing-candidate-atlas.json"
ALIGNMENTS = {"not_reviewed", "clear", "partial", "misaligned"}
CAUSES = {"not_reviewed", "speech_pause_or_boundary", "editing_or_cut", "music_or_ambience", "turn_or_response", "caption_segmentation", "missing_or_unclear"}


def validate(payload: object, atlas: dict | None = None) -> list[str]:
    atlas = atlas or json.loads(ATLAS.read_text())
    allowed = {row["candidate_id"] for row in atlas["items"]}
    if not isinstance(payload, list):
        return ["export must be a JSON list"]
    errors: list[str] = []
    seen: set[str] = set()
    for index, row in enumerate(payload):
        prefix = f"record {index}"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        if candidate_id not in allowed:
            errors.append(f"{prefix} references an unknown candidate_id")
        if candidate_id in seen:
            errors.append(f"{prefix} duplicates candidate_id")
        seen.add(candidate_id)
        if not str(row.get("reviewer", "")).strip():
            errors.append(f"{prefix} reviewer is required")
        if row.get("alignment") not in ALIGNMENTS:
            errors.append(f"{prefix} alignment is invalid")
        if row.get("cause") not in CAUSES:
            errors.append(f"{prefix} cause is invalid")
        if not str(row.get("observation", "")).strip():
            errors.append(f"{prefix} observation is required")
        if not str(row.get("accessibility", "")).strip():
            errors.append(f"{prefix} accessibility is required")
        if not str(row.get("updated_at", "")).strip():
            errors.append(f"{prefix} updated_at is required")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_timing_candidate_reviews.py EXPORT.json", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text())
    errors = validate(payload)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"valid timing review export: {len(payload)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
