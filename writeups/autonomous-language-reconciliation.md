# Autonomous language reconciliation

Status: **internal phrase and recurrence reconciliation complete; not independent validation**.

This report reconciles the exact phrase inventory and recurrence-review queue against retained transcript text. It does not establish independent agreement, speaker intent, function, delivery meaning, effectiveness or listener outcomes.

The report covers **50 exact phrase forms** and **192 recurrence candidates**.

## Phrase-form inventory

| Form | Family | Occurrences | Videos | Train | Holdout | Mechanism status |
|---|---|---:|---:|---:|---:|---|
| `don't` | `call_to_action` | 2234 | 326 | 268 | 58 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `you can` | `call_to_action` | 702 | 225 | 196 | 29 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `let's` | `call_to_action` | 417 | 168 | 141 | 27 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `do not` | `call_to_action` | 159 | 83 | 68 | 15 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `we need to` | `call_to_action` | 148 | 70 | 58 | 12 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `join us` | `call_to_action` | 29 | 28 | 21 | 7 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `take action` | `call_to_action` | 9 | 7 | 5 | 2 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `so the` | `conclusion_or_summary` | 106 | 63 | 52 | 11 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `ultimately` | `conclusion_or_summary` | 48 | 39 | 34 | 5 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `the point is` | `conclusion_or_summary` | 13 | 11 | 9 | 2 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `what matters` | `conclusion_or_summary` | 13 | 11 | 8 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `in short` | `conclusion_or_summary` | 9 | 9 | 7 | 2 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `the lesson` | `conclusion_or_summary` | 5 | 3 | 3 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `in conclusion` | `conclusion_or_summary` | 3 | 3 | 3 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `but` | `contrast_or_disagreement` | 5039 | 374 | 309 | 65 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `used to` | `contrast_or_disagreement` | 214 | 105 | 87 | 18 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `now i` | `contrast_or_disagreement` | 151 | 98 | 87 | 11 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `instead` | `contrast_or_disagreement` | 118 | 86 | 70 | 16 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `however` | `contrast_or_disagreement` | 71 | 54 | 45 | 9 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `rather than` | `contrast_or_disagreement` | 58 | 48 | 40 | 8 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `on the other hand` | `contrast_or_disagreement` | 7 | 7 | 7 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `is when` | `definition` | 32 | 26 | 22 | 4 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `means that` | `definition` | 23 | 19 | 16 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `in other words` | `definition` | 18 | 14 | 11 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `what i mean` | `definition` | 14 | 14 | 13 | 1 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `the definition` | `definition` | 8 | 6 | 4 | 2 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `defined as` | `definition` | 1 | 1 | 1 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `for example` | `example` | 67 | 42 | 37 | 5 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `such as` | `example` | 36 | 26 | 23 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `for instance` | `example` | 18 | 15 | 12 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `one example` | `example` | 8 | 6 | 3 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `?` | `question` | 2709 | 219 | 183 | 36 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `how` | `question` | 1905 | 325 | 267 | 58 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `why` | `question` | 894 | 246 | 207 | 39 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `can we` | `question` | 63 | 41 | 38 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `what if` | `question` | 29 | 16 | 13 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `i was` | `story_or_personal_experience` | 1621 | 255 | 213 | 42 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `when i` | `story_or_personal_experience` | 766 | 245 | 203 | 42 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `years ago` | `story_or_personal_experience` | 180 | 107 | 88 | 19 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `i remember` | `story_or_personal_experience` | 125 | 77 | 65 | 12 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `one day` | `story_or_personal_experience` | 109 | 72 | 56 | 16 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `my first` | `story_or_personal_experience` | 96 | 69 | 60 | 9 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `growing up` | `story_or_personal_experience` | 40 | 32 | 29 | 3 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `i think` | `uncertainty_or_qualification` | 1436 | 214 | 177 | 37 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `maybe` | `uncertainty_or_qualification` | 382 | 159 | 132 | 27 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `perhaps` | `uncertainty_or_qualification` | 91 | 65 | 52 | 13 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `i'm not sure` | `uncertainty_or_qualification` | 16 | 15 | 15 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `it depends` | `uncertainty_or_qualification` | 12 | 11 | 9 | 2 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `not necessarily` | `uncertainty_or_qualification` | 5 | 5 | 5 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |
| `to some extent` | `uncertainty_or_qualification` | 2 | 2 | 2 | 0 | `exact_retrieval_form_reconciled_not_validated_best_practice` |

Families: `call_to_action`=7; `conclusion_or_summary`=7; `contrast_or_disagreement`=7; `definition`=6; `example`=4; `question`=5; `story_or_personal_experience`=7; `uncertainty_or_qualification`=7

## Recurrence candidates

Internal context checks: `candidate_form_visible_in_retained_text`=156; `pattern_not_reproduced_check_registry`=36.

| Candidate | Family | Split | Evidence | Matched form(s) | Internal check |
|---|---|---|---|---|---|
| `contrast_or_disagreement:-54zUwySKCg:00023` | `contrast_or_disagreement` | `train` | [-54zUwySKCg:00023](https://www.youtube.com/watch?v=-54zUwySKCg) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:-6qN3bm2RYo:00162` | `contrast_or_disagreement` | `train` | [-6qN3bm2RYo:00162](https://www.youtube.com/watch?v=-6qN3bm2RYo) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:-HA8kSdsf_M:00001` | `contrast_or_disagreement` | `train` | [-HA8kSdsf_M:00001](https://www.youtube.com/watch?v=-HA8kSdsf_M) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:-URn1fARvts:00023` | `contrast_or_disagreement` | `train` | [-URn1fARvts:00023](https://www.youtube.com/watch?v=-URn1fARvts) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:-Unkvng_jp8:00000` | `contrast_or_disagreement` | `train` | [-Unkvng_jp8:00000](https://www.youtube.com/watch?v=-Unkvng_jp8) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:-s-h-eebSgw:00053` | `contrast_or_disagreement` | `train` | [-s-h-eebSgw:00053](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:0KFVLWX7eEY:00019` | `contrast_or_disagreement` | `train` | [0KFVLWX7eEY:00019](https://www.youtube.com/watch?v=0KFVLWX7eEY) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:0eNEz2lhyk8:00059` | `contrast_or_disagreement` | `train` | [0eNEz2lhyk8:00059](https://www.youtube.com/watch?v=0eNEz2lhyk8) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:0kjuI8M3NHk:00025` | `contrast_or_disagreement` | `train` | [0kjuI8M3NHk:00025](https://www.youtube.com/watch?v=0kjuI8M3NHk) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:0nUDkCgyppM:00016` | `contrast_or_disagreement` | `train` | [0nUDkCgyppM:00016](https://www.youtube.com/watch?v=0nUDkCgyppM) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:19rhQUB_FQc:00016` | `contrast_or_disagreement` | `train` | [19rhQUB_FQc:00016](https://www.youtube.com/watch?v=19rhQUB_FQc) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:1DXo2fcfleY:00007` | `contrast_or_disagreement` | `train` | [1DXo2fcfleY:00007](https://www.youtube.com/watch?v=1DXo2fcfleY) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:1Bc3LkP7dh8:00033` | `contrast_or_disagreement` | `holdout` | [1Bc3LkP7dh8:00033](https://www.youtube.com/watch?v=1Bc3LkP7dh8) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:1crhwQPKr7w:00001` | `contrast_or_disagreement` | `holdout` | [1crhwQPKr7w:00001](https://www.youtube.com/watch?v=1crhwQPKr7w) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:2fWJh-_UG5s:00013` | `contrast_or_disagreement` | `holdout` | [2fWJh-_UG5s:00013](https://www.youtube.com/watch?v=2fWJh-_UG5s) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:2mqQMA7CSLQ:00018` | `contrast_or_disagreement` | `holdout` | [2mqQMA7CSLQ:00018](https://www.youtube.com/watch?v=2mqQMA7CSLQ) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:3AIoHLr8nTI:00019` | `contrast_or_disagreement` | `holdout` | [3AIoHLr8nTI:00019](https://www.youtube.com/watch?v=3AIoHLr8nTI) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:3l0_J20c4dI:00004` | `contrast_or_disagreement` | `holdout` | [3l0_J20c4dI:00004](https://www.youtube.com/watch?v=3l0_J20c4dI) | `\bused to\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:5xRv-eOuras:00020` | `contrast_or_disagreement` | `holdout` | [5xRv-eOuras:00020](https://www.youtube.com/watch?v=5xRv-eOuras) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:65v4EyR774E:00020` | `contrast_or_disagreement` | `holdout` | [65v4EyR774E:00020](https://www.youtube.com/watch?v=65v4EyR774E) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:69vFAHLkAlI:00028` | `contrast_or_disagreement` | `holdout` | [69vFAHLkAlI:00028](https://www.youtube.com/watch?v=69vFAHLkAlI) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:74ZgwDcjeGc:00033` | `contrast_or_disagreement` | `holdout` | [74ZgwDcjeGc:00033](https://www.youtube.com/watch?v=74ZgwDcjeGc) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:7iHNwOAr-9E:00002` | `contrast_or_disagreement` | `holdout` | [7iHNwOAr-9E:00002](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `contrast_or_disagreement:AwA0Jnfj3ao:00022` | `contrast_or_disagreement` | `holdout` | [AwA0Jnfj3ao:00022](https://www.youtube.com/watch?v=AwA0Jnfj3ao) | `\bbut\b` | `candidate_form_visible_in_retained_text` |
| `example:-6qN3bm2RYo:00079` | `example` | `train` | [-6qN3bm2RYo:00079](https://www.youtube.com/watch?v=-6qN3bm2RYo) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:-URn1fARvts:00249` | `example` | `train` | [-URn1fARvts:00249](https://www.youtube.com/watch?v=-URn1fARvts) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:0eNEz2lhyk8:00119` | `example` | `train` | [0eNEz2lhyk8:00119](https://www.youtube.com/watch?v=0eNEz2lhyk8) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:1i9kcBHX2Nw:00045` | `example` | `train` | [1i9kcBHX2Nw:00045](https://www.youtube.com/watch?v=1i9kcBHX2Nw) | `\bone example\b` | `candidate_form_visible_in_retained_text` |
| `example:2wf1qE7AC8Y:00007` | `example` | `train` | [2wf1qE7AC8Y:00007](https://www.youtube.com/watch?v=2wf1qE7AC8Y) | `\bfor example\b` | `candidate_form_visible_in_retained_text` |
| `example:3TWYqYJqU8U:00264` | `example` | `train` | [3TWYqYJqU8U:00264](https://www.youtube.com/watch?v=3TWYqYJqU8U) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:3x4zM7O8pZI:00064` | `example` | `train` | [3x4zM7O8pZI:00064](https://www.youtube.com/watch?v=3x4zM7O8pZI) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:4u71aIcrxtQ:00139` | `example` | `train` | [4u71aIcrxtQ:00139](https://www.youtube.com/watch?v=4u71aIcrxtQ) | `\bfor instance\b` | `candidate_form_visible_in_retained_text` |
| `example:7XO7kVaEgpM:00018` | `example` | `train` | [7XO7kVaEgpM:00018](https://www.youtube.com/watch?v=7XO7kVaEgpM) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:7zUUV8_CY2M:00655` | `example` | `train` | [7zUUV8_CY2M:00655](https://www.youtube.com/watch?v=7zUUV8_CY2M) | `\bone example\b` | `candidate_form_visible_in_retained_text` |
| `example:9FVVUMTVch8:00029` | `example` | `train` | [9FVVUMTVch8:00029](https://www.youtube.com/watch?v=9FVVUMTVch8) | `\bfor instance\b` | `candidate_form_visible_in_retained_text` |
| `example:9MLd7kt2lKQ:00157` | `example` | `train` | [9MLd7kt2lKQ:00157](https://www.youtube.com/watch?v=9MLd7kt2lKQ) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:74ZgwDcjeGc:00009` | `example` | `holdout` | [74ZgwDcjeGc:00009](https://www.youtube.com/watch?v=74ZgwDcjeGc) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:7iHNwOAr-9E:00105` | `example` | `holdout` | [7iHNwOAr-9E:00105](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bfor example\b` | `candidate_form_visible_in_retained_text` |
| `example:KtjaB1SnA7Y:00294` | `example` | `holdout` | [KtjaB1SnA7Y:00294](https://www.youtube.com/watch?v=KtjaB1SnA7Y) | `\bfor example\b` | `candidate_form_visible_in_retained_text` |
| `example:PvcLdCo03TM:00394` | `example` | `holdout` | [PvcLdCo03TM:00394](https://www.youtube.com/watch?v=PvcLdCo03TM) | `\bone example\b` | `candidate_form_visible_in_retained_text` |
| `example:aHXxveJTJoE:00044` | `example` | `holdout` | [aHXxveJTJoE:00044](https://www.youtube.com/watch?v=aHXxveJTJoE) | `\bfor instance\b` | `candidate_form_visible_in_retained_text` |
| `example:aXmM0VZv810:00274` | `example` | `holdout` | [aXmM0VZv810:00274](https://www.youtube.com/watch?v=aXmM0VZv810) | `\bfor example\b` | `candidate_form_visible_in_retained_text` |
| `example:gVRlg4BXKVo:00035` | `example` | `holdout` | [gVRlg4BXKVo:00035](https://www.youtube.com/watch?v=gVRlg4BXKVo) | `\bfor example\b` | `candidate_form_visible_in_retained_text` |
| `example:jxY2-YgAgm0:00087` | `example` | `holdout` | [jxY2-YgAgm0:00087](https://www.youtube.com/watch?v=jxY2-YgAgm0) | `\bsuch as\b` | `candidate_form_visible_in_retained_text` |
| `example:l2ojUrbq8EM:00104` | `example` | `holdout` | [l2ojUrbq8EM:00104](https://www.youtube.com/watch?v=l2ojUrbq8EM) | `\bfor example\b` | `candidate_form_visible_in_retained_text` |
| `example:ttGQj3yCFYA:00108` | `example` | `holdout` | [ttGQj3yCFYA:00108](https://www.youtube.com/watch?v=ttGQj3yCFYA) | `\bfor instance\b` | `candidate_form_visible_in_retained_text` |
| `example:x45lP81Pmq8:00273` | `example` | `holdout` | [x45lP81Pmq8:00273](https://www.youtube.com/watch?v=x45lP81Pmq8) | `\bone example\b` | `candidate_form_visible_in_retained_text` |
| `example:yjo8chlSbQE:00053` | `example` | `holdout` | [yjo8chlSbQE:00053](https://www.youtube.com/watch?v=yjo8chlSbQE) | `\bone example\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:-54zUwySKCg:00021` | `story_or_personal_experience` | `train` | [-54zUwySKCg:00021](https://www.youtube.com/watch?v=-54zUwySKCg) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:-URn1fARvts:00158` | `story_or_personal_experience` | `train` | [-URn1fARvts:00158](https://www.youtube.com/watch?v=-URn1fARvts) | `\bmy first\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:-Unkvng_jp8:00017` | `story_or_personal_experience` | `train` | [-Unkvng_jp8:00017](https://www.youtube.com/watch?v=-Unkvng_jp8) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:-s-h-eebSgw:00020` | `story_or_personal_experience` | `train` | [-s-h-eebSgw:00020](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\bwhen I\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:0eNEz2lhyk8:00000` | `story_or_personal_experience` | `train` | [0eNEz2lhyk8:00000](https://www.youtube.com/watch?v=0eNEz2lhyk8) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:0kjuI8M3NHk:00000` | `story_or_personal_experience` | `train` | [0kjuI8M3NHk:00000](https://www.youtube.com/watch?v=0kjuI8M3NHk) | `\byears ago\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:0nUDkCgyppM:00133` | `story_or_personal_experience` | `train` | [0nUDkCgyppM:00133](https://www.youtube.com/watch?v=0nUDkCgyppM) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:19rhQUB_FQc:00008` | `story_or_personal_experience` | `train` | [19rhQUB_FQc:00008](https://www.youtube.com/watch?v=19rhQUB_FQc) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:1DXo2fcfleY:00014` | `story_or_personal_experience` | `train` | [1DXo2fcfleY:00014](https://www.youtube.com/watch?v=1DXo2fcfleY) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:1QvLB4yEHsI:00020` | `story_or_personal_experience` | `train` | [1QvLB4yEHsI:00020](https://www.youtube.com/watch?v=1QvLB4yEHsI) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:1TAuuyvIZjA:00081` | `story_or_personal_experience` | `train` | [1TAuuyvIZjA:00081](https://www.youtube.com/watch?v=1TAuuyvIZjA) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:1c4QHf5Ul3c:00037` | `story_or_personal_experience` | `train` | [1c4QHf5Ul3c:00037](https://www.youtube.com/watch?v=1c4QHf5Ul3c) | `\byears ago\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:1Bc3LkP7dh8:00283` | `story_or_personal_experience` | `holdout` | [1Bc3LkP7dh8:00283](https://www.youtube.com/watch?v=1Bc3LkP7dh8) | `\byears ago\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:2fWJh-_UG5s:00091` | `story_or_personal_experience` | `holdout` | [2fWJh-_UG5s:00091](https://www.youtube.com/watch?v=2fWJh-_UG5s) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:2mqQMA7CSLQ:00019` | `story_or_personal_experience` | `holdout` | [2mqQMA7CSLQ:00019](https://www.youtube.com/watch?v=2mqQMA7CSLQ) | `\bmy first\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:3AIoHLr8nTI:00009` | `story_or_personal_experience` | `holdout` | [3AIoHLr8nTI:00009](https://www.youtube.com/watch?v=3AIoHLr8nTI) | `\bwhen I\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:5xRv-eOuras:00184` | `story_or_personal_experience` | `holdout` | [5xRv-eOuras:00184](https://www.youtube.com/watch?v=5xRv-eOuras) | `\bwhen I\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:65v4EyR774E:00044` | `story_or_personal_experience` | `holdout` | [65v4EyR774E:00044](https://www.youtube.com/watch?v=65v4EyR774E) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:69vFAHLkAlI:00004` | `story_or_personal_experience` | `holdout` | [69vFAHLkAlI:00004](https://www.youtube.com/watch?v=69vFAHLkAlI) | `\byears ago\b` | `candidate_form_visible_in_retained_text` |
| `story_or_personal_experience:74ZgwDcjeGc:00020` | `story_or_personal_experience` | `holdout` | [74ZgwDcjeGc:00020](https://www.youtube.com/watch?v=74ZgwDcjeGc) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:7iHNwOAr-9E:00051` | `story_or_personal_experience` | `holdout` | [7iHNwOAr-9E:00051](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bwhen I\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:AwA0Jnfj3ao:00006` | `story_or_personal_experience` | `holdout` | [AwA0Jnfj3ao:00006](https://www.youtube.com/watch?v=AwA0Jnfj3ao) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:C8-twwwTETE:00005` | `story_or_personal_experience` | `holdout` | [C8-twwwTETE:00005](https://www.youtube.com/watch?v=C8-twwwTETE) | `\bwhen I\b` | `pattern_not_reproduced_check_registry` |
| `story_or_personal_experience:DY2s25yRa3M:00008` | `story_or_personal_experience` | `holdout` | [DY2s25yRa3M:00008](https://www.youtube.com/watch?v=DY2s25yRa3M) | `\bI was\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:-54zUwySKCg:00188` | `uncertainty_or_qualification` | `train` | [-54zUwySKCg:00188](https://www.youtube.com/watch?v=-54zUwySKCg) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:-Unkvng_jp8:00036` | `uncertainty_or_qualification` | `train` | [-Unkvng_jp8:00036](https://www.youtube.com/watch?v=-Unkvng_jp8) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:-s-h-eebSgw:00256` | `uncertainty_or_qualification` | `train` | [-s-h-eebSgw:00256](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:0eNEz2lhyk8:00044` | `uncertainty_or_qualification` | `train` | [0eNEz2lhyk8:00044](https://www.youtube.com/watch?v=0eNEz2lhyk8) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:0kjuI8M3NHk:00008` | `uncertainty_or_qualification` | `train` | [0kjuI8M3NHk:00008](https://www.youtube.com/watch?v=0kjuI8M3NHk) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:0nUDkCgyppM:00000` | `uncertainty_or_qualification` | `train` | [0nUDkCgyppM:00000](https://www.youtube.com/watch?v=0nUDkCgyppM) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:19rhQUB_FQc:00024` | `uncertainty_or_qualification` | `train` | [19rhQUB_FQc:00024](https://www.youtube.com/watch?v=19rhQUB_FQc) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:1DXo2fcfleY:00007` | `uncertainty_or_qualification` | `train` | [1DXo2fcfleY:00007](https://www.youtube.com/watch?v=1DXo2fcfleY) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:1QvLB4yEHsI:00095` | `uncertainty_or_qualification` | `train` | [1QvLB4yEHsI:00095](https://www.youtube.com/watch?v=1QvLB4yEHsI) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:1TAuuyvIZjA:00005` | `uncertainty_or_qualification` | `train` | [1TAuuyvIZjA:00005](https://www.youtube.com/watch?v=1TAuuyvIZjA) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:1c4QHf5Ul3c:00050` | `uncertainty_or_qualification` | `train` | [1c4QHf5Ul3c:00050](https://www.youtube.com/watch?v=1c4QHf5Ul3c) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:1gK42jcb_WM:00031` | `uncertainty_or_qualification` | `train` | [1gK42jcb_WM:00031](https://www.youtube.com/watch?v=1gK42jcb_WM) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:1Bc3LkP7dh8:00480` | `uncertainty_or_qualification` | `holdout` | [1Bc3LkP7dh8:00480](https://www.youtube.com/watch?v=1Bc3LkP7dh8) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:2fWJh-_UG5s:00055` | `uncertainty_or_qualification` | `holdout` | [2fWJh-_UG5s:00055](https://www.youtube.com/watch?v=2fWJh-_UG5s) | `\bperhaps\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:2mqQMA7CSLQ:00070` | `uncertainty_or_qualification` | `holdout` | [2mqQMA7CSLQ:00070](https://www.youtube.com/watch?v=2mqQMA7CSLQ) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:3AIoHLr8nTI:00004` | `uncertainty_or_qualification` | `holdout` | [3AIoHLr8nTI:00004](https://www.youtube.com/watch?v=3AIoHLr8nTI) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:3l0_J20c4dI:00003` | `uncertainty_or_qualification` | `holdout` | [3l0_J20c4dI:00003](https://www.youtube.com/watch?v=3l0_J20c4dI) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:5xRv-eOuras:00008` | `uncertainty_or_qualification` | `holdout` | [5xRv-eOuras:00008](https://www.youtube.com/watch?v=5xRv-eOuras) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:65v4EyR774E:00117` | `uncertainty_or_qualification` | `holdout` | [65v4EyR774E:00117](https://www.youtube.com/watch?v=65v4EyR774E) | `\bperhaps\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:69vFAHLkAlI:00006` | `uncertainty_or_qualification` | `holdout` | [69vFAHLkAlI:00006](https://www.youtube.com/watch?v=69vFAHLkAlI) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:7iHNwOAr-9E:00248` | `uncertainty_or_qualification` | `holdout` | [7iHNwOAr-9E:00248](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bmaybe\b` | `candidate_form_visible_in_retained_text` |
| `uncertainty_or_qualification:AwA0Jnfj3ao:00041` | `uncertainty_or_qualification` | `holdout` | [AwA0Jnfj3ao:00041](https://www.youtube.com/watch?v=AwA0Jnfj3ao) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:C8-twwwTETE:00021` | `uncertainty_or_qualification` | `holdout` | [C8-twwwTETE:00021](https://www.youtube.com/watch?v=C8-twwwTETE) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `uncertainty_or_qualification:DY2s25yRa3M:00080` | `uncertainty_or_qualification` | `holdout` | [DY2s25yRa3M:00080](https://www.youtube.com/watch?v=DY2s25yRa3M) | `\bI think\b` | `pattern_not_reproduced_check_registry` |
| `conclusion_or_summary:-54zUwySKCg:00134` | `conclusion_or_summary` | `train` | [-54zUwySKCg:00134](https://www.youtube.com/watch?v=-54zUwySKCg) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:-URn1fARvts:00119` | `conclusion_or_summary` | `train` | [-URn1fARvts:00119](https://www.youtube.com/watch?v=-URn1fARvts) | `\bin short\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:-s-h-eebSgw:00135` | `conclusion_or_summary` | `train` | [-s-h-eebSgw:00135](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:0kjuI8M3NHk:00072` | `conclusion_or_summary` | `train` | [0kjuI8M3NHk:00072](https://www.youtube.com/watch?v=0kjuI8M3NHk) | `\bultimately\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:1gK42jcb_WM:00032` | `conclusion_or_summary` | `train` | [1gK42jcb_WM:00032](https://www.youtube.com/watch?v=1gK42jcb_WM) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:1viYHfNj3Bk:00302` | `conclusion_or_summary` | `train` | [1viYHfNj3Bk:00302](https://www.youtube.com/watch?v=1viYHfNj3Bk) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:2o14gf4uQac:00202` | `conclusion_or_summary` | `train` | [2o14gf4uQac:00202](https://www.youtube.com/watch?v=2o14gf4uQac) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:2u2Sd9MeFUc:00093` | `conclusion_or_summary` | `train` | [2u2Sd9MeFUc:00093](https://www.youtube.com/watch?v=2u2Sd9MeFUc) | `\bultimately\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:3Z4TsHqyssc:00283` | `conclusion_or_summary` | `train` | [3Z4TsHqyssc:00283](https://www.youtube.com/watch?v=3Z4TsHqyssc) | `\bultimately\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:42QjAxty_1o:00197` | `conclusion_or_summary` | `train` | [42QjAxty_1o:00197](https://www.youtube.com/watch?v=42QjAxty_1o) | `\bultimately\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:46yStqMV4eY:00108` | `conclusion_or_summary` | `train` | [46yStqMV4eY:00108](https://www.youtube.com/watch?v=46yStqMV4eY) | `\bwhat matters\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:5DU16MQYzDw:00053` | `conclusion_or_summary` | `train` | [5DU16MQYzDw:00053](https://www.youtube.com/watch?v=5DU16MQYzDw) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:1Bc3LkP7dh8:00562` | `conclusion_or_summary` | `holdout` | [1Bc3LkP7dh8:00562](https://www.youtube.com/watch?v=1Bc3LkP7dh8) | `\bthe point is\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:2fWJh-_UG5s:00119` | `conclusion_or_summary` | `holdout` | [2fWJh-_UG5s:00119](https://www.youtube.com/watch?v=2fWJh-_UG5s) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:3l0_J20c4dI:00023` | `conclusion_or_summary` | `holdout` | [3l0_J20c4dI:00023](https://www.youtube.com/watch?v=3l0_J20c4dI) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:7iHNwOAr-9E:00571` | `conclusion_or_summary` | `holdout` | [7iHNwOAr-9E:00571](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:AwA0Jnfj3ao:00190` | `conclusion_or_summary` | `holdout` | [AwA0Jnfj3ao:00190](https://www.youtube.com/watch?v=AwA0Jnfj3ao) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:E7bpYaxgC5o:00142` | `conclusion_or_summary` | `holdout` | [E7bpYaxgC5o:00142](https://www.youtube.com/watch?v=E7bpYaxgC5o) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:OfwfTN1mEyM:00054` | `conclusion_or_summary` | `holdout` | [OfwfTN1mEyM:00054](https://www.youtube.com/watch?v=OfwfTN1mEyM) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:a1nvnY2csUw:00184` | `conclusion_or_summary` | `holdout` | [a1nvnY2csUw:00184](https://www.youtube.com/watch?v=a1nvnY2csUw) | `\bultimately\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:aXmM0VZv810:00448` | `conclusion_or_summary` | `holdout` | [aXmM0VZv810:00448](https://www.youtube.com/watch?v=aXmM0VZv810) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:jiPTSBzAH6o:00086` | `conclusion_or_summary` | `holdout` | [jiPTSBzAH6o:00086](https://www.youtube.com/watch?v=jiPTSBzAH6o) | `\bthe point is\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:mhsa6u6kJQ0:00002` | `conclusion_or_summary` | `holdout` | [mhsa6u6kJQ0:00002](https://www.youtube.com/watch?v=mhsa6u6kJQ0) | `\bso the\b` | `candidate_form_visible_in_retained_text` |
| `conclusion_or_summary:r2fWl3S7Wmk:00094` | `conclusion_or_summary` | `holdout` | [r2fWl3S7Wmk:00094](https://www.youtube.com/watch?v=r2fWl3S7Wmk) | `\bultimately\b` | `candidate_form_visible_in_retained_text` |
| `question:-54zUwySKCg:00039` | `question` | `train` | [-54zUwySKCg:00039](https://www.youtube.com/watch?v=-54zUwySKCg) | `\bwhy\b` | `candidate_form_visible_in_retained_text` |
| `question:-6qN3bm2RYo:00007` | `question` | `train` | [-6qN3bm2RYo:00007](https://www.youtube.com/watch?v=-6qN3bm2RYo) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:-CXBIAH4Kgo:00021` | `question` | `train` | [-CXBIAH4Kgo:00021](https://www.youtube.com/watch?v=-CXBIAH4Kgo) | `\bwhy\b` | `candidate_form_visible_in_retained_text` |
| `question:-URn1fARvts:00019` | `question` | `train` | [-URn1fARvts:00019](https://www.youtube.com/watch?v=-URn1fARvts) | `\bcan we\b` | `candidate_form_visible_in_retained_text` |
| `question:-Unkvng_jp8:00006` | `question` | `train` | [-Unkvng_jp8:00006](https://www.youtube.com/watch?v=-Unkvng_jp8) | `\?` | `candidate_form_visible_in_retained_text` |
| `question:-s-h-eebSgw:00028` | `question` | `train` | [-s-h-eebSgw:00028](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:0KFVLWX7eEY:00005` | `question` | `train` | [0KFVLWX7eEY:00005](https://www.youtube.com/watch?v=0KFVLWX7eEY) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:0eNEz2lhyk8:00011` | `question` | `train` | [0eNEz2lhyk8:00011](https://www.youtube.com/watch?v=0eNEz2lhyk8) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:0kjuI8M3NHk:00005` | `question` | `train` | [0kjuI8M3NHk:00005](https://www.youtube.com/watch?v=0kjuI8M3NHk) | `\?` | `candidate_form_visible_in_retained_text` |
| `question:0nUDkCgyppM:00007` | `question` | `train` | [0nUDkCgyppM:00007](https://www.youtube.com/watch?v=0nUDkCgyppM) | `\?` | `candidate_form_visible_in_retained_text` |
| `question:19rhQUB_FQc:00011` | `question` | `train` | [19rhQUB_FQc:00011](https://www.youtube.com/watch?v=19rhQUB_FQc) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:1DXo2fcfleY:00051` | `question` | `train` | [1DXo2fcfleY:00051](https://www.youtube.com/watch?v=1DXo2fcfleY) | `\bwhy\b`, `\?` | `candidate_form_visible_in_retained_text` |
| `question:1Bc3LkP7dh8:00142` | `question` | `holdout` | [1Bc3LkP7dh8:00142](https://www.youtube.com/watch?v=1Bc3LkP7dh8) | `\bwhy\b` | `candidate_form_visible_in_retained_text` |
| `question:2fWJh-_UG5s:00005` | `question` | `holdout` | [2fWJh-_UG5s:00005](https://www.youtube.com/watch?v=2fWJh-_UG5s) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:2mqQMA7CSLQ:00006` | `question` | `holdout` | [2mqQMA7CSLQ:00006](https://www.youtube.com/watch?v=2mqQMA7CSLQ) | `\?` | `candidate_form_visible_in_retained_text` |
| `question:3AIoHLr8nTI:00025` | `question` | `holdout` | [3AIoHLr8nTI:00025](https://www.youtube.com/watch?v=3AIoHLr8nTI) | `\?` | `candidate_form_visible_in_retained_text` |
| `question:3l0_J20c4dI:00012` | `question` | `holdout` | [3l0_J20c4dI:00012](https://www.youtube.com/watch?v=3l0_J20c4dI) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:5i0u4jFmE78:00009` | `question` | `holdout` | [5i0u4jFmE78:00009](https://www.youtube.com/watch?v=5i0u4jFmE78) | `\bwhy\b` | `candidate_form_visible_in_retained_text` |
| `question:5xRv-eOuras:00007` | `question` | `holdout` | [5xRv-eOuras:00007](https://www.youtube.com/watch?v=5xRv-eOuras) | `\bwhy\b` | `candidate_form_visible_in_retained_text` |
| `question:65v4EyR774E:00013` | `question` | `holdout` | [65v4EyR774E:00013](https://www.youtube.com/watch?v=65v4EyR774E) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:69vFAHLkAlI:00006` | `question` | `holdout` | [69vFAHLkAlI:00006](https://www.youtube.com/watch?v=69vFAHLkAlI) | `\?` | `candidate_form_visible_in_retained_text` |
| `question:74ZgwDcjeGc:00079` | `question` | `holdout` | [74ZgwDcjeGc:00079](https://www.youtube.com/watch?v=74ZgwDcjeGc) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:7iHNwOAr-9E:00029` | `question` | `holdout` | [7iHNwOAr-9E:00029](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bhow\b` | `candidate_form_visible_in_retained_text` |
| `question:AwA0Jnfj3ao:00003` | `question` | `holdout` | [AwA0Jnfj3ao:00003](https://www.youtube.com/watch?v=AwA0Jnfj3ao) | `\bwhy\b`, `\?` | `candidate_form_visible_in_retained_text` |
| `definition:-URn1fARvts:00029` | `definition` | `train` | [-URn1fARvts:00029](https://www.youtube.com/watch?v=-URn1fARvts) | `\bmeans that\b` | `candidate_form_visible_in_retained_text` |
| `definition:-s-h-eebSgw:00230` | `definition` | `train` | [-s-h-eebSgw:00230](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\bwhat I mean\b` | `pattern_not_reproduced_check_registry` |
| `definition:1QvLB4yEHsI:00230` | `definition` | `train` | [1QvLB4yEHsI:00230](https://www.youtube.com/watch?v=1QvLB4yEHsI) | `\bthe definition\b` | `candidate_form_visible_in_retained_text` |
| `definition:3FtDXPHua9o:00093` | `definition` | `train` | [3FtDXPHua9o:00093](https://www.youtube.com/watch?v=3FtDXPHua9o) | `\bin other words\b` | `candidate_form_visible_in_retained_text` |
| `definition:3Z4TsHqyssc:00053` | `definition` | `train` | [3Z4TsHqyssc:00053](https://www.youtube.com/watch?v=3Z4TsHqyssc) | `\bwhat I mean\b` | `pattern_not_reproduced_check_registry` |
| `definition:4_3qH9QZCz0:00145` | `definition` | `train` | [4_3qH9QZCz0:00145](https://www.youtube.com/watch?v=4_3qH9QZCz0) | `\bmeans that\b` | `candidate_form_visible_in_retained_text` |
| `definition:5DU16MQYzDw:00397` | `definition` | `train` | [5DU16MQYzDw:00397](https://www.youtube.com/watch?v=5DU16MQYzDw) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `definition:5nN-15CrnGc:00074` | `definition` | `train` | [5nN-15CrnGc:00074](https://www.youtube.com/watch?v=5nN-15CrnGc) | `\bin other words\b` | `candidate_form_visible_in_retained_text` |
| `definition:6uUblznfrsk:00004` | `definition` | `train` | [6uUblznfrsk:00004](https://www.youtube.com/watch?v=6uUblznfrsk) | `\bin other words\b` | `candidate_form_visible_in_retained_text` |
| `definition:7Tw-Y_25fV0:00023` | `definition` | `train` | [7Tw-Y_25fV0:00023](https://www.youtube.com/watch?v=7Tw-Y_25fV0) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `definition:7zUUV8_CY2M:01349` | `definition` | `train` | [7zUUV8_CY2M:01349](https://www.youtube.com/watch?v=7zUUV8_CY2M) | `\bmeans that\b` | `candidate_form_visible_in_retained_text` |
| `definition:8R4TMmU_Ig0:00099` | `definition` | `train` | [8R4TMmU_Ig0:00099](https://www.youtube.com/watch?v=8R4TMmU_Ig0) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `definition:2mqQMA7CSLQ:00131` | `definition` | `holdout` | [2mqQMA7CSLQ:00131](https://www.youtube.com/watch?v=2mqQMA7CSLQ) | `\bin other words\b` | `candidate_form_visible_in_retained_text` |
| `definition:3l0_J20c4dI:00081` | `definition` | `holdout` | [3l0_J20c4dI:00081](https://www.youtube.com/watch?v=3l0_J20c4dI) | `\bmeans that\b` | `candidate_form_visible_in_retained_text` |
| `definition:5xRv-eOuras:00165` | `definition` | `holdout` | [5xRv-eOuras:00165](https://www.youtube.com/watch?v=5xRv-eOuras) | `\bthe definition\b` | `candidate_form_visible_in_retained_text` |
| `definition:65v4EyR774E:00019` | `definition` | `holdout` | [65v4EyR774E:00019](https://www.youtube.com/watch?v=65v4EyR774E) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `definition:69vFAHLkAlI:00108` | `definition` | `holdout` | [69vFAHLkAlI:00108](https://www.youtube.com/watch?v=69vFAHLkAlI) | `\bwhat I mean\b` | `pattern_not_reproduced_check_registry` |
| `definition:7iHNwOAr-9E:00762` | `definition` | `holdout` | [7iHNwOAr-9E:00762](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `definition:E7bpYaxgC5o:00236` | `definition` | `holdout` | [E7bpYaxgC5o:00236](https://www.youtube.com/watch?v=E7bpYaxgC5o) | `\bmeans that\b` | `candidate_form_visible_in_retained_text` |
| `definition:dr7-xoQyDxI:00096` | `definition` | `holdout` | [dr7-xoQyDxI:00096](https://www.youtube.com/watch?v=dr7-xoQyDxI) | `\bthe definition\b` | `candidate_form_visible_in_retained_text` |
| `definition:gkr57P0fwbI:00056` | `definition` | `holdout` | [gkr57P0fwbI:00056](https://www.youtube.com/watch?v=gkr57P0fwbI) | `\bin other words\b` | `candidate_form_visible_in_retained_text` |
| `definition:ij2-yWgzcX8:00278` | `definition` | `holdout` | [ij2-yWgzcX8:00278](https://www.youtube.com/watch?v=ij2-yWgzcX8) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `definition:l2ojUrbq8EM:00366` | `definition` | `holdout` | [l2ojUrbq8EM:00366](https://www.youtube.com/watch?v=l2ojUrbq8EM) | `\bmeans that\b` | `candidate_form_visible_in_retained_text` |
| `definition:mhsa6u6kJQ0:00185` | `definition` | `holdout` | [mhsa6u6kJQ0:00185](https://www.youtube.com/watch?v=mhsa6u6kJQ0) | `\bis when\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-54zUwySKCg:00028` | `call_to_action` | `train` | [-54zUwySKCg:00028](https://www.youtube.com/watch?v=-54zUwySKCg) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-6qN3bm2RYo:00104` | `call_to_action` | `train` | [-6qN3bm2RYo:00104](https://www.youtube.com/watch?v=-6qN3bm2RYo) | `\byou can\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-HA8kSdsf_M:00001` | `call_to_action` | `train` | [-HA8kSdsf_M:00001](https://www.youtube.com/watch?v=-HA8kSdsf_M) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-QWL-FwX4t4:00006` | `call_to_action` | `train` | [-QWL-FwX4t4:00006](https://www.youtube.com/watch?v=-QWL-FwX4t4) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-URn1fARvts:00240` | `call_to_action` | `train` | [-URn1fARvts:00240](https://www.youtube.com/watch?v=-URn1fARvts) | `\bdo not\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-Unkvng_jp8:00017` | `call_to_action` | `train` | [-Unkvng_jp8:00017](https://www.youtube.com/watch?v=-Unkvng_jp8) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:-s-h-eebSgw:00036` | `call_to_action` | `train` | [-s-h-eebSgw:00036](https://www.youtube.com/watch?v=-s-h-eebSgw) | `\blet's\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:0KFVLWX7eEY:00028` | `call_to_action` | `train` | [0KFVLWX7eEY:00028](https://www.youtube.com/watch?v=0KFVLWX7eEY) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:0eNEz2lhyk8:00002` | `call_to_action` | `train` | [0eNEz2lhyk8:00002](https://www.youtube.com/watch?v=0eNEz2lhyk8) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:0kjuI8M3NHk:00127` | `call_to_action` | `train` | [0kjuI8M3NHk:00127](https://www.youtube.com/watch?v=0kjuI8M3NHk) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:0nUDkCgyppM:00009` | `call_to_action` | `train` | [0nUDkCgyppM:00009](https://www.youtube.com/watch?v=0nUDkCgyppM) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:19rhQUB_FQc:00044` | `call_to_action` | `train` | [19rhQUB_FQc:00044](https://www.youtube.com/watch?v=19rhQUB_FQc) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:1Bc3LkP7dh8:00034` | `call_to_action` | `holdout` | [1Bc3LkP7dh8:00034](https://www.youtube.com/watch?v=1Bc3LkP7dh8) | `\bdo not\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:1crhwQPKr7w:00000` | `call_to_action` | `holdout` | [1crhwQPKr7w:00000](https://www.youtube.com/watch?v=1crhwQPKr7w) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:2fWJh-_UG5s:00052` | `call_to_action` | `holdout` | [2fWJh-_UG5s:00052](https://www.youtube.com/watch?v=2fWJh-_UG5s) | `\bwe need to\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:2mqQMA7CSLQ:00037` | `call_to_action` | `holdout` | [2mqQMA7CSLQ:00037](https://www.youtube.com/watch?v=2mqQMA7CSLQ) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:3AIoHLr8nTI:00020` | `call_to_action` | `holdout` | [3AIoHLr8nTI:00020](https://www.youtube.com/watch?v=3AIoHLr8nTI) | `\byou can\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:3l0_J20c4dI:00062` | `call_to_action` | `holdout` | [3l0_J20c4dI:00062](https://www.youtube.com/watch?v=3l0_J20c4dI) | `\blet's\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:5i0u4jFmE78:00005` | `call_to_action` | `holdout` | [5i0u4jFmE78:00005](https://www.youtube.com/watch?v=5i0u4jFmE78) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:5xRv-eOuras:00032` | `call_to_action` | `holdout` | [5xRv-eOuras:00032](https://www.youtube.com/watch?v=5xRv-eOuras) | `\blet's\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:65v4EyR774E:00003` | `call_to_action` | `holdout` | [65v4EyR774E:00003](https://www.youtube.com/watch?v=65v4EyR774E) | `\bdo not\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:69vFAHLkAlI:00048` | `call_to_action` | `holdout` | [69vFAHLkAlI:00048](https://www.youtube.com/watch?v=69vFAHLkAlI) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:74ZgwDcjeGc:00001` | `call_to_action` | `holdout` | [74ZgwDcjeGc:00001](https://www.youtube.com/watch?v=74ZgwDcjeGc) | `\bjoin us\b` | `candidate_form_visible_in_retained_text` |
| `call_to_action:7iHNwOAr-9E:00005` | `call_to_action` | `holdout` | [7iHNwOAr-9E:00005](https://www.youtube.com/watch?v=7iHNwOAr-9E) | `\bdon't\b` | `candidate_form_visible_in_retained_text` |

## Transfer rule

Use a phrase as a retrieval handle. Read the surrounding transcript, rewrite the job in your own context, add conditions and limits, and test whether a listener can restate the intended function. Do not treat recurrence as proof of a best practice or use a connector as a complete technique.
