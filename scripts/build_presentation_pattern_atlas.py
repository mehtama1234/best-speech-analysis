#!/usr/bin/env python3
"""Build one presenter-facing index over the current corpus pattern system."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/presentation-pattern-atlas.json"
MD = ROOT / "writeups/presentation-pattern-atlas.md"
HTML = ROOT / "writeups/presentation-pattern-atlas.html"


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def build() -> dict:
    inventory = read("research/exhaustive-pattern-inventory.json")
    corpus = read("research/corpus-overview.json")
    cards = read("research/expanded-pattern-candidate-cards.json")
    bundles = read("research/compound-pattern-bundles.json")
    triads = read("research/compound-pattern-triads.json")
    sequences = read("research/presentation-sequence-library.json")
    shortlist = read("research/expanded-pattern-llm-shortlist.json")
    browser = read("research/expanded-pattern-browser-smoke.json")
    compound_browser = read("research/compound-pattern-browser-smoke.json")
    triad_browser = read("research/compound-triad-browser-smoke.json")
    draft_judge = read("research/local-llm-draft-judge.json")
    return {
        "schema_version": "1.0",
        "atlas_id": "presentation-pattern-atlas",
        "status": "corpus_mined_candidate_system_indexed_for_practice",
        "coverage": {
            "unique_inventory_videos": corpus["video_count"],
            "nonempty_transcript_videos": corpus["nonempty_transcript_count"],
            "full_context_reviews": inventory["review_count"],
            "inspected_captions": corpus["segment_count"],
            "episode_records": inventory["episode_record_count"],
            "relation_records": inventory["relation_record_count"],
        },
        "discovery_layers": {
            "broad_themes": inventory["theme_count"],
            "relation_architectures": inventory["relation_pattern_count"],
            "unmatched_clusters": inventory["unmatched_cluster_count"],
            "expanded_cards": cards["card_count"],
            "all_compound_bundles": bundles["candidate_bundle_count"],
            "practice_compound_bundles": bundles["bundle_count"],
            "all_compound_triads": triads["candidate_triad_count"],
            "practice_compound_triads": triads["practice_triad_count"],
            "presentation_sequences": sequences["sequence_count"],
            "llm_shortlist_cards": shortlist["candidate_count"],
        },
        "practice_surfaces": [
            {"id": "expanded_pattern_browser", "path": "writeups/expanded-pattern-candidate-cards.html", "smoke_status": browser["status"]},
            {"id": "compound_pattern_browser", "path": "writeups/compound-pattern-bundles.html", "smoke_status": compound_browser["status"]},
            {"id": "compound_triad_browser", "path": "writeups/compound-pattern-triads.html", "smoke_status": triad_browser["status"]},
            {"id": "sequence_library", "path": "writeups/presentation-sequence-library.md", "smoke_status": "source_linked_library_generated"},
            {"id": "cli_speech_worksheet", "path": "scripts/build_speech_draft.py", "smoke_status": "sequence_stems_and_boundaries_tested"},
            {"id": "local_llm_draft_judge", "path": "writeups/local-llm-draft-judge.md", "smoke_status": draft_judge["status"]},
        ],
        "sequence_ids": [sequence["sequence_id"] for sequence in sequences["sequences"]],
        "claim_boundary": "This atlas indexes transcript-derived candidate patterns and local practice surfaces. It does not establish speaker intent, universal effectiveness, learner improvement, listener outcomes, causality, or independent human validation.",
    }


def render(report: dict) -> str:
    coverage = report["coverage"]
    layers = report["discovery_layers"]
    lines = [
        "# Presentation pattern atlas",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        "## Corpus coverage",
        "",
        f"- **{coverage['unique_inventory_videos']}** unique inventory videos; **{coverage['nonempty_transcript_videos']}** have non-empty canonical transcripts",
        f"- **{coverage['full_context_reviews']}** full-context reviews",
        f"- **{coverage['inspected_captions']}** inspected captions",
        f"- **{coverage['episode_records']}** episode records",
        f"- **{coverage['relation_records']}** relation records",
        "",
        "## Discovery layers",
        "",
        f"- **{layers['broad_themes']}** broad themes + **{layers['relation_architectures']}** relation architectures + **{layers['unmatched_clusters']}** unmatched clusters",
        f"- **{layers['expanded_cards']}** source-linked expanded cards",
        f"- **{layers['all_compound_bundles']}** recurring compound pairings; top **{layers['practice_compound_bundles']}** surfaced for rehearsal",
        f"- **{layers['all_compound_triads']}** recurring three-move triads; top **{layers['practice_compound_triads']}** retained as practice candidates",
        f"- **{layers['presentation_sequences']}** presentation sequences",
        f"- **{layers['llm_shortlist_cards']}** local-LLM-prioritized cards",
        "",
        "## Start a presentation",
        "",
        "1. Choose a sequence in the [sequence library](presentation-sequence-library.md): explain, propose, report, lead, answer, or tell a story.",
        "2. Use the [presentation builder](presentation-builder.html) to enter a topic, audience and outcome, then combine one architecture with up to three pattern moves.",
        "3. Use the [expanded pattern browser](expanded-pattern-candidate-cards.html) to select moves and draft each sentence-level step.",
        "4. Use the [compound bundle browser](compound-pattern-bundles.html) when two recurring moves need to be rehearsed together.",
        "5. Record the listener restatement, uncertainty, non-fit and next revision before exporting the local practice record.",
        "",
        "For the complete human-readable catalog of themes, subthemes, source-linked examples and presentation uses, read the [amazing presentation patterns guide](amazing-presentation-patterns.md).",
        "",
        "## Sequence IDs",
        "",
    ]
    lines.extend(f"- `{sequence_id}`" for sequence_id in report["sequence_ids"])
    lines += ["", "## Runtime evidence", ""]
    lines.extend(f"- `{surface['id']}` — `{surface['path']}` — **{surface['smoke_status']}**" for surface in report["practice_surfaces"])
    lines += ["", "The local LLM screen is a prioritization aid. It does not promote a pattern or replace independent review.", ""]
    return "\n".join(lines)


def render_html(report: dict) -> str:
    coverage = report["coverage"]
    layers = report["discovery_layers"]
    sequence_links = "".join(f'<li><code>{sequence_id}</code></li>' for sequence_id in report["sequence_ids"])
    surface_links = "".join(f'<li><a href="{surface["path"].split("/")[-1]}">{surface["id"]}</a> — {surface["smoke_status"]}</li>' for surface in report["practice_surfaces"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Presentation pattern atlas</title><style>:root{{--bg:#f6f7fb;--fg:#172033;--muted:#5b6475;--card:#fff;--line:#d9deea;--accent:#2457d6;--warn:#fff3d6}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}}main{{max-width:950px;margin:auto;padding:32px 18px 70px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}}.muted{{color:var(--muted)}}.boundary{{background:var(--warn);padding:12px;border-radius:8px}}a{{color:var(--accent)}}code{{font-size:.9em}}</style></head><body><main><h1>Presentation pattern atlas</h1><p class=muted>{report['status']}</p><p class=boundary>{report['claim_boundary']}</p><p><a href="amazing-presentation-patterns.md">Read the complete themes, subthemes, examples and usage guide</a>.</p><h2>Corpus coverage</h2><div class=grid><div class=card><strong>{coverage['unique_inventory_videos']}</strong><br>unique inventory videos</div><div class=card><strong>{coverage['nonempty_transcript_videos']}</strong><br>non-empty transcript videos</div><div class=card><strong>{coverage['full_context_reviews']}</strong><br>full-context reviews</div><div class=card><strong>{coverage['inspected_captions']}</strong><br>inspected captions</div><div class=card><strong>{coverage['episode_records']}</strong><br>episode records</div><div class=card><strong>{coverage['relation_records']}</strong><br>relation records</div></div><h2>Discovery layers</h2><ul><li>{layers['broad_themes']} broad themes, {layers['relation_architectures']} relation architectures, {layers['unmatched_clusters']} unmatched clusters</li><li>{layers['expanded_cards']} expanded cards</li><li>{layers['all_compound_bundles']} compound pairings ({layers['practice_compound_bundles']} surfaced for practice)</li><li>{layers['all_compound_triads']} three-move triads ({layers['practice_compound_triads']} surfaced for practice)</li><li>{layers['presentation_sequences']} presentation sequences</li><li>{layers['llm_shortlist_cards']} local-LLM-prioritized cards</li></ul><h2>Practice surfaces</h2><ul>{surface_links}</ul><h2>Sequence IDs</h2><ul>{sequence_links}</ul><p class=muted>Use the sequence library to choose a talk shape, the expanded browser to draft individual moves, and the compound browser to rehearse recurring two-move pairings.</p></main></body></html>'''


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    HTML.write_text(render_html(report))
    print(f"presentation pattern atlas: {len(report['sequence_ids'])} sequences, {report['discovery_layers']['expanded_cards']} cards, {report['discovery_layers']['all_compound_bundles']} compound candidates")
