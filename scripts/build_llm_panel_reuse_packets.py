#!/usr/bin/env python3
"""Build blinded, evidence-preserving packet queues for the full corpus."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = Path("/home/mehta/git-repo/speaking-humor-and-communication-concepts-research")
PLAYBOOK = ROOT / "research/presentation-pattern-playbook.json"
CROSSWALK = ROOT / "research/wave-2-unified-candidate-crosswalk.json"
EXPANSION_SOURCES = {
    "ali-siddiq-wave-2": ATLAS / "analysis/ali-siddiq-wave-2-context-packets.json",
    "dry-bar-comedy-wave-2-starter": ATLAS / "analysis/dry-bar-comedy-wave-2-starter-context-packets.json",
    "ted-wave-2-starter": ATLAS / "analysis/ted-wave-2-starter-context-packets.json",
}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def transcript_examples(card: dict) -> list[dict]:
    """Return the five cited captions with a small, source-blinded text window."""
    video_id = card["example_video_id"]
    captions = json.loads((ROOT / "data/transcripts" / f"{video_id}.json").read_text())["transcript"]
    examples = []
    for number, evidence_id in enumerate(card["example_evidence_ids"], 1):
        ordinal = int(evidence_id.rsplit(":", 1)[1])
        window = captions[max(0, ordinal - 2): ordinal + 3]
        examples.append({
            "evidence_ref": f"E{number}",
            "excerpt": captions[ordinal]["text"],
            "context": [row["text"] for row in window],
            "source_type": "retained_caption_context",
        })
    return examples


def make_fixed() -> tuple[dict, dict]:
    cards = json.loads(PLAYBOOK.read_text())["cards"]
    packets, key = [], []
    for number, card in enumerate(cards, 1):
        blind_id = f"FIELD-{number:03d}"
        packets.append({
            "blind_packet_id": blind_id,
            "review_readiness": "ready_with_missing_controls",
            "claim": card["candidate_form"],
            "examples": transcript_examples(card),
            "controls": [],
            "counterexample_status": {"status": "no_explicit_control_packet", "required_followup": "Add evidence-linked counterexamples before promotion."},
            "lesson": {"draft_task": card["draft_prompt"], "self_check": card["practice_check"], "status": "draft_only"},
            "media_limit": "The cited caption text does not establish delivery, audience response, or effectiveness.",
            "required_boundary": "Judge only the supplied text/context and lesson. Do not infer speaker intent, audience response, learning, or effectiveness.",
        })
        key.append({"blind_packet_id": blind_id, "pattern_id": card["pattern_id"], "source_video_id": card["example_video_id"], "evidence_ids": card["example_evidence_ids"], "card_sha256": digest(card)})
    return packet_set("llm-panel-fixed-fieldbook", packets), {"packet_set_id": "llm-panel-fixed-fieldbook", "key": key}


def load_expansion_items() -> dict[str, dict]:
    items = {}
    for source, path in EXPANSION_SOURCES.items():
        for packet in json.loads(path.read_text())["packets"]:
            items[(source, packet["item_id"])] = packet
    return items


def expansion_examples(item: dict) -> list[dict]:
    rows = []
    for reference in item.get("references", []):
        for excerpt in reference.get("bounded_retrieval_excerpts", []):
            rows.append({"excerpt": excerpt.get("text", ""), "context": [excerpt.get("text", "")], "source_type": "bounded_transcript_retrieval"})
    return [{"evidence_ref": f"E{number}", **row} for number, row in enumerate(rows[:5], 1)]


def make_expansion() -> tuple[dict, dict]:
    rows = json.loads(CROSSWALK.read_text())["rows"]
    source_items = load_expansion_items()
    packets, key = [], []
    for number, row in enumerate(rows, 1):
        item = source_items[(row["source"], row["review_item_id"])]
        examples = expansion_examples(item)
        blind_id = f"EXP-{number:03d}"
        readiness = "ready_for_model_review" if len(examples) >= 5 else "not_panel_ready_insufficient_distinct_excerpts"
        packets.append({
            "blind_packet_id": blind_id,
            "review_readiness": readiness,
            "claim": item["review_prompt"],
            "examples": examples,
            "controls": [],
            "counterexample_status": {"status": "no_explicit_control_packet", "required_followup": "Add counterexamples and at least five distinct contextual excerpts before promotion."},
            "lesson": {"draft_task": "State the move in neutral language, then write one original version for a different topic.", "self_check": "Name the claimed move, the supplied evidence, and what it cannot establish.", "status": "draft_only"},
            "media_limit": "Retrieved transcript excerpts do not establish delivery, audience response, transfer, or effectiveness.",
            "required_boundary": item["claim_boundary"],
        })
        key.append({"blind_packet_id": blind_id, "source": row["source"], "candidate_pattern": row["candidate_pattern"], "review_item_id": row["review_item_id"], "evidence_refs": row["evidence_refs"], "source_sha256": digest(item)})
    return packet_set("llm-panel-humor-ted-expansion", packets), {"packet_set_id": "llm-panel-humor-ted-expansion", "key": key}


def packet_set(packet_set_id: str, packets: list[dict]) -> dict:
    return {"schema_version": "1.0", "packet_set_id": packet_set_id, "status": "ready_for_packet_adapter", "packet_count": len(packets), "packets": packets, "claim_boundary": "Packets blind source identity and internal labels. A model-panel verdict is evidence review, not evidence of learner, listener, or effectiveness outcomes."}


def write(name: str, report: dict, key: dict) -> None:
    (ROOT / "research" / f"{name}-packets.json").write_text(json.dumps(report, indent=2) + "\n")
    (ROOT / "research" / f"{name}-packet-key.json").write_text(json.dumps(key, indent=2) + "\n")


if __name__ == "__main__":
    fixed, fixed_key = make_fixed()
    expansion, expansion_key = make_expansion()
    write("llm-panel-fixed-fieldbook", fixed, fixed_key)
    write("llm-panel-expansion", expansion, expansion_key)
    print(f"wrote {fixed['packet_count']} fieldbook and {expansion['packet_count']} expansion packets")
