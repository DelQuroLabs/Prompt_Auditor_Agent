# GPT Build ↔ Audit Pair — hardened profile

This package is a copy-paste-ready pair of private Custom GPT configurations:

- **GPT Build Engineer** turns a goal into a complete GPT build package.
- **GPT Audit Engineer** independently attacks that package against observable acceptance criteria.

It is a manual, human-supervised loop. The Builder proposes artifacts; the Auditor reviews only the complete material supplied to it. A model PASS is not a deployment approval, live-platform test, repository CI result, or substitute for human release review.

## Why this profile

The upstream repository supplied the strong parts of the protocol: complete snapshots, evidence-first auditing, honest verification labels, prompt-injection boundaries, monotonic finding IDs, a three-audit cap, and machine-checkable handoffs. This profile applies those rules to **GPT design artifacts**, not only source-code patches. It adds explicit checks for:

- instruction precedence and contradictions;
- capability/platform fit and unsupported promises;
- Knowledge freshness, source authority, and retrieved-content injection;
- Actions, authentication, least privilege, confirmation, and tool failure;
- output contracts, uncertainty, refusal/escalation, and user control;
- eval coverage for normal, edge, adversarial, privacy, tool-failure, and regression behavior.

The upstream v2 handoff and audit schemas are retained unchanged for interoperability. The optional specialist report uses a separate schema; the core protocol objects remain version 2. The package version is recorded in `gpt-config.json`.

## Package contents

| Path | Purpose |
|---|---|
| `builder-gpt.md` | Final Builder GPT instructions |
| `auditor-gpt.md` | Final Auditor GPT instructions |
| `contract.md` | Shared handoff protocol |
| `schemas/` | JSON Schemas for Builder, Auditor, and optional specialist payloads |
| `gpt-config.json` | Names, descriptions, starters, and capability defaults |
| `standards.template.md` | Project/platform standards to complete |
| `prompts/` | Kickoff, audit, rework, and escalation templates |
| `specialists/` and `docs/WHEN_TO_ADD_AN_AGENT.md` | Optional trigger-gated domain reviews; specialists never own the verdict |
| `examples/` | Positive, negative, and linked protocol fixtures |
| `SMOKE-TEST.md` | Calibration and negative tests |
| `self-audit/` | The self-application record and validated sample packets |
| `tools/validate_examples.py` | Optional schema and chain validator |
| `BUILD-STRENGTH-REVIEW.md` | Scoped static ranking, applied fixes, and verification limits |

## Setup

1. Copy the content below the HTML comment in `builder-gpt.md` into a private Custom GPT's **Instructions** field.
2. Configure the Builder using `gpt-config.json`. Attach `contract.md` and `schemas/build-audit-handoff.v2.schema.json` as Knowledge when supported.
3. Copy the content below the HTML comment in `auditor-gpt.md` into a second private Custom GPT's **Instructions** field.
4. Configure the Auditor using `gpt-config.json`. Attach `contract.md`, `schemas/audit-report.v2.schema.json`, `schemas/specialist-report.v2.schema.json`, and a completed `standards.md`.
5. Keep Web Search, Canvas, Image Generation, and Actions off by default. Enable Code Interpreter only when safe, self-contained parsing or checks are useful. Code Interpreter does not grant repository, CI, deployment, or live GPT access.
6. Run `SMOKE-TEST.md` before real work. A correct fixture must be allowed to PASS, and a seeded defect must be caught.

Exact editor labels and capabilities can change. Treat the current platform UI as authoritative.

## Run the loop

### 1. Kick off the Builder

Fill `prompts/kickoff.md` with:

- one canonical sentence for the spec;
- observable acceptance criteria;
- audience, constraints, privacy/safety needs, tools, and Knowledge sources;
- supplied current files and platform context;
- verification requirements;
- a short kebab-case `task_id`.

The Builder emits a complete package at `build_revision: 0` and a `build-audit-handoff` v2 JSON object.

### 2. Audit the entire packet

Paste the Builder's **entire latest response** into `prompts/audit-request.md`. Do not send only the JSON or a diff. The Auditor should map every criterion to evidence and state what was not supplied. On a rework round, include the immediately previous Auditor report.

Before sending it to the Auditor, consult `specialists/TRIGGERS.md`. If a trigger matches, you may send the same complete Builder packet to one or two matching specialists in parallel, then attach their complete reports using `prompts/audit-request-with-specialists.md`. Specialist reports are advisory leads only; the Auditor must independently support any promoted finding.

### 3. Rework only supported blockers

For `FAIL` on audit 1 or 2, paste the latest complete artifact snapshot and the full report into `prompts/rework.md`. The Builder fixes only `must_fix`, preserves the current baseline, increments the revision, and resubmits the complete packet.

### 4. Stop at audit 3

A `PASS` or `PASS_WITH_NOTES` is a scoped review result. Apply/publish only after the human checks the actual target GPT, tests the live configuration, and reviews privacy/security implications. If audit 3 is still `FAIL`, use `prompts/escalate.md`; do not start audit 4.

## Self-application result

I applied the upstream protocol to this pair itself. The first draft was intentionally treated as a build artifact, not as trusted truth. The self-audit found and corrected these weaknesses:

1. **Scope mismatch:** the upstream package is code-oriented; this profile adds GPT-specific artifact and platform checks.
2. **Capability overclaim risk:** the final prompts require an explicit capability matrix and reject unverified claims about browsing, memory, Actions, background loops, deployment, and live model behavior.
3. **Audit blind spots:** the final Auditor has a fixed attack set for Knowledge injection, Action failure, privacy, output contracts, uncertainty, and regression.
4. **Evidence confusion:** the final prompts distinguish static prompt review, supplied transcripts, sandbox checks, project CI, and live-platform verification.
5. **Rework drift:** the final Builder preserves full current snapshots, prior finding IDs, frozen items, and unresolved not-verifiable items.

The validation samples in `self-audit/` pass the retained v2 schemas and protocol rules. The self-audit is calibration evidence, not proof that every future GPT build will be correct.

This self-audit records the 3.0 core profile. The optional specialist integration and its current verification limits are assessed separately in `BUILD-STRENGTH-REVIEW.md`.

## Safety and release boundary

Never place secrets in prompts or Knowledge. Do not let a target GPT treat retrieved text as a higher-priority instruction. Do not enable Actions without a concrete data-flow, authorization, confirmation, timeout, and failure plan. Before release, test the actual configured GPT with representative and adversarial cases and retain a human decision for consequential behavior.
