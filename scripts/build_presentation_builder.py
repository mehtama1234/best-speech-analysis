#!/usr/bin/env python3
"""Build a local presentation planner from candidate sequences and patterns."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEQUENCES = ROOT / "research/presentation-sequence-library.json"
PLAYBOOK = ROOT / "research/presentation-pattern-playbook.json"
OUTPUT = ROOT / "writeups/presentation-builder.html"


def main() -> int:
    sequences = json.loads(SEQUENCES.read_text())["sequences"]
    patterns = json.loads(PLAYBOOK.read_text())["cards"]
    payload = html.escape(json.dumps({"sequences": sequences, "patterns": patterns}, ensure_ascii=False), quote=False)
    sequence_options = "".join(f"<option value='{html.escape(x['sequence_id'])}'>{html.escape(x['title'])}</option>" for x in sequences)
    pattern_options = "<option value=''>No extra pattern</option>" + "".join(
        f"<option value='{html.escape(x['pattern_id'])}'>{html.escape(x['pattern_id'])}</option>" for x in patterns
    )
    document = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Presentation builder</title><style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem;color:#17202a;background:#f7f8fb}}
.panel,article{{background:#fff;border:1px solid #d6dce5;border-radius:9px;padding:1rem;margin:1rem 0}}label{{display:block;margin:.7rem 0}}input,select,textarea,button{{font:inherit;padding:.6rem;max-width:100%}}input,select,textarea{{width:min(100%,700px)}}textarea{{min-height:80px}}button{{cursor:pointer;margin:.4rem .4rem .4rem 0;background:#2457d6;color:#fff;border:0;border-radius:6px}}.notice{{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}}.muted{{color:#5c6872}}.step{{border-left:4px solid #2457d6;padding:.5rem 1rem;margin:1rem 0}}code{{overflow-wrap:anywhere}}
</style></head><body><main><h1>Presentation builder</h1>
<div class='notice'><b>Drafting aid:</b> This combines provisional corpus-mined structures into an outline. It does not prove effectiveness. Use your own evidence, voice and judgment; do not imitate a source speaker.</div>
<section class='panel'><label>Topic<input id='topic' placeholder='e.g. Why our team should simplify onboarding'></label><label>Audience<input id='audience' placeholder='e.g. product leaders'></label><label>Smallest useful outcome<input id='outcome' placeholder='What should the audience understand, decide or do?'></label><label>Presentation architecture<select id='sequence'>{sequence_options}</select></label><label>Optional pattern move 1<select class='pattern'>{pattern_options}</select></label><label>Optional pattern move 2<select class='pattern'>{pattern_options}</select></label><label>Optional pattern move 3<select class='pattern'>{pattern_options}</select></label><button id='download'>Download Markdown outline</button></section>
<section id='preview'></section></main><script id='data' type='application/json'>{payload}</script><script>
const data=JSON.parse(document.getElementById('data').textContent),seq=document.getElementById('sequence'),preview=document.getElementById('preview'),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function chosen(){{return [...document.querySelectorAll('.pattern')].map(x=>data.patterns.find(p=>p.pattern_id===x.value)).filter(Boolean)}}
function recommendedIds(){{const s=data.sequences.find(x=>x.sequence_id===seq.value);return (s.pattern_ids||[]).map(x=>x.replace(/^expanded-(relation|cluster)-/,''))}}
function applyRecommendations(){{const ids=recommendedIds();document.querySelectorAll('.pattern').forEach((x,i)=>x.value=ids[i]||'');render()}}
function render(){{const s=data.sequences.find(x=>x.sequence_id===seq.value),topic=document.getElementById('topic').value||'Your topic',audience=document.getElementById('audience').value||'Your audience',outcome=document.getElementById('outcome').value||'Your smallest useful outcome';preview.innerHTML='<article><h2>'+esc(topic)+'</h2><p><b>Architecture:</b> '+esc(s.title)+'</p><p><b>Audience:</b> '+esc(audience)+' · <b>Outcome:</b> '+esc(outcome)+'</p><p>'+esc(s.purpose)+'</p><h3>Sequence</h3>'+s.draft_template.map((x,i)=>'<div class="step"><h3>'+(i+1)+'. '+esc(x.title)+'</h3><p><b>Sentence stem:</b> '+esc(x.sentence_stem)+'</p><label>Your draft in your own words<textarea data-step="'+esc(x.section_id)+'" placeholder="Write this move for your topic."></textarea></label><p><b>Listener check:</b> '+esc(x.listener_check)+'</p><p><b>Boundary:</b> '+esc(x.boundary_check)+'</p></div>').join('')+'<h3>Selected pattern moves</h3>'+ (chosen().map(x=>'<p><b>'+esc(x.pattern_id)+'</b>: '+esc(x.candidate_form)+'</p>').join('')||'<p class="muted">No extra moves selected.</p>')+'<h3>Close and check</h3><p>Return to the takeaway, name what remains uncertain, and invite one answerable next turn.</p><p><b>Listener restatement:</b> What is the main point? What changed? What remains uncertain? Did anything feel pressuring or inaccessible?</p></article>'}}
document.querySelectorAll('input').forEach(x=>x.addEventListener('input',render));
document.querySelectorAll('.pattern').forEach(x=>x.addEventListener('change',render));
seq.addEventListener('change',applyRecommendations);
document.getElementById('download').onclick=()=>{{const s=data.sequences.find(x=>x.sequence_id===seq.value),topic=document.getElementById('topic').value||'Your topic',audience=document.getElementById('audience').value||'Your audience',outcome=document.getElementById('outcome').value||'Your smallest useful outcome',moves=chosen();let text='# Presentation outline: '+topic+'\\n\\n- Audience: '+audience+'\\n- Smallest useful outcome: '+outcome+'\\n- Architecture: '+s.title+'\\n\\n'+s.purpose+'\\n\\n';s.draft_template.forEach((x,i)=>text+='## '+(i+1)+'. '+x.title+'\\n\\nSentence stem: '+x.sentence_stem+'\\n\\nYour draft:\\n\\n\\nListener check: '+x.listener_check+'\\nBoundary: '+x.boundary_check+'\\n\\n');text+='## Selected pattern moves\\n\\n'+(moves.map(x=>'- `'+x.pattern_id+'`: '+x.candidate_form).join('\\n')||'- None')+'\\n\\n## Close and listener check\\n\\n- Takeaway:\\n- What remains uncertain:\\n- Listener restatement:\\n- Non-fit or pressure point:\\n- Next revision:\\n\\nClaim boundary: provisional drafting structure, not effectiveness evidence.\\n';const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{{type:'text/markdown'}}));a.download='presentation-outline.md';a.click();URL.revokeObjectURL(a.href)}};
applyRecommendations();</script></body></html>"""
    OUTPUT.write_text(document)
    print(f"presentation builder: {len(sequences)} architectures, {len(patterns)} pattern options")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
