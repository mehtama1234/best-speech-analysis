#!/usr/bin/env python3
"""Build a self-contained browser for the annotation review queue."""

from __future__ import annotations

import html
import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = [json.loads(line) for line in (root / "research/annotation-queue.jsonl").read_text().splitlines() if line.strip()]
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Speech Analysis — Evidence Browser</title>
<style>
:root {{ color-scheme: light; font-family: system-ui,-apple-system,Segoe UI,sans-serif; background:#f4f1ea; color:#1f2933; }}
body {{ margin:0; }} header {{ background:#17212b; color:#f8fafc; padding:28px max(22px,calc((100vw - 1200px)/2)); }}
main {{ max-width:1200px; margin:24px auto; padding:0 22px 60px; }}
.controls {{ display:flex; gap:12px; flex-wrap:wrap; align-items:center; background:#fff; border:1px solid #d8d1c5; padding:14px; border-radius:10px; position:sticky; top:0; z-index:2; }}
select,input {{ font:inherit; padding:8px 10px; border:1px solid #b9b1a4; border-radius:6px; background:#fff; }}
.card {{ background:#fff; border:1px solid #d8d1c5; border-radius:10px; padding:18px; margin:16px 0; }}
.meta {{ color:#59636e; font-size:.9rem; }} .tag {{ display:inline-block; background:#e7edf4; border-radius:99px; padding:3px 8px; margin:2px; font-size:.82rem; }}
.metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:8px; margin:12px 0; }}
.metric {{ background:#f5f7f8; padding:9px; border-radius:6px; }} .metric b {{ display:block; font-size:.78rem; color:#59636e; }}
.context {{ border-left:3px solid #d8d1c5; padding-left:12px; margin:12px 0; }} .context div {{ margin:4px 0; }}
a {{ color:#075985; }} .empty {{ color:#59636e; padding:30px 0; }}
</style></head><body>
<header><h1>Best Speech Analysis — Evidence Browser</h1><p>Heuristic candidates for review; measurements are observations, not psychological conclusions.</p></header>
<main><div class="controls"><label>Function <select id="label"><option value="">All</option></select></label><label>Search <input id="search" placeholder="words, video ID, title"></label><span id="count"></span></div><section id="results"></section></main>
<script id="evidence-data" type="application/json">{payload}</script>
<script>
const rows=JSON.parse(document.getElementById('evidence-data').textContent);
const labels=[...new Set(rows.flatMap(r=>r.review_targets))].sort();
const label=document.getElementById('label'), search=document.getElementById('search'), results=document.getElementById('results'), count=document.getElementById('count');
for(const x of labels){{const o=document.createElement('option');o.value=x;o.textContent=x;label.appendChild(o);}}
function esc(v){{return String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));}}
function render(){{const q=search.value.toLowerCase(), l=label.value; const filtered=rows.filter(r=>(!l||r.review_targets.includes(l))&&(!q||JSON.stringify(r).toLowerCase().includes(q))); count.textContent=filtered.length+' evidence units'; results.innerHTML=filtered.map(r=>{{const t=Math.floor(r.start_seconds);const url='https://www.youtube.com/watch?v='+encodeURIComponent(r.video_id)+'&t='+t+'s'; return `<article class="card"><div class="meta"><a href="${{url}}" target="_blank">${{esc(r.video_id)}} @ ${{esc(r.start_seconds)}}s</a> · review status: ${{esc(r.review_status)}}</div><div>${{r.review_targets.map(x=>`<span class="tag">${{esc(x)}}</span>`).join('')}}</div><h2>${{esc(r.text)}}</h2><div class="metrics"><div class="metric"><b>RMS dB</b>${{esc(r.mean_rms_db)}}</div><div class="metric"><b>Activity fraction</b>${{esc(r.speech_activity_fraction)}}</div><div class="metric"><b>Pause before</b>${{esc(r.pause_before_seconds)}}s</div><div class="metric"><b>Pause after</b>${{esc(r.pause_after_seconds)}}s</div><div class="metric"><b>Spectral centroid</b>${{esc(r.mean_spectral_centroid_hz)}} Hz</div></div><div class="context">${{r.context.map(c=>`<div><span class="meta">${{esc(c.start_time)}} · ${{c.ordinal===Number(r.evidence_id.split(':').pop())?'TARGET':''}}</span> ${{esc(c.text)}}</div>`).join('')}}</div></article>`}}).join('')||'<div class="empty">No matching evidence units.</div>';}}
label.addEventListener('change',render);search.addEventListener('input',render);render();
</script></body></html>'''
    output = root / "writeups/evidence-browser.html"
    output.write_text(page)
    print(f"wrote {output} with {len(rows)} evidence units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

