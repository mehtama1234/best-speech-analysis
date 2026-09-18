#!/usr/bin/env python3
"""Build the shared JSON/HTML lesson index for vertical slice 01."""

from __future__ import annotations

import html
import json
from pathlib import Path


NAMES = ["contrast-or-disagreement", "example", "story", "uncertainty", "conclusion"]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "research/vertical-slice-01.json").read_text())
    records = []
    for pattern in manifest["patterns"]:
        packet = json.loads((root / pattern["evidence_packet"]).read_text())
        records.append(
            {
                "pattern_id": pattern["pattern_id"],
                "communication_job": packet["communication_job"],
                "practice_hypothesis": packet["practice_hypothesis"],
                "evidence_level": packet["evidence_level"],
                "packet": pattern["evidence_packet"],
                "lesson": pattern["lesson"],
                "practice_flows": manifest["practice_flows"],
                "learner_check": manifest["learner_check_instrument"],
                "lesson_status": pattern["lesson_status"],
                "packet_status": packet["status"],
                "independence_status": packet["independence_status"]["status"],
                "review_status": packet["independent_review"]["status"],
                "learner_status": manifest["learner_check_status"],
                "representative_example_count": len(packet["representative_examples"]),
                "counterexample_count": len(packet.get("counterexamples", [])),
                "source_limit": packet["source_policy"],
            }
        )
    shared = {
        "schema_version": "1.0",
        "index_id": "vertical-slice-01-lesson-index",
        "status": "draft_lessons_not_validated",
        "evidence_level": "provisional_practice_hypothesis",
        "learner_check": manifest["learner_check"],
        "lessons": records,
        "product_boundary": "This index links evidence and practice hypotheses. It does not present them as proven communication effects.",
    }
    json_path = root / "writeups/vertical-slice-01-lesson-index.json"
    json_path.write_text(json.dumps(shared, indent=2, ensure_ascii=False) + "\n")
    payload = json.dumps(records, ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Speech Analysis — Vertical Slice 01</title>
<style>
:root {{ font-family: system-ui,-apple-system,Segoe UI,sans-serif; color:#202938; background:#f5f3ee; }}
body {{ margin:0; }} header {{ background:#17212b; color:white; padding:28px max(22px,calc((100vw - 1100px)/2)); }}
main {{ max-width:1100px; margin:24px auto; padding:0 22px 60px; }}
.notice {{ background:#fff7d6; border:1px solid #d8bd61; padding:14px; border-radius:8px; }}
.controls {{ margin:16px 0; }} input {{ font:inherit; padding:9px; width:min(100%,480px); border:1px solid #aaa; border-radius:6px; }}
.card {{ background:white; border:1px solid #d7d0c5; border-radius:10px; padding:18px; margin:14px 0; }}
.tag {{ display:inline-block; background:#e2edf5; border-radius:99px; padding:3px 8px; margin:2px; font-size:.82rem; }}
.meta {{ color:#5b6570; font-size:.9rem; }} a {{ color:#075985; }}
</style></head><body><header><h1>Vertical Slice 01</h1><p>Communication jobs, evidence packets, and draft practice lessons.</p></header>
<main><div class="notice"><b>Evidence boundary:</b> These are provisional practice hypotheses. They have not been independently adjudicated or learner-validated and do not prove trust, memory, persuasion, or action effects.</div>
<div class="controls"><label>Filter lessons <input id="search" placeholder="communication job or pattern"></label></div><section id="lessons"></section></main>
<script id="lesson-data" type="application/json">{payload}</script><script>
const rows=JSON.parse(document.getElementById('lesson-data').textContent), out=document.getElementById('lessons'), input=document.getElementById('search');
function esc(v){{return String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));}}
function render(){{const q=input.value.toLowerCase(); const xs=rows.filter(x=>!q||JSON.stringify(x).toLowerCase().includes(q)); out.innerHTML=xs.map(x=>`<article class="card"><div class="meta">${{esc(x.pattern_id)}} · ${{esc(x.evidence_level)}}</div><h2>${{esc(x.communication_job)}}</h2><p>${{esc(x.practice_hypothesis)}}</p><p><span class="tag">packet: ${{esc(x.packet_status)}}</span><span class="tag">review: ${{esc(x.review_status)}}</span><span class="tag">learner: ${{esc(x.learner_status)}}</span></p><p>${{x.representative_example_count}} examples · ${{x.counterexample_count}} controls</p><p><a href="../${{esc(x.lesson)}}">Open draft lesson</a> · <a href="../${{esc(x.packet)}}">Inspect evidence packet</a> · <a href="../${{esc(x.practice_flows)}}">Practice flow</a> · <a href="../${{esc(x.learner_check)}}">Learner check</a></p></article>`).join('')||'<p>No matching lesson.</p>';}}
input.addEventListener('input',render); render();
</script></body></html>"""
    html_path = root / "writeups/vertical-slice-01-lesson-index.html"
    html_path.write_text(page)
    print(f"wrote {json_path}, {html_path}, {len(records)} lessons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
