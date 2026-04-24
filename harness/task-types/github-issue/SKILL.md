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

## Validation

Do not claim issue resolution unless root cause is documented, the patch is implemented, relevant tests pass, issue acceptance criteria are satisfied, and the PR summary explains what changed and why.
