#!/usr/bin/env python3
"""Create label-blinded LLM review packets from evidence-linked lesson packets."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLICE = ROOT / "research/vertical-slice-01.json"
OUT = ROOT / "research/llm-panel-vertical-slice-packets.json"
KEY = ROOT / "research/llm-panel-vertical-slice-packet-key.json"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def compact_example(example: dict, number: int) -> dict:
    return {
        "evidence_ref": f"E{number}",
        "excerpt": example.get("text", ""),
        "context": [row.get("text", "") for row in example.get("context", [])],
        "existing_label_hidden": True,
        "source_type": "retained_caption_context",
    }


def compact_controls(packet: dict) -> list[dict]:
    raw = packet.get("counterexamples", {})
    rows = []
    for value in raw.values() if isinstance(raw, dict) else []:
        if isinstance(value, list):
            rows.extend(value)
    return [
        {
            "control_ref": f"C{index}",
            "surface_status": row.get("contrast_pattern_present", row.get("status", "not_stated")),
            "reason": row.get("why_it_is_a_control", row.get("why_selected", "")),
            "context": [part.get("text", "") for part in row.get("context", [])],
        }
        for index, row in enumerate(rows[:8], 1)
    ]


def counterexample_summary(packet: dict) -> dict:
    """Keep the review state without leaking unblinded source metadata."""
    raw = packet.get("counterexample_status", {})
    return {
        key: value for key, value in raw.items()
        if isinstance(value, (str, int, float, bool, type(None)))
        or (isinstance(value, list) and all(isinstance(item, str) for item in value))
    }


def build() -> dict:
    slice_data = json.loads(SLICE.read_text())
    packets, key = [], []
    for index, row in enumerate(slice_data["patterns"], 1):
        packet = json.loads((ROOT / row["evidence_packet"]).read_text())
        lesson = packet["learner_lesson"]
        blind_id = f"BLIND-{index:02d}"
        public = {
            "blind_packet_id": blind_id,
            "claim": packet["practice_hypothesis"],
            "examples": [compact_example(item, n) for n, item in enumerate(packet["representative_examples"], 1)],
            "controls": compact_controls(packet),
            "counterexample_status": counterexample_summary(packet),
            "lesson": {key: lesson.get(key) for key in ("draft_task", "self_check", "status")},
            "media_limit": packet.get("multimodal_status", {}).get("audio_measurement_caveat", "Media meaning not established."),
            "required_boundary": "Judge only the supplied text/context and lesson. Do not infer speaker intent, audience response, learning, or effectiveness.",
        }
        packets.append(public)
        key.append({"blind_packet_id": blind_id, "packet_id": packet["packet_id"], "pattern_id": packet["pattern_id"], "source_packet": row["evidence_packet"], "packet_sha256": digest(packet)})
    report = {
        "schema_version": "1.0", "packet_set_id": "llm-panel-vertical-slice-01", "status": "ready_for_model_panel",
        "packet_count": len(packets), "packets": packets,
        "claim_boundary": "These packets blind original pattern labels and source identity from model judges. They are for model review of retained text, controls and lesson wording; they do not supply human, learner, listener or effectiveness evidence.",
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    KEY.write_text(json.dumps({"packet_set_id": report["packet_set_id"], "key": key}, indent=2) + "\n")
    return report


if __name__ == "__main__":
    print(f"wrote {len(build()['packets'])} blinded LLM panel packets")
