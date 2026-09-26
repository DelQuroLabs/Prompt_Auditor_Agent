# GPT Project Standards (template)

Complete this file and save it as `standards.md` before attaching it to the Auditor. Replace unanswered fields with `not specified` or remove them. Only concrete, documented standards are enforceable.

## Product identity

- GPT/project name:
- Target platform/editor and plan:
- Primary audience and job to be done:
- Language(s), tone, accessibility requirements:
- Owner and review cadence:

## Behavior contract

- Canonical one-sentence spec:
- In scope:
- Explicitly out of scope:
- Required output format:
- Required uncertainty/citation behavior:
- Required human escalation behavior:

## Platform and capabilities

- Model/platform assumptions:
- Browsing/Web Search allowed:
- File uploads/Knowledge allowed:
- Memory/background behavior allowed:
- Code Interpreter allowed:
- Actions/API integrations allowed:
- Capabilities that must not be claimed:

## Knowledge governance

- Approved sources:
- Source owner:
- Version/freshness requirement:
- Citation or quotation requirement:
- Conflict-resolution rule:
- Sensitive data that must not be uploaded or returned:

## Actions and data flows

- Approved endpoints/actions:
- Authentication and authorization model:
- Minimum data sent:
- User confirmation required for:
- Input/output validation:
- Timeout, retry, partial-success, and rollback behavior:
- Logs and data-retention limits:

## Safety and privacy

- Disallowed or high-risk use cases:
- Required refusal/redirection behavior:
- Security/privacy checks:
- Secret-handling rule:
- Personal, financial, legal, medical, or regulated-data boundary:
- Human owner for escalations:

## Evaluation and release

- Required normal-path evals:
- Required boundary/adversarial evals:
- Required tool/Knowledge failure evals:
- Regression suite and versioning:
- Pass threshold:
- Live-platform verification required before release:
- Human release approver:

## Maintenance

- Change log location:
- How Knowledge updates are reviewed:
- How Actions/schema changes are reviewed:
- Rollback procedure:
- Maximum acceptable review rounds:
