# Execution Flow

## End-to-end stage sequence

1. `00-intake`
2. `01-ambiguity-resolution`
3. `02-scope-contract`
4. `03-planning`
5. `04-plan-review`
6. `05-work-phase-selection`
7. `06-work-phase-execution`
8. `07-integration`
9. `08-validation-gauntlet`
10. `09-repair-loop`
11. `10-release`

## Stage-level control loop

At every stage:

1. Validate required inputs.
2. Produce required outputs.
3. Write ledger event.
4. Check gate condition.
5. Advance or route to repair/escalation.

## Failure routing

- **Missing artifact** -> repair loop.
- **Scope mismatch** -> replan or scope renegotiation.
- **Validation failure** -> repair loop + independent re-check.
- **Repeated failure/stall** -> overseer escalation.

## Integration checkpoint

Before validation gauntlet:

- all child outputs are promoted or rejected explicitly,
- manifest is current,
- traceability reflects integrated state,
- dissent entries are triaged.
