# Brownfield Feature Harness

## Purpose

Add functionality to an existing application while preserving current behavior, architecture constraints, and operational quality.

## Required Inputs

- feature request
- existing repository or current-state description
- acceptance criteria
- constraints and non-functional requirements, when known

## Required Artifacts

- `FEATURE_INTAKE.md`
- `CURRENT_STATE.md`
- `IMPACT_ANALYSIS.md`
- `DESIGN_OPTIONS.md`
- `IMPLEMENTATION_PLAN.md`
- `TEST_PLAN.md`
- `REGRESSION_EVIDENCE.md`
- `RELEASE_PACKET.md`

## Workflow

1. Feature intake
2. Current-state discovery
3. Impact analysis
4. Design options
5. Implementation plan
6. Code or artifact change
7. Test plan
8. Regression validation
9. Release notes

## Validation Gates

- acceptance criteria trace to tests or review evidence
- existing behavior is preserved
- blast radius is understood
- failure and rollback paths are documented
- observability and security impacts are considered

## Role Model

- orchestrator: route, gate, and sequence changes safely
- planner: convert accepted scope into implementation and validation phases
- implementer: ship incremental changes with evidence
- reviewer: challenge design and regression assumptions
- independent validator: verify behavior from evidence and tests
- release certifier: approve release packet and residual risks

## End-to-End Flow Coverage

This task family maps to the full NLAH-MoVE lifecycle:

1. intake and feature classification
2. ambiguity resolution for constraints and acceptance criteria
3. scope contract and blast-radius guardrails
4. phased implementation and regression checks
5. independent validation and dissent handling
6. release certification with rollback notes

## Release Expectations

Release must include changed scope, regression evidence, known risks, rollback strategy, and operator-facing notes.
