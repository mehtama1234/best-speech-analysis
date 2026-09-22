#!/usr/bin/env python3
"""Build a presenter-facing playbook for every mined pattern candidate.

The playbook is a drafting aid. It keeps source evidence and provisional
boundaries visible and never upgrades discovery counts into effectiveness claims.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "research/exhaustive-pattern-inventory.json"
EVIDENCE = ROOT / "research/all-55-pattern-evidence.json"
JSON_OUT = ROOT / "research/presentation-pattern-playbook.json"
MD_OUT = ROOT / "writeups/presentation-pattern-playbook.md"


def stages(form: str) -> list[str]:
    return [part.strip() for part in form.replace("→", "->").split("->") if part.strip()]


def cards() -> list[dict]:
    inventory = json.loads(INVENTORY.read_text())
    evidence = {row["pattern_id"]: row for row in json.loads(EVIDENCE.read_text())["patterns"]}
    groups = [
        ("core_theme", "themes", "theme_id", "episode_hit_count"),
        ("structural_subtheme", "relation_patterns", "relation_type", "relation_count"),
        ("additional_subtheme", "unmatched_clusters", "cluster_id", "label_hit_count"),
    ]
    output = []
    for category, collection, id_key, count_key in groups:
        for item in inventory[collection]:
            pattern_id = item[id_key]
            form = item.get("candidate_form", "")
            examples = item.get("examples") or [{}]
            example = examples[0]
            sequence = stages(form)
            if category == "core_theme":
                use_when = "Use as a primary presentation move when the audience needs this communication job made explicit."
            elif category == "structural_subtheme":
                use_when = "Use inside a section as a transition or reasoning architecture; keep the surrounding claim and evidence visible."
            else:
                use_when = "Use as a creative variation when the ordinary structure feels too flat, broad, or impersonal."
            output.append({
                "pattern_id": pattern_id,
                "category": category,
                "candidate_form": form,
                "move_sequence": sequence,
                "use_when": use_when,
                "draft_prompt": "Draft one sentence for each move, using your own topic and evidence; then state the limit or non-fit condition.",
                "practice_check": "Ask a listener to name the communication job, the main point, and what the example or pattern does not prove.",
                "safety_boundary": "Do not copy the source speaker's wording, identity, accent, biography, certainty or mannerism.",
                "canonical_video_count": item.get("video_count", 0),
                "canonical_record_count": item.get(count_key, 0),
                "example_video_id": example.get("video_id", ""),
                "example_label": example.get("label") or example.get("claim", "source-linked candidate"),
                "example_writeup": example.get("writeup", ""),
                "example_evidence_ids": example.get("evidence_ids", [])[:5],
                "direct_recovered_video_count": evidence[pattern_id].get("direct_recovered_video_count", 0),
                "alternate_source_video_count": evidence[pattern_id].get("alternate_source_video_count", 0),
                "external_transcript_video_count": evidence[pattern_id].get("external_transcript_video_count", 0),
                "status": "candidate_pattern_not_effectiveness_validated",
            })
    return output


def render_markdown(items: list[dict]) -> str:
    lines = [
        "# Presentation pattern playbook",
        "",
        "This playbook turns all 55 corpus-mined candidates into drafting cards.",
        "They are provisional structures, not proven techniques or effectiveness findings.",
        "Use your own evidence and voice; do not imitate a source speaker.",
        "",
        f"Coverage: **{len(items)}** cards — 22 core themes, 18 structural subthemes and 15 additional subthemes.",
        "",
    ]
    for number, item in enumerate(items, 1):
        lines += [
            f"## {number}. `{item['pattern_id']}`",
            "",
            f"**Category:** `{item['category']}`  ",
            f"**Candidate form:** {item['candidate_form']}",
            "",
            f"**Use it when:** {item['use_when']}",
            "",
            "**Draft moves:**",
            *[f"{index}. {stage}" for index, stage in enumerate(item["move_sequence"], 1)],
            "",
            f"**Draft prompt:** {item['draft_prompt']}",
            f"**Practice check:** {item['practice_check']}",
            f"**Boundary:** {item['safety_boundary']}",
            "",
            f"**Source anchor:** `{item['example_video_id']}` — {item['example_label']}  ",
            f"**Evidence:** {', '.join(f'`{x}`' for x in item['example_evidence_ids']) or 'not available'}  ",
            f"**Writeup:** `{item['example_writeup'] or 'not available'}`  ",
            f"**Discovery counts:** {item['canonical_video_count']} canonical videos; {item['canonical_record_count']} canonical records; {item['direct_recovered_video_count']} direct recovery candidates; {item['alternate_source_video_count']} alternate-source candidates; {item['external_transcript_video_count']} external candidates.",
            "",
        ]
    return "\n".join(lines)


def render_html(items: list[dict]) -> str:
    payload = html.escape(json.dumps(items, ensure_ascii=False), quote=False)
    return f"""<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Presentation pattern playbook</title><style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a;background:#f7f8fb}}
.notice{{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem;margin-bottom:1rem}}input,select{{font:inherit;padding:.65rem;margin:.25rem .5rem .75rem 0}}article{{background:#fff;border:1px solid #d6dce5;border-radius:9px;padding:1rem;margin:1rem 0}}.tag{{color:#2457d6;font-weight:700;text-transform:uppercase;font-size:.8rem}}.moves{{background:#f1f5ff;padding:.6rem 1.5rem}}.muted{{color:#5c6872}}a{{color:#075985}}code{{overflow-wrap:anywhere}}
</style><main><h1>Presentation pattern playbook</h1>
<div class='notice'><b>Boundary:</b> 55 source-linked drafting candidates. They do not prove intent, universal effectiveness, listener outcomes or causality. Adapt the underlying communication choice; do not imitate a person.</div>
<label>Search <input id='q' type='search' placeholder='theme, form, use, source'></label><select id='cat'><option value=''>All categories</option><option>core_theme</option><option>structural_subtheme</option><option>additional_subtheme</option></select><p id='count' class='muted'></p><section id='cards'></section></main>
<script id='data' type='application/json'>{payload}</script><script>
const data=JSON.parse(document.getElementById('data').textContent),out=document.getElementById('cards'),q=document.getElementById('q'),cat=document.getElementById('cat'),count=document.getElementById('count');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function render(){{const text=q.value.toLowerCase(),group=cat.value,rows=data.filter(x=>(!group||x.category===group)&&(!text||JSON.stringify(x).toLowerCase().includes(text)));count.textContent=rows.length+' of '+data.length+' cards';out.innerHTML=rows.map(x=>'<article><span class="tag">'+esc(x.category)+'</span><h2>'+esc(x.pattern_id)+'</h2><p><b>Form:</b> '+esc(x.candidate_form)+'</p><p><b>Use it when:</b> '+esc(x.use_when)+'</p><ol class="moves">'+x.move_sequence.map(esc).map(s=>'<li>'+s+'</li>').join('')+'</ol><p><b>Draft prompt:</b> '+esc(x.draft_prompt)+'</p><p><b>Practice check:</b> '+esc(x.practice_check)+'</p><p><b>Boundary:</b> '+esc(x.safety_boundary)+'</p><p class="muted">Source: <code>'+esc(x.example_video_id)+'</code> · '+esc(x.example_label)+' · <a href="../'+esc(x.example_writeup)+'">open writeup</a></p></article>').join('')}}
q.oninput=render;cat.onchange=render;render();</script></main>"""


def main() -> int:
    items = cards()
    assert len(items) == 55, len(items)
    JSON_OUT.write_text(json.dumps({"schema_version": "1.0", "status": "source_linked_drafting_playbook_not_validated", "card_count": len(items), "cards": items, "claim_boundary": "These are provisional drafting structures, not effectiveness evidence."}, ensure_ascii=False, indent=2) + "\n")
    MD_OUT.write_text(render_markdown(items))
    (ROOT / "writeups/presentation-pattern-playbook.html").write_text(render_html(items))
    print(f"presentation playbook: {len(items)} cards written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
