# Stage 05 — Work Phase Selection

## Owner

Orchestrator

## Purpose

Select rooms, role pairs, and delegation strategy for each plan item while preserving scope boundaries and validator independence.

## Inputs

- `PLAN.md`
- `SCOPE_CONTRACT.md`
- task risk/tier
- available rooms and roles

## Outputs

- work phase assignments in `PLAN.md`
- optional child workspace task packets
- orchestration ledger events for assignments

## Gate

Each phase declares room, role pair, required artifacts, allowed tools, and completion verdict criteria.

## Next Stage Rule

Proceed to work phase execution once all non-trivial phases are assigned.
