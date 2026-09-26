#!/usr/bin/env python3
"""Validate bundled examples or a real Build ↔ Audit v2 packet/report.

Requires the optional `jsonschema` package. With no arguments, validates the
Builder, Auditor, and specialist examples. To validate a generated object, pass its JSON file. For an
audit round after the first, also pass the immediately previous audit report:

    python tools/validate_examples.py handoff.json
    python tools/validate_examples.py current-audit.json --previous-report prior-audit.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "build-audit-handoff": ROOT / "schemas/build-audit-handoff.v2.schema.json",
    "audit-report": ROOT / "schemas/audit-report.v2.schema.json",
    "specialist-report": ROOT / "schemas/specialist-report.v2.schema.json",
}
EXAMPLES = [
    (ROOT / "examples/build-handoff.v2.json", None),
    (ROOT / "examples/audit-pass.v2.json", None),
    (ROOT / "examples/audit-notes.v2.json", None),
    (ROOT / "examples/audit-fail.v2.json", None),
    (ROOT / "examples/audit-rework.v2.json", ROOT / "examples/audit-fail.v2.json"),
    (ROOT / "examples/audit-escalation.v2.json", ROOT / "examples/audit-rework.v2.json"),
    (ROOT / "examples/specialist-security.v2.json", None),
    (ROOT / "examples/specialist-ux.v2.json", None),
    (ROOT / "examples/specialist-researcher.v2.json", None),
    (ROOT / "examples/audit-with-specialist-promotion.v2.json", None),
]
NEGATIVE_EXAMPLES = [
    (ROOT / "examples/invalid/audit-round1-regression.v2.json", None,
     "audit 1 must have an empty regression_check"),
    (ROOT / "examples/invalid/audit-closed-id-reuse.v2.json",
     ROOT / "examples/audit-rework.v2.json", "reuses previously closed finding ID(s)"),
    (ROOT / "examples/invalid/audit-not-verifiable-omitted.v2.json",
     ROOT / "examples/audit-rework.v2.json", "prior not_verifiable finding F2 must remain in current findings"),
    (ROOT / "examples/invalid/audit-nonmonotonic-id.v2.json",
     ROOT / "examples/invalid/audit-id-gap-reuse-prior.v2.json",
     "new finding ID(s) must be greater than prior ID F3"),
    (ROOT / "examples/invalid/specialist-researcher-missing-brief.v2.json", None,
     "research_brief"),
    (ROOT / "examples/invalid/specialist-orphan-recommendation.v2.json", None,
     "recommended_to_auditor references missing finding ID(s)"),
]
STOP_CONDITION = re.compile(r"^(F[1-9][0-9]*): .+$")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def get_schema(instance: Any) -> tuple[str, Path] | None:
    if not isinstance(instance, dict):
        return None
    contract = instance.get("contract")
    if not isinstance(contract, str):
        return None
    schema_path = SCHEMAS.get(contract)
    if schema_path is None:
        return None
    return contract, schema_path


def schema_errors(label: str, instance: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = []
    for error in validator.iter_errors(instance):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{label} at {location}: {error.message}")
    return errors


def protocol_errors(
    label: str,
    instance: Any,
    previous_report: Any = None,
    *,
    require_previous: bool = False,
) -> list[str]:
    """Check cross-field rules that are awkward to express in JSON Schema."""
    if not isinstance(instance, dict):
        return []
    if instance.get("contract") == "specialist-report":
        return specialist_protocol_errors(label, instance)
    if instance.get("contract") != "audit-report":
        return []

    errors: list[str] = []
    findings = instance.get("findings", [])
    if not isinstance(findings, list) or any(not isinstance(item, dict) for item in findings):
        return errors  # The JSON Schema reports malformed findings safely.

    finding_ids = [item.get("id") for item in findings]
    by_id = {finding_id: finding for finding_id, finding in zip(finding_ids, findings)
             if isinstance(finding_id, str)}
    if len(by_id) != len(findings):
        errors.append(f"{label}: finding IDs must be present and unique")

    audit_round = instance.get("audit_round")
    expected_revision = {1: 0, 2: 1, 3: 2}.get(audit_round) if isinstance(audit_round, int) else None
    if instance.get("build_revision") != expected_revision:
        errors.append(f"{label}: build_revision must equal audit_round - 1")
    if audit_round == 1 and instance.get("regression_check"):
        errors.append(f"{label}: audit 1 must have an empty regression_check")

    brief = instance.get("rework_brief")
    if isinstance(brief, dict):
        must_fix = brief.get("must_fix", [])
        deferred = brief.get("deferred", [])
        if not isinstance(must_fix, list) or not all(isinstance(x, str) for x in must_fix):
            must_fix = []  # Schema reports the type error.
        if not isinstance(deferred, list) or not all(isinstance(x, str) for x in deferred):
            deferred = []  # Schema reports the type error.

        if instance.get("verdict") == "FAIL" and audit_round in (1, 2) and not must_fix:
            errors.append(f"{label}: FAIL on audit 1 or 2 must assign at least one ID to must_fix")

        for finding_id in must_fix + deferred:
            finding = by_id.get(finding_id)
            if finding is None:
                errors.append(f"{label}: rework ID {finding_id} is absent from findings")
            elif not isinstance(finding.get("severity"), str) or finding.get("severity") not in {"BLOCKER", "MAJOR"}:
                errors.append(f"{label}: rework ID {finding_id} is not BLOCKER/MAJOR")

        overlap = set(must_fix) & set(deferred)
        if overlap:
            errors.append(f"{label}: IDs cannot be both must_fix and deferred: {sorted(overlap)}")

        unresolved = {
            finding.get("id")
            for finding in findings
            if isinstance(finding.get("id"), str)
            and isinstance(finding.get("severity"), str)
            and finding.get("severity") in {"BLOCKER", "MAJOR"}
        }
        untracked = unresolved - set(must_fix) - set(deferred)
        if untracked:
            errors.append(f"{label}: unresolved BLOCKER/MAJOR IDs omitted from rework tracking: {sorted(untracked)}")

        conditions = brief.get("stop_conditions", [])
        if isinstance(conditions, list) and all(isinstance(item, str) for item in conditions):
            condition_ids = [match.group(1) for item in conditions
                             if (match := STOP_CONDITION.fullmatch(item))]
            malformed = len(condition_ids) != len(conditions)
            duplicates = len(condition_ids) != len(set(condition_ids))
            if malformed:
                errors.append(f"{label}: each stop condition must use `F<n>: <observable check>` format")
            if duplicates or set(condition_ids) != set(must_fix) or len(condition_ids) != len(must_fix):
                errors.append(f"{label}: provide exactly one stop condition for each must_fix ID")

    regression = instance.get("regression_check", [])
    if not isinstance(regression, list) or any(not isinstance(item, dict) for item in regression):
        regression = []  # Schema reports malformed regression rows.
    regression_ids = [item.get("finding_id") for item in regression]
    valid_regression_ids = [finding_id for finding_id in regression_ids if isinstance(finding_id, str)]
    if len(valid_regression_ids) != len(set(valid_regression_ids)):
        errors.append(f"{label}: regression_check finding IDs must be unique")

    if require_previous and audit_round in (2, 3) and previous_report is None:
        errors.append(f"{label}: provide the immediately previous audit report with --previous-report")

    if previous_report is not None:
        if not isinstance(previous_report, dict) or previous_report.get("contract") != "audit-report":
            errors.append(f"{label}: --previous-report must be an audit-report object")
            return errors

        previous_round = previous_report.get("audit_round")
        if instance.get("task_id") != previous_report.get("task_id"):
            errors.append(f"{label}: task_id does not match the previous report")
        if previous_round not in (1, 2) or audit_round != previous_round + 1:
            errors.append(f"{label}: audit_round must immediately follow a previous FAIL on round 1 or 2")
        previous_revision = previous_report.get("build_revision")
        if (not isinstance(previous_revision, int)
                or instance.get("build_revision") != previous_revision + 1):
            errors.append(f"{label}: build_revision must increase by exactly one from the previous report")
        if previous_report.get("verdict") != "FAIL":
            errors.append(f"{label}: the previous report must have verdict FAIL to continue rework")

        previous_brief = previous_report.get("rework_brief")
        if not isinstance(previous_brief, dict):
            errors.append(f"{label}: the previous FAIL report must contain a rework_brief")
        else:
            prior_must_fix = previous_brief.get("must_fix", [])
            prior_deferred = previous_brief.get("deferred", [])
            if (not isinstance(prior_must_fix, list)
                    or not isinstance(prior_deferred, list)
                    or not all(isinstance(x, str) for x in prior_must_fix + prior_deferred)):
                prior_ids = []
            else:
                prior_ids = prior_must_fix + prior_deferred
            expected_ids = set(prior_ids)
            if len(prior_ids) != len(expected_ids):
                errors.append(f"{label}: previous must_fix and deferred IDs must be unique across both lists")
            actual_ids = set(valid_regression_ids)
            if expected_ids != actual_ids or len(valid_regression_ids) != len(prior_ids):
                errors.append(f"{label}: regression_check must contain exactly one status for every prior must_fix/deferred ID")

            regression_by_id = {
                item.get("finding_id"): item for item in regression
                if isinstance(item.get("finding_id"), str)
            }
            for finding_id in expected_ids:
                status = regression_by_id.get(finding_id, {}).get("status")
                if isinstance(status, str) and status in {"open", "reopened", "not_verifiable"} and finding_id not in by_id:
                    errors.append(f"{label}: prior {status} finding {finding_id} must remain in current findings")

            # A closed ID cannot be reassigned to a later defect. New IDs must
            # also sort above every ID already present in the supplied history.
            prior_history_ids: set[str] = set()
            previous_findings = previous_report.get("findings", [])
            if not isinstance(previous_findings, list):
                previous_findings = []
            for row in previous_findings:
                if isinstance(row, dict) and isinstance(row.get("id"), str):
                    prior_history_ids.add(row["id"])
            previous_regression = previous_report.get("regression_check", [])
            if not isinstance(previous_regression, list):
                previous_regression = []
            for row in previous_regression:
                if isinstance(row, dict) and isinstance(row.get("finding_id"), str):
                    prior_history_ids.add(row["finding_id"])
            prior_closed_ids = {
                row.get("finding_id")
                for row in previous_regression
                if isinstance(row, dict) and row.get("status") == "fixed"
                and isinstance(row.get("finding_id"), str)
            }
            frozen = previous_brief.get("frozen", [])
            if not isinstance(frozen, list):
                frozen = []
            for row in frozen:
                if isinstance(row, dict) and isinstance(row.get("id"), str):
                    prior_history_ids.add(row["id"])
                    prior_closed_ids.add(row["id"])
            prior_history_ids.update(expected_ids)

            current_ids = set(by_id)
            reused_closed = current_ids & prior_closed_ids
            if reused_closed:
                errors.append(
                    f"{label}: reuses previously closed finding ID(s): {sorted(reused_closed)}"
                )

            def finding_number(finding_id: str) -> int | None:
                match = re.fullmatch(r"F([1-9][0-9]*)", finding_id)
                return int(match.group(1)) if match else None

            prior_numbers = [number for item in prior_history_ids
                             if (number := finding_number(item)) is not None]
            new_ids = current_ids - prior_history_ids
            if prior_numbers:
                highest_prior = max(prior_numbers)
                nonmonotonic = sorted(
                    finding_id for finding_id in new_ids
                    if (number := finding_number(finding_id)) is not None
                    and number <= highest_prior
                )
                if nonmonotonic:
                    errors.append(
                        f"{label}: new finding ID(s) must be greater than prior ID F{highest_prior}: {nonmonotonic}"
                    )

    return errors


def specialist_protocol_errors(label: str, instance: Any) -> list[str]:
    """Check specialist finding identity and recommendation references."""
    if not isinstance(instance, dict) or instance.get("contract") != "specialist-report":
        return []

    errors: list[str] = []
    findings = instance.get("findings", [])
    if not isinstance(findings, list) or any(not isinstance(item, dict) for item in findings):
        return errors  # The JSON Schema reports malformed findings safely.

    finding_ids = [item.get("id") for item in findings if isinstance(item.get("id"), str)]
    if len(finding_ids) != len(findings):
        return errors  # The JSON Schema reports missing or malformed IDs.
    if len(finding_ids) != len(set(finding_ids)):
        errors.append(f"{label}: specialist finding IDs must be unique within the report")

    recommended = instance.get("recommended_to_auditor", [])
    if not isinstance(recommended, list) or any(not isinstance(item, str) for item in recommended):
        return errors  # The JSON Schema reports malformed recommendations safely.
    missing = sorted(set(recommended) - set(finding_ids))
    if missing:
        errors.append(f"{label}: recommended_to_auditor references missing finding ID(s): {missing}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="A generated v2 handoff or audit report JSON file")
    parser.add_argument("--previous-report", type=Path,
                        help="The immediately previous audit report when validating audit round 2 or 3")
    args = parser.parse_args(argv)

    using_examples = args.file is None
    if using_examples and args.previous_report is not None:
        parser.error("--previous-report requires a generated audit report file")

    errors: list[str] = []
    documents: list[tuple[Path, Any, Any]] = []
    negative_documents: list[tuple[Path, Any, Any, str]] = []
    try:
        if using_examples:
            documents = [
                (path, load_json(path), load_json(previous_path) if previous_path else None)
                for path, previous_path in EXAMPLES
            ]
            negative_documents = [
                (path, load_json(path), load_json(previous_path) if previous_path else None, expected_error)
                for path, previous_path, expected_error in NEGATIVE_EXAMPLES
            ]
        else:
            documents = [(args.file, load_json(args.file), None)]
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read JSON input: {exc}", file=sys.stderr)
        return 2

    previous: Any = None
    if args.previous_report is not None:
        try:
            previous = load_json(args.previous_report)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Could not read previous report: {exc}", file=sys.stderr)
            return 2
        previous_schema = get_schema(previous)
        if previous_schema is None or previous_schema[0] != "audit-report":
            errors.append(f"{args.previous_report}: expected an audit-report JSON object")
        else:
            errors.extend(schema_errors(str(args.previous_report), previous, previous_schema[1]))
            errors.extend(protocol_errors(str(args.previous_report), previous))

    if not using_examples and documents and args.previous_report is not None:
        path, instance, _ = documents[0]
        documents[0] = (path, instance, previous)

    for path, instance, example_previous in documents:
        schema_info = get_schema(instance)
        if schema_info is None:
            errors.append(f"{path}: unknown contract; expected build-audit-handoff, audit-report, or specialist-report")
            continue
        contract, schema_path = schema_info
        errors.extend(schema_errors(str(path), instance, schema_path))
        if args.previous_report is not None and contract != "audit-report":
            errors.append(f"{path}: --previous-report can only be used with an audit-report JSON file")
        if contract == "audit-report":
            errors.extend(protocol_errors(
                str(path), instance, example_previous,
                require_previous=not using_examples,
            ))
        elif contract == "specialist-report":
            errors.extend(specialist_protocol_errors(str(path), instance))

    for path, instance, example_previous, expected_error in negative_documents:
        negative_errors: list[str] = []
        schema_info = get_schema(instance)
        if schema_info is None:
            negative_errors.append("unknown contract")
        else:
            negative_errors.extend(schema_errors(str(path), instance, schema_info[1]))
            if schema_info[0] == "audit-report":
                negative_errors.extend(protocol_errors(str(path), instance, example_previous))
            elif schema_info[0] == "specialist-report":
                negative_errors.extend(specialist_protocol_errors(str(path), instance))
        if not any(expected_error in error for error in negative_errors):
            errors.append(
                f"{path}: expected validator rejection containing {expected_error!r}; "
                f"observed {negative_errors or 'no errors'}"
            )

    if errors:
        print("Invalid document(s):")
        for error in errors:
            print(f" - {error}")
        return 1

    count = len(documents)
    if using_examples:
        print(
            f"Validated {count} bundled examples and {len(negative_documents)} expected-rejection fixtures "
            "against Draft 2020-12 schemas and protocol cross-field rules."
        )
    else:
        print(f"Validated {args.file} against its Draft 2020-12 schema and protocol cross-field rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
