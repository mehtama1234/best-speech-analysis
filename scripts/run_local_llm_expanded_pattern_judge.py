#!/usr/bin/env python3
"""Run a local LLM screen over the expanded corpus-mined pattern candidates."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775")
IN = ROOT / "research/expanded-pattern-candidate-cards.json"
OUT = ROOT / "research/local-llm-expanded-pattern-judge.json"
MD = ROOT / "writeups/local-llm-expanded-pattern-judge.md"


def parse_json_object(raw_output: str) -> dict | None:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_output, re.DOTALL | re.IGNORECASE)
    candidates = [fenced.group(1)] if fenced else []
    candidates.extend(raw_output[pos:] for pos, char in enumerate(raw_output) if char == "{")
    decoder = json.JSONDecoder()
    for candidate in candidates:
        try:
            value, _ = decoder.raw_decode(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def run() -> dict:
    source = json.loads(IN.read_text())
    cards = [
        {
            "card_id": card["card_id"],
            "title": card["title"],
            "source_kind": card["source_kind"],
            "source_record_count": card["source_record_count"],
            "source_video_count": card["source_video_count"],
            "candidate_form": card["candidate_form"],
            "source_excerpts": [example.get("excerpt", "")[:700] for example in card.get("examples", [])[:2] if example.get("excerpt")],
            "claim_boundary": card["claim_boundary"],
        }
        for card in source["cards"]
    ]
    if not MODEL.is_dir():
        raise RuntimeError(f"local model snapshot is missing: {MODEL}")
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    messages = [
        {
            "role": "system",
            "content": "You are a conservative curriculum judge. Return one short JSON object with keys overall, strongest_candidates, concerns, next_action. Treat every card as provisional. Never call a pattern validated, effective, causal, or a best practice. Human review and participant outcomes cannot be inferred.",
        },
        {
            "role": "user",
            "content": "Screen these 33 corpus-mined candidate speech patterns for whether they are clear enough to enter contextual review. Keep the answer concise.\n" + json.dumps(cards, ensure_ascii=False),
        },
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=180, do_sample=False)
    raw = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    parsed = parse_json_object(raw)
    return {
        "schema_version": "1.0",
        "report_id": "local-llm-expanded-pattern-judge",
        "status": "local_model_candidate_screen_recorded_review_open",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_snapshot": str(MODEL),
        "candidate_card_count": len(cards),
        "judgment_scope": "33_expanded_candidate_pattern_aggregate_screen",
        "input_scope": "candidate_metadata_plus_two_retained_caption_excerpts_per_card_when_available",
        "parsed_judgment_count": int(parsed is not None),
        "raw_model_output": raw,
        "judgment": parsed,
        "promotion_eligible": False,
        "claim_boundary": "This is a local language-model screen of corpus-mined candidate patterns. It is not contextual semantic validation, independent review, learner evidence, listener outcome evidence, causal evidence or proof of effectiveness. Promotion is forced false.",
    }


def render(report: dict) -> str:
    return "\n".join([
        "# Local LLM expanded-pattern judge",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Model: `{report['model_id']}` · candidate cards: **{report['candidate_card_count']}** · parsed judgment: **{report['parsed_judgment_count']}** · promotion eligible: **{report['promotion_eligible']}**.",
        f"Input: `{report['input_scope']}`.",
        "",
        "The raw output is retained in the JSON receipt. Candidate cards remain review leads until contextual and independent checks are complete.",
        "",
    ])


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"local LLM expanded pattern judge: {report['status']} ({report['parsed_judgment_count']}/1 parsed)")
