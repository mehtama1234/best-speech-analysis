#!/usr/bin/env python3
"""Run a local language model as a conservative lesson-readiness judge."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775")
OUT = ROOT / "research/local-llm-lesson-judge.json"
MD = ROOT / "writeups/local-llm-lesson-judge.md"


def compact_cards() -> list[dict]:
    payload = json.loads((ROOT / "research/shared-lesson-cards.json").read_text())
    return [
        {
            "job": card["canonical_job"],
            "status": card["status"],
            "evidence_level": card["evidence_level"],
            "mechanism_status": card["mechanism_status"],
            "validation": card["validation"],
            "limits": card["limits"]["do_not_claim"],
        }
        for card in payload["cards"]
    ]


def parse_json_object(raw_output: str) -> dict | None:
    """Parse a model JSON object from a fenced or plain response."""
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
    cards = compact_cards()
    if not MODEL.is_dir():
        raise RuntimeError(f"local model snapshot is missing: {MODEL}")
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    system_message = (
        "You are a conservative research-readiness judge. Return one short JSON object "
        "with keys card_id, overall, concerns, next_action. overall must be provisional "
        "unless the metadata is internally unusable. Never call a lesson validated or "
        "effective. Human review and participant outcomes cannot be inferred."
    )
    aggregate_messages = [
        {
            "role": "system",
            "content": "You are a conservative research-readiness judge. Return one short JSON object with keys overall, concerns, next_action. Never call lessons validated or effective. Human review and participant outcomes cannot be inferred.",
        },
        {
            "role": "user",
            "content": "Judge these 18 provisional lesson records in one short response:\n" + json.dumps(cards, ensure_ascii=False),
        },
    ]
    def generate(messages: list[dict], max_new_tokens: int) -> tuple[str, dict | None]:
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        raw_output = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        return raw_output, parse_json_object(raw_output)

    aggregate_raw, aggregate = generate(aggregate_messages, 100)
    aggregate_judgments = [aggregate] if aggregate else []
    card_judgments = []
    for card in cards:
        raw_card, parsed_card = generate(
            [
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Judge this provisional lesson metadata.\n" + json.dumps(card, ensure_ascii=False)},
            ],
            80,
        )
        card_judgments.append(
            {
                "card_id": card["job"],
                "canonical_job": card["job"],
                "raw_model_output": raw_card,
                "judgment": parsed_card,
            }
        )
    return {
        "schema_version": "1.1",
        "report_id": "local-llm-lesson-judge",
        "status": "local_model_judgment_recorded_human_validation_open",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_snapshot": str(MODEL),
        "card_count": len(cards),
        "judgment_scope": "18_card_per_card_and_aggregate_metadata_screen",
        "parsed_judgment_count": len(aggregate_judgments),
        "per_card_judgment_count": sum(item["judgment"] is not None for item in card_judgments),
        "raw_model_output": aggregate_raw,
        "judgments": aggregate_judgments,
        "per_card_judgments": card_judgments,
        "promotion_eligible": False,
        "claim_boundary": "This is a local language-model readiness screen over provisional metadata. It is not independent human review, learner evidence, listener outcome evidence, causal evidence or proof of effectiveness. Promotion is forced false while human gates remain open.",
    }


def render(report: dict) -> str:
    return "\n".join([
        "# Local LLM lesson judge",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Model: `{report['model_id']}` · cards: **{report['card_count']}** · aggregate parsed: **{report['parsed_judgment_count']}** · per-card parsed: **{report['per_card_judgment_count']}** · promotion eligible: **{report['promotion_eligible']}**.",
        "",
        "The raw model output is retained in the JSON receipt for auditability. Human review and participant outcome gates remain open.",
        "",
    ])


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"local LLM lesson judge: {report['status']} ({report['parsed_judgment_count']}/{report['card_count']} parsed)")
