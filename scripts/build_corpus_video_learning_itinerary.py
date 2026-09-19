#!/usr/bin/env python3
"""Build one bounded learner entry point for every reviewed corpus video."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/corpus-learner-card-inventory.json"
OUT = ROOT / "research/corpus-video-learning-itinerary.json"
MD = ROOT / "writeups/corpus-video-learning-itinerary.md"
HTML = ROOT / "writeups/corpus-video-learning-itinerary.html"


def rank_function(card: dict) -> tuple:
    return (
        card.get("canonical_job_status") == "heuristic_mapping",
        bool(card.get("exact_evidence")),
        card.get("canonical_job") not in {"media_or_publisher", "unclassified"},
        len(card.get("observed_move", "")),
    )


def build() -> dict:
    data = json.loads(CARDS.read_text())
    by_video = {}
    for card in data["cards"]:
        by_video.setdefault(card["video_id"], []).append(card)
    relations = {}
    for card in data["structural_cards"]:
        relations.setdefault(card["video_id"], []).append(card)
    rows = []
    for video_id in sorted(by_video):
        functions = sorted(by_video[video_id], key=rank_function, reverse=True)
        chosen = functions[0]
        sequence = sorted(relations.get(video_id, []), key=lambda x: bool(x.get("exact_evidence")), reverse=True)
        bridge = sequence[0] if sequence else None
        rows.append({
            "video_id": video_id,
            "title": chosen["title"],
            "writeup": chosen.get("writeup"),
            "lesson_card_id": chosen["card_id"],
            "canonical_job": chosen["canonical_job"],
            "raw_function_label": chosen["raw_function_label"],
            "observed_move": chosen["observed_move"],
            "why_it_might_help": chosen["why_it_might_help"],
            "repeatable_form": chosen["repeatable_form"],
            "practice": chosen["practice"],
            "self_check": chosen["self_check"],
            "exact_evidence": chosen["exact_evidence"],
            "sequence_card_id": bridge["card_id"] if bridge else None,
            "sequence_type": bridge["relation_type"] if bridge else None,
            "sequence_claim": bridge["sequence_claim"] if bridge else None,
            "sequence_evidence": bridge["exact_evidence"] if bridge else [],
            "limits": chosen["review_limits"],
            "next_test": chosen["next_test"],
            "claim_boundary": "One selected transcript-derived learning entry; selection is a navigation aid, not a best-practice ranking or effectiveness result.",
        })
    report = {
        "schema_version": "1.0",
        "itinerary_id": "corpus-video-learning-itinerary",
        "status": "one_entry_per_reviewed_video_transcript_derived_not_validated",
        "claim_boundary": "This itinerary gives one practical starting lesson for each reviewed video. It does not claim that the selected item is the most important, representative, recurrent, effective or independently verified lesson from that video.",
        "source": "research/corpus-learner-card-inventory.json",
        "video_count": len(rows),
        "entries_with_exact_evidence": sum(bool(row["exact_evidence"]) for row in rows),
        "entries_with_sequence_bridge": sum(bool(row["sequence_card_id"]) for row in rows),
        "entries": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Corpus video-learning itinerary", "", "Status: **one selected starting lesson per reviewed video; transcript-derived and not validated**.", "", report["claim_boundary"], "", f"Entries: **{len(rows)} videos** · exact evidence attached: **{report['entries_with_exact_evidence']}** · sequence bridge attached: **{report['entries_with_sequence_bridge']}**.", "", "Use one entry as a short lesson: read the evidence, name the move, adapt the form, practice it in a new situation, then run the self-check. Open the linked card inventory for alternate functions and the full writeup for limits.", "", "## Selected entries", "", "| Video | Job | Selected move | Bridge |", "|---|---|---|---|"]
    for row in rows:
        title = row["title"].replace("|", "\\|")
        move = (row["observed_move"] or row["raw_function_label"] or "(no move text)").replace("|", "\\|")[:140]
        lines.append(f"| `{row['video_id']}` {title} | `{row['canonical_job']}` | {move} | `{row['sequence_type'] or 'none'}` |")
    lines += ["", "The [searchable itinerary](corpus-video-learning-itinerary.html) provides the full entry cards and filters.", ""]
    MD.write_text("\n".join(lines))
    articles = []
    for row in rows:
        search = " ".join([row["video_id"], row["title"], row["canonical_job"], row["raw_function_label"], row["observed_move"], row["sequence_type"] or ""]).lower()
        evidence = " ".join(f"<blockquote><code>{html.escape(x['evidence_id'])}</code> {html.escape(x['text'])}</blockquote>" for x in row["exact_evidence"]) or "<p>No exact segment was linked; inspect the full writeup.</p>"
        bridge = f"<p><b>Sequence bridge:</b> <code>{html.escape(row['sequence_type'] or '')}</code> {html.escape(row['sequence_claim'] or '')}</p>" if row["sequence_card_id"] else "<p>No sequence bridge was recorded.</p>"
        writeup = f"<a href='../{html.escape(row['writeup'])}'>full writeup</a>" if row.get("writeup") else ""
        articles.append(f"<article class='entry' data-search='{html.escape(search, quote=True)}'><h2>{html.escape(row['title'])}</h2><p><code>{html.escape(row['video_id'])}</code> · {writeup}</p><p><b>Job:</b> <code>{html.escape(row['canonical_job'])}</code> · <b>Original label:</b> {html.escape(row['raw_function_label'])}</p><h3>What to notice</h3><p>{html.escape(row['observed_move'])}</p><h3>Exact evidence</h3>{evidence}{bridge}<h3>Try it</h3><p><b>Form:</b> {html.escape(row['repeatable_form'])}</p><p>{html.escape(row['practice'])}</p><h3>Self-check</h3><p>{html.escape(row['self_check'])}</p><details><summary>Limits and next test</summary><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in row['limits'])}</ul><p>{html.escape(row['next_test'])}</p><p>{html.escape(row['claim_boundary'])}</p></details></article>")
    HTML.write_text("""<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Corpus video-learning itinerary</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1150px;margin:2rem auto;padding:0 1rem;color:#17202a}input{font:inherit;padding:.7rem;width:min(700px,100%);margin:1rem 0}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.entry{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.entry h2{margin:.1rem 0}.entry h3{margin-bottom:.2rem}blockquote{background:#f4f8fb;border-left:4px solid #39739d;padding:.6rem;margin:.5rem 0}code{overflow-wrap:anywhere}</style><main><h1>Corpus video-learning itinerary</h1><div class='notice'><b>Starting points, not rankings.</b> One transcript-derived learning entry is selected for each reviewed video. Search, read the exact context, adapt the move and keep the stated limits visible.</div><p>395 video entries · exact evidence and practice prompts included.</p><label for='search'>Search by video, title, job, label or wording</label><input id='search' type='search'><p id='count' aria-live='polite'></p><section id='entries'>__ENTRIES__</section></main><script>const entries=[...document.querySelectorAll('.entry')],input=document.querySelector('#search'),count=document.querySelector('#count');function filter(){const q=input.value.toLowerCase();let n=0;entries.forEach(x=>{const ok=!q||x.dataset.search.includes(q);x.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${entries.length} videos`}input.oninput=filter;filter()</script>""".replace("__ENTRIES__", "\n".join(articles)))
    return report


if __name__ == "__main__":
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": build()["video_count"]}, indent=2))
