#!/usr/bin/env python3
"""Build a learner-facing card for every transcript-derived function item.

Cards are navigation and practice aids.  They retain the original review
language and exact evidence while borrowing only the provisional form and
limits of the shared communication-job cards.  They never promote a
transcript observation to an effectiveness or best-practice claim.
"""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/corpus-lesson-index.json"
TAXONOMY = ROOT / "research/corpus-function-taxonomy.json"
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"
JOBS = ROOT / "research/communication-job-cards.json"
OUT = ROOT / "research/corpus-learner-card-inventory.json"
MD = ROOT / "writeups/corpus-learner-card-inventory.md"
HTML = ROOT / "writeups/corpus-learner-card-inventory.html"


def _job_cards() -> dict[str, dict]:
    data = json.loads(JOBS.read_text())
    return {card["canonical_job"]: card for card in data["cards"]}


def _taxonomy_lookup() -> dict[tuple[str, int], dict]:
    data = json.loads(TAXONOMY.read_text())
    lookup = {}
    for entry in data["entries"]:
        for item in entry["functions"]:
            lookup[(entry["review_id"], item["sequence"])] = item
    return lookup


def build() -> dict:
    index = json.loads(INDEX.read_text())
    evidence = {}
    for record in json.loads(EVIDENCE.read_text())["records"]:
        for segment in record.get("segments", []):
            evidence[segment["evidence_id"]] = {
                "text": segment.get("text", ""),
                "start_seconds": segment.get("start_seconds"),
                "end_seconds": segment.get("end_seconds"),
                "source_url": record.get("source_url"),
            }
    taxonomy = _taxonomy_lookup()
    jobs = _job_cards()
    cards = []
    relation_cards = []
    job_counts = Counter()
    unclassified = 0
    boundary_items = 0
    for entry in index["entries"]:
        for item in entry["communication_function_inventory"]:
            mapped = taxonomy.get((entry["review_id"], item["sequence"]), {})
            job = mapped.get("canonical_job", "unclassified")
            template = jobs.get(job)
            if job == "unclassified":
                unclassified += 1
            elif job == "media_or_publisher":
                boundary_items += 1
            else:
                job_counts[job] += 1
            segments = []
            for evidence_id in item.get("evidence_ids", [])[:5]:
                row = evidence.get(evidence_id, {})
                segments.append({
                    "evidence_id": evidence_id,
                    "text": row.get("text", ""),
                    "start_seconds": row.get("start_seconds"),
                    "end_seconds": row.get("end_seconds"),
                    "source_url": row.get("source_url"),
                })
            if template:
                form = template["form"]
                mechanism = template["mechanism"]
                practice = template["practice"]
                self_check = template["self_check"]
                non_fit = template["non_fit"]
            else:
                form = "Inspect the complete context first; do not imitate this label without a clearer function decision."
                mechanism = "No shared-job mechanism is assigned until the original function label is reviewed."
                practice = "Rewrite the observed move in plain language, then test whether a listener can identify its purpose."
                self_check = "Can you describe what the speaker is doing without relying on the label alone?"
                non_fit = "Do not turn an unclassified episode into a recommendation."
            cards.append({
                "card_id": f"{entry['review_id']}:{item['sequence']}",
                "review_id": entry["review_id"],
                "video_id": entry["video_id"],
                "title": entry["title"],
                "writeup": entry.get("writeup"),
                "canonical_job": job,
                "canonical_job_status": (
                    "heuristic_mapping" if job not in {"unclassified", "media_or_publisher"}
                    else "non_speech_boundary" if job == "media_or_publisher"
                    else "unclassified_pending_review"
                ),
                "raw_function_label": item.get("function", ""),
                "observed_move": item.get("reason", ""),
                "why_it_might_help": mechanism,
                "repeatable_form": form,
                "practice": practice,
                "self_check": self_check,
                "non_fit": non_fit,
                "exact_evidence": segments,
                "review_limits": entry.get("limits", []),
                "next_test": entry.get("next_test", ""),
                "claim_boundary": "Transcript-derived discovery and practice hypothesis only; not independently reviewed, delivery-validated, learner-validated or listener-outcome evidence.",
            })
        for relation_number, relation in enumerate(entry["structural_relation_inventory"], start=1):
            from_ids = relation.get("from_evidence_ids", [])[:3]
            to_ids = relation.get("to_evidence_ids", [])[:3]
            evidence_ids = list(dict.fromkeys(from_ids + to_ids))
            segments = []
            for evidence_id in evidence_ids:
                row = evidence.get(evidence_id, {})
                segments.append({
                    "evidence_id": evidence_id,
                    "text": row.get("text", ""),
                    "start_seconds": row.get("start_seconds"),
                    "end_seconds": row.get("end_seconds"),
                    "source_url": row.get("source_url"),
                })
            relation_cards.append({
                "card_id": f"{entry['review_id']}:relation:{relation_number}",
                "review_id": entry["review_id"],
                "video_id": entry["video_id"],
                "title": entry["title"],
                "writeup": entry.get("writeup"),
                "card_type": "structural_sequence",
                "relation_type": relation.get("type", ""),
                "sequence_claim": relation.get("claim", ""),
                "from_evidence_ids": from_ids,
                "to_evidence_ids": to_ids,
                "exact_evidence": segments,
                "why_it_might_help": "Hypothesis: making the bridge between these two moves explicit may reduce the listener's need to infer why the talk changed direction.",
                "repeatable_approach": "Complete the first move, name the relationship, then make the second move; do not assume the audience will supply the bridge.",
                "practice": "Give a 30–60 second explanation using the same move-to-move relationship with a new topic. Ask a listener to name the bridge.",
                "self_check": "Can a listener state what changed and why the second move followed the first?",
                "non_fit": "Do not force a sequence onto a talk whose source context, speaker turns or editing make the relationship uncertain.",
                "review_limits": entry.get("limits", []),
                "next_test": entry.get("next_test", ""),
                "claim_boundary": "Transcript-derived structural relation and practice hypothesis only; not independently reviewed, delivery-validated, learner-validated or listener-outcome evidence.",
            })
    report = {
        "schema_version": "1.0",
        "inventory_id": "corpus-learner-card-inventory",
        "status": "transcript_derived_practice_navigation_not_validated",
        "claim_boundary": "Every card is a way to learn from and inspect a recorded transcript review. It does not establish that the move works, that the speaker intended the inferred function, or that the form should be used universally.",
        "source_artifacts": [str(INDEX.relative_to(ROOT)), str(TAXONOMY.relative_to(ROOT)), str(EVIDENCE.relative_to(ROOT)), str(JOBS.relative_to(ROOT))],
        "summary": {
            "review_count": len(index["entries"]),
            "card_count": len(cards),
            "structural_card_count": len(relation_cards),
            "total_card_count": len(cards) + len(relation_cards),
            "cards_with_exact_evidence": sum(bool(card["exact_evidence"]) for card in cards),
            "structural_cards_with_exact_evidence": sum(bool(card["exact_evidence"]) for card in relation_cards),
            "cards_with_shared_job_template": sum(job_counts.values()),
            "non_speech_or_publisher_boundary_cards": boundary_items,
            "unclassified_cards": unclassified,
            "canonical_job_counts": dict(job_counts.most_common()),
        },
        "cards": cards,
        "structural_cards": relation_cards,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    summary = report["summary"]
    MD.write_text("\n".join([
        "# Corpus learner-card inventory", "",
        "Status: **transcript-derived practice navigation; not validated curriculum**.", "",
        report["claim_boundary"], "",
        f"This inventory contains **{summary['card_count']} function cards** and **{summary['structural_card_count']} sequence cards** from **{summary['review_count']} full-context reviews**. "
        f"Each card preserves the original function label and reason, up to five exact caption segments, a provisional shared-job form where available, a drill, self-check, non-fit warning, limits and next test.", "",
        f"Function cards with exact evidence: **{summary['cards_with_exact_evidence']}** · sequence cards with exact evidence: **{summary['structural_cards_with_exact_evidence']}** of {summary['structural_card_count']} · cards with a shared speech-job template: **{summary['cards_with_shared_job_template']}** · publisher/media boundary cards: **{summary['non_speech_or_publisher_boundary_cards']}** · unclassified and requiring review: **{summary['unclassified_cards']}**.", "",
        "Use the [searchable inventory](corpus-learner-card-inventory.html) to filter by video, raw label, canonical job, relation type or wording. Use the linked full writeup and source context before treating a card as a lesson.", "",
        "## How to use one card", "",
        "1. Read the exact evidence and the surrounding writeup.",
        "2. State the communication problem in your own words.",
        "3. Try the repeatable form in a low-stakes example.",
        "4. Run the self-check and note where the form does not fit.",
        "5. Keep delivery, audience effect and factual claims separate until they are independently checked.", "",
        "## Canonical-job distribution", "",
        "| Job | Cards |", "|---|---:|",
        *[f"| `{job}` | {count} |" for job, count in summary["canonical_job_counts"].items()], "",
        "The [JSON inventory](../research/corpus-learner-card-inventory.json) retains every card and its provenance.", "",
    ]) + "\n")
    articles = []
    all_cards = cards + relation_cards
    for card in all_cards:
        is_relation = card.get("card_type") == "structural_sequence"
        search = " ".join([
            card["title"], card["video_id"], card.get("canonical_job", ""),
            card.get("raw_function_label", ""), card.get("observed_move", ""),
            card.get("relation_type", ""), card.get("sequence_claim", ""),
        ]).lower()
        evidence_html = " ".join(
            f"<blockquote><code>{html.escape(row['evidence_id'])}</code> {html.escape(row['text'])}</blockquote>"
            for row in card["exact_evidence"]
        ) or "<p>No exact segment was linked; inspect the full writeup.</p>"
        writeup = f"<a href='../{html.escape(card['writeup'])}'>full writeup</a>" if card.get("writeup") else ""
        if is_relation:
            heading = f"<p><b>Sequence:</b> <code>{html.escape(card['relation_type'])}</code></p><h3>Sequence claim</h3><p>{html.escape(card['sequence_claim'])}</p>"
            form_heading = "Repeatable approach"
            form = card["repeatable_approach"]
            label = "Structural sequence"
        else:
            heading = f"<p><b>Job:</b> <code>{html.escape(card['canonical_job'])}</code> · <b>Original label:</b> {html.escape(card['raw_function_label'])}</p><h3>Observed move</h3><p>{html.escape(card['observed_move'])}</p>"
            form_heading = "Repeatable form"
            form = card["repeatable_form"]
            label = "Function"
        articles.append(
            f"<article class='card' data-search='{html.escape(search, quote=True)}' data-job='{html.escape(card.get('canonical_job', ''), quote=True)}' data-relation='{html.escape(card.get('relation_type', ''), quote=True)}' data-kind='{html.escape(card.get('card_type', 'function'), quote=True)}'>"
            f"<h2>{html.escape(card['title'])}</h2><p><code>{html.escape(card['card_id'])}</code> · {writeup}</p>"
            f"<p><b>Card type:</b> {label}</p>{heading}<h3>Exact evidence</h3>{evidence_html}"
            f"<h3>Why it might help</h3><p>{html.escape(card['why_it_might_help'])}</p>"
            f"<h3>{form_heading}</h3><p>{html.escape(form)}</p>"
            f"<h3>Practice</h3><p>{html.escape(card['practice'])}</p>"
            f"<details><summary>Self-check, non-fit and limits</summary><p><b>Self-check:</b> {html.escape(card['self_check'])}</p><p><b>Non-fit:</b> {html.escape(card['non_fit'])}</p><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in card['review_limits'])}</ul><p>{html.escape(card['claim_boundary'])}</p></details></article>"
        )
    jobs_select = "".join(f"<option>{html.escape(job)}</option>" for job in sorted({c['canonical_job'] for c in cards}))
    relation_select = "".join(f"<option>{html.escape(kind)}</option>" for kind in sorted({c['relation_type'] for c in relation_cards}))
    page = """<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Corpus learner-card inventory</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1150px;margin:2rem auto;padding:0 1rem;color:#17202a}input,select{font:inherit;padding:.6rem;margin:.3rem .5rem .8rem 0}input{width:min(620px,100%)}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.card{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.card h2{margin:.1rem 0}.card h3{margin-bottom:.2rem}blockquote{background:#f4f8fb;border-left:4px solid #39739d;padding:.6rem;margin:.5rem 0}code{overflow-wrap:anywhere}.muted{color:#5c6872}</style><main><h1>Corpus learner-card inventory</h1><div class='notice'><b>Practice navigation, not proof.</b> These cards expose transcript-derived observations from all reviewed videos. “Why it might help” is a hypothesis; exact wording remains retained caption text; delivery and listener effects are not established.</div><p class='muted'>395 reviews · 4,016 function cards + 2,800 sequence cards. Search, inspect the full context, then practice with the limits visible.</p><label>Job <select id='job'><option value=''>All jobs</option>__JOBS__</select></label><label>Sequence type <select id='relation'><option value=''>All sequences</option>__RELATIONS__</select></label><label>Search <input id='search' type='search' placeholder='title, video ID, original label, relation or wording'></label><p id='count' aria-live='polite'></p><section id='cards'>__CARDS__</section></main><script>const cards=[...document.querySelectorAll('.card')],search=document.querySelector('#search'),job=document.querySelector('#job'),relation=document.querySelector('#relation'),count=document.querySelector('#count');function filter(){const q=search.value.toLowerCase(),j=job.value,r=relation.value;let n=0;cards.forEach(c=>{const ok=(!j||c.dataset.job===j)&&(!r||c.dataset.relation===r)&&(!q||c.dataset.search.includes(q));c.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${cards.length} cards`}search.oninput=filter;job.onchange=filter;relation.onchange=filter;filter()</script>"""
    HTML.write_text(page.replace("__JOBS__", jobs_select).replace("__RELATIONS__", relation_select).replace("__CARDS__", "\n".join(articles)))
    return report


if __name__ == "__main__":
    print(json.dumps(build()["summary"], indent=2))
