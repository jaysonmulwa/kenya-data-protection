# Eval results

Run on 2026-10-06 and 2026-10-07 with Claude Opus 5.5 (`claude-opus-5-5`) through headless Claude Code, using [`run_skill_benchmark.py`](run_skill_benchmark.py).

## Setup

Eight realistic questions ([`evals.json`](evals.json)), each answered **3 times** in each of three setups:

| Setup | What the model had |
|---|---|
| **With skill** | This skill (its `SKILL.md`, references and scanner). No web. |
| **Plain model** | Nothing but its own knowledge. No tools at all. |
| **Plain model + ODPC web** | Told to research the ODPC website (odpc.go.ke) before answering. It could search the web, but fetch pages only from odpc.go.ke. |

The code-check question also gave every setup read-only access to a copy of the sample app ([`files/acorns-parent-app/`](files/acorns-parent-app/)), kept outside this repo.

A blind grader (same model, no tools, not told which setup wrote the answer) scored every answer against 42 fixed checks. The checks were taken from the official texts on Kenya Law: the Act and the Registration and General Regulations 2021, as revised to 31 December 2022. A check passes only if the answer states the fact clearly and correctly.

The with-skill answers are from the final skill version, the one in this repo. The plain-model and web answers come from earlier rounds with the same model, prompts and grader. Nothing they depend on changed, so they weren't rerun.

## Summary

| | With skill | Plain model | Plain model + ODPC web |
|---|---|---|---|
| **Checks passed (126 = 42 × 3)** | **124 (98.4%)** | 97 (77.0%) | 106 (84.1%) |
| Per-run pass rate, mean ± sd | 98.8% ± 4.2% | 77.9% ± 16.9% | 84.2% ± 14.8% |
| Average time per answer | 51 s | 42 s | 122 s |
| Average tokens per answer | 63k | 15k | 222k |
| Average cost per answer | $0.27 | $0.13 | $0.97 |
| Extra legal errors flagged by the grader* | 17 | 17 | 14 |

\* Wrong claims the checks don't cover, as flagged by the grader. I checked the 17 with-skill flags against the official texts: 8 were the grader's own mistakes (it denied the reg 15(4) KES 20,000 penalty, the reg 51(3) 60-day deemed approval, and that a DPO is optional under s.24). The real ones are listed under "Where the skill still falls short". The other setups' flags weren't checked.

## By question

| Question | With skill | Plain model | Plain + ODPC web |
|---|---|---|---|
| Bakery, 12 staff, KES 3.2M: must it register? | 15/15 | 12/15 | 13/15 |
| Deadlines for access and deletion requests | 12/12 | 12/12 | 12/12 |
| Digital lender data breach | 15/15 | 11/15 | 10/15 |
| Telemedicine app hosted in Ireland | 12/12 | 12/12 | 12/12 |
| Wedding client list used for marketing | 15/15 | 9/15 | 11/15 |
| School parent app code check | 23/24 | 20/24 | 23/24 |
| Exempt startup: any paperwork needed? | 15/15 | 9/15 | 11/15 |
| Mall adding facial recognition to CCTV | 17/18 | 12/18 | 14/18 |
| **Total** | **124/126** | **97/126** | **106/126** |

## By check

Each cell is how many of the 3 runs passed.

| Question | Check | With skill | Plain | Plain + web |
|---|---|---|---|---|
| Bakery | Must register: the exemption needs both revenue under KES 5M and fewer than 10 employees | 3/3 | 3/3 | 3/3 |
| Bakery | Registration fee KES 4,000 | 3/3 | 3/3 | 3/3 |
| Bakery | Renewal fee KES 2,000 | 3/3 | 3/3 | 3/3 |
| Bakery | Certificate valid 24 months | 3/3 | 3/3 | 3/3 |
| Bakery | The Act's duties apply whether or not registration is required | 3/3 | **0/3** | 1/3 |
| Deadlines | Access request: 7 days | 3/3 | 3/3 | 3/3 |
| Deadlines | Access is free of charge | 3/3 | 3/3 | 3/3 |
| Deadlines | Erasure: respond within 14 days | 3/3 | 3/3 | 3/3 |
| Deadlines | No one-month (GDPR) deadline given for access | 3/3 | 3/3 | 3/3 |
| Breach | Notify the ODPC within 72 hours of awareness | 3/3 | 3/3 | 3/3 |
| Breach | Notifiable under reg 37's specific tests (ID number with other data; account identifier with password) | 3/3 | 1/3 | **0/3** |
| Breach | Tell affected users in writing | 3/3 | 3/3 | 3/3 |
| Breach | Max fine KES 5M or 1% of turnover, whichever is lower | 3/3 | 3/3 | 3/3 |
| Breach | A digital lender must register, whatever its size | 3/3 | 1/3 | 1/3 |
| Telemedicine | Primary health care needs a server or serving copy in Kenya (reg 26) | 3/3 | 3/3 | 3/3 |
| Telemedicine | Health data is sensitive; abroad needs consent and safeguards | 3/3 | 3/3 | 3/3 |
| Telemedicine | Must register whatever its size (patient care) | 3/3 | 3/3 | 3/3 |
| Telemedicine | DPIA before processing | 3/3 | 3/3 | 3/3 |
| Wedding | Marital status and parents' names are sensitive data | 3/3 | 3/3 | 3/3 |
| Wedding | Marketing needs express consent | 3/3 | 3/3 | 2/3 |
| Wedding | No sensitive data in direct marketing, even with consent (reg 15(1)) | 3/3 | **0/3** | 3/3 |
| Wedding | Opt-out in every message | 3/3 | 3/3 | 3/3 |
| Wedding | Stop sharing for third-party marketing within 7 days (reg 18) | 3/3 | **0/3** | **0/3** |
| School app | Must register although under both thresholds (education) | 3/3 | 3/3 | 3/3 |
| School app | Ireland-only hosting breaks reg 26 for basic education | 3/3 | 1/3 | 3/3 |
| School app | Parent or guardian consent for pupils' data | 2/3 | 3/3 | 2/3 |
| School app | Pupils' health fields and guardians' marital status are sensitive | 3/3 | 2/3 | 3/3 |
| School app | Names 3+ third-party services; each needs a written contract | 3/3 | 3/3 | 3/3 |
| School app | No privacy notice at sign-up | 3/3 | 3/3 | 3/3 |
| School app | DPIA required | 3/3 | 2/3 | 3/3 |
| School app | Questions the need for marital status or ID numbers | 3/3 | 3/3 | 3/3 |
| Startup | Probably exempt from registration | 3/3 | 3/3 | 3/3 |
| Startup | Duties still apply when exempt | 3/3 | 3/3 | 3/3 |
| Startup | Must publish and update a data protection policy (reg 23) | 3/3 | **0/3** | **0/3** |
| Startup | Tell users at sign-up what, why, and their rights (s.29) | 3/3 | 1/3 | 2/3 |
| Startup | Newsletter needs consent and an opt-out in every message | 3/3 | 2/3 | 3/3 |
| Mall | DPIA before switching on | 3/3 | 3/3 | 3/3 |
| Mall | Large-scale monitoring of a public area is a DPIA trigger | 2/3 | 3/3 | 2/3 |
| Mall | Facial recognition data is biometric, so sensitive | 3/3 | 3/3 | 3/3 |
| Mall | Must register whatever its size (security CCTV) | 3/3 | **0/3** | 3/3 |
| Mall | High-risk DPIA: consult the ODPC first; it has 60 days | 3/3 | 0/3 | 0/3 |
| Mall | Tell shoppers first, e.g. signs at entrances | 3/3 | 3/3 | 3/3 |

## What this shows

- **The skill adds about 21 points over the plain model and 14 over the plain model with ODPC web research.** It is also the most consistent setup: its per-run spread is a quarter of the others'.
- **Web research closes some gaps but not others.** Reading the ODPC site fixed the registration lists (security CCTV), local hosting for schools and the reg 15 ban on sensitive data in marketing. It never found the reg 23 published-policy duty, the 7-day third-party marketing deadline or reg 37's breach tests. Those sit in the regulations' fine print, and the ODPC site isn't laid out to surface them.
- **Web research costs most.** It took more than twice as long as the skill and cost about 3.5 times as much per answer.
- **The plain model is strong on headline rules.** All three setups tie on the 72 hours, the deadlines for requests, the fine cap and local hosting for health care.

### Where the skill still falls short

The two missed checks (school consent 2/3, mall monitoring trigger 2/3) are single misses, within run-to-run noise. The grader's extra flags point to two real gaps:

- **Grounds for sensitive data (s.44–46).** For the mall's shoplifter watchlist, answers relied on "legitimate interests" alone. Biometric data is sensitive, so it also needs one of the specific grounds the Act sets for sensitive data. The skill doesn't cover these grounds yet.
- **Loose wording that answers repeat.** Answers sometimes cited the mandatory-registration list as "Act s.18, Third Schedule" (it's the Registration Regulations' schedule), and called any next-of-kin field sensitive (only names of a child, parent or spouse are).

### How the skill improved between rounds

| Skill version | Checks passed |
|---|---|
| After the reg 15, reg 23, DPIA-list and s.31(5) fixes | 119/126 |
| Final: gaps written so the reader can act on them (spell out s.29, name sensitive fields, both DPIA steps) | **124/126** |

## Rerun

```
python evals/run_skill_benchmark.py eval-workspace/new-run --runs 3
python evals/run_skill_benchmark.py eval-workspace/new-run --configs with_web
```

It needs the `claude` CLI and prints the tables above. The scanner's own check is `python tests/test_scan_repo.py`.
