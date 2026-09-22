#!/usr/bin/env python3
"""Copy the bounded wave-2 crosswalk into the local browser evidence boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/home/mehta/git-repo/speaking-humor-and-communication-concepts-research/analysis/wave-2-unified-candidate-crosswalk.json")
OUTPUT = ROOT / "research/wave-2-unified-candidate-crosswalk.json"


def main() -> int:
    if not SOURCE.is_file():
        raise SystemExit(f"missing source crosswalk: {SOURCE}")
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    snapshot = dict(data)
    snapshot["local_snapshot"] = {
        "source_path": str(SOURCE),
        "status": "bounded_snapshot_not_independently_validated",
        "claim_boundary": "This is a local navigation snapshot of the broad-repository wave-2 crosswalk. It does not promote candidates into the fixed corpus or establish independent review, recurrence, learner outcomes, listener outcomes or effectiveness.",
    }
    OUTPUT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "row_count": len(snapshot.get("rows", [])), "status": snapshot["local_snapshot"]["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
