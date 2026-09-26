# Rework request — only after FAIL on audit 1 or 2

Paste the Auditor's entire latest response below, including its JSON. In the same message, provide the **latest complete current artifact snapshot** from the previous Builder response. If using a new Builder conversation, also include the original spec/acceptance criteria, platform standards, and the current finding-status ledger. Never restart from round-0 artifacts after changes have been made.

---

Fix only IDs in `rework_brief.must_fix`. Do not change `frozen` IDs or unrelated artifacts. Confirm the task ID, prior build revision, and audit round; increment `build_revision` by one. If the current snapshot or required context is missing or stale, ask for it instead of guessing. Preserve unresolved `deferred` and `not_verifiable` items. Demonstrate each fix honestly with an eval, artifact evidence, or static explanation. Return complete current contents for every changed artifact and a `build-audit-handoff` v2 JSON block.

## Latest complete current artifact snapshot

<paste every current artifact required for review here>

## Original spec and acceptance criteria (required when starting a new conversation)

<paste original kickoff fields here>

## Platform/project standards

<paste the completed standards or say `not specified`>

## Finding-status ledger (required when starting a new conversation)

<list every prior finding ID as fixed/open/deferred/not-verifiable/overruled, with evidence>

## Latest Auditor report

<paste complete Auditor response here>
