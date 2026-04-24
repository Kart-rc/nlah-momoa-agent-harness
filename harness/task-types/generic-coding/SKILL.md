# Generic Coding Harness

## Purpose

Execute coding tasks that do not fit a narrower task family while preserving scope discipline and validation rigor.

## Required Inputs

- coding objective
- acceptance criteria
- repository context and constraints

## Required Artifacts

- `TASK_INTAKE.md`
- `SCOPE_CONTRACT.md`
- `IMPLEMENTATION_PLAN.md`
- `IMPLEMENTATION_EVIDENCE.md`
- `VALIDATION_REPORT.md`
- `RELEASE_PACKET.md`

## Workflow

1. Intake and scope contract
2. Plan and risk review
3. Implement
4. Validate
5. Repair if needed
6. Prepare release evidence

## Validation Gates

- acceptance criteria are satisfied
- deterministic checks pass or are explicitly waived
- risks and tradeoffs are documented
- unrelated changes are avoided

## Role Model

- orchestrator: select validation tier and enforce gates
- planner: produce an execution plan proportional to change risk
- implementer: complete changes and implementation evidence
- reviewer: challenge assumptions and code-level quality
- independent validator: verify outcomes without implementer bias
- release certifier: confirm completion against scope contract

## End-to-End Flow Coverage

This task family still executes all harness stages with scaled rigor:

1. classify coding scope and risk
2. resolve ambiguities that affect implementation
3. plan and execute implementation phases
4. run validation and independent verification
5. repair if needed and certify release

## Release Expectations

Release must include what changed, why, how validated, and any known limitations or follow-up work.
