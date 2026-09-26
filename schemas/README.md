# JSON Schemas

These files define the v2 JSON objects emitted at the end of each agent response:

- `build-audit-handoff.v2.schema.json` — Builder output
- `audit-report.v2.schema.json` — Auditor output
- `specialist-report.v2.schema.json` — optional advisory specialist output; it does not change either core v2 contract

Both use JSON Schema Draft 2020-12. The optional `tools/validate_examples.py` validator checks key cross-field rules, including finding tracking, one-to-one stop conditions, no round-1 regression rows, and (when given `--previous-report`) task, revision, round, and finding-status continuity. It also checks closed-ID reuse and monotonic new IDs when the supplied report history permits. The normative rules remain in `../contract.md`.
