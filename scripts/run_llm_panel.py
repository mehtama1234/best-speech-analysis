#!/usr/bin/env python3
"""Run two local models through four bounded review rubrics on blinded packets."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "research/llm-panel-vertical-slice-packets.json"
OUT = ROOT / "research/llm-panel-vertical-slice-results.json"
MODELS = {
    "qwen-0.5b": "/home/mehta/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775",
    "smollm-360m": next(iter(Path("/home/mehta/.cache/huggingface/hub/models--HuggingFaceTB--SmolLM2-360M-Instruct/snapshots").glob("*"))),
}
RUBRICS = {
    "source_context": "Does the supplied context support the stated claim? Flag overreach or ambiguity.",
    "counterexample_scope": "Do the controls and listed gaps prevent an overbroad lesson? Flag missing alternatives.",
    "lesson_transfer_safety": "Is the lesson task adaptable, specific, and safe without copying a speaker? Flag risks.",
    "adversarial": "Try to disprove the claim from this packet. Prefer revise or indeterminate when evidence is thin.",
}

def parse(raw: str) -> dict | None:
    for match in re.finditer(r"\{.*?\}", raw, re.S):
        try:
            value = json.loads(match.group())
            if value.get("decision") in {"support", "revise", "indeterminate"}: return value
        except json.JSONDecodeError: pass
    # Small local models often answer plainly despite the requested JSON. Recover
    # only unmistakable language; everything else remains fail-closed.
    lowered = raw.lower().strip()
    if re.search(r"\b(does not support|not enough|evidence is thin|missing|overbroad|unsafe|risk)\b", lowered):
        decision = "revise"
    elif re.search(r"^(yes[,!. ]|the provided context supports|the controls .*prevent|the lesson task is)", lowered):
        decision = "support"
    else:
        return None
    citations = re.findall(r"\bE[1-5]\b", raw)
    return {"decision": decision, "citations": citations, "reason": raw[:280], "confidence": "low"}

def prompt(packet: dict, rubric: str) -> list[dict]:
    return [
        {"role":"system","content":"You are one member of a cautious model-review panel. Judge only supplied evidence. Return exactly JSON: {\"decision\":\"support|revise|indeterminate\",\"citations\":[\"E1\"],\"reason\":\"max 35 words\",\"confidence\":\"low|medium|high\"}. Never claim audience response, learning, or effectiveness."},
        {"role":"user","content":RUBRICS[rubric] + "\n\n" + json.dumps(packet, ensure_ascii=False)},
    ]

def run_model(model_name: str, path: Path, packets: list[dict]) -> list[dict]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(min(4, torch.get_num_threads()))
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(path, local_files_only=True)
    results=[]
    for packet in packets:
        for rubric in RUBRICS:
            messages=prompt(packet, rubric)
            text=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs=tokenizer(text, return_tensors="pt", truncation=True, max_length=7500)
            generated=model.generate(**inputs, max_new_tokens=120, do_sample=False)
            raw=tokenizer.decode(generated[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            judgment=parse(raw) or {"decision":"indeterminate","citations":[],"reason":"Model output was not valid panel JSON.","confidence":"low"}
            results.append({"blind_packet_id":packet["blind_packet_id"],"rubric":rubric,"model":model_name,"raw_output":raw,"judgment":judgment})
    del model
    return results

def adjudicate(rows: list[dict], packet_id: str) -> dict:
    subset=[r for r in rows if r["blind_packet_id"]==packet_id]
    by_rubric={r: [x for x in subset if x["rubric"]==r] for r in RUBRICS}
    decisions={r:[x["judgment"]["decision"] for x in values] for r,values in by_rubric.items()}
    citation_complete=all(row["judgment"].get("citations") for row in subset)
    unanimous=all(len(set(values))==1 and values[0]=="support" for values in decisions.values()) and citation_complete
    return {"blind_packet_id":packet_id,"rubric_decisions":decisions,"model_disagreement":any(len(set(v))>1 for v in decisions.values()),"citation_complete":citation_complete,"decision":"model_panel_supported_for_bounded_practice" if unanimous else "model_panel_revision_or_more_evidence_needed","promotion_eligible":False}

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packets", type=Path, default=PACKETS, help="Blinded packet-set JSON.")
    parser.add_argument("--output", type=Path, default=OUT, help="Results JSON.")
    parser.add_argument("--include-not-ready", action="store_true", help="Run packets explicitly held for evidence gaps.")
    args=parser.parse_args()
    packet_set=json.loads(args.packets.read_text())
    packets=[packet for packet in packet_set["packets"] if args.include_not_ready or not packet.get("review_readiness", "").startswith("not_panel_ready")]
    rows=[]
    for name,path in MODELS.items(): rows.extend(run_model(name, Path(path), packets))
    report={"schema_version":"1.0","report_id":"llm-panel-vertical-slice-results","status":"two_model_four_rubric_panel_complete","packet_set":packet_set["packet_set_id"],"judgments":rows,"adjudications":[adjudicate(rows,p["blind_packet_id"]) for p in packets],"promotion_eligible":False,"claim_boundary":"Model-panel judgments assess supplied text, controls and lesson wording. They are not human review, learner evidence, listener evidence, or proof of effectiveness."}
    args.output.write_text(json.dumps(report,indent=2)+"\n")
    print(f"LLM panel complete: {len(rows)} judgments across {len(packets)} packets")
