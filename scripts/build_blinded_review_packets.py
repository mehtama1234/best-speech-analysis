#!/usr/bin/env python3
"""Build label-blinded packets for independent transcript review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/blinded-review-packet.json"
KEY = ROOT / "research/blinded-review-packet-key.json"
MD = ROOT / "writeups/blinded-review-packet.md"


def blind_id(gate: str, source_id: str) -> str:
    digest = hashlib.sha256(f"{gate}:{source_id}".encode()).hexdigest()[:12]
    return f"blind-{gate}-{digest}"


def main() -> int:
    function = json.loads((ROOT / "research/corpus-function-independent-review-workbook.json").read_text())
    recurrence = json.loads((ROOT / "research/corpus-recurrence-independent-review-workbook.json").read_text())
    phrase = json.loads((ROOT / "research/corpus-phrase-form-independent-review-workbook.json").read_text())
    packet = {"schema_version": "1.0", "packet_id": "blinded-corpus-transcript-review", "status": "blinded_operational_packet_no_human_records", "claim_boundary": "This packet removes internal candidate labels and decisions for independent transcript review. It is an instrument, not evidence that any label, recurrence or phrase form is correct or effective.", "independence_instruction": "The reviewer must not be the analyst who created the source labels, phrase families or packet.", "gates": {}}
    key = {"schema_version": "1.0", "key_id": "blinded-corpus-transcript-review-key", "status": "internal_mapping_do_not_send_with_packet", "claim_boundary": "This key maps blinded IDs to internal source labels for later adjudication; it is not independent evidence.", "items": []}

    function_items = []
    for item in function["items"]:
        bid = blind_id("function", item["review_item_id"])
        function_items.append({"blind_item_id": bid, "video_id": item["video_id"], "title": item["title"], "evidence_id": item["evidence_id"], "start_seconds": item["start_seconds"], "end_seconds": item["end_seconds"], "transcript_text": item["transcript_text"], "source_url": item["source_url"], "event_split": item.get("event_split"), "review_prompt": "Read the surrounding context. Does this segment perform a distinct communication function? Name the primary function in your own words, an alternate if relevant, and whether the segment is interpretable."})
        key["items"].append({"blind_item_id": bid, "gate": "function", "source_review_item_id": item["review_item_id"], "internal_candidate_function": item.get("candidate_function")})
    packet["gates"]["function"] = {"item_count": len(function_items), "source_workbook": "research/corpus-function-independent-review-workbook.json", "items": sorted(function_items, key=lambda x: x["blind_item_id"])}

    recurrence_items = []
    for item in recurrence["items"]:
        bid = blind_id("recurrence", item["review_item_id"])
        recurrence_items.append({"blind_item_id": bid, "video_id": item["video_id"], "title": item["title"], "evidence_id": item["evidence_id"], "start_seconds": item["start_seconds"], "end_seconds": item["end_seconds"], "transcript_text": item["transcript_text"], "source_url": item["source_url"], "event_split": item.get("event_split"), "review_prompt": "Read the surrounding context. Describe what role the retrieved wording plays, whether another function is more plausible, and whether this occurrence should count for a recurrence comparison."})
        key["items"].append({"blind_item_id": bid, "gate": "recurrence", "source_review_item_id": item["review_item_id"], "internal_phrase_family": item.get("phrase_family"), "internal_matched_forms": item.get("matched_forms")})
    packet["gates"]["recurrence"] = {"item_count": len(recurrence_items), "source_workbook": "research/corpus-recurrence-independent-review-workbook.json", "items": sorted(recurrence_items, key=lambda x: x["blind_item_id"])}

    phrase_items = []
    for item in phrase["items"]:
        bid = blind_id("phrase", item["review_item_id"])
        examples = [{key: example.get(key) for key in ("evidence_id", "video_id", "title", "start_seconds", "end_seconds", "text", "event_split", "source_url")} for example in item.get("examples", [])]
        phrase_items.append({"blind_item_id": bid, "phrase_form": item["phrase_form"], "matched_pattern": item["matched_pattern"], "examples": examples, "review_prompt": "Check whether the exact form matches the retained examples, whether its context supports the retrieved family, and whether the sample supports inclusion in recurrence counting. Record ambiguity or duplication risk."})
        key["items"].append({"blind_item_id": bid, "gate": "phrase_form", "source_review_item_id": item["review_item_id"], "internal_family": item.get("family"), "internal_counts": {key: item.get(key) for key in ("occurrence_count", "video_count", "train_video_count", "holdout_video_count")}})
    packet["gates"]["phrase_form"] = {"item_count": len(phrase_items), "source_workbook": "research/corpus-phrase-form-independent-review-workbook.json", "items": sorted(phrase_items, key=lambda x: x["blind_item_id"])}
    key["items"].sort(key=lambda x: x["blind_item_id"])
    OUT.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    KEY.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Blinded transcript-review packet", "", "Status: **operational packet; no human records received**.", "", packet["claim_boundary"], "", "Send the packet without the key. The reviewer should use the exact source links and surrounding context, record uncertainty and disagreement, and return a separate coded export. Do not treat a completed packet as effectiveness evidence.", "", "| Gate | Items | Internal labels hidden |", "|---|---:|---|", f"| function | {len(function_items)} | candidate function and internal review state |", f"| recurrence | {len(recurrence_items)} | phrase family, matched-form list and internal review state |", f"| phrase form | {len(phrase_items)} | family, counts and internal review state |", "", "Files:", "", "- Packet to send: `research/blinded-review-packet.json`", "- Internal key: `research/blinded-review-packet-key.json` (do not send)", "- Source workbooks remain the authoritative response schemas and validators.", "", "Review boundaries:", "", "- Inspect complete context and source identity; use indeterminate when needed.", "- Do not infer speaker intent, delivery meaning, audience outcome or effectiveness.", "- Preserve disagreement and conflict statements.", "- Keep the internal key separate until adjudication.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"packet": str(OUT.relative_to(ROOT)), "key": str(KEY.relative_to(ROOT)), "function": len(function_items), "recurrence": len(recurrence_items), "phrase_form": len(phrase_items)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
