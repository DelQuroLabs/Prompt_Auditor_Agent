# Examples

The JSON files are examples for the v2 schemas, including PASS, PASS_WITH_NOTES, FAIL, rework, and final escalation. The round-1 FAIL, round-2 rework, and round-3 escalation files form a linked chain that the validator checks. Fixed good/bad source fixtures and their shared spec are in `fixtures/`.

Run the optional validator from the package root after installing `tools/requirements.txt`. With no arguments it checks the positive examples as linked reports and verifies that the negative fixtures are rejected. Pass a generated handoff or audit report to validate a real packet; round 2 or 3 reports also require the immediately previous audit report:

```sh
python tools/validate_examples.py
python tools/validate_examples.py path/to/build-handoff.json
python tools/validate_examples.py path/to/current-audit.json --previous-report path/to/prior-audit.json
```

The optional specialist reports and the specialist-promotion audit example are included in the no-argument fixture run. Specialist reports must match the Builder `task_id` and `build_revision`; they do not replace the complete Builder packet.
