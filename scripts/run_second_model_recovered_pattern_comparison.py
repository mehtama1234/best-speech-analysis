#!/usr/bin/env python3
"""Run a second local-model comparison over one representative item per pattern."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--HuggingFaceTB--SmolLM2-360M-Instruct/snapshots/a10cc1512eabd3dde888204e902eca88bddb4951")
PACKET = ROOT / "research/recovered-pattern-priority-review.json"
KEY = ROOT / "research/recovered-pattern-priority-review-key.json"
OUT = ROOT / "research/second-model-recovered-pattern-comparison.json"
MD = ROOT / "writeups/second-model-recovered-pattern-comparison.md"


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
        raise RuntimeError(f"second model snapshot is missing: {MODEL}")
    packet = json.loads(PACKET.read_text())
    key = json.loads(KEY.read_text())
    key_by_id = {item["blind_item_id"]: item for item in key["items"]}
    chosen = {}
    for item in packet["items"]:
        pattern_id = key_by_id[item["blind_item_id"]]["pattern_id"]
        chosen.setdefault(pattern_id, (item, key_by_id[item["blind_item_id"]]))
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    reports = []
    for pattern_id in sorted(chosen):
        item, mapping = chosen[pattern_id]
        prompt_data = {
            "candidate_form": mapping["candidate_form"],
            "category": mapping["category"],
            "evidence_layer": item["evidence_layer"],
            "excerpt": " ".join(e.get("text", "") for e in item.get("evidence", [])[:2])[:900],
        }
        messages = [
            {"role": "system", "content": (
                "You are a cautious second-review model. Return one JSON object "
                "with keys pattern_id, assessment, concerns, priority. assessment "
                "must be supports, alternate, insufficient, or indeterminate; "
                "concerns must be an array; priority must be high, medium, or low. "
                "Do not claim effectiveness or validation."
            )},
            {"role": "user", "content": f"pattern_id={pattern_id}\n" + json.dumps(prompt_data, ensure_ascii=False)},
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=180, do_sample=False)
        raw = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        reports.append({
            "pattern_id": pattern_id,
            "blind_item_id": item["blind_item_id"],
            "parsed_judgment": parse_object(raw),
            "raw_output": raw,
        })
    parsed = sum(1 for report in reports if report.get("parsed_judgment"))
    report = {
        "schema_version": "1.0",
        "status": "second_local_model_comparison_not_validation",
        "model_id": "HuggingFaceTB/SmolLM2-360M-Instruct",
        "model_snapshot": str(MODEL),
        "pattern_count": len(chosen),
        "parsed_judgment_count": parsed,
        "reports": reports,
        "promotion_eligible": False,
        "claim_boundary": "This is a second local-model comparison screen over one representative priority-packet item per pattern. It is not independent human semantic validation, recurrence evidence, delivery evidence, learner evidence, listener outcomes, causal evidence or effectiveness.",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Second-model recovered-pattern comparison",
        "",
        report["claim_boundary"],
        "",
        f"Patterns screened: **{report['pattern_count']}** · parseable second-model judgments: **{parsed}** · promotion eligible: **False**.",
        "",
        "Use disagreements to prioritize human review. Do not treat agreement between two small local models as validation.",
    ]) + "\n")
    print(json.dumps({"pattern_count": len(chosen), "parsed_judgment_count": parsed, "promotion_eligible": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
