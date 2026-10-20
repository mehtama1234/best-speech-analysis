#!/usr/bin/env python3
"""Validate reusable LLM panel queues and fail on label/source leaks."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETS = (("llm-panel-fixed-fieldbook", 55), ("llm-panel-expansion", 19))
FORBIDDEN = ("pattern_id", "candidate_pattern", "video_id", "channel", "title", "review_item_id", "source_video_id")


def contains_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(key.lower() in FORBIDDEN or contains_forbidden_key(child) for key, child in value.items())
    if isinstance(value, list):
        return any(contains_forbidden_key(child) for child in value)
    return False


def validate(report: dict, key: dict, expected: int) -> list[str]:
    errors = []
    packets = report.get("packets", [])
    if report.get("packet_count") != expected or len(packets) != expected:
        errors.append(f"expected {expected} packets")
    if len(key.get("key", [])) != len(packets):
        errors.append("packet key does not reconcile")
    for packet in packets:
        if contains_forbidden_key(packet):
            errors.append(f"identity or label leak in {packet.get('blind_packet_id')}")
        if not packet.get("examples"):
            errors.append(f"no evidence in {packet.get('blind_packet_id')}")
        if packet.get("review_readiness") == "ready_for_model_review" and len(packet["examples"]) < 5:
            errors.append(f"ready packet has fewer than five excerpts: {packet.get('blind_packet_id')}")
    return errors


if __name__ == "__main__":
    errors = []
    for name, expected in SETS:
        report = json.loads((ROOT / "research" / f"{name}-packets.json").read_text())
        key = json.loads((ROOT / "research" / f"{name}-packet-key.json").read_text())
        errors.extend(f"{name}: {error}" for error in validate(report, key, expected))
    if errors:
        raise SystemExit("\n".join(errors))
    print("Reusable LLM panel packets valid")
