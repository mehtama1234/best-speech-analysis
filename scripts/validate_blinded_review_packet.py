#!/usr/bin/env python3
"""Check that a blinded packet does not leak internal candidate labels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FORBIDDEN = {"candidate_function", "phrase_family", "matched_forms", "internal_candidate_function", "internal_family", "internal_counts", "internal_reviewed_evidence"}


def validate(packet: dict) -> list[str]:
    errors = []
    if packet.get("packet_id") != "blinded-corpus-transcript-review":
        errors.append("packet_id is invalid")
    if "not" not in str(packet.get("claim_boundary", "")).lower():
        errors.append("claim boundary is missing")
    ids = set()
    for gate, payload in packet.get("gates", {}).items():
        for item in payload.get("items", []):
            bid = item.get("blind_item_id")
            if not bid or bid in ids:
                errors.append(f"duplicate or missing blind_item_id: {bid}")
            ids.add(bid)
            leaked = FORBIDDEN.intersection(item)
            if leaked:
                errors.append(f"{bid} leaks internal fields: {sorted(leaked)}")
    if len(ids) != sum(len(payload.get("items", [])) for payload in packet.get("gates", {}).values()):
        errors.append("blind IDs are not unique")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_blinded_review_packet.py PATH", file=sys.stderr)
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid blinded packet:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("blinded review packet valid: internal candidate labels absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
