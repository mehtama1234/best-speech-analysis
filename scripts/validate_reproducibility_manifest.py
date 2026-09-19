#!/usr/bin/env python3
"""Validate that the reproducibility manifest still matches local artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from .build_reproducibility_manifest import build
except ImportError:
    from build_reproducibility_manifest import build

ROOT = Path(__file__).resolve().parents[1]


def validate(manifest: dict) -> list[str]:
    current = build()
    errors = []
    if manifest.get("manifest_id") != current["manifest_id"]:
        errors.append("manifest_id is invalid")
    if manifest.get("status") != current["status"]:
        errors.append("manifest status is invalid")
    if manifest.get("coverage_snapshot") != current["coverage_snapshot"]:
        errors.append("coverage snapshot is stale")
    expected = {(item["path"], item["sha256"]) for item in current["artifacts"]}
    actual = {(item.get("path"), item.get("sha256")) for item in manifest.get("artifacts", [])}
    if actual != expected:
        errors.append("artifact hashes or artifact set are stale")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "research/reproducibility-manifest.json"
    errors = validate(json.loads(path.read_text()))
    if errors:
        print("invalid reproducibility manifest:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("reproducibility manifest valid: artifact hashes and coverage reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
