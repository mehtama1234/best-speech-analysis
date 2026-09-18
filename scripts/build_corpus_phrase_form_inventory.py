#!/usr/bin/env python3
"""Expose exact recurring phrase forms behind the provisional phrase atlas."""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

try:
    from .build_corpus_pattern_atlas import PHRASE_FORMS, event_split, normalize
    from .source_restrictions import load_restrictions
except ImportError:
    from build_corpus_pattern_atlas import PHRASE_FORMS, event_split, normalize
    from source_restrictions import load_restrictions


FAMILY_HYPOTHESES = {
    "contrast_or_disagreement": "Hypothesis: contrast markers may make a distinction or change visible; the surrounding content must show what is being contrasted.",
    "example": "Hypothesis: example cues may give a general claim a concrete handle; an example is not automatically representative evidence.",
    "story_or_personal_experience": "Hypothesis: story-entry forms may signal a bounded event that gives an idea human and temporal scale; personal detail is optional and not universal proof.",
    "uncertainty_or_qualification": "Hypothesis: qualification forms may locate certainty and revision conditions; vague hedging can obscure rather than calibrate a claim.",
    "conclusion_or_summary": "Hypothesis: summary forms may mark a takeaway; the marker does not prove comprehension or truth.",
    "question": "Hypothesis: question forms may allocate attention or the next conversational turn; their use must preserve answerability and consent.",
    "definition": "Hypothesis: definition forms may reduce ambiguity around a term; the surrounding explanation must state scope and exclusions.",
    "call_to_action": "Hypothesis: action forms may make a next role visible; a clear request does not prove feasibility or impact.",
}


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    restrictions = load_restrictions(root)
    forms = defaultdict(lambda: {
        "family": None,
        "matched_pattern": None,
        "occurrence_count": 0,
        "video_ids": set(),
        "train_video_ids": set(),
        "holdout_video_ids": set(),
        "examples": [],
    })
    segment_count = 0
    for line in (root / "research/segment-registry.jsonl").open():
        row = json.loads(line)
        if row["video_id"] in restrictions:
            continue
        text = normalize(row.get("text", ""))
        if not text:
            continue
        segment_count += 1
        split = event_split(row["video_id"])
        for family, patterns in PHRASE_FORMS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.I):
                    phrase = normalize(match.group(0)).lower()
                    key = (family, phrase)
                    item = forms[key]
                    item["family"] = family
                    item["matched_pattern"] = pattern
                    item["occurrence_count"] += 1
                    item["video_ids"].add(row["video_id"])
                    item[f"{split}_video_ids"].add(row["video_id"])
                    if len(item["examples"]) < 12 and row["video_id"] not in {e["video_id"] for e in item["examples"]}:
                        item["examples"].append({
                            "evidence_id": row["evidence_id"],
                            "video_id": row["video_id"],
                            "title": row.get("title"),
                            "start_seconds": row.get("start_seconds"),
                            "end_seconds": row.get("end_seconds"),
                            "text": text,
                            "event_split": split,
                            "source_url": row.get("video_url"),
                        })
    serialized = []
    for (family, phrase), item in sorted(forms.items(), key=lambda pair: (pair[0][0], -pair[1]["occurrence_count"], pair[0][1])):
        serialized.append({
            "phrase_form": phrase,
            "family": family,
            "matched_pattern": item["matched_pattern"],
            "occurrence_count": item["occurrence_count"],
            "video_count": len(item["video_ids"]),
            "train_video_count": len(item["train_video_ids"]),
            "holdout_video_count": len(item["holdout_video_ids"]),
            "examples": item["examples"],
            "mechanism_status": "bounded_hypothesis_not_outcome_evidence",
            "mechanism_hypothesis": FAMILY_HYPOTHESES[family],
            "review_status": "heuristic_exact_form_requires_context_and_independent_review",
        })
    return {
        "schema_version": "1.0",
        "inventory_id": "corpus-exact-recurrent-phrase-forms",
        "status": "heuristic_exact_phrase_inventory_not_validated",
        "claim_boundary": "Forms are exact matches to retained caption text within individual caption segments. Counts describe phrase recurrence in this restricted transcript registry, not speech effectiveness, speaker intent, independent events, delivery or listener outcomes.",
        "source": "research/segment-registry.jsonl",
        "eligible_caption_segment_count": segment_count,
        "family_hypotheses": FAMILY_HYPOTHESES,
        "form_count": len(serialized),
        "forms": serialized,
        "event_split": "sha256(video_id) train/holdout split inherited from corpus pattern atlas",
        "source_restrictions": restrictions,
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/corpus-phrase-form-inventory.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Corpus exact recurrent phrase forms", "", "Status: **heuristic phrase inventory; not validated**.", "", result["claim_boundary"], "", f"- Caption segments scanned: {result['eligible_caption_segment_count']}", f"- Exact form variants: {result['form_count']}", "", "| Family | Exact form | Videos | Train | Holdout | Occurrences |", "|---|---|---:|---:|---:|---:|"]
    lines += [f"| `{item['family']}` | `{item['phrase_form']}` | {item['video_count']} | {item['train_video_count']} | {item['holdout_video_count']} | {item['occurrence_count']} |" for item in result["forms"]]
    lines += ["", "Each form carries a bounded mechanism hypothesis and exact source examples in the JSON inventory. Open surrounding context and complete independent review before teaching it."]
    (root / "writeups/corpus-phrase-form-inventory.md").write_text("\n".join(lines) + "\n")
    cards = []
    for item in result["forms"]:
        examples = "".join(f"<li><a href='{html.escape((example['source_url'] or '') + '&t=' + str(int(example['start_seconds'] or 0)), quote=True)}'>{html.escape(example['title'] or example['video_id'])}</a>: <code>{html.escape(example['evidence_id'])}</code> — {html.escape(example['text'])}</li>" for example in item["examples"])
        search = html.escape((item["family"] + " " + item["phrase_form"] + " " + item["mechanism_hypothesis"]).lower(), quote=True)
        cards.append(f"<article class='item' data-search='{search}'><h2><code>{html.escape(item['phrase_form'])}</code></h2><p><strong>Family:</strong> {html.escape(item['family'])} · <strong>Videos:</strong> {item['video_count']} (train {item['train_video_count']}, holdout {item['holdout_video_count']}) · <strong>Occurrences:</strong> {item['occurrence_count']}</p><p>{html.escape(item['mechanism_hypothesis'])}</p><details><summary>Exact examples ({len(item['examples'])})</summary><ul>{examples}</ul></details></article>")
    browser = """<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Corpus exact phrase forms</title><style>body{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}input{width:100%;box-sizing:border-box;padding:.7rem;font:inherit;margin:1rem 0 1.5rem}.notice{background:#fff4ce;padding:1rem;border-left:4px solid #b8860b}.item{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}code{overflow-wrap:anywhere}</style><main><h1>Corpus exact recurrent phrase forms</h1><div class='notice'><strong>Heuristic transcript inventory.</strong> Recurrence is not effectiveness, intent, delivery or listener evidence.</div><label for='search'>Search family, phrase or hypothesis</label><input id='search' type='search'><p id='count' aria-live='polite'></p>""" + "\n".join(cards) + """</main><script>const i=document.querySelector('#search'),c=[...document.querySelectorAll('.item')],n=document.querySelector('#count');function f(){let q=i.value.toLowerCase(),x=0;c.forEach(a=>{let s=!q||a.dataset.search.includes(q);a.hidden=!s;if(s)x++});n.textContent=`Showing ${x} of ${c.length} forms`}i.oninput=f;f()</script>"""
    (root / "writeups/corpus-phrase-form-inventory.html").write_text(browser)
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps({"form_count": result["form_count"], "segments": result["eligible_caption_segment_count"]}, indent=2))
