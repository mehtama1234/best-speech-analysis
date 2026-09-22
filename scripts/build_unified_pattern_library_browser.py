#!/usr/bin/env python3
"""Build a searchable browser joining fixed and expansion pattern candidates."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "research/all-55-pattern-evidence.json"
WAVE2 = ROOT / "research/wave-2-unified-candidate-crosswalk.json"
OUTPUT = ROOT / "writeups/unified-pattern-library.html"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def fixed_card(item: dict) -> dict:
    writeup = item.get("example_writeup")
    evidence = ", ".join(item.get("example_evidence_ids", [])[:3])
    return {
        "layer": "fixed corpus",
        "source": "395 full-context reviews",
        "pattern": item.get("pattern_id"),
        "category": item.get("category"),
        "form": item.get("candidate_form"),
        "status": item.get("status", "candidate_pattern_not_effectiveness_validated"),
        "counts": f"{item.get('canonical_video_count', 0)} canonical · {item.get('direct_recovered_video_count', 0)} recovered",
        "evidence": evidence,
        "link": Path(writeup).name if writeup else "",
    }


def wave_card(item: dict) -> dict:
    return {
        "layer": "expansion source",
        "source": item.get("source"),
        "pattern": item.get("candidate_pattern"),
        "category": ", ".join(item.get("communication_jobs", [])),
        "form": item.get("candidate_form") or item.get("description") or "Inspect the bounded context packet.",
        "status": "provisional_contextual_review_required",
        "counts": "wave-2 candidate",
        "evidence": ", ".join(item.get("evidence_refs", [])),
        "link": "../research/wave-2-unified-candidate-crosswalk.json",
    }


def main() -> int:
    fixed = json.loads(PATTERNS.read_text(encoding="utf-8"))
    wave = json.loads(WAVE2.read_text(encoding="utf-8")) if WAVE2.is_file() else {"rows": []}
    cards = [fixed_card(item) for item in fixed.get("patterns", [])]
    cards.extend(wave_card(item) for item in wave.get("rows", []))
    payload = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")
    card_count = len(cards)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Unified speaking pattern library</title>
<style>
:root{{color-scheme:light;--ink:#17202a;--muted:#53616b;--line:#d8e0e6;--blue:#185a7d;--wash:#f4f8fa;--warn:#fff5d6}}
body{{font:16px/1.5 system-ui,sans-serif;max-width:1240px;margin:0 auto;padding:1.5rem;color:var(--ink)}}
h1{{margin:.2rem 0}} h2{{margin-top:2rem}} .notice{{background:var(--warn);border-left:4px solid #b8860b;padding:.8rem 1rem;margin:1rem 0}}
.controls{{display:grid;grid-template-columns:2fr 1fr 1fr;gap:.7rem;margin:1rem 0}} label{{font-weight:650}} input,select{{display:block;width:100%;box-sizing:border-box;padding:.65rem;border:1px solid #aebbc3;border-radius:6px;font:inherit}}
#count{{color:var(--muted)}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:1rem}}
.card{{border:1px solid var(--line);border-radius:10px;padding:1rem;background:var(--wash);display:flex;flex-direction:column;gap:.45rem}}
.card[hidden]{{display:none}} .eyebrow{{color:var(--blue);font-size:.78rem;font-weight:750;text-transform:uppercase;letter-spacing:.05em}}
.card h3{{margin:0;font-size:1.05rem;overflow-wrap:anywhere}} .meta{{font-size:.88rem;color:var(--muted)}} .form{{font-weight:600}}
.status{{font-size:.82rem;color:#53616b;border-top:1px solid var(--line);padding-top:.45rem}} a{{color:var(--blue)}} code{{overflow-wrap:anywhere}}
@media(max-width:700px){{.controls{{grid-template-columns:1fr}}}}
</style></head><body>
<main><p class="eyebrow">Traceable candidate synthesis</p><h1>Unified speaking pattern library</h1>
<div class="notice"><strong>Candidate library, not a ranking.</strong> This browser joins {len(fixed.get('patterns', []))} fixed-corpus candidates and {len(wave.get('rows', []))} expansion-source candidates. Search and practice are supported; independent review, learner outcomes, listener outcomes and effectiveness remain open.</div>
<section class="controls" aria-label="Pattern filters"><label>Search<input id="search" type="search" placeholder="pattern, form, source or evidence"></label><label>Evidence layer<select id="layer"><option value="">All layers</option><option>fixed corpus</option><option>expansion source</option></select></label><label>Category / job<select id="category"><option value="">All categories</option></select></label></section>
<p id="count" aria-live="polite"></p><section id="cards" class="grid" aria-label="Pattern candidates"></section></main>
<script>const data={payload};const root=document.querySelector('#cards'),search=document.querySelector('#search'),layer=document.querySelector('#layer'),category=document.querySelector('#category'),count=document.querySelector('#count');
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
const categories=[...new Set(data.map(x=>x.category).filter(Boolean))].sort();categories.forEach(x=>{{const o=document.createElement('option');o.value=x;o.textContent=x;category.append(o)}});
function render(){{const q=search.value.toLowerCase(),l=layer.value,c=category.value;let shown=0;root.innerHTML='';data.forEach(x=>{{const hay=[x.pattern,x.form,x.source,x.evidence,x.category].join(' ').toLowerCase();if((!q||hay.includes(q))&&(!l||x.layer===l)&&(!c||x.category===c)){{shown++;const el=document.createElement('article');el.className='card';el.innerHTML='<div class="eyebrow">'+esc(x.layer)+' · '+esc(x.source)+'</div><h3>'+esc(x.pattern)+'</h3><div class="meta">'+esc(x.category)+' · '+esc(x.counts)+'</div><div class="form">'+esc(x.form)+'</div><div class="meta">Evidence: '+esc(x.evidence||'inspect linked source')+'</div><div class="status">'+esc(x.status)+(x.link?' · <a href="'+esc(x.link)+'">open evidence bridge</a>':'')+' · <a href="communication-job-practice.html">open practice jobs</a></div>';root.append(el)}}}});count.textContent='Showing '+shown+' of '+data.length+' candidate patterns'}}
search.oninput=render;layer.onchange=render;category.onchange=render;render();</script></body></html>"""
    OUTPUT.write_text(page, encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "fixed_count": len(fixed.get("patterns", [])), "expansion_count": len(wave.get("rows", [])), "card_count": card_count}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
