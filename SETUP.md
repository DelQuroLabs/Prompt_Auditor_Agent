# Setup Guide — GPT Build ↔ Audit Pair 3.1.0 profile

This package creates two private Custom GPTs using the upstream Build ↔ Audit v2 protocol, specialized for GPT design. Exact editor labels and plan availability can change; follow the current platform UI. Optional local validation uses `tools/requirements.txt` and `tools/validate_examples.py`.

## Before starting

- Keep the `prompts/`, `schemas/`, `examples/`, and `self-audit/` folders together.
- Complete `standards.template.md` and save the result as `standards.md`.
- Never put credentials, private URLs, personal data, or hidden system prompts in Knowledge, examples, or prompts.
- Decide whether the target GPT is allowed to use browsing, files, memory, code execution, or Actions. Start with the minimum capabilities.

## 1. Create the Builder GPT

Use:

- **Name:** `GPT Build Engineer`
- **Description:** from `gpt-config.json`
- **Instructions:** paste everything below the HTML comment in `builder-gpt.md`
- **Knowledge:** `contract.md`, `schemas/build-audit-handoff.v2.schema.json`, and completed `standards.md`
- **Capabilities:** Code Interpreter optional; Web Search, Canvas, Image Generation, and Actions off by default
- **Conversation starters:** copy the Builder entries from `gpt-config.json`
- **Sharing:** Only me unless intentional

The Builder produces a complete proposed package in its response. It does not automatically create or publish the target GPT.

## 2. Create the Auditor GPT

Use:

- **Name:** `GPT Audit Engineer`
- **Description:** from `gpt-config.json`
- **Instructions:** paste everything below the HTML comment in `auditor-gpt.md`
+ **Knowledge:** `contract.md`, `schemas/audit-report.v2.schema.json`, `schemas/specialist-report.v2.schema.json`, and completed `standards.md`
- **Capabilities:** Code Interpreter optional for safe, self-contained checks; Web Search, Canvas, Image Generation, and Actions off by default
- **Conversation starters:** copy the Auditor entries from `gpt-config.json`
- **Sharing:** Only me unless intentional

The Auditor must receive the complete current package in the prompt. Knowledge files do not magically provide the Builder's current artifacts or a live GPT.

## 3. Calibrate

Run `SMOKE-TEST.md`. The Auditor must allow a correct sample to PASS or PASS_WITH_NOTES and must catch the seeded defective sample. It must also identify stale snapshots, missing context, mismatched rounds, embedded instructions in submitted artifacts, and unsupported live-capability claims.

## 4. Use a task

1. Fill `prompts/kickoff.md` and send it to the Builder.
2. Copy the Builder's entire response to `prompts/audit-request.md` and send it to the Auditor.
3. If the Auditor returns FAIL on audit 1 or 2, copy the latest complete package and report into `prompts/rework.md`. Do not restart from round 0.
4. Repeat once at most. Audit 3 is final; if still FAIL, use `prompts/escalate.md` and make the human decision.
5. Before release, test the actual configured GPT with representative and adversarial inputs, review Knowledge/Action data flows, and obtain human approval.

## Optional specialists (off by default)

Do not create a permanent specialist roster for every task. Use `specialists/TRIGGERS.md`; when a signal matches, create only the private specialist GPTs needed for that revision, usually no more than two (a ship review may pair Release and Security). Configure each from its file in `specialists/`, attach `contract.md` and `schemas/specialist-report.v2.schema.json`, and leave Actions off. Enable Web Search for the Researcher only when current external facts are required and the source can be cited.

Send each selected specialist the full current Builder packet, not just changed lines or JSON. Then attach the complete reports to the Auditor request. The Auditor remains the only source of the verdict and must confirm each promoted issue against the Builder packet.

## 5. Optional validation

From the package root:

```sh
python -m pip install -r tools/requirements.txt
python tools/validate_examples.py
```

The validator checks the retained positive examples as a linked chain and confirms that the negative fixtures are rejected. It checks packet structure and protocol history, not the quality of a GPT's prose or live behavior.
