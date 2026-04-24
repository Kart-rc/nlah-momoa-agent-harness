# NLAH-MoVE Harness Skill

## Purpose

Execute complex tasks using explicit contracts, durable artifacts, delegated work phases, adversarial expert review, independent validation, targeted repair, and release certification.

## Global Execution Rule

Do not mark a task complete until:

1. The scope contract is satisfied.
2. Required artifacts exist.
3. Validation gates pass.
4. Evidence is written.
5. Critical dissent is resolved.
6. The release packet is complete.

## Harness Stages

1. Task routing
2. Intake
3. Ambiguity resolution
4. Scope contract
5. Planning
6. Plan review
7. Work phase selection
8. Work phase execution
9. Integration
10. Validation gauntlet
11. Repair loop
12. Release certification

## Runtime Assumptions

The runtime can read and write repository files, create run workspaces, invoke deterministic scripts, and maintain path-addressable state. The runtime may use child agents, but this harness does not require a specific framework.

## Role Model

- The **orchestrator** owns flow control, routing, and stage progression.
- The **planner** converts scope into a staged execution plan.
- The **implementer** produces artifacts and evidence.
- The **reviewer** challenges assumptions and checks local quality.
- The **independent validator** validates from artifact evidence, not implementer confidence.
- The **release certifier** decides whether the run can be released.
- The **overseer** detects stuck loops, drift, unresolved dissent, and unsafe release attempts.

## Context Isolation

Use `clean_context` for validation, security review, scope audit, paradox resolution, and release certification.

Use `fork_context` for repair, continuation, and debugging.

Use `artifact_only` for independent validation when the validator should not inherit implementation reasoning.

## Work Phase Rule

Every non-trivial work phase must declare:

- room
- role pair
- task contract
- allowed tools
- required artifacts
- success condition
- completion verdict

Allowed verdicts are `COMPLETE`, `COMPLETE_WITH_RISK`, `INCOMPLETE`, `BLOCKED`, and `CONFLICT_UNRESOLVED`.

## Validation Rule

Validation must be independent from implementation. Validators must not repair their own findings. Implementers must provide evidence before release.

## Failure Handling

Classify every failure using `harness/failure-taxonomy.md`. Map failures to retry, repair, replan, ask user, escalate to overseer, abort unsafe, or abort impossible.

## Release Rule

Final release requires:

- `RESPONSE.md`
- `RELEASE_PACKET.md`
- `artifacts/manifest.json`
- validation report
- scope traceability
- evidence summary
