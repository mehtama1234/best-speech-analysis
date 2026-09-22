#!/usr/bin/env python3
"""Run a conservative local-model triage over all recovered pattern candidates."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775")
CARDS = ROOT / "research/recovered-pattern-candidate-cards.json"
OUT = ROOT / "research/local-llm-recovered-pattern-screen.json"
MD = ROOT / "writeups/local-llm-recovered-pattern-screen.md"


def parse_object(raw: str) -> dict | None:
    candidates = []
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL | re.IGNORECASE)
    if fenced:
        candidates.append(fenced.group(1))
    candidates.extend(raw[pos:] for pos, char in enumerate(raw) if char == "{")
    decoder = json.JSONDecoder()
    for candidate in candidates:
        try:
            value, _ = decoder.raw_decode(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def make_batches(cards: list[dict]) -> list[list[dict]]:
    grouped = defaultdict(list)
    for card in cards:
        grouped[card["pattern_id"]].append(card)
    patterns = []
    for pattern_id, candidates in sorted(grouped.items()):
        candidates.sort(key=lambda card: (len(card.get("quality_flags", [])), card["video_id"]))
        patterns.append({
            "pattern_id": pattern_id,
            "category": candidates[0]["category"],
            "candidate_form": candidates[0]["candidate_form"],
            "candidate_video_count": len({card["video_id"] for card in candidates}),
            "excerpts": [
                {
                    "video_id": card["video_id"],
                    "evidence_layer": card["evidence_layer"],
                    "quality_flags": card.get("quality_flags", []),
                    "text": " ".join(item.get("text", "") for item in card.get("evidence", [])[:2])[:700],
                }
                for card in candidates[:3]
            ],
        })
    return [patterns[index:index + 5] for index in range(0, len(patterns), 5)]


def run() -> dict:
    if not MODEL.is_dir():
        raise RuntimeError(f"local model snapshot is missing: {MODEL}")
    source = json.loads(CARDS.read_text())
    batches = make_batches(source["cards"])
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    batch_reports = []
    for batch_number, batch in enumerate(batches, 1):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a conservative transcript triage assistant. "
                    "Return one JSON object with key patterns, an array with one "
                    "entry per pattern_id. Each entry must have pattern_id, "
                    "clarity (clear, mixed, or unclear), concerns (array), and "
                    "recommended_review_priority (high, medium, or low). "
                    "Judge only whether the excerpts plausibly instantiate the "
                    "candidate form. Never call a pattern validated, effective, "
                    "causal, or a best practice."
                ),
            },
            {
                "role": "user",
                "content": "Triage these recovered transcript candidates:\n" + json.dumps(batch, ensure_ascii=False),
            },
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=320, do_sample=False)
        raw = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        batch_reports.append({
            "batch_number": batch_number,
            "pattern_ids": [item["pattern_id"] for item in batch],
            "parsed_judgment": parse_object(raw),
            "raw_output": raw,
        })
    parsed = [item for batch in batch_reports if batch["parsed_judgment"] for item in batch["parsed_judgment"].get("patterns", [])]
    return {
        "schema_version": "1.0",
        "status": "local_model_recovered_pattern_triage_not_validation",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_snapshot": str(MODEL),
        "pattern_count": len(batches) and sum(len(batch) for batch in batches) or 0,
        "candidate_card_count": len(source["cards"]),
        "batch_count": len(batches),
        "parsed_judgment_count": len(parsed),
        "batch_reports": batch_reports,
        "promotion_eligible": False,
        "claim_boundary": (
            "This is a local language-model triage of representative recovered "
            "transcript excerpts. It is not human semantic validation, source "
            "identity review, recurrence evidence, delivery evidence, learner "
            "evidence, listener outcomes, causal evidence or effectiveness."
        ),
    }


def main() -> int:
    report = run()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Local-model recovered-pattern triage",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Patterns screened: **{report['pattern_count']}** · cards: **{report['candidate_card_count']}** · parsed judgments: **{report['parsed_judgment_count']}** · promotion eligible: **{report['promotion_eligible']}**.",
        "",
        "Use this report only to prioritize human context review. The raw model outputs are retained in the JSON receipt, and no model judgment changes pattern counts or status.",
    ]) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "pattern_count", "candidate_card_count", "batch_count", "parsed_judgment_count", "promotion_eligible")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
