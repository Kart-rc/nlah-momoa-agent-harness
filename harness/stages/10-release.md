# Stage 10 — Release

## Owner

Release Certifier

## Purpose

Produce the final response and release packet only after validation gates pass.

## Inputs

- `SCOPE_CONTRACT.md`
- `VALIDATION_REPORT.md`
- `REQUIREMENT_TRACEABILITY.md`
- `IMPLEMENTATION_EVIDENCE.md`
- `artifacts/manifest.json`

## Outputs

- `RESPONSE.md`
- `RELEASE_PACKET.md`
- release ledger entry

## Gate

Release requires a passing validation verdict or an explicit `COMPLETE_WITH_RISK` decision with accepted residual risks.

## Release Packet Minimum Contents

- summary
- scope satisfied
- artifacts changed or created
- validation performed
- evidence references
- open risks
- follow-up recommendations
