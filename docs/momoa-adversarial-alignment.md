# MoMoA Adversarial Review Alignment Audit

## Objective

Verify that this harness reflects the adversarial review approach described in the MoMoA write-up and remains comprehensive across roles, rooms, skills, stages, and task types.

## Alignment criteria

1. Independence between orchestration, execution, review, and validation.
2. Explicit adversarial collaboration guidance for experts in the same room.
3. Validation that checks scope mismatch and missing work, not just syntax or test success.
4. Coverage completeness of harness primitives: roles, rooms, skills, stages, and task types.

## Findings and updates

### 1) Adversarial prompt module

Added a reusable prompt module at `harness/prompts/adversarial-collaboration.md` mirroring the MoMoA-style instruction for direct, skeptical, and constructive challenge.

### 2) Room-level enforcement

Updated Engineering, Research, and Validation rooms to require adversarial collaboration behavior and explicit dissent/challenge behavior where appropriate.

### 3) Role-model completeness

Added role definitions that were referenced by rooms and stage logic but previously implicit:

- implementer
- reviewer
- skeptical expert
- creative expert
- deterministic verifier
- scope auditor
- security reviewer
- release certifier

### 4) Task-type completeness

Added explicit harnesses for router-listed task families that previously lacked task-type modules:

- research-analysis
- generic-documentation
- generic-coding

Updated the task-type catalog and router mappings accordingly.

## Completeness checklist

- **Roles:** comprehensive and explicitly documented, including adversarial and release roles.
- **Rooms:** include domain scopes, default role pairs, and output contracts.
- **Skills:** include brainstorming, file-backed state, evidence-backed answering, and verifier separation.
- **Stages:** full staged lifecycle from intake to release remains intact.
- **Task types:** now covers all families listed by the router.

## Notes

This repository remains a markdown-first harness template. Runtime enforcement still depends on the agent runtime that interprets these artifacts and invokes deterministic scripts.
