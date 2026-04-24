# GitHub Issue Harness

## Purpose

Resolve GitHub issues using classification, repository discovery, root-cause analysis, implementation, validation, and PR-ready release evidence.

## Supported Issue Classes

- bug
- enhancement
- vulnerability
- dependency upgrade
- build failure
- test failure
- documentation issue
- performance issue

## Required Inputs

At least one of:

- GitHub issue URL or number
- issue text
- failing test output
- stack trace
- vulnerability alert
- dependency upgrade request

## Required Artifacts

- `ISSUE_INTAKE.md`
- `ISSUE_CLASSIFICATION.md`
- `ROOT_CAUSE_ANALYSIS.md`
- `PATCH_PLAN.md`
- `VALIDATION_EVIDENCE.md`
- `PR_SUMMARY.md`
- `RELEASE_PACKET.md`

## Workflow

1. Intake
2. Classify issue
3. Inspect repository
4. Reproduce or gather evidence
5. Root-cause analysis
6. Patch plan
7. Implement
8. Test
9. Independent review
10. Release packet

## Validation Gates

Do not claim issue resolution unless root cause is documented, the patch is implemented, TDD evidence is captured (failing test before fix + passing test after fix), relevant tests pass, issue acceptance criteria are satisfied, and the PR summary explains what changed and why.

## Role Model

- orchestrator: coordinate issue lifecycle and compliance gates
- planner: produce patch plan and risk-aware execution sequence
- implementer: remediate issue and capture implementation evidence
- reviewer: challenge root cause and fix completeness
- independent validator: validate fix independently from implementer reasoning
- release certifier: certify patch readiness and residual risk statement

## End-to-End Flow Coverage

This task family covers all harness stages:

1. intake and issue classification
2. ambiguity resolution for reproduction and scope boundaries
3. scope contract and root-cause planning
4. implementation, integration, and validation gauntlet
5. repair loop for failed checks or dissent
6. release certification with PR summary and evidence packet

## Release Expectations

Release must include issue class, root cause summary, fix evidence, validation outcomes, and explicit residual risks.
