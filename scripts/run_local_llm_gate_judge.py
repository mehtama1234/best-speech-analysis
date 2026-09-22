#!/usr/bin/env python3
"""Run a real local-model prioritization screen over the open evidence gates."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775")
INDEX = ROOT / "research/external-review-gate-index.json"
OUT = ROOT / "research/local-llm-gate-judge.json"
MD = ROOT / "writeups/local-llm-gate-judge.md"


def parse_json_object(raw: str) -> dict | None:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL | re.IGNORECASE)
    candidates = [fenced.group(1)] if fenced else []
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


def run() -> dict:
    gates = json.loads(INDEX.read_text())["gates"]
    compact = [{"gate_id": g["gate_id"], "title": g["title"], "status": g["status"], "item_count": g["item_count"], "action": g["action"], "claim_boundary": g["claim_boundary"]} for g in gates]
    if not MODEL.is_dir():
        raise RuntimeError(f"local model snapshot is missing: {MODEL}")
    import torch
    torch.set_num_threads(min(4, torch.get_num_threads()))
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, local_files_only=True)
    messages = [
        {"role": "system", "content": "You are a conservative research operations judge. Return one concise JSON object with keys overall, priority_gates, concerns, next_action. This is only prioritization. Never say a human gate is closed, evidence is complete, or a pattern is effective. Human review and participant outcomes remain open."},
        {"role": "user", "content": "Prioritize the next work across these ten open evidence gates. Prefer gates that unblock later work, but preserve the stated boundaries.\n" + json.dumps(compact, ensure_ascii=False)},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=160, do_sample=False)
    raw = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    parsed = parse_json_object(raw)
    if parsed and str(parsed.get("overall", "")).lower() in {"complete", "completed", "ready", "validated"}:
        parsed["overall"] = "prioritized_not_completed"
    return {
        "schema_version": "1.0",
        "report_id": "local-llm-gate-judge",
        "status": "local_model_gate_prioritization_recorded_human_gates_open",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "model_snapshot": str(MODEL),
        "gate_count": len(gates),
        "judgment_scope": "10_open_evidence_gate_prioritization_screen",
        "parsed_judgment_count": int(parsed is not None),
        "raw_model_output": raw,
        "judgment": parsed,
        "promotion_eligible": False,
        "claim_boundary": "This local-model judgment prioritizes validation operations from gate metadata. It is not independent human review, learner observation, listener outcome evidence, causal evidence or a promotion decision. All human gates remain open.",
    }


def render(report: dict) -> str:
    return "\n".join([
        "# Local LLM gate judge",
        "",
        f"Status: **{report['status']}**. Gates: **{report['gate_count']}**. Parsed judgment: **{report['parsed_judgment_count']}**.",
        "",
        report["claim_boundary"],
        "",
        "The raw model output is retained in the JSON receipt for auditability.",
        "",
    ])


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"local LLM gate judge: {report['status']} ({report['parsed_judgment_count']}/1 parsed)")
