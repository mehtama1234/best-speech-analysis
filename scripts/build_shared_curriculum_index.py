#!/usr/bin/env python3
"""Build one provisional curriculum index across vertical slices 01 and 02."""

from __future__ import annotations

import html
import json
from pathlib import Path


def first_slice(root: Path) -> list[dict]:
    manifest = json.loads((root / "research/vertical-slice-01.json").read_text())
    rows = []
    for pattern in manifest["patterns"]:
        packet = json.loads((root / pattern["evidence_packet"]).read_text())
        rows.append({
            "pattern_id": pattern["pattern_id"],
            "slice": "vertical-slice-01",
            "communication_job": packet["communication_job"],
            "practice_hypothesis": packet["practice_hypothesis"],
            "evidence_level": packet["evidence_level"],
            "packet": pattern["evidence_packet"],
            "lesson": pattern["lesson"],
            "practice_flows": manifest["practice_flows"],
            "learner_check": manifest["learner_check_instrument"],
            "lesson_status": pattern["lesson_status"],
            "packet_status": packet["status"],
            "independent_review_status": pattern.get("independent_review_status", "pending"),
            "learner_status": manifest["learner_check_status"],
            "representative_example_count": len(packet.get("representative_examples", [])),
            "counterexample_count": len(packet.get("counterexamples", [])),
            "source_limit": packet["source_policy"],
            "multimodal_status": "partial_internal_review; independent_review_pending",
        })
    return rows


def second_slice(root: Path) -> list[dict]:
    manifest = json.loads((root / "research/vertical-slice-02.json").read_text())
    plan = json.loads((root / "research/vertical-slice-02-candidate-plan.json").read_text())
    by_id = {row["pattern_id"]: row for row in plan["candidates"]}
    rows = []
    for pattern in manifest["patterns"]:
        candidate = by_id[pattern["pattern_id"]]
        packet = json.loads((root / pattern["packet"]).read_text())
        rows.append({
            "pattern_id": pattern["pattern_id"],
            "slice": "vertical-slice-02",
            "communication_job": candidate["communication_job"],
            "practice_hypothesis": candidate["mechanism_hypothesis"],
            "evidence_level": "candidate_practice_hypothesis",
            "packet": pattern["packet"],
            "lesson": pattern["lesson"],
            "practice_flows": None,
            "learner_check": "writeups/vertical-slice-02-learner-check.html",
            "lesson_status": "draft_candidate_not_validated",
            "packet_status": packet["status"],
            "independent_review_status": "not_started",
            "learner_status": "not_started",
            "representative_example_count": len(packet.get("representative_examples", [])),
            "counterexample_count": len(packet.get("counterexamples", [])),
            "source_limit": packet["claim_boundary"],
            "multimodal_status": "internal_sample_review_complete; independent_review_pending",
        })
    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = first_slice(root) + second_slice(root)
    payload = {
        "schema_version": "1.0",
        "index_id": "shared-provisional-curriculum",
        "status": "eight_draft_lessons_not_validated",
        "evidence_level": "provisional_and_candidate_practice_hypotheses",
        "lesson_count": len(rows),
        "claim_boundary": "This index links transcript evidence, partial multimodal observations and draft practice tasks. It does not present patterns as proven communication effects or claim that learners have completed the tasks.",
        "shared_learner_check": "research/shared-learner-check.json",
        "shared_learner_check_html": "writeups/shared-learner-check.html",
        "shared_learner_check_validator": "scripts/validate_shared_learner_record.py",
        "shared_lesson_cards": "research/shared-lesson-cards.json",
        "shared_lesson_cards_html": "writeups/shared-lesson-cards.html",
        "lessons": rows,
        "validation_gates": {
            "independent_review": "pending_or_not_started",
            "learner_observations": "not_started",
            "listener_outcomes": "not_tested",
            "full_corpus_audiovisual_coverage": "not_complete",
        },
    }
    out = root / "research/shared-provisional-curriculum.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Speech Analysis — Provisional Curriculum</title>
<style>
:root {{ font-family: system-ui,-apple-system,Segoe UI,sans-serif; color:#202938; background:#f5f3ee; }}
body {{ margin:0; }} header {{ background:#17212b; color:white; padding:28px max(22px,calc((100vw - 1100px)/2)); }}
main {{ max-width:1100px; margin:24px auto; padding:0 22px 60px; }}
.notice {{ background:#fff7d6; border:1px solid #d8bd61; padding:14px; border-radius:8px; }}
.controls {{ margin:16px 0; display:flex; gap:12px; flex-wrap:wrap; }} input,select {{ font:inherit; padding:9px; border:1px solid #aaa; border-radius:6px; }}
.card {{ background:white; border:1px solid #d7d0c5; border-radius:10px; padding:18px; margin:14px 0; }}
.tag {{ display:inline-block; background:#e2edf5; border-radius:99px; padding:3px 8px; margin:2px; font-size:.82rem; }}
.meta {{ color:#5b6570; font-size:.9rem; }} a {{ color:#075985; }}
</style></head><body><header><h1>Provisional communication curriculum</h1><p>Eight evidence-linked draft lessons across two validation slices.</p></header>
<main><div class="notice"><b>Evidence boundary:</b> These are provisional practice hypotheses. Independent review, learner observations, listener outcomes and full-corpus audiovisual coverage remain incomplete. Use the <a href="../writeups/shared-lesson-cards.html">lesson-card learning surface</a> and <a href="../writeups/shared-learner-check.html">shared eight-lesson learner check</a> only as unvalidated tools.</div>
<div class="controls"><label>Search <input id="search" placeholder="pattern or communication job"></label><label>Slice <select id="slice"><option value="">All slices</option><option value="vertical-slice-01">Slice 01</option><option value="vertical-slice-02">Slice 02</option></select></label></div>
<p id="count"></p><section id="lessons"></section></main>
<script id="lesson-data" type="application/json">{data}</script><script>
const rows=JSON.parse(document.getElementById('lesson-data').textContent), out=document.getElementById('lessons'), input=document.getElementById('search'), slice=document.getElementById('slice'), count=document.getElementById('count');
function esc(v){{return String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));}}
function link(path,label){{return path ? `<a href="../${{esc(path)}}">${{label}}</a>` : '<span>practice flow not yet linked</span>';}}
function render(){{const q=input.value.toLowerCase(), s=slice.value; const xs=rows.filter(x=>(!q||JSON.stringify(x).toLowerCase().includes(q))&&(!s||x.slice===s)); count.textContent=`${{xs.length}} of ${{rows.length}} lessons`; out.innerHTML=xs.map(x=>`<article class="card"><div class="meta">${{esc(x.slice)}} · ${{esc(x.pattern_id)}} · ${{esc(x.evidence_level)}}</div><h2>${{esc(x.communication_job)}}</h2><p>${{esc(x.practice_hypothesis)}}</p><p><span class="tag">packet: ${{esc(x.packet_status)}}</span><span class="tag">review: ${{esc(x.independent_review_status)}}</span><span class="tag">learner: ${{esc(x.learner_status)}}</span><span class="tag">media: ${{esc(x.multimodal_status)}}</span></p><p>${{x.representative_example_count}} examples · ${{x.counterexample_count}} controls</p><p>${{link(x.lesson,'Open lesson')}} · ${{link(x.packet,'Evidence packet')}} · ${{link(x.learner_check,'Learner check')}}</p></article>`).join('')||'<p>No matching lesson.</p>';}}
input.addEventListener('input',render); slice.addEventListener('change',render); render();
</script></body></html>'''
    html_path = root / "writeups/shared-provisional-curriculum.html"
    html_path.write_text(page)
    md = root / "writeups/shared-provisional-curriculum.md"
    lines = [
        "# Shared provisional curriculum",
        "",
        "Eight draft lessons are linked across the two current evidence slices. This is a curriculum index, not a promotion claim.",
        "",
        "| Pattern | Slice | Lesson status | Independent review | Learner status |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| `{row['pattern_id']}` | `{row['slice']}` | `{row['lesson_status']}` | `{row['independent_review_status']}` | `{row['learner_status']}` |")
    lines += ["", "See the JSON for evidence links and limits, or use the HTML index for filtering. The shared eight-lesson lesson-card model is `research/shared-lesson-cards.json` with browser surface `writeups/shared-lesson-cards.html`; the learner protocol is `writeups/shared-learner-check.html`.", ""]
    md.write_text("\n".join(lines))
    print(json.dumps({"json": str(out), "html": str(html_path), "markdown": str(md), "lessons": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
