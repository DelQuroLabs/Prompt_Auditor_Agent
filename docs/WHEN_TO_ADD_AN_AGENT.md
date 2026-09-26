# When to add an agent (Custom GPT edition)

This package’s default is still **two GPTs**: Builder and Auditor. Extra GPTs are optional specialists under `specialists/`.

## The bar (all must pass)

1. **Named failure mode** — one sentence: without this agent, shipped work systematically has X.
2. **Distinct evidence** — sees something the Auditor’s general pass under-detects (trust boundary depth, UX empty states, migration safety, external facts, ship packaging).
3. **Observable trigger** — path/flag/standards signal in `specialists/TRIGGERS.md`.
4. **Typed output** — `specialist-report` v2 only (or a research brief inside it).
5. **Exit criterion** — you know when the specialist is done for this revision.
6. **Non-writer / non-verdict** — does not patch product code; does not PASS/FAIL the task.

If any item fails → extend `standards.template.md` / Auditor instructions / smoke fixtures — **do not** mint a peer GPT.

## Core pair failure modes

| Agent | If missing |
|---|---|
| Builder | No minimal patch packet |
| Auditor | No evidence-based verdict, ID ledger, or 3-round cap |

## Specialists that usually pay rent

See `specialists/README.md`. Prefer **Security** and **UX** for app work; **Data** + **Release** at schema/ship boundaries; **Researcher** only for real unknowns; **Perf** only with a scale/latency claim.

## Agents that usually do not

| Tempting role | Why skip |
|---|---|
| Second Auditor | Same evidence class → tighten Auditor + standards |
| Style/format bot | Linters in real CI |
| Refactor muse | No trigger; fights minimal-diff rule |
| Scrum/PM GPT | Human + kickoff prompt already scope the task |
| Per-framework Auditor clones | Triggers + standards scale better |
| Summary-only manager | Human copies packets; no new evidence |

## Decision flowchart

```
Pain in real tasks
    │
    ▼
Checklist/standards fix?
  yes → edit standards.md / auditor-gpt.md
  no ──▶ Different evidence class?
           no → better smoke fixtures / prompts
           yes ▶ Trigger writable in TRIGGERS.md?
                    no → drop or tag in kickoff only
                    yes ▶ Add specialists/<role>-gpt.md
                          + schema example + gpt-config entry
```
