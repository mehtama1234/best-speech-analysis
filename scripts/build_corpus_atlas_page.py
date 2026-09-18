#!/usr/bin/env python3
"""Build a searchable browser view of the corpus transcript atlas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "research/corpus-pattern-atlas.json"
OUT = ROOT / "writeups/corpus-pattern-atlas.html"


def main() -> int:
    atlas = json.loads(ATLAS.read_text())
    payload = json.dumps({
        "videos": atlas["videos"],
        "phrase_forms": atlas["phrase_forms"],
        "candidate_function_summary": atlas["candidate_function_summary"],
    }, ensure_ascii=False).replace("</", "<\\/")
    family_options = "".join(f"<option>{label}</option>" for label in atlas["phrase_forms"])
    function_options = "".join(f"<option>{label}</option>" for label in atlas["candidate_function_summary"] if label != "unclassified")
    document = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Corpus pattern atlas</title><style>
:root { font-family:system-ui,sans-serif; color:#1d2935; background:#f5f3ee; }
body { margin:0; } header { background:#17212b; color:white; padding:24px max(18px,calc((100vw - 1160px)/2)); }
main { max-width:1160px; margin:20px auto; padding:0 18px 50px; }
.notice { background:#fff7d6; border:1px solid #d8bd61; border-radius:8px; padding:12px; }
.controls { display:flex; gap:8px; flex-wrap:wrap; margin:14px 0; }
input,select { font:inherit; padding:8px; border:1px solid #aab3bb; border-radius:6px; }
.video { background:#fff; border:1px solid #d6d0c7; border-radius:9px; padding:15px; margin:12px 0; }
.meta,.muted { color:#5c6872; font-size:.9rem; } .tag { display:inline-block; background:#e2edf5; border-radius:99px; padding:3px 8px; margin:2px; font-size:.8rem; }
details { margin-top:10px; border-top:1px solid #e1e5e8; padding-top:8px; } summary { cursor:pointer; font-weight:650; }
.hit { background:#f4f8fb; border-left:4px solid #39739d; padding:8px; margin:8px 0; } a { color:#075985; }
</style></head><body><header><h1>Corpus pattern atlas</h1><p>Searchable transcript retrieval across __VIDEO_COUNT__ eligible videos and __SEGMENT_COUNT__ caption segments.</p></header>
<main><div class="notice"><b>Boundary:</b> Phrase hits and candidate speech-function labels are heuristic transcript retrieval aids. They are not validated semantic annotations, delivery evidence, effectiveness evidence or listener outcomes. Inspect context before using an item.</div>
<div class="controls"><label>Search <input id="search" placeholder="title, phrase, evidence ID"></label><label>Phrase family <select id="family"><option value="">All</option>__FAMILY_OPTIONS__</select></label><label>Candidate function <select id="function"><option value="">All</option>__FUNCTION_OPTIONS__</select></label><label>Event split <select id="split"><option value="">All</option><option value="train">Train</option><option value="holdout">Holdout</option></select></label></div>
<p id="count"></p><section id="summary"></section><section id="videos"></section></main>
<script id="data" type="application/json">__PAYLOAD__</script><script>
const data=JSON.parse(document.querySelector('#data').textContent),out=document.querySelector('#videos'),summary=document.querySelector('#summary'),search=document.querySelector('#search'),family=document.querySelector('#family'),func=document.querySelector('#function'),split=document.querySelector('#split'),count=document.querySelector('#count');
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]);}
function hit(x,label){return `<div class="hit"><b>${esc(label)} · ${esc(x.evidence_id)}</b> · ${esc(x.start_seconds)}–${esc(x.end_seconds)}s · <a href="https://www.youtube.com/watch?v=${esc(x.video_id)}" target="_blank" rel="noopener">source</a><p>${esc(x.text)}</p><span class="tag">${esc(x.event_split)}</span>${(x.matched_forms||[]).map(f=>`<span class="tag">${esc(f)}</span>`).join('')}</div>`;}
function renderSummary(){summary.innerHTML='<h2>Retrieval denominators</h2>'+Object.entries(data.phrase_forms).map(([label,x])=>`<span class="tag">${esc(label)}: ${x.video_hit_count} videos / ${x.segment_hit_count} segments</span>`).join('');}
function card(v){const families=Object.keys(v.phrase_candidates||{}),selected=family.value,selectedFunction=func.value,relevantFamily=selected?families.includes(selected):families.length,relevantFunction=selectedFunction?(v.candidate_function_counts||{})[selectedFunction]>0:true;if(!relevantFamily||!relevantFunction)return '';return `<article class="video"><div class="meta">${esc(v.event_split)} · ${esc(v.video_id)} · <a href="${esc(v.video_url)}" target="_blank" rel="noopener">source</a></div><h2>${esc(v.title)}</h2><p>${Object.entries(v.candidate_function_counts||{}).map(([k,n])=>`<span class="tag">function ${esc(k)}: ${n}</span>`).join('')}</p>${families.filter(k=>!selected||k===selected).map(k=>`<details><summary>${esc(k)} · ${v.phrase_segment_counts[k]||0} segment hits</summary>${(v.phrase_candidates[k]||[]).map(x=>hit({...x,video_id:v.video_id,event_split:v.event_split},k)).join('')}</details>`).join('')}</article>`;}
function render(){const q=search.value.toLowerCase(),s=split.value,rows=data.videos.filter(v=>(!s||v.event_split===s)&&(!q||JSON.stringify(v).toLowerCase().includes(q))).map(card).filter(Boolean);count.textContent=`${rows.length} of ${data.videos.length} eligible videos`;out.innerHTML=rows.join('')||'<p>No matching videos.</p>';}
search.addEventListener('input',render);family.addEventListener('change',render);func.addEventListener('change',render);split.addEventListener('change',render);renderSummary();render();
</script></body></html>"""
    document = document.replace("__VIDEO_COUNT__", str(atlas["eligible_video_count"]))
    document = document.replace("__SEGMENT_COUNT__", str(atlas["eligible_segment_count"]))
    document = document.replace("__FAMILY_OPTIONS__", family_options)
    document = document.replace("__FUNCTION_OPTIONS__", function_options)
    document = document.replace("__PAYLOAD__", payload)
    OUT.write_text(document)
    print(f"wrote {OUT.relative_to(ROOT)} ({atlas['eligible_video_count']} videos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
