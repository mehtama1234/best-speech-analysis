#!/usr/bin/env python3
"""Build a local, backend-free learner-check form from the research protocol."""
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/vertical-slice-01-learner-check.json"
TASK_BANK = ROOT / "research/vertical-slice-01-learner-task-bank.json"
OUT = ROOT / "writeups/vertical-slice-01-learner-check.html"


def esc(value):
    return html.escape(str(value), quote=True)


def pattern_section(pattern, number, tasks):
    checks = "".join(
        f'<label><input type="checkbox" name="p{number}_self_check_{index}"> {esc(item)}</label>'
        for index, item in enumerate(pattern["self_check"], 1)
    )
    task_markup = "".join(
        f'<div class="task"><strong>{esc(task["phase"])} — {esc(task["task_id"])}</strong><p>{esc(task["prompt"])}</p></div>'
        for task in tasks
    )
    task_ids = ",".join(task["task_id"] for task in tasks)
    return f"""
    <fieldset class="pattern">
      <legend>{number}. {esc(pattern['pattern_id'])}</legend>
      <input type="hidden" name="p{number}_task_bank_ids" value="{esc(task_ids)}">
      <p><strong>Recognition task:</strong> {esc(pattern['recognition_task'])}</p>
      <div class="task-bank"><strong>Fixed stimuli shown in this section</strong>{task_markup}</div>
      <label>Baseline response<textarea name="p{number}_baseline" rows="4"></textarea></label>
      <label>New-example / transfer response<textarea name="p{number}_transfer" rows="4"></textarea></label>
      <label>Misuse or non-fit judgment<textarea name="p{number}_non_fit" rows="3"></textarea></label>
      <label>Matched plain-communication control response<textarea name="p{number}_control" rows="3"></textarea></label>
      <label>Second-listener restatement<textarea name="p{number}_listener" rows="3"></textarea></label>
      <label>Revision after feedback<textarea name="p{number}_revision" rows="4"></textarea></label>
      <div class="checks"><strong>Self-check</strong>{checks}</div>
      <div class="scores">
        <label>Transfer score (0–2)<input type="number" name="p{number}_transfer_score" min="0" max="2"></label>
        <label>Boundary score (0–2)<input type="number" name="p{number}_boundary_score" min="0" max="2"></label>
        <label>Listener-restatement score (0–2)<input type="number" name="p{number}_listener_score" min="0" max="2"></label>
      </div>
    </fieldset>"""


def build():
    protocol = json.loads(PROTOCOL.read_text())
    task_bank = json.loads(TASK_BANK.read_text())
    tasks_by_pattern = {}
    for task in task_bank["tasks"]:
        tasks_by_pattern.setdefault(task["pattern_id"], []).append(task)
    sections = "\n".join(
        pattern_section(pattern, number, tasks_by_pattern[pattern["pattern_id"]])
        for number, pattern in enumerate(protocol["patterns"], 1)
    )
    protocol_json = json.dumps(protocol, ensure_ascii=False).replace("</", "<\\/")
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vertical slice 01 learner check</title>
<style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#17202a}}
h1{{line-height:1.15}} fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1.5rem 0;padding:1rem}}
legend{{font-weight:700;padding:0 .4rem}} label{{display:block;margin:.75rem 0}} textarea{{display:block;width:100%;box-sizing:border-box;margin-top:.3rem}}
input[type=text],input[type=date],input[type=number]{{max-width:24rem;padding:.35rem}} button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0;cursor:pointer}}
.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}} .checks label{{margin:.25rem 0}}
.scores{{display:flex;gap:1rem;flex-wrap:wrap}} .scores label{{margin:.5rem 0}}
#result{{white-space:pre-wrap;background:#f3f5f7;padding:1rem;display:none}}
.task-bank{{background:#eef5fb;border-left:4px solid #39739d;padding:.6rem;margin:.8rem 0}} .task{{background:white;padding:.45rem;margin:.45rem 0}}
</style></head><body>
<h1>Vertical slice 01 learner check</h1>
<div class="notice"><strong>Research boundary:</strong> This local form records teachability observations only. It does not test trust, memory, persuasion, engagement or action. Do not enter identifying personal stories or sensitive information.</div>
<form id="check">
<fieldset><legend>Session record</legend>
<label>Pseudonym or participant code<input required type="text" name="participant_code"></label>
<label>Date<input required type="date" name="date"></label>
<label>Lesson version<input required type="text" name="lesson_version" value="vertical-slice-01-draft"></label>
<label>Accessibility needs or modality<textarea name="accessibility" rows="2"></textarea></label>
<label><input required type="checkbox" name="consent"> I consent to this local research record being saved for the stated learner-check purpose.</label>
</fieldset>
{sections}
<fieldset><legend>Facilitator record</legend>
<label>Feedback given<textarea name="facilitator_feedback" rows="4"></textarea></label>
<label>Facilitator changes or accommodations<textarea name="facilitator_changes" rows="3"></textarea></label>
<label>Unresolved disagreement<textarea name="unresolved_disagreement" rows="3"></textarea></label>
</fieldset>
<button type="button" id="download">Download JSON record</button>
<button type="reset">Clear form</button>
</form><pre id="result" aria-live="polite"></pre>
<script type="application/json" id="protocol">{protocol_json}</script>
<script>
const form=document.querySelector('#check'), result=document.querySelector('#result');
document.querySelector('#download').addEventListener('click',()=>{{
  if(!form.reportValidity()) return;
  const data={{schema_version:'1.0',protocol_id:'vertical-slice-01-learner-check',record_type:'learner_observation',responses:{{}}}};
  for(const el of form.elements){{ if(!el.name) continue; if(el.type==='checkbox') data.responses[el.name]=el.checked; else data.responses[el.name]=el.value; }}
  data.claim_boundary='Teachability observations only; not listener outcomes.';
  const blob=new Blob([JSON.stringify(data,null,2)+'\\n'],{{type:'application/json'}}), url=URL.createObjectURL(blob), a=document.createElement('a');
  a.href=url; a.download='vertical-slice-01-learner-record-'+data.responses.participant_code+'.json'; a.click(); URL.revokeObjectURL(url);
  result.style.display='block'; result.textContent='Record prepared for download. Keep the participant code non-identifying.';
}});
</script></body></html>"""
    OUT.write_text(document)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
