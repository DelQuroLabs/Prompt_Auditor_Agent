# Changelog

## 3.1.0-gpt-profile

- Integrated the value-gated specialist extension as optional, advisory-only profiles; the Builder/Auditor protocol remains v2.
- Added same-task/revision specialist handling, schema validation, cross-field checks, and promotion fixtures.
- Clarified package integration, trigger discipline, and the limits of the available verification evidence.

## 3.0.0-gpt-profile

- Applied the upstream v2.2.0 Build ↔ Audit protocol to GPT design artifacts, not only code patches.
- Added Builder gates for capability/platform fit, Knowledge governance, Actions/data flows, output contracts, uncertainty, and live-verification limits.
- Added Auditor attack cases for retrieved-content injection, tool failure, privacy, consequential actions, unsupported capability claims, and output-format collisions.
- Added GPT-specific kickoff and rework templates, standards, configuration, and a self-application record.
- Kept protocol objects and JSON Schemas at version 2 for interoperability.

## 2.2.0 upstream base

- Made the smoke test repeatable with fixed good/bad source fixtures and a linked three-round audit chain.
- Required an evidence and result row for every Auditor acceptance criterion.
- Added a Builder stop rule for packets too large to include completely.
- Aligned the audit-report task ID pattern with the handoff schema and prohibited round-1 regression rows.
- Extended protocol validation for fixed example chains, not-verifiable findings, closed-ID reuse, and monotonic new finding IDs.

## 2.1.0 upstream base

- Corrected the Auditor starter so it asks for complete current source; the diff is supplemental.
- Added explicit handling for conflicts among the request, acceptance criteria, standards, source, and prior reports.
- Tightened rework stop conditions so each `must_fix` ID has one observable check.
- Extended the validator to accept generated handoffs and reports, check prior-report chains, and track unresolved rework IDs.

## 2.0.0 upstream base

- Replaced the Auditor's assumed-defect posture with evidence-first adversarial review.
- Separated build revision from audit round and fixed the cap at three audits total.
- Distinguished execution environment and verification evidence from code-defect severity.
- Required complete current source/context in every audit packet and fixed fresh-conversation rework state.
- Added explicit trust boundaries for untrusted source artifacts and prompt-injection attempts.
- Defined PASS as limited to supplied scope, not as CI/merge approval.
- Added JSON Schemas, a calibrated good/bad smoke test, and consistent package paths.
