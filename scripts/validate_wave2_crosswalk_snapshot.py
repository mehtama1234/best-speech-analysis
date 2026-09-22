#!/usr/bin/env python3
"""Verify that the local wave-2 navigation snapshot matches its source crosswalk."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/home/mehta/git-repo/speaking-humor-and-communication-concepts-research/analysis/wave-2-unified-candidate-crosswalk.json")
SNAPSHOT = ROOT / "research/wave-2-unified-candidate-crosswalk.json"


def validate(source: dict, snapshot: dict) -> list[str]:
    errors: list[str] = []
    if snapshot.get("status") != source.get("status"):
        errors.append("snapshot status differs from source crosswalk")
    if snapshot.get("rows") != source.get("rows"):
        errors.append("snapshot rows differ from source crosswalk")
    if snapshot.get("source_scope") != source.get("source_scope"):
        errors.append("snapshot source scope differs from source crosswalk")
    local = snapshot.get("local_snapshot", {})
    if local.get("status") != "bounded_snapshot_not_independently_validated":
        errors.append("snapshot must retain its bounded non-validation status")
    if len(snapshot.get("rows", [])) != 19:
        errors.append(f"expected 19 wave-2 rows, found {len(snapshot.get('rows', []))}")
    return errors


def main() -> int:
    if not SOURCE.is_file():
        print(f"ERROR: missing source crosswalk: {SOURCE}")
        return 1
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    errors = validate(source, snapshot)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("wave-2 crosswalk snapshot valid: local rows, source scope and provisional boundary reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
