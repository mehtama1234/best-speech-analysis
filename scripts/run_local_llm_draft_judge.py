#!/usr/bin/env python3
"""Use the local Qwen model as a conservative screen of a speech worksheet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775")


def parse_json(raw: str) -> dict | None:
    decoder = json.JSONDecoder()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL | re.IGNORECASE)
    candidates = [fenced.group(1)] if fenced else []
    candidates.extend(raw[pos:] for pos, char in enumerate(raw) if char == "{")
    for candidate in candidates:
        try:
            value, _ = decoder.raw_decode(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def run(draft: str, sequence_id: str) -> dict:
    if not MODEL.is_dir():
        raise RuntimeError(f"local model snapshot is missing: {MODEL}")
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    messages = [
        {"role": "system", "content": "You are a conservative speech-workshop judge. Return one short JSON object with keys overall, strengths, missing_moves, boundary_concerns, listener_check, revision_priority. Judge only whether the draft visibly attempts its structure and leaves a listener check. Never claim effectiveness, persuasion, learning, causality, speaker intent, or validation. Use overall values draft_screen_clear, draft_screen_revise, or draft_screen_incomplete."},
        {"role": "user", "content": f"Sequence: {sequence_id}\nReview this draft worksheet:\n{draft[:12000]}"},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=140, do_sample=False)
    raw = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    judgment = parse_json(raw)
    if isinstance(judgment, dict) and judgment.get("overall") not in {"draft_screen_clear", "draft_screen_revise", "draft_screen_incomplete"}:
        judgment["overall"] = "draft_screen_revise"
    return {
        "schema_version": "1.0",
        "report_id": "local-llm-draft-judge",
        "status": "local_model_draft_screen_recorded_not_effectiveness_evidence",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_snapshot": str(MODEL),
        "sequence_id": sequence_id,
        "draft_character_count": len(draft),
        "draft_sha256": hashlib.sha256(draft.encode("utf-8")).hexdigest(),
        "parsed_judgment_count": int(judgment is not None),
        "raw_model_output": raw,
        "judgment": judgment,
        "promotion_eligible": False,
        "claim_boundary": "This local-model screen evaluates visible worksheet structure and revision prompts. It is not learner evidence, listener outcome evidence, causal evidence, independent review, speaker-intent evidence or proof of effectiveness.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "research/local-llm-draft-judge.json")
    args = parser.parse_args()
    report = run(args.draft.read_text(), args.sequence)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"local LLM draft judge: {report['status']} ({report['parsed_judgment_count']}/1 parsed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
