# Stage 09 — Repair Loop

## Owner

Integrator with validator separation

## Purpose

Repair failed gates narrowly without restarting the entire run.

## Inputs

- failed validation report
- failure taxonomy classification
- affected artifacts

## Outputs

- repaired artifacts
- updated evidence
- updated validation ledger

## Rules

- Repair only the failed gate unless the scope contract or plan is invalid.
- Validators must not repair their own findings.
- If the same failure repeats more than twice, escalate to overseer.
- If artifacts change, rerun full release validation before completion.

## Next Stage Rule

Return to validation gauntlet after repair.
