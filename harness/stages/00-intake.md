# Stage 00 — Intake

## Owner

Orchestrator

## Purpose

Capture the user request, task type, known inputs, missing inputs, risk level, and likely validation tier.

## Inputs

- user request
- repository state, if available
- linked issue, document, or requirement

## Outputs

- `TASK.md`
- `TASK_CLASSIFICATION.md`
- initial `state/orchestration_ledger.jsonl` entry

## Gate

The task must be clear enough to classify or must be routed to ambiguity resolution.

## Failure Modes

- unclear objective
- missing repository or issue context
- hidden assumption affects outcome

## Next Stage Rule

Proceed to ambiguity resolution if material ambiguity exists; otherwise proceed to scope contract.
