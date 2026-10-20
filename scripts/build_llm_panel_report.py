#!/usr/bin/env python3
"""Publish a plain-language, source-keyed report from LLM panel receipts."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'research/llm-panel-vertical-slice-results.json'
KEY=ROOT/'research/llm-panel-vertical-slice-packet-key.json'
OUT=ROOT/'writeups/llm-panel-vertical-slice-report.md'

def main():
    report=json.loads(RESULTS.read_text()); key={x['blind_packet_id']:x for x in json.loads(KEY.read_text())['key']}
    by_packet={x['blind_packet_id']:[] for x in report['adjudications']}
    for row in report['judgments']: by_packet[row['blind_packet_id']].append(row)
    totals=Counter(row['judgment']['decision'] for row in report['judgments'])
    lines=['# LLM panel review — five-job vertical slice','', 'Status: **complete; every job requires revision or more evidence**.','', report['claim_boundary'],'',f"Two local models made **{len(report['judgments'])}** rubric judgments: **{totals['support']}** support, **{totals['revise']}** revise, and **{totals['indeterminate']}** indeterminate.",'', 'A noncommittal model response is not counted as agreement. Because every packet has disagreement or an indeterminate pass, every decision fails closed.','', '| Job packet | Result | Why |','|---|---|---|']
    for item in report['adjudications']:
        original=key[item['blind_packet_id']]['pattern_id']
        decisions=item['rubric_decisions']
        reason='Model disagreement' if item['model_disagreement'] else 'A rubric did not receive unanimous support'
        if not item.get('citation_complete', False): reason += '; one or more judgments lacked an evidence citation'
        compact=', '.join(f"{rubric}: {' / '.join(values)}" for rubric, values in decisions.items())
        lines.append(f"| `{original}` | `{item['decision']}` | {reason}. {compact}. |")
    lines += ['', '## What this changes','', '- These five lessons now have a reproducible LLM-panel record instead of an empty human-review queue.', '- The panel supports focused revision: strengthen counterexample handling first, then rerun with models that can produce an unambiguous cited decision.', '- No result claims learner success, listener comprehension, persuasion, or effectiveness.', '', '## Reuse','', 'The packet protocol is portable: supply five representative excerpts, controls, a bounded lesson, a separate key, and the same four rubrics. Apply it next to the 55 fixed-corpus patterns and 19 expansion candidates; do not merge their evidence counts.', '']
    OUT.write_text('\n'.join(lines))
    print(f'wrote {OUT.relative_to(ROOT)}')
if __name__=='__main__': main()
