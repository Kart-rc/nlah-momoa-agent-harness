# Stage 07 — Integration

## Owner

Integrator

## Purpose

Merge outputs from multiple phases or child workspaces into a coherent run state and prepare for validation gauntlet.

## Inputs

- produced phase artifacts
- child response packets
- `artifacts/manifest.json`
- `REQUIREMENT_TRACEABILITY.md`

## Outputs

- integrated artifacts in run workspace
- updated `artifacts/manifest.json`
- updated `REQUIREMENT_TRACEABILITY.md`
- `INTEGRATION_NOTES.md` (recommended)

## Gate

Integrated state is internally consistent: artifact paths exist, manifest entries match files, and traceability references integrated outputs.

## Next Stage Rule

Proceed to validation gauntlet when integration gate passes; otherwise route to targeted repair.
