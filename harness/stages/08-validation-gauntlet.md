# Stage 08 — Validation Gauntlet

## Owner

Independent Validator

## Purpose

Block false completion by validating artifacts, scope coverage, evidence, tests, security posture, and release readiness.

## Validation Layers

1. V1 deterministic checks
2. V2 artifact existence check
3. V3 scope traceability check
4. V4 evidence check
5. V5 independent validator review
6. V6 security review, when Tier 3+
7. V7 release certification

## Inputs

- `SCOPE_CONTRACT.md`
- `PLAN.md`
- `IMPLEMENTATION_EVIDENCE.md`
- `VALIDATION_REPORT.md`
- `artifacts/manifest.json`

## Outputs

- updated `VALIDATION_REPORT.md`
- updated `state/validation_ledger.jsonl`
- repair tickets for failed gates

## Gate

Release is blocked when required artifacts are missing, critical claims lack evidence, or scope traceability is incomplete.

## Next Stage Rule

If validation passes, proceed to release. If validation fails, proceed to repair loop.
