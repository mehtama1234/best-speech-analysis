#!/usr/bin/env python3
"""Resolve curated synthesis links to existing source-bound observations."""
import hashlib
import json
from pathlib import Path
if __package__:
    from .review_evidence import context_digest
else:
    from review_evidence import context_digest


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(ref, reviews, source):
    review = reviews[ref["review_id"]]
    if type(ref["observation_index"]) is not int or ref["observation_index"] < 0:
        raise ValueError("Observation index must be a nonnegative integer")
    observation = review["observations"][ref["observation_index"]]
    rows = [source[eid] for eid in observation["evidence_ids"]]
    if not rows or not set(observation["evidence_ids"]) <= set(review["context_evidence_ids"]):
        raise ValueError("Observation outside inspected context")
    core = set(review["core_evidence_ids"])
    start, end = min(r["start_seconds"] for r in rows), max(r["end_seconds"] for r in rows)
    return {**ref, **observation, "passage_id": review["passage_id"],
            "video_id": rows[0]["video_id"], "start_seconds": start, "end_seconds": end,
            "url": f"https://www.youtube.com/watch?v={rows[0]['video_id']}&t={int(start)}",
            "sampled_core_overlap_count": len(set(observation["evidence_ids"]) & core),
            "context_only_count": len(set(observation["evidence_ids"]) - core),
            "format_evidence": review["format_evidence"], "writeup": review["writeup"]}


def main():
    root = Path(__file__).resolve().parents[1]
    spec_path = root / "research/passage-synthesis-spec.json"
    reviews_path = root / "research/passage-context-reviews.json"
    registry_path = root / "research/segment-registry.jsonl"
    spec = json.loads(spec_path.read_text())
    reviews = {r["review_id"]: r for r in json.loads(reviews_path.read_text())["reviews"]}
    needed = {e for r in reviews.values() for e in r["context_evidence_ids"]}
    source = {}
    with registry_path.open() as stream:
        for line in stream:
            r = json.loads(line)
            if r["evidence_id"] in needed:
                source[r["evidence_id"]] = r
    for review in reviews.values():
        if context_digest([source[e] for e in review["context_evidence_ids"]]) != review["context_sha256"]:
            raise ValueError("Stale passage review: " + review["review_id"])
    cards = []
    for card in spec["cards"]:
        resolved = {**card}
        for kind in ("supports", "contrasts"):
            resolved[kind] = [resolve(ref, reviews, source) for ref in card[kind]]
        resolved["linked_support_video_count"] = len({r["video_id"] for r in resolved["supports"]})
        resolved["speaker_recurrence"] = "not established; videos are not independent speakers"
        resolved["delivery_effect"] = "not measured"
        cards.append(resolved)
    inputs = (spec_path, reviews_path, registry_path, Path(__file__).resolve(), root / "scripts/review_evidence.py")
    core_count = len({e for r in reviews.values() for e in r["core_evidence_ids"]})
    context_count = len(needed)
    report = {"schema_version": "1.0", "policy": spec["policy"], "status": spec["status"],
              "reviewed_passages": len(reviews), "reviewed_core_captions": core_count,
              "inspected_context_captions": context_count, "cards": cards,
              "source_sha256": {str(p.relative_to(root)): digest(p) for p in inputs}}
    (root / "research/passage-synthesis.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    lines = ["# What the 24-passage sample suggests", "", spec["policy"], "",
             "The useful unit is a relationship between statements: an example leading to a claim, "
             "a question and its answer, an earlier image revisited, or a later sentence reversing an opening. "
             "These six comparisons are hypotheses and analytical distinctions, not six proven best practices.", "",
             f"The reviewed sample contains {core_count:,} core captions across {len(reviews)} passages, with {context_count:,} inspected context captions. "
             "Selection was label-independent; synthesis was interpretive and unblinded. No speaker-independent rates, "
             "causal benefits or complete-transcript coverage are inferred. Evidence links can include expanded context outside the sampled core; counts below expose this.", ""]
    for c in cards:
        lines += [f"## {c['title']}", "", c["mechanism"], "",
                  f"Linked supporting videos: {c['linked_support_video_count']} (curated examples, not prevalence).", ""]
        for kind, title in (("supports", "Supporting comparisons"), ("contrasts", "Contrasts and boundary cases")):
            lines += [f"### {title}", ""]
            for r in c[kind]:
                lines.append(f"- [{r['function'].replace('_', ' ')}]({r['url']}) — {r['reason']} "
                             f"Evidence `{r['evidence_ids'][0]}` through `{r['evidence_ids'][-1]}`; "
                             f"{r['sampled_core_overlap_count']} core / {r['context_only_count']} expanded-context captions.")
            lines.append("")
        lines += ["**Limit:** " + c["limit"], "", "**Proposed exercise:** " + c["exercise"], "",
                  "**Next test, not yet performed:** " + c["test"], ""]
    lines += ["## Shared evidence boundaries", "",
              "Source assertions about politics, health, law, finance, biography and scientific history are not independently verified. "
              "The analyses do not endorse harmful appeals or fabricated premises. Quoted advice, fictional speech, publisher framing, "
              "reported experience and current speaker claims must remain distinct. Captioned laughter, music and self-described emotion are not acoustic or visual validation.", "",
              "## Next research step", "",
              "Freeze these definitions before new sampling. Annotate complete episodes with speaker/format and source-boundary checks, "
              "record disagreement, and select matched counterexamples. Localized audio/video can then test whether delivery marks the identified transitions. "
              "Do not retrofit the seven unresolved legacy pause judgments or treat these cards as replacements for the broader corpus goal.", ""]
    (root / "writeups/passage-synthesis.md").write_text("\n".join(lines))
    print(json.dumps({"cards": len(cards), "reviewed_passages": len(reviews),
                      "linked_videos": {c["id"]: c["linked_support_video_count"] for c in cards}}))


if __name__ == "__main__":
    main()
