#!/usr/bin/env python3
"""Build source-linked candidate lesson cards from exhaustive pattern leads."""

from __future__ import annotations

import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "research/exhaustive-pattern-inventory.json"
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"
SHORTLIST = ROOT / "research/expanded-pattern-llm-shortlist.json"
SEQUENCES = ROOT / "research/presentation-sequence-library.json"
OUT = ROOT / "research/expanded-pattern-candidate-cards.json"
MD = ROOT / "writeups/expanded-pattern-candidate-cards.md"
HTML = ROOT / "writeups/expanded-pattern-candidate-cards.html"


def card(source: dict, card_id: str, title: str, form_key: str, form: str, examples: list[dict], count: int, video_count: int, evidence_map: dict[str, dict], shortlisted: bool = False) -> dict:
    enriched_examples = []
    for example in examples[:8]:
        excerpt_parts = []
        for evidence_id in example.get("evidence_ids", [])[:5]:
            segment = evidence_map.get(evidence_id)
            if segment and segment.get("text"):
                excerpt_parts.append(segment["text"])
        enriched_examples.append({**example, "excerpt": " ".join(excerpt_parts)})
    examples = enriched_examples
    evidence_ids = sorted({eid for example in examples for eid in example.get("evidence_ids", [])})
    return {
        "card_id": card_id,
        "llm_shortlisted": shortlisted,
        "title": title,
        "source_kind": form_key,
        "status": "candidate_discovery_not_validated",
        "source_record_count": count,
        "source_video_count": video_count,
        "candidate_form": form,
        "practice_prompt": f"Write a 60-second version of your own situation using: {form}",
        "self_check": "Can a listener identify the move, the evidence or condition, and what remains open?",
        "non_fit_warning": "Do not use this form to manufacture certainty, pressure consent, or turn one vivid example into proof.",
        "evidence_ids": evidence_ids,
        "examples": examples[:8],
        "claim_boundary": "This is a corpus-mined candidate pattern. It is a retrieval and practice hypothesis, not a validated best practice, delivery finding, learner result, listener outcome or effectiveness claim.",
    }


def build() -> dict:
    inventory = json.loads(INVENTORY.read_text())
    shortlist_ids = {card["card_id"] for card in json.loads(SHORTLIST.read_text()).get("cards", [])} if SHORTLIST.exists() else set()
    evidence_map = {}
    for record in json.loads(EVIDENCE.read_text())["records"]:
        for segment in record.get("segments", []):
            evidence_map[segment["evidence_id"]] = segment
    cards = []
    for item in inventory["relation_patterns"]:
        if not item["examples"]:
            continue
        cards.append(card(
            item,
            "expanded-relation-" + item["relation_type"],
            item["relation_type"].replace("_", " ").title(),
            "structural_relation",
            item["candidate_form"],
            item["examples"],
            item["relation_count"],
            item["video_count"],
            evidence_map,
            "expanded-relation-" + item["relation_type"] in shortlist_ids,
        ))
    for item in inventory["unmatched_clusters"]:
        if not item["examples"]:
            continue
        cards.append(card(
            item,
            "expanded-cluster-" + item["cluster_id"],
            item["cluster_id"].replace("_", " ").title(),
            "unmatched_label_cluster",
            item["candidate_form"],
            item["examples"],
            item["label_hit_count"],
            item["video_count"],
            evidence_map,
            "expanded-cluster-" + item["cluster_id"] in shortlist_ids,
        ))
    return {
        "schema_version": "1.0",
        "card_set_id": "expanded-pattern-candidate-cards",
        "status": "source_linked_discovery_cards_not_validated",
        "source_inventory": "research/exhaustive-pattern-inventory.json",
        "card_count": len(cards),
        "relation_card_count": sum(c["source_kind"] == "structural_relation" for c in cards),
        "unmatched_cluster_card_count": sum(c["source_kind"] == "unmatched_label_cluster" for c in cards),
        "claim_boundary": "These cards expand the practice search from the original 18-job curriculum using all-review discovery leads. They remain candidate forms until contextual review, independent review, counterexamples, learner checks and listener outcomes are complete.",
        "cards": cards,
    }


def render(report: dict) -> str:
    lines = [
        "# Expanded pattern candidate cards",
        "",
        f"Status: **{report['status']}**. Cards: **{report['card_count']}** ({report['relation_card_count']} structural-relation leads; {report['unmatched_cluster_card_count']} unmatched-label clusters).",
        "",
        report["claim_boundary"],
        "",
        "These cards are intentionally separate from the validated product lesson set. Each card points back to the exact review and evidence IDs that generated the lead.",
        "",
    ]
    for c in report["cards"]:
        lines += [
            f"## {c['title']}",
            "",
            f"**ID:** `{c['card_id']}`  ",
            f"**Source coverage:** {c['source_record_count']} records across {c['source_video_count']} videos  ",
            f"**Candidate form:** {c['candidate_form']}",
            "**LLM shortlist:** yes" if c["llm_shortlisted"] else "",
            "",
            f"**Practice:** {c['practice_prompt']}",
            "",
            f"**Self-check:** {c['self_check']}",
            "",
            f"**Non-fit:** {c['non_fit_warning']}",
            "",
            "**Source examples:**",
        ]
        for e in c["examples"][:5]:
            label = e.get("label") or e.get("relation_type")
            claim = f" — {e['claim']}" if e.get("claim") else ""
            lines.append(f"- `{e['review_id']}` / `{e['video_id']}` / `{label}`{claim}; evidence `{', '.join(e['evidence_ids'][:4])}`; [{e['writeup']}]({e['writeup']})")
            if e.get("excerpt"):
                lines.append(f"  > {e['excerpt']}")
        lines += ["", "---", ""]
    return "\n".join(lines)


def render_html(report: dict) -> str:
    cards = []
    options = []
    sequence_options = []
    sequence_data = {}
    if SEQUENCES.exists():
        library = json.loads(SEQUENCES.read_text())
        sequence_data = {sequence["sequence_id"]: sequence["pattern_ids"] for sequence in library.get("sequences", [])}
        sequence_options = [f'<option value="{html.escape(sequence_id)}">{html.escape(sequence_id.replace("_", " ").title())}</option>' for sequence_id in sequence_data]
    for c in report["cards"]:
        checked = ' checked' if c["llm_shortlisted"] else ''
        options.append(f'<label class="pick"><input type="checkbox" value="{html.escape(c["card_id"])}"{checked}><span>{html.escape(c["title"])}</span></label>')
        examples = "".join(
            f'<li><a href="../{html.escape(e["writeup"])}">{html.escape(e["review_id"])} / {html.escape(e["video_id"])}</a> — {html.escape(e.get("label") or e.get("relation_type") or "source example")} (evidence: {html.escape(", ".join(e["evidence_ids"][:3]))})'
            f'<blockquote>{html.escape(e.get("excerpt", ""))}</blockquote></li>'
            for e in c["examples"][:5]
        )
        cards.append(
            f'<article class="card{" shortlisted" if c["llm_shortlisted"] else ""}" data-shortlisted="{"true" if c["llm_shortlisted"] else "false"}" data-search="{html.escape((c["title"] + " " + c["source_kind"] + " " + c["candidate_form"]).lower())}">'
            f'<div class="meta">{html.escape(c["source_kind"])} · {c["source_record_count"]} records · {c["source_video_count"]} videos</div>'
            f'<h2>{html.escape(c["title"])}{" <span class=\"badge\">LLM shortlist</span>" if c["llm_shortlisted"] else ""}</h2>'
            f'<p class="form"><strong>Candidate form:</strong> {html.escape(c["candidate_form"])}</p>'
            f'<p><strong>Practice:</strong> {html.escape(c["practice_prompt"])}</p>'
            f'<p><strong>Self-check:</strong> {html.escape(c["self_check"])}</p>'
            f'<p class="boundary"><strong>Non-fit:</strong> {html.escape(c["non_fit_warning"])}</p>'
            f'<details><summary>Source examples</summary><ul>{examples}</ul></details>'
            '</article>'
        )
    body = "\n".join(cards)
    picker = "\n".join(options)
    card_data = json.dumps({c["card_id"]: {"title": c["title"], "form": c["candidate_form"], "practice": c["practice_prompt"], "check": c["self_check"], "evidence": c["evidence_ids"]} for c in report["cards"]}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Expanded speech-pattern practice</title>
<style>
:root{{color-scheme:light dark;--bg:#f6f7fb;--fg:#172033;--muted:#5b6475;--card:#fff;--line:#d9deea;--accent:#2457d6;--warn:#fff3d6}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:28px 18px 70px}}h1{{margin-bottom:8px}}.intro{{color:var(--muted);max-width:850px}}.controls{{position:sticky;top:0;background:var(--bg);padding:12px 0;z-index:2}}input{{box-sizing:border-box;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:var(--card);color:var(--fg)}}#search{{width:100%}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}.card,.builder{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px}}.meta{{font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}h2{{font-size:1.2rem;margin:8px 0}}.form{{color:var(--accent);font-weight:500}}.boundary{{background:var(--warn);padding:10px;border-radius:6px}}summary{{cursor:pointer;font-weight:600}}a{{color:var(--accent)}}.count{{color:var(--muted);margin:8px 0 18px}}.builder{{margin:22px 0}}.builder h2{{margin-top:0}}.fields{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}}.fields label,.pick{{display:flex;flex-direction:column;gap:4px;font-weight:600}}.pick{{display:block;font-weight:400;padding:4px 0}}.pick input{{width:auto;margin-right:8px}}.picker{{columns:repeat(auto-fit,minmax(220px,1fr));margin:10px 0}}textarea{{width:100%;min-height:220px;box-sizing:border-box;padding:12px;border:1px solid var(--line);border-radius:8px;font:inherit;background:var(--card);color:var(--fg)}}button{{padding:10px 14px;border:0;border-radius:8px;background:var(--accent);color:#fff;font:inherit;cursor:pointer;margin:6px 6px 6px 0}}.badge{{font-size:.7rem;padding:3px 6px;border-radius:4px;background:var(--accent);color:#fff;font-weight:500}}@media(prefers-color-scheme:dark){{:root{{--bg:#101522;--fg:#f3f5fb;--muted:#acb5c8;--card:#171e2e;--line:#303a50;--warn:#3b301d}}}}
</style></head><body><main>
<h1>Expanded speech-pattern practice</h1>
<p class="intro">{html.escape(report["claim_boundary"])} These are candidate structures mined from the full corpus. Use the form to draft a talk, then check whether a listener can restate the point and its limit.</p>
<section class="builder" aria-labelledby="builder-title"><h2 id="builder-title">Build a presentation outline</h2>
<div class="fields"><label>Topic<input id="topic" placeholder="What is this talk about?"></label><label>Audience<input id="audience" placeholder="Who is listening?"></label><label>Smallest useful outcome<input id="outcome" placeholder="What should they leave able to do?" ></label></div>
<p>Choose a sequence preset or select up to five pattern moves:</p><div class="sequence-row"><label for="sequence-preset">Sequence preset</label><select id="sequence-preset"><option value="">Choose a sequence…</option>{"".join(sequence_options)}</select><button id="apply-sequence" type="button">Apply sequence</button></div><div class="picker">{picker}</div>
<button id="generate" type="button">Generate outline</button><button id="save" type="button">Save draft locally</button><button id="load" type="button">Load saved draft</button><button id="download" type="button">Download outline</button><button id="download-record" type="button">Download practice JSON</button><span id="save-status" role="status" aria-live="polite"></span>
<label for="outline">Draft outline</label><textarea id="outline" aria-live="polite" placeholder="Your outline will appear here."></textarea>
<div class="reflection"><h3>Practice reflection</h3><div class="fields"><label>Listener restatement<textarea id="listener-restatement" placeholder="What did the listener say they heard?"></textarea></label><label>Still unclear<textarea id="still-unclear" placeholder="What remained unclear or unanswered?"></textarea></label><label>Non-fit or pressure point<textarea id="non-fit" placeholder="What did not fit this person or context?"></textarea></label><label>Next revision<textarea id="next-revision" placeholder="What will you change next time?"></textarea></label></div></div></section>
<div class="controls"><label for="search">Find a pattern</label><input id="search" type="search" placeholder="Try premise, credit, failure, analogy…" autocomplete="off"><label><input id="shortlist-only" type="checkbox"> Show LLM shortlist only</label><div class="count" id="count"></div></div>
<section class="grid" id="cards">{body}</section>
</main><script>
const input=document.getElementById('search'), cards=[...document.querySelectorAll('.card')], count=document.getElementById('count');
const shortlistOnly=document.getElementById('shortlist-only');
function filter(){{const q=input.value.trim().toLowerCase();let n=0;cards.forEach(c=>{{const show=(!q||c.dataset.search.includes(q))&&(!shortlistOnly.checked||c.dataset.shortlisted==='true');c.hidden=!show;if(show)n++;}});count.textContent=n+' of '+cards.length+' candidate patterns';}}
input.addEventListener('input',filter);shortlistOnly.addEventListener('change',filter);filter();
const patternData={card_data};
const sequenceData={json.dumps(sequence_data, ensure_ascii=False)};
const outline=document.getElementById('outline');
const reflectionIds=['listener-restatement','still-unclear','non-fit','next-revision'];
function reflectionText(){{return reflectionIds.map(id=>{{const el=document.getElementById(id);return '\\n## '+el.previousElementSibling.textContent+'\\n'+(el.value||'[not recorded]')+'\\n';}}).join('');}}
function recordPayload(){{const selected=[...document.querySelectorAll('.pick input:checked')].map(x=>x.value);return {{record_type:'local_expanded_pattern_practice_record',schema_version:'1.0',pattern_ids:selected,topic:document.getElementById('topic').value,audience:document.getElementById('audience').value,outcome:document.getElementById('outcome').value,source_evidence_ids:[...new Set(selected.flatMap(id=>patternData[id].evidence||[]))],outline:outline.value,step_responses:Object.fromEntries(reflectionIds.map(id=>[id,document.getElementById(id).value])),claim_boundary:'Local candidate-pattern practice record; not learner-validation evidence, listener outcome evidence, causal evidence, or effectiveness evidence.',saved_at:new Date().toISOString()}};}}
document.getElementById('apply-sequence').addEventListener('click',()=>{{const ids=sequenceData[document.getElementById('sequence-preset').value]||[];document.querySelectorAll('.pick input').forEach(x=>x.checked=ids.includes(x.value));}});
document.getElementById('generate').addEventListener('click',()=>{{const topic=document.getElementById('topic').value.trim()||'[topic]';const audience=document.getElementById('audience').value.trim()||'[audience]';const outcome=document.getElementById('outcome').value.trim()||'[smallest useful outcome]';const chosen=[...document.querySelectorAll('.pick input:checked')].slice(0,5).map(x=>patternData[x.value]);let text='# Presentation draft: '+topic+'\\n\\nAudience: '+audience+'\\nSmallest useful outcome: '+outcome+'\\n\\n## 1. Orient\\nName the situation, why it matters, and the route.\\n\\n';chosen.forEach((p,i)=>{{text+='## '+(i+2)+'. '+p.title+'\\n'+p.form+'\\nDraft move: '+p.practice+'\\nListener check: '+p.check+'\\n\\n';}});text+='## Close\\nReturn to the takeaway, name the remaining limit or next step, and invite one answerable next turn.\\n';outline.value=text;}});
document.getElementById('save').addEventListener('click',()=>{{const payload={{topic:document.getElementById('topic').value,audience:document.getElementById('audience').value,outcome:document.getElementById('outcome').value,selected:[...document.querySelectorAll('.pick input:checked')].map(x=>x.value),outline:outline.value,reflections:Object.fromEntries(reflectionIds.map(id=>[id,document.getElementById(id).value])),saved_at:new Date().toISOString()}};localStorage.setItem('expanded-pattern-draft',JSON.stringify(payload));document.getElementById('save-status').textContent='Saved on this device.';}});
document.getElementById('load').addEventListener('click',()=>{{const raw=localStorage.getItem('expanded-pattern-draft');if(!raw){{document.getElementById('save-status').textContent='No saved draft on this device.';return;}}const p=JSON.parse(raw);document.getElementById('topic').value=p.topic||'';document.getElementById('audience').value=p.audience||'';document.getElementById('outcome').value=p.outcome||'';document.querySelectorAll('.pick input').forEach(x=>x.checked=(p.selected||[]).includes(x.value));outline.value=p.outline||'';reflectionIds.forEach(id=>document.getElementById(id).value=(p.reflections||{{}})[id]||'');document.getElementById('save-status').textContent='Loaded from this device.';}});
document.getElementById('download').addEventListener('click',()=>{{const blob=new Blob([(outline.value||'Generate an outline first.')+reflectionText()],{{type:'text/markdown'}});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='presentation-outline.md';a.click();URL.revokeObjectURL(a.href);}});
document.getElementById('download-record').addEventListener('click',()=>{{const blob=new Blob([JSON.stringify(recordPayload(),null,2)],{{type:'application/json'}});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='expanded-pattern-practice-record.json';a.click();URL.revokeObjectURL(a.href);}});
</script></body></html>'''


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    HTML.write_text(render_html(report))
    print(f"expanded pattern candidate cards: {report['card_count']} cards")
