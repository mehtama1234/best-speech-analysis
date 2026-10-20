#!/usr/bin/env python3
"""Fail closed if a blinded panel packet leaks its source identity or label."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate(report: dict, key: dict) -> list[str]:
    errors = []
    if report.get("packet_count") != 5 or len(report.get("packets", [])) != 5: errors.append("expected five vertical-slice packets")
    if len(key.get("key", [])) != len(report.get("packets", [])): errors.append("packet key does not reconcile")
    for packet in report.get("packets", []):
        text = json.dumps(packet).lower()
        if any(field in text for field in ("pattern_id", "video_id", "channel", "title", "reviewed_speech_function")): errors.append(f"identity or label leak in {packet.get('blind_packet_id')}")
        if len(packet.get("examples", [])) != 5: errors.append(f"wrong example count in {packet.get('blind_packet_id')}")
    return errors

if __name__ == "__main__":
    report = json.loads((ROOT / "research/llm-panel-vertical-slice-packets.json").read_text())
    key = json.loads((ROOT / "research/llm-panel-vertical-slice-packet-key.json").read_text())
    errors = validate(report, key)
    if errors: raise SystemExit("\n".join(errors))
    print("LLM panel packets valid")
