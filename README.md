# NLAH-MoVE Agent Harness

NLAH-MoVE is a markdown-first, contract-first agent harness template that combines Natural-Language Agent Harness structure with MoMoA-style validation, context isolation, work phases, dissent, and release certification.

This repository is designed for humans or agent runtimes that can read markdown control files, create durable run workspaces, invoke deterministic scripts, and enforce validation gates.

## Core Ideas

- **Natural-language harness logic**: orchestration, roles, gates, and recovery policies are explicit markdown artifacts.
- **Deterministic adapters**: scripts handle mechanical checks such as required files, manifests, evidence, and release packets.
- **File-backed state**: important run state is written to path-addressable ledgers and artifacts.
- **Verifier separation**: implementation and validation are intentionally separated.
- **MoVE validation overlay**: Mixture-of-Validators Execution adds adversarial review, independent validators, and overseer escalation.

## Quick Start

```bash
python scripts/init_run.py --task examples/simple-doc-task/TASK.md --run-id demo-001
bash scripts/run_all_checks.sh runs/demo-001
python scripts/create_child_workspace.py --run-dir runs/demo-001 --child-id phase-1 --task-contract runs/demo-001/PLAN.md
```

The generated run workspace contains copied templates, ledgers, an artifact manifest, and placeholders for evidence and release documentation.

## Harness Lifecycle

```text
Task Router
  -> Intake
  -> Ambiguity Resolution
  -> Scope Contract
  -> Planning
  -> Plan Review
  -> Work Phase Selection
  -> Work Phase Execution
  -> Integration
  -> Validation Gauntlet
  -> Repair Loop
  -> Release Certification
```

## Repository Layout

```text
harness/              Natural-language harness policy, stages, roles, rooms, skills, and task-type catalog
templates/            Reusable run artifacts and task-type-specific templates
schemas/              JSON schemas for contracts, ledgers, manifests, and validation reports
scripts/              Deterministic validation and workspace helper scripts
adapters/             Markdown contracts for runtime adapters and checkers
examples/             Concrete example tasks and expected artifacts
evaluations/          Ablation and scorecard scaffolding
runs/                 Generated run workspaces, ignored except for .gitkeep
```

## Validation Tiers

- **Tier 0 — Direct**: low-risk answers or small edits.
- **Tier 1 — Standard**: normal documentation, presentation, or analysis work.
- **Tier 2 — Critical**: code, architecture, migration, or high-impact design work.
- **Tier 3 — High Assurance**: security, vulnerability, compliance, or major production changes.
- **Tier 4 — Research / Benchmark**: controlled evaluations, ablations, or harness experiments.

## Common Task Families

The task router supports reusable harness patterns for:

1. GitHub issue resolution: bug, enhancement, vulnerability, dependency upgrade.
2. Brownfield feature delivery.
3. Greenfield application delivery.
4. Presentations: leadership, pitch, and technical stakeholder decks.
5. Requirements-to-architecture: BRD analysis, HLD, LLD, ADR, and traceability.

## Definition of Done

A run is not complete until:

1. The scope contract is satisfied.
2. Required artifacts exist.
3. Validation gates pass.
4. Evidence is written.
5. Critical dissent is resolved.
6. A release packet is complete.
