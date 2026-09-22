#!/usr/bin/env python3
"""Mine all full-context reviews for recurring, source-linked pattern leads.

This is a discovery index, not a semantic validation pass. It deliberately
keeps every matched label/relation tied to the originating review and evidence
IDs so later review can accept, split or reject a theme.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/full-context-reviews.json"
OUT = ROOT / "research/exhaustive-pattern-inventory.json"
MD = ROOT / "writeups/exhaustive-pattern-inventory.md"

THEMES = [
    ("orientation_and_roadmap", "opening|introduction|welcome|preview|roadmap|route|agenda|structure|transition|beginning", "Orient the listener before detail: situation → stake → route."),
    ("question_and_reframe", "question|ask|prompt|reframe|redefine|more useful|what matters", "Name the question, answer its useful version, and show what changed."),
    ("objection_and_response", "objection|challenge|dismiss|skeptic|criticism|response|answer|defen[cs]|counter", "State the objection fairly, answer it, and preserve the remaining uncertainty."),
    ("contrast_and_reversal", "contrast|reversal|reverse|rather than|instead|however|but|opposition|turnaround", "Make the earlier frame and the changed frame visible without a false binary."),
    ("qualification_and_boundary", "qualif|limit|bound|scope|condition|caveat|uncertain|calendar|exception|not literal", "State the point, then its condition, scope, or evidence limit."),
    ("cause_and_mechanism", "caus|mechan|because|reason|why|process|pathway|how", "Connect claim to mechanism, and distinguish explanation from proof."),
    ("scale_shift", "scale|collective|individual|community|global|universal|wider|narrow|audience", "Move between personal, institutional, and collective scale with an explicit bridge."),
    ("story_memory_and_scene", "story|memory|remember|childhood|personal|experience|scene|encounter|recollection|origin", "Use a bounded scene, then say what it illustrates and cannot establish."),
    ("credit_and_collective_agency", "credit|acknow|contribution|partner|team|collective|support|family|community|distributed", "Name contributors, connect credit to the result, and assign agency precisely."),
    ("risk_safety_and_limit", "risk|safety|danger|harm|failure|blocked|threat|burden|cost|loss", "Name the risk or failure mode before asking for trust or action."),
    ("choice_and_responsibility", "choice|decision|responsib|account|agency|option|voluntary|duty|obligation", "Show who can choose, what support is required, and what remains their responsibility."),
    ("value_and_moral_frame", "moral|value|ethic|honor|justice|fair|dignity|meaning|principle|belief", "Separate the value interpretation from the factual claim it accompanies."),
    ("grief_loss_and_continuation", "grief|sorrow|loss|memorial|mourning|death|continu|surviv|farewell", "Acknowledge loss, then name what continues without pretending loss is resolved."),
    ("identity_status_and_belonging", "identity|status|belong|outsider|insider|class|gender|race|citizen|role|name", "Make identity or status relevant to the claim without using it as proof."),
    ("analogy_metaphor_and_callback", "analogy|metaphor|image|symbol|callback|return|motif|repetition|echo", "Introduce an anchor, develop the reasoning, and return with changed application."),
    ("definition_and_explanation", "definition|define|explain|meaning|term|category|distinction|clarif|demyst", "Give a plain definition, example, and boundary."),
    ("audience_invitation_and_next_turn", "audience|invite|join|question|ask|particip|call|hands.off|release|respond", "Make the next turn specific, answerable, and safe to decline."),
    ("humor_rapport_and_self_undercut", "humor|joke|laugh|comic|rapport|self.direct|self.undercut|satire", "Use lightness to open room, then return clearly to the substantive point."),
    ("future_hope_and_action", "future|hope|possib|tomorrow|next|mission|action|change|build|create", "Turn aspiration into a bounded next action and name its limit."),
    ("institution_system_and_policy", "institution|system|policy|government|organization|architecture|infrastructure|law|program", "Move from individual experience to the system that shapes the option set."),
    ("repair_and_self_correction", "repair|correct|mistake|error|wrong|incomplete|clarif|apolog|retract", "Mark the error, replace it plainly, and continue."),
    ("metrics_and_revaluation", "metric|measure|number|count|success|revalu|worth|checklist|benchmark|percent", "Show what the metric captures, what it misses, and why the measure matters."),
]

RELATION_FORMS = {
    "story_to_thesis": "bounded scene → explicit lesson → what the scene cannot prove",
    "premise_correction": "acknowledge the starting premise → identify the missing distinction → answer the corrected question",
    "expectation_reversal": "name what the audience expects → show the observed turn → explain the consequence",
    "analogy_transfer": "name the source image → map the relevant relation → state where the analogy stops",
    "credit_redirection": "receive or name praise → widen the causal chain → identify the people and conditions that made it possible",
    "metric_revaluation": "show the familiar measure → expose what it misses → propose the human-relevant measure",
    "optional_support": "name the need → offer a support choice → preserve agency and an opt-out",
    "reciprocal_learning": "share an observation → invite the other person’s correction → update the shared account",
    "evidence_gap": "state the claim → name the missing evidence → specify the next test",
    "scope_repair": "identify where the claim was too broad → narrow it → preserve the valid core",
    "register_shift": "signal the shift in audience or tone → keep the underlying point stable → return to the shared frame",
    "self_undercut": "acknowledge your own stake or limitation → state the claim anyway → give the listener a way to check it",
    "question_redefinition": "repeat the surface question → explain why it is insufficient → ask the decision-relevant question",
    "sorrow_and_continuation": "name the loss → refuse false resolution → identify what care or work continues",
    "moral_to_memorial": "move from a disputed judgment → mark the human significance → avoid treating tribute as proof",
    "despair_to_hope": "let the difficulty remain visible → identify a live possibility → name the next bounded action",
    "audience_shift": "locate who is being addressed → change the level of explanation → make the new role explicit",
    "hands_off": "state what you cannot control → identify the decision owner → offer the information or support you can provide",
}

UNMATCHED_CLUSTERS = [
    ("difficulty_to_capability", "difficulty|obstacle|under difficulty|captaincy difficulty|pressure resistance", "name the difficulty → show the response or support → identify the capability being built"),
    ("unfinished_work_to_commitment", "unfinished work|remaining|still|promise|commitment|renewed offer", "acknowledge what is unfinished → name the commitment → state the next accountable step"),
    ("purpose_attention_example", "purpose|attention|examples selection|purpose over", "state why the exchange matters → select one concrete example → return to the purpose"),
    ("authority_to_service", "authority|captaincy|leadership|status|role", "name the authority or role → show its responsibility → return agency to the people affected"),
    ("recognition_to_specific_credit", "host praise|host endorsement|repeated gratitude|recognition|gratitude", "receive or give recognition → name the specific contribution → avoid turning praise into proof"),
    ("craft_process_over_outcome", "writing|production|craft|script versus production|adaptable", "show the process and choices → explain the constraint → separate craft from the final outcome"),
    ("selection_and_incentive", "selection|fan selection|incentive|choice|ranking", "state the selection criterion → show the choice → name what the incentive changes"),
    ("emotion_to_composure", "emotion|composure|stage|evolving craft", "name the felt difficulty → choose a controllable response → continue without pretending the feeling vanished"),
    ("failure_to_reframe", "outcome fails|rejection|alternative career|loss|refusal quit", "state the failed outcome → distinguish it from identity → choose the next experiment"),
    ("access_obstacle_to_support", "helper access|obstacle|unknown helper|support|opportunity", "name the access barrier → identify available support → preserve the recipient's choice"),
    ("technical_explanation_and_interruption", "technical explanation|interrupted|diagnosis", "pause the technical thread → translate the key point → answer the interruption before continuing"),
    ("authenticity_vs_performance", "authenticity|script versus|performance|fictional inspiration", "separate performed form from lived claim → explain the choice → mark what remains constructed"),
    ("invitation_to_low_barrier_entry", "invitation|philanthropic entry|join|involvement", "make the invitation concrete → offer a low-barrier entry → state the role and limit"),
    ("familiarity_to_scope", "pervasiveness|familiar settings|local connection|shared", "start with a familiar setting → widen the scope carefully → state where the analogy stops"),
    ("unity_across_scale", "unity|national|collective|community|global", "name the shared value → bridge personal and collective scale → preserve disagreement within the unity"),
]


def evidence_sample(item: dict, review: dict, kind: str) -> dict:
    if kind == "episode":
        evidence = item.get("evidence_ids", [])
        return {
            "review_id": review["review_id"],
            "video_id": review["video_id"],
            "sequence": item.get("sequence"),
            "label": item.get("function", ""),
            "evidence_ids": evidence[:5],
            "writeup": review.get("writeup"),
        }
    evidence = item.get("from_evidence_ids", []) + item.get("to_evidence_ids", [])
    return {
        "review_id": review["review_id"],
        "video_id": review["video_id"],
        "relation_type": item.get("type", ""),
        "claim": item.get("claim", ""),
        "evidence_ids": evidence[:8],
        "writeup": review.get("writeup"),
    }


def build() -> dict:
    reviews = json.loads(SOURCE.read_text())["reviews"]
    episode_total = 0
    relation_total = 0
    raw_labels = Counter()
    raw_relations = Counter()
    themes = []
    relation_patterns = []
    unmatched_clusters = []
    for theme_id, pattern, form in THEMES:
        regex = re.compile(pattern, re.I)
        episode_hits = []
        relation_hits = []
        videos = set()
        for review in reviews:
            for item in review.get("episode_map", []):
                label = (item.get("function") or "").strip()
                if not label:
                    continue
                episode_total += 1
                raw_labels[label] += 1
                if regex.search(label):
                    episode_hits.append(evidence_sample(item, review, "episode"))
                    videos.add(review["video_id"])
            for item in review.get("relations", []):
                relation_type = (item.get("type") or "").strip()
                claim = item.get("claim") or ""
                if not relation_type:
                    continue
                relation_total += 1
                raw_relations[relation_type] += 1
                if regex.search(relation_type) or regex.search(claim):
                    relation_hits.append(evidence_sample(item, review, "relation"))
                    videos.add(review["video_id"])
        # Keep distinct source examples, not a claim that every hit is a separate pattern.
        seen = set()
        examples = []
        for item in episode_hits + relation_hits:
            key = (item["review_id"], item.get("sequence"), item.get("relation_type"))
            if key in seen:
                continue
            seen.add(key)
            examples.append(item)
            if len(examples) >= 8:
                break
        themes.append({
            "theme_id": theme_id,
            "candidate_form": form,
            "matching_rule": pattern,
            "episode_hit_count": len(episode_hits),
            "relation_hit_count": len(relation_hits),
            "video_count": len(videos),
            "examples": examples,
            "status": "candidate_theme_requires_contextual_and_independent_review",
        })
    for relation_type, candidate_form in RELATION_FORMS.items():
        examples = []
        videos = set()
        count = 0
        for review in reviews:
            for item in review.get("relations", []):
                if (item.get("type") or "").strip() != relation_type:
                    continue
                count += 1
                videos.add(review["video_id"])
                if len(examples) < 8:
                    examples.append(evidence_sample(item, review, "relation"))
        relation_patterns.append({
            "relation_type": relation_type,
            "candidate_form": candidate_form,
            "relation_count": count,
            "video_count": len(videos),
            "examples": examples,
            "status": "candidate_structural_pattern_requires_contextual_and_independent_review",
        })
    for cluster_id, pattern, candidate_form in UNMATCHED_CLUSTERS:
        regex = re.compile(pattern, re.I)
        examples = []
        videos = set()
        label_count = 0
        for review in reviews:
            for item in review.get("episode_map", []):
                label = (item.get("function") or "").strip()
                if not label or re.search(r"publisher|promotion|media|outro|advert|music tail|channel|inserted english", label, re.I):
                    continue
                if any(re.search(theme_pattern, label, re.I) for _, theme_pattern, _ in THEMES):
                    continue
                if not regex.search(label):
                    continue
                label_count += 1
                videos.add(review["video_id"])
                if len(examples) < 8:
                    examples.append(evidence_sample(item, review, "episode"))
        unmatched_clusters.append({
            "cluster_id": cluster_id,
            "matching_rule": pattern,
            "candidate_form": candidate_form,
            "label_hit_count": label_count,
            "video_count": len(videos),
            "examples": examples,
            "status": "unmatched_label_cluster_requires_semantic_review",
        })
    covered_labels = sum(1 for label in raw_labels if any(re.search(p, label, re.I) for _, p, _ in THEMES))
    covered_relations = sum(1 for label in raw_relations if any(re.search(p, label, re.I) for _, p, _ in THEMES))
    return {
        "schema_version": "1.0",
        "inventory_id": "exhaustive-corpus-pattern-discovery",
        "status": "all_review_records_mined_candidate_themes_unvalidated",
        "source": "research/full-context-reviews.json",
        "review_count": len(reviews),
        "episode_record_count": episode_total,
        "relation_record_count": relation_total,
        "distinct_episode_labels": len(raw_labels),
        "distinct_relation_types": len(raw_relations),
        "theme_count": len(themes),
        "relation_pattern_count": len(relation_patterns),
        "unmatched_cluster_count": len(unmatched_clusters),
        "coverage": {
            "episode_labels_with_keyword_theme_match": covered_labels,
            "relation_types_with_keyword_theme_match": covered_relations,
            "unmatched_episode_labels": len(raw_labels) - covered_labels,
            "unmatched_relation_types": len(raw_relations) - covered_relations,
        },
        "claim_boundary": "This inventory mines every full-context review record and links candidate themes to source review/evidence IDs. Keyword grouping is a discovery aid, not semantic validation, recurrence proof, delivery evidence, learner evidence, listener outcome evidence or effectiveness evidence.",
        "themes": sorted(themes, key=lambda x: (-(x["video_count"]), -(x["episode_hit_count"] + x["relation_hit_count"]), x["theme_id"])),
        "relation_patterns": sorted(relation_patterns, key=lambda x: (-x["relation_count"], x["relation_type"])),
        "unmatched_clusters": sorted(unmatched_clusters, key=lambda x: (-x["video_count"], -x["label_hit_count"], x["cluster_id"])),
        "unmatched_top_episode_labels": [{"label": k, "count": v} for k, v in raw_labels.most_common(100) if not any(re.search(p, k, re.I) for _, p, _ in THEMES)],
        "raw_label_counts": dict(raw_labels),
        "raw_relation_counts": dict(raw_relations),
    }


def render(report: dict) -> str:
    lines = [
        "# Exhaustive corpus pattern inventory",
        "",
        "Status: **all 395 full-context reviews mined; candidate themes remain unvalidated**.",
        "",
        report["claim_boundary"],
        "",
        f"Coverage: **{report['review_count']} reviews**, **{report['episode_record_count']:,} episode records**, **{report['relation_record_count']:,} relation records**, **{report['distinct_episode_labels']:,} distinct episode labels**, and **{report['distinct_relation_types']:,} relation types**.",
        "",
        "## Candidate themes",
        "",
        "Counts are source-linked discovery counts. A theme hit is a lead for contextual review, not a validated communication effect.",
        "",
        "| Theme | Videos | Episode hits | Relation hits | Candidate use |",
        "|---|---:|---:|---:|---|",
    ]
    for theme in report["themes"]:
        lines.append(f"| `{theme['theme_id']}` | {theme['video_count']} | {theme['episode_hit_count']} | {theme['relation_hit_count']} | {theme['candidate_form']} |")
    lines += ["", "## Source-linked examples", ""]
    for theme in report["themes"]:
        lines += [f"### `{theme['theme_id']}`", "", f"Candidate use: {theme['candidate_form']}", ""]
        for item in theme["examples"][:5]:
            label = item.get("label") or item.get("relation_type")
            claim = f" — {item['claim']}" if item.get("claim") else ""
            lines.append(f"- `{item['review_id']}` / `{item['video_id']}` / `{label}`{claim}; evidence: `{', '.join(item['evidence_ids'][:3])}`; [{item['writeup']}]({item['writeup']})")
        lines += ["", "Review the linked full-context writeup before converting this lead into a lesson or phrase form.", ""]
    lines += ["## Structural relation patterns", "", "These are the named relations recorded inside reviews. They are higher-level architecture leads and remain provisional until contextual and independent review.", "", "| Relation | Videos | Records | Candidate architecture |", "|---|---:|---:|---|"]
    for item in report["relation_patterns"]:
        lines.append(f"| `{item['relation_type']}` | {item['video_count']} | {item['relation_count']} | {item['candidate_form']} |")
    lines += ["", "### Source-linked relation examples", ""]
    for item in report["relation_patterns"]:
        if not item["examples"]:
            continue
        lines += [f"#### `{item['relation_type']}`", "", f"Candidate architecture: {item['candidate_form']}", ""]
        for example in item["examples"][:3]:
            lines.append(f"- `{example['review_id']}` / `{example['video_id']}` — {example['claim']}; evidence: `{', '.join(example['evidence_ids'][:3])}`; [{example['writeup']}]({example['writeup']})")
        lines.append("")
    lines += ["## Additional clusters from previously unmatched labels", "", "These clusters are deliberately separate from the 22 broad themes. They are discovery leads mined from labels that did not match the first taxonomy pass; they need semantic review before becoming new lesson cards.", "", "| Cluster | Videos | Label hits | Candidate architecture |", "|---|---:|---:|---|"]
    for item in report["unmatched_clusters"]:
        lines.append(f"| `{item['cluster_id']}` | {item['video_count']} | {item['label_hit_count']} | {item['candidate_form']} |")
    lines += ["", "### Source-linked unmatched-cluster examples", ""]
    for item in report["unmatched_clusters"]:
        if not item["examples"]:
            continue
        lines += [f"#### `{item['cluster_id']}`", "", f"Candidate architecture: {item['candidate_form']}", ""]
        for example in item["examples"][:3]:
            lines.append(f"- `{example['review_id']}` / `{example['video_id']}` — {example['label']}; evidence: `{', '.join(example['evidence_ids'][:3])}`; [{example['writeup']}]({example['writeup']})")
        lines.append("")
    lines += [
        "## Coverage gaps for the next mining pass", "",
        f"The keyword themes matched {report['coverage']['episode_labels_with_keyword_theme_match']} of {report['distinct_episode_labels']} distinct episode labels and {report['coverage']['relation_types_with_keyword_theme_match']} of {report['distinct_relation_types']} relation types. The remaining labels are retained in the JSON for a second semantic-clustering pass rather than being discarded.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    result = build()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(result))
    print(f"exhaustive pattern inventory: {result['review_count']} reviews, {result['theme_count']} candidate themes, {result['episode_record_count']} episode records")
