# Human escalation — after audit 3 still FAIL

Do not start audit 4. Review the final Auditor report, current complete artifact snapshot, and decision requested. Choose one path:

1. **Clarify or change the spec:** make the human decision, update acceptance criteria, assign a new `task_id`, and start a fresh revision-0 task.
2. **Split the task:** divide the GPT into smaller independently reviewable builds with new IDs and explicit interfaces.
3. **Overrule a finding:** record the finding ID, rationale, owner, accepted risk, and expiry/review date. Do not silently call it fixed.
4. **Disable or remove a capability:** if the issue is an Action, Knowledge source, or platform assumption, reduce scope and restart the relevant build.
5. **Stop or defer:** do not publish the GPT until the unresolved issue is addressed.

A GPT PASS does not replace testing the actual configured GPT, reviewing Knowledge and Action data flows, or obtaining human release approval.
