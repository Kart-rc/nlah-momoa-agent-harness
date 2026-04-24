# Validation Tiers

## Tier 0 — Direct

Use for low-risk tasks. Required gates: basic response completeness.

## Tier 1 — Standard

Use for normal documentation, presentations, and analysis. Required gates: artifact existence, scope coverage, and clarity review.

## Tier 2 — Critical

Use for coding, architecture, migrations, design decisions, and high-impact technical recommendations. Required gates: scope traceability, evidence, deterministic checks, independent review, and release packet.

## Tier 3 — High Assurance

Use for vulnerability fixes, security, compliance, financial-risk, privacy-risk, or production-impacting changes. Required gates: all Tier 2 gates plus security review, stricter evidence, residual-risk notes, and rollback plan.

## Tier 4 — Research / Benchmark

Use for harness experiments, ablations, benchmark comparisons, and scientific claims. Required gates: reproducibility notes, metrics, experiment design, limitations, and data provenance.

## Default Tier Selection

- GitHub bug or enhancement: Tier 2
- Vulnerability or dependency security issue: Tier 3
- Version upgrade: Tier 2 or Tier 3 depending on blast radius
- Brownfield feature: Tier 2
- Greenfield application: Tier 2
- Leadership or pitch deck: Tier 1
- Technical stakeholder deck: Tier 1 or Tier 2
- Requirements to architecture: Tier 2
