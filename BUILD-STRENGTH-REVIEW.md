# Build strength review

**Review date:** 26 September 2026

## Scope and rating basis

This is a static review of the two supplied directories: the complete GPT Build ↔ Audit pair and the separate specialist extension set. It covers prompt instructions, configuration, contracts, schemas, examples, setup, and the included validator. No Custom GPT instances or live platform behavior were supplied.

The ranking describes package maturity and integration, not model quality. A directory ranks higher when it is internally coherent, installable from its own instructions, machine-checkable, and honest about what has not been verified.

## Rank of the supplied builds

| Rank | Supplied material | Strength | Evidence and limit |
|---:|---|---|---|
| 1 | `gpt-build-audit-pair` 3.0.0 profile | Strong core | Clear three-round contract, full-snapshot handoffs, evidence-based findings, scope limits, schemas, positive/negative fixtures, and a validator. This was the only complete stand-alone pair. |
| 2 | `gpt_Build-Audit_Agent-v2.3-new-files` | Promising extension, incomplete as supplied | Specialist roles, explicit triggers, advisory-only IDs, and an Auditor promotion prompt are well bounded. The extension had no core-pair integration, its README validation command pointed to a tool absent from that directory, and its schema did not require the researcher brief that the prompt requires. |

**Overall before fixes:** strong core protocol, with the specialist extension not yet a working addition to it. The strongest end product is the core pair with specialists kept optional and connected through explicit triggers.

## Ranked improvements

1. **Connect the specialist reports to the core Auditor and validator.** Without this, the new prompts can produce reports but the actual pair does not know how to consume or validate them. Applied: reports are optional, bound to the same task and revision, and independently confirmed by the Auditor; specialists cannot issue verdicts or expand scope.
2. **Make the specialist output contract enforce its own written requirements.** Applied: `research_brief` is now required for every specialist report, and the validator checks unique local S IDs and that recommendations refer to findings in that report.
3. **Make the extension installable and its examples unambiguous.** Applied: optional profiles are registered in configuration, setup and smoke guidance describe the trigger-gated workflow, the extension directory explains that it must be merged, and the promotion fixture records the report as reviewed rather than unavailable.
4. **Run package validation and live behavior checks.** Still pending: the bundled validator could not run in this environment because the available Python runtime lacks the declared `jsonschema` dependency. I did not install packages. The source package's historical self-audit records a prior successful run, but that result was not reproducible here. No live GPT behavior is verified.

## Current build status

The package has been updated to profile version 3.1.0 while retaining protocol version 2. The core pair remains usable without specialists; the specialist profiles are disabled by default. A standard-library check parsed 28 JSON files with duplicate-key rejection, parsed the updated validator source, resolved all optional profile/schema paths, and exercised the specialist cross-field checks with valid, duplicate-ID, and orphan-recommendation inputs. Full JSON Schema/fixture validation remains unverified because the available Python runtime lacks the declared `jsonschema` dependency. Live GPT smoke tests are also unverified. Do not treat this review as a release approval.

## Next verification

From the complete pair root, install the declared optional dependency and run `python tools/validate_examples.py`. Then run the updated specialist smoke cases and test the configured private GPTs with matching and mismatched task/revision reports. Record observed outputs before claiming the optional specialist workflow is verified.
