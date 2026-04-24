# Greenfield Application Harness

## Purpose

Create a new application from product intent through architecture, scaffold, baseline implementation, validation, and developer runbook.

## Required Inputs

- product idea or requirement
- target users
- MVP boundary
- preferred stack or constraints
- deployment target, if known

## Required Artifacts

- `PRODUCT_BRIEF.md`
- `MVP_SCOPE.md`
- `ARCHITECTURE_OPTIONS.md`
- `TECH_STACK_DECISION.md`
- `PROJECT_SCAFFOLD_PLAN.md`
- `IMPLEMENTATION_EVIDENCE.md`
- `RUNBOOK.md`
- `RELEASE_PACKET.md`

## Workflow

1. Product brief
2. Ambiguity resolution
3. Architecture options
4. Tech stack decision
5. Scaffold plan
6. Implementation
7. Validation
8. Runbook / developer guide

## Validation Gates

- MVP scope is explicit
- architecture decision is documented
- scaffold is coherent
- tests or smoke checks exist
- setup instructions are usable
- risks and deferred work are stated

## Role Model

- orchestrator: enforce stage-gate progression from idea to release
- planner: map MVP scope into phased build and validation tracks
- implementer: scaffold and implement the agreed baseline
- reviewer: challenge architecture and delivery risks
- independent validator: verify setup, smoke paths, and evidence quality
- release certifier: certify launch readiness and deferred work

## End-to-End Flow Coverage

This task family maps to the full NLAH-MoVE lifecycle:

1. intake and product intent capture
2. ambiguity resolution on users, constraints, and boundaries
3. scope contract and architecture planning
4. scaffold and implementation work phases
5. validation gauntlet and repair loop as needed
6. release certification with runbook and deferred backlog

## Release Expectations

Release must include runnable setup instructions, baseline validation evidence, architecture rationale, and explicit deferred scope.
