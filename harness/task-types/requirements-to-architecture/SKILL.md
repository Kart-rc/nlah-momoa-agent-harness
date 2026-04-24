# Requirements to Architecture Harness

## Purpose

Convert business requirements into architecture artifacts, HLD, LLD, ADRs, and traceability.

## Required Inputs

- business requirement
- target users
- constraints
- existing environment, if brownfield
- expected scale
- security and compliance needs
- timeline or delivery expectations

## Required Artifacts

- `BRD_ANALYSIS.md`
- `AMBIGUITY_REGISTER.md`
- `CAPABILITY_MAP.md`
- `FUNCTIONAL_REQUIREMENTS.md`
- `NON_FUNCTIONAL_REQUIREMENTS.md`
- `ARCHITECTURE_OPTIONS.md`
- `HLD.md`
- `ADR.md`
- `LLD.md`
- `TRACEABILITY_MATRIX.md`
- `REVIEW_REPORT.md`
- `RELEASE_PACKET.md`

## Workflow

1. BRD analysis
2. Ambiguity resolution
3. Capability map
4. Functional requirements
5. Non-functional requirements
6. Architecture options
7. HLD
8. ADRs
9. LLD
10. Traceability review

## Validation Gates

- requirements map to capabilities
- capabilities map to architecture components
- NFRs are addressed
- major trade-offs are documented
- HLD and LLD are consistent
- assumptions and risks are explicit

## Role Model

- orchestrator: maintain traceability from requirements to decisions
- planner: structure architecture exploration and decision cadence
- implementer: produce architecture artifacts and rationale
- reviewer: challenge assumptions, trade-offs, and constraints
- independent validator: verify consistency and requirement coverage
- release certifier: certify architecture packet for stakeholder use

## End-to-End Flow Coverage

This task family executes all harness stages with architecture focus:

1. intake and requirement normalization
2. ambiguity resolution for non-functional constraints
3. planning, optioning, and ADR-driven decisions
4. synthesis into HLD/LLD and traceability artifacts
5. independent validation and dissent closure
6. release certification with risks and open decisions

## Release Expectations

Release must include traceability matrix, selected architecture with rationale, unresolved risks, and decision follow-ups.
