#!/usr/bin/env python3
"""Build the runnable learner-check form for candidate slice 02."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK_BANK = ROOT / "research/vertical-slice-02-learner-task-bank.json"
OUT = ROOT / "writeups/vertical-slice-02-learner-check.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def build_section(pattern_id: str, number: int, tasks: list[dict]) -> str:
    task_markup = []
    for task in tasks:
        field = f"p{number}_{task['task_id']}"
        task_markup.append(
            f'<div class="task"><strong>{esc(task["phase"])} — {esc(task["task_id"])}</strong>'
            f'<p><b>Stimulus:</b> {esc(task["stimulus"])}</p><p>{esc(task["prompt"])}</p>'
            f'<label>Response<textarea required name="{esc(field)}" rows="4"></textarea></label></div>'
        )
    ids = ",".join(task["task_id"] for task in tasks)
    return f"""
    <fieldset class="pattern"><legend>{number}. {esc(pattern_id)}</legend>
      <input type="hidden" name="p{number}_task_bank_ids" value="{esc(ids)}">
      {''.join(task_markup)}
      <label>Listener restatement<textarea required name="p{number}_listener_restatement" rows="3"></textarea></label>
      <label>Revision after feedback<textarea required name="p{number}_revision" rows="3"></textarea></label>
      <label>Boundary or safety note<textarea required name="p{number}_boundary_note" rows="3"></textarea></label>
    </fieldset>"""


def main() -> int:
    bank = json.loads(TASK_BANK.read_text())
    grouped: dict[str, list[dict]] = {}
    for task in bank["tasks"]:
        grouped.setdefault(task["pattern_id"], []).append(task)
    sections = "\n".join(
        build_section(pattern_id, number, tasks)
        for number, (pattern_id, tasks) in enumerate(grouped.items(), 1)
    )
    task_ids = [task["task_id"] for task in bank["tasks"]]
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vertical slice 02 learner check</title>
<style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#17202a}}
h1{{line-height:1.15}} fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1.5rem 0;padding:1rem}}
legend{{font-weight:700;padding:0 .4rem}} label{{display:block;margin:.75rem 0}} textarea{{display:block;width:100%;box-sizing:border-box;margin-top:.3rem}}
input[type=text],input[type=date]{{max-width:24rem;padding:.35rem}} button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0;cursor:pointer}}
.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}} .task{{background:#eef5fb;border-left:4px solid #39739d;padding:.6rem;margin:.7rem 0}}
#result{{white-space:pre-wrap;background:#f3f5f7;padding:1rem;display:none}}
</style></head><body>
<h1>Vertical slice 02 learner check</h1>
<div class="notice"><strong>Research boundary:</strong> This records teachability observations for three unvalidated candidate patterns. It does not test trust, memory, persuasion, engagement or action. Do not enter identifying personal stories or sensitive information. Written, typed, captioned and asynchronous responses are allowed.</div>
<form id="check">
<fieldset><legend>Session record</legend>
<label>Pseudonym or participant code<input required type="text" name="participant_code"></label>
<label>Date<input required type="date" name="date"></label>
<label>Lesson version<input required type="text" name="lesson_version" value="vertical-slice-02-draft"></label>
<label>Accessibility needs or modality<textarea name="accessibility" rows="2"></textarea></label>
<label><input required type="checkbox" name="consent"> I consent to this local research record being saved for the stated learner-check purpose.</label>
</fieldset>
{sections}
<fieldset><legend>Facilitator record</legend>
<label>Feedback given<textarea name="facilitator_feedback" rows="4"></textarea></label>
<label>Accommodations or unresolved disagreement<textarea name="facilitator_notes" rows="3"></textarea></label>
</fieldset>
<button type="button" id="download">Download JSON record</button><button type="reset">Clear form</button>
</form><pre id="result" aria-live="polite"></pre>
<script type="application/json" id="task-bank">{json.dumps(task_ids, ensure_ascii=False)}</script>
<script>
const form=document.querySelector('#check'), result=document.querySelector('#result');
document.querySelector('#download').addEventListener('click',()=>{{
  if(!form.reportValidity()) return;
  const data={{schema_version:'1.0',protocol_id:'vertical-slice-02-learner-check',record_type:'learner_observation',responses:{{}}}};
  for(const el of form.elements){{if(!el.name)continue;if(el.type==='checkbox')data.responses[el.name]=el.checked;else data.responses[el.name]=el.value;}}
  data.task_bank_ids=JSON.parse(document.querySelector('#task-bank').textContent);
  data.claim_boundary='Teachability observations only; not listener outcomes or communication-effectiveness evidence.';
  const blob=new Blob([JSON.stringify(data,null,2)+'\\n'],{{type:'application/json'}}),url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download='vertical-slice-02-learner-record-'+data.responses.participant_code+'.json';a.click();URL.revokeObjectURL(url);
  result.style.display='block';result.textContent='Record prepared for download. Keep the participant code non-identifying.';
}});
</script></body></html>"""
    OUT.write_text(document)
    print(f"wrote {OUT.relative_to(ROOT)} with {len(bank['tasks'])} fixed tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
