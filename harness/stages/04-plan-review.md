# Stage 04 — Plan Review

## Owner

Reviewer

## Purpose

Stress-test the plan for scope completeness, sequencing risk, validation sufficiency, and ambiguity carryover before execution begins.

## Inputs

- `SCOPE_CONTRACT.md`
- `PLAN.md`
- `REQUIREMENT_TRACEABILITY.md`
- task-type workflow files

## Outputs

- updated `PLAN.md`
- `PLAN_REVIEW_NOTES.md` (optional but recommended)
- review entry in `state/orchestration_ledger.jsonl`

## Gate

Every in-scope requirement is mapped to at least one execution step and one validation gate with a named owner.

## Next Stage Rule

If plan review passes, proceed to work phase selection. If review fails, return to planning.
