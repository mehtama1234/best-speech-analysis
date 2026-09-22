#!/usr/bin/env python3
"""Screen only pattern IDs still absent from the reconciled triage receipt."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775")
CARDS = ROOT / "research/recovered-pattern-candidate-cards.json"
AUDIT = ROOT / "research/local-llm-recovered-pattern-screen-audit.json"
OUT = ROOT / "research/local-llm-recovered-pattern-gap-screen.json"
MD = ROOT / "writeups/local-llm-recovered-pattern-gap-screen.md"


def parse_object(raw: str) -> dict | None:
    decoder = json.JSONDecoder()
    for pos, char in enumerate(raw):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(raw[pos:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def main() -> int:
    if not MODEL.is_dir():
        raise RuntimeError(f"local model snapshot is missing: {MODEL}")
    unresolved = json.loads(AUDIT.read_text())["unresolved_pattern_ids"]
    grouped = defaultdict(list)
    for card in json.loads(CARDS.read_text())["cards"]:
        if card["pattern_id"] in unresolved:
            grouped[card["pattern_id"]].append(card)
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    reports = []
    for pattern_id in unresolved:
        candidates = sorted(grouped[pattern_id], key=lambda card: (len(card.get("quality_flags", [])), card["video_id"]))[:3]
        item = {
            "pattern_id": pattern_id,
            "category": candidates[0]["category"],
            "candidate_form": candidates[0]["candidate_form"],
            "excerpts": [{
                "video_id": card["video_id"],
                "evidence_layer": card["evidence_layer"],
                "quality_flags": card.get("quality_flags", []),
                "text": " ".join(e.get("text", "") for e in card.get("evidence", [])[:2])[:700],
            } for card in candidates],
        }
        messages = [
            {"role": "system", "content": (
                "Return exactly one JSON object with key patterns. The value must "
                "be an array containing exactly one object with keys pattern_id, "
                "clarity, concerns, recommended_review_priority. clarity must be "
                "clear, mixed, or unclear; concerns must be an array; priority "
                "must be high, medium, or low. Judge only plausibility of the "
                "candidate form. Never claim validation, effectiveness, causality, "
                "or best practice."
            )},
            {"role": "user", "content": "Triage this one candidate:\n" + json.dumps(item, ensure_ascii=False)},
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=180, do_sample=False)
        raw = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        parsed = parse_object(raw)
        reports.append({"pattern_id": pattern_id, "parsed_judgment": parsed, "raw_output": raw})
    parsed_ids = [r["pattern_id"] for r in reports if isinstance(r.get("parsed_judgment"), dict)]
    report = {
        "schema_version": "1.0",
        "status": "local_model_recovered_pattern_gap_screen_not_validation",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_snapshot": str(MODEL),
        "requested_pattern_ids": unresolved,
        "parsed_pattern_ids": parsed_ids,
        "batch_reports": reports,
        "promotion_eligible": False,
        "claim_boundary": (
            "This is a bounded local-model screen of previously unresolved pattern "
            "IDs. It is not human semantic validation, recurrence evidence, source "
            "identity review, delivery evidence, learner evidence, listener outcomes, "
            "causal evidence or effectiveness."
        ),
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Local-model recovered-pattern gap screen",
        "",
        report["claim_boundary"],
        "",
        f"Requested gaps: **{len(unresolved)}** · parsed: **{len(parsed_ids)}** · still unparsed: **{len(unresolved) - len(parsed_ids)}**.",
        "",
        "Raw outputs are retained. No failed parse is treated as a judgment.",
    ]) + "\n")
    print(json.dumps({"requested": len(unresolved), "parsed": len(parsed_ids), "unparsed": len(unresolved)-len(parsed_ids), "promotion_eligible": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
