# Specialist GPTs (optional, value-gated)

Specialists are **not** a standing army and **not** a second Auditor.

They exist only when a **trigger** fires (see `TRIGGERS.md`) and only when they own a **failure mode** the core Builder ↔ Auditor pair systematically under-detects.

## Invariants (non-negotiable)

1. **Advisory only.** Specialists never issue `PASS` / `FAIL` / `rework_brief` / `escalation`.
2. **No product patches.** Only Builder proposes code. Specialists may suggest a minimal fix in a finding, not emit a handoff.
3. **Provisional IDs.** Specialist findings use `S1`, `S2`, … The **Auditor** promotes supported items into task-wide `F` IDs (or discards them with reason).
4. **Same packet honesty.** Review only the supplied Builder packet + any prior specialist reports for this revision. Disclose missing context.
5. **Evidence or open_questions.** Unsupported suspicions never become findings.
6. **Human still owns ship.** Project CI + human review remain the release gate.

## Roster

| Specialist | Failure mode if missing | Typical trigger |
|---|---|---|
| **Security** | Trust-boundary defects under-weighted in general review | auth/session/secret paths, payments, PII, multi-tenant |
| **UX** | Correct code, hostile or incomplete human flow | UI components, forms, empty/error/loading states |
| **Perf** | Correct but unbounded latency, leaks, amplification | hot paths, lists, realtime, batch, tight SLAs |
| **Data** | Destructive or unrollbackable schema/data changes | migrations, ORM schema, backfills |
| **Release** | Works in chat packet, fails in CI/prod packaging | Dockerfile, workflows, deploy manifests, ship checklist |
| **Researcher** | Hallucinated APIs / outdated external facts | explicit unknowns, unfamiliar SDK, license questions |

## When *not* to add a specialist

- The work is a checklist item the Auditor already covers → extend `standards.md` or Auditor instructions.
- You cannot name the failure mode **and** the trigger in one sentence each.
- The agent would only summarize other agents.
- Two specialists would emit the same finding class → keep one.

## How they enter the loop

```
Builder packet
    │
    ├─► always → Auditor
    │
    └─► if TRIGGERS match → optional specialist(s) in parallel
              │
              └─► specialist-report JSON(s)
                        │
                        └─► Auditor merges: promote S* → F* or drop
```

Use `prompts/specialist-request.md` and `prompts/audit-request-with-specialists.md`.
Validate reports with:

```bash
python tools/validate_examples.py examples/specialist-security.v2.json
```

Run that command from the complete core pair package root after applying this extension. The extension folder by itself does not include `tools/validate_examples.py`.
