#!/usr/bin/env python3
"""Build a browser lesson surface from the shared lesson-card data model."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/shared-lesson-cards.json"
OUT = ROOT / "writeups/shared-lesson-cards.html"


def main() -> int:
    cards = json.loads(DATA.read_text())["cards"]
    payload = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")
    document = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Speech Analysis — Lesson Cards</title>
<style>
:root { font-family:system-ui,-apple-system,Segoe UI,sans-serif; color:#1d2935; background:#f5f3ee; }
body { margin:0; } header { background:#17212b; color:white; padding:28px max(20px,calc((100vw - 1160px)/2)); }
main { max-width:1160px; margin:22px auto; padding:0 20px 60px; }
.notice { background:#fff7d6; border:1px solid #d8bd61; border-radius:8px; padding:14px; }
.controls { display:flex; gap:10px; flex-wrap:wrap; margin:16px 0; }
input,select { font:inherit; padding:9px; border:1px solid #aab3bb; border-radius:6px; }
.card { background:white; border:1px solid #d6d0c7; border-radius:10px; margin:16px 0; padding:18px; }
.meta,.muted { color:#5c6872; font-size:.9rem; } .tag { display:inline-block; background:#e2edf5; border-radius:99px; padding:3px 8px; margin:2px; font-size:.82rem; }
details { margin-top:12px; border-top:1px solid #e1e5e8; padding-top:10px; } summary { cursor:pointer; font-weight:650; }
.example { background:#f4f8fb; border-left:4px solid #39739d; padding:10px; margin:10px 0; }
.task { background:#f8f6ef; border-left:4px solid #a87921; padding:10px; margin:8px 0; } a { color:#075985; }
</style></head><body><header><h1>Lesson cards</h1><p>Evidence-linked draft lessons for practising communication choices.</p></header>
<main><div class="notice"><b>Evidence boundary:</b> These cards are provisional practice hypotheses. Transcript evidence, delivery evidence, recurrence and learner status are shown separately. They do not prove effectiveness, intent, listener outcomes or universal best practice. Use the <a href="shared-learner-check.html">shared learner check</a> only as an unrun teachability protocol.</div>
<div class="controls"><label>Search <input id="search" placeholder="problem, pattern or phrase"></label><label>Slice <select id="slice"><option value="">All slices</option><option value="vertical-slice-01">Slice 01</option><option value="vertical-slice-02">Slice 02</option></select></label><label>Status <select id="status"><option value="">All statuses</option><option value="draft_not_validated">Draft not validated</option><option value="draft_candidate_not_validated">Candidate not validated</option></select></label></div><p id="count"></p><section id="cards"></section></main>
<script id="card-data" type="application/json">""" + payload + """</script><script>
const cards=JSON.parse(document.querySelector('#card-data').textContent), out=document.querySelector('#cards'), search=document.querySelector('#search'), slice=document.querySelector('#slice'), status=document.querySelector('#status'), count=document.querySelector('#count');
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function example(x){return `<div class="example"><b>${esc(x.evidence_id)}</b> · ${esc(x.start_seconds)}–${esc(x.end_seconds)}s · ${x.source_url?`<a href="${esc(x.source_url)}" target="_blank" rel="noopener">source</a>`:'<span class="muted">source link unavailable</span>'}<p>${esc(x.exact_text)}</p><details><summary>Surrounding context and limits</summary><p>${(x.surrounding_context||[]).map(c=>esc(c.text||'')).join(' ')}</p><p class="muted">Function: ${esc(x.observed_function)} · Measurement: ${esc(x.measurement_status)}</p></details></div>`;}
function counterexample(x){return `<div class="example"><b>${esc(x.evidence_id)}</b> · <span class="tag">${esc(x.counterexample_status)}</span> · ${x.source_url?`<a href="${esc(x.source_url)}" target="_blank" rel="noopener">source</a>`:'<span class="muted">source link unavailable</span>'}<p>${esc(x.exact_text||'Context-only control or candidate')}</p><p>${esc(x.why_selected||'')}</p><details><summary>Boundary and follow-up</summary><p>${esc(x.what_it_can_support||'')}</p><p>${esc(x.what_it_cannot_support||'')}</p><p class="muted">Follow-up: ${esc((x.required_followup||[]).join('; ')||'none recorded')}</p></details></div>`;}
function delivery(x){return x.delivery_evidence.observations.length?x.delivery_evidence.observations.map(o=>`<div class="example"><b>${esc(o.evidence_id)}</b> · alignment: ${esc(o.alignment_decision)}<p>${esc(o.frame_observation)}</p><p class="muted">Audio proxy: ${esc(JSON.stringify(o.measured_audio_proxy||'not available'))} · Review: ${esc(o.review_status)}</p><p class="muted">Limit: ${esc(o.feature_limit||o.alignment_limit)}</p></div>`).join(''):'<p class="muted">No linked delivery observation for these reviewed examples.</p>';}
function card(x){return `<article class="card"><div class="meta">${esc(x.slice)} · ${esc(x.card_id)} · ${esc(x.status)}</div><h2>${esc(x.communication_problem)}</h2><p><a href="../${esc(x.lesson_writeup)}">Draft lesson</a> · <a href="../${esc(x.source_packet)}">Evidence packet</a> · <a href="shared-learner-check.html">Practise/check</a></p><p><b>Why it might help:</b> ${esc(x.mechanism_hypothesis)} <span class="muted">(${esc(x.mechanism_status)})</span></p><p><b>Practice hypothesis:</b> ${esc(x.practice.hypothesis)}</p><p><span class="tag">${x.examples.length} examples</span><span class="tag">${x.counterexamples.length} counterexamples</span><span class="tag">${x.recurrence.eligible_video_hit_count} corpus videos with phrase hits</span><span class="tag">${x.delivery_evidence.observations.length} delivery observations</span><span class="tag">learner: ${esc(x.validation.learner_status)}</span></p><details><summary>Exact phrase forms (heuristic retrieval aids)</summary><p>${x.recurrence.phrase_forms.map(esc).join(' · ')}</p>${x.recurrence.retrieval_samples.map(s=>`<div class="example"><b>${esc(s.evidence_id)}</b> · ${esc(s.text)} · <a href="https://www.youtube.com/watch?v=${esc(s.video_id)}" target="_blank" rel="noopener">source</a></div>`).join('')}</details><details open><summary>Exact reviewed examples</summary>${x.examples.map(example).join('')}</details><details><summary>Counterexamples, controls and failure candidates</summary>${x.counterexamples.map(counterexample).join('')||'<p class="muted">No counterexample record is currently linked.</p>'}</details><details><summary>Audio/video observations</summary>${delivery(x)}</details><details><summary>Evidence chain and validation gates</summary><ul><li>Exact language/function: ${esc(x.evidence_chain.exact_language_and_function.function_status)}</li><li>Delivery: ${esc(x.evidence_chain.delivery_evidence.status)}</li><li>Recurrence: ${esc(x.evidence_chain.cross_talk_recurrence.status)}</li><li>Practice: ${esc(x.evidence_chain.practice.status)}</li><li>Learner check: ${esc(x.evidence_chain.learner_check.status)}</li><li>Listener outcomes: ${esc(x.evidence_chain.listener_outcome_check.status)}</li></ul></details><details><summary>Limits and validation status</summary><p>${esc(x.claim_boundary)}</p><ul>${x.limits.do_not_claim.map(v=>`<li>${esc(v)}</li>`).join('')}</ul><p class="muted">Independent review: ${esc(x.validation.independent_review)} · Speaker/event identity: ${esc(x.validation.speaker_event_independence)} · Listener outcomes: ${esc(x.validation.listener_outcomes)}</p></details><details><summary>Practise this choice</summary><p>${esc(x.practice.hypothesis)}</p>${x.practice.tasks.map(t=>`<div class="task"><b>${esc(t.phase)} — ${esc(t.task_id)}</b><p>${esc(t.prompt)}</p></div>`).join('')}${x.practice.self_check.length?`<p><b>Self-check:</b> ${x.practice.self_check.map(esc).join(' · ')}</p>`:''}</details></article>`;}
function render(){const q=search.value.toLowerCase(), s=slice.value, st=status.value; const rows=cards.filter(x=>(!q||JSON.stringify(x).toLowerCase().includes(q))&&(!s||x.slice===s)&&(!st||x.status===st)); count.textContent=`${rows.length} of ${cards.length} lesson cards`; out.innerHTML=rows.map(card).join('')||'<p>No matching lesson card.</p>';}
search.addEventListener('input',render); slice.addEventListener('change',render); status.addEventListener('change',render); render();
</script></body></html>"""
    OUT.write_text(document)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(cards)} cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
