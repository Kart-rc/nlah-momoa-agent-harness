# NLAH-MoVE Agent Harness

NLAH-MoVE is a **markdown-first, contract-first agent harness** that combines Natural-Language Agent Harness structure with MoMoA-style validation, context isolation, work phases, dissent handling, and release certification.

It is designed for human+agent workflows where process and quality gates are explicit in version-controlled files.

---

## Why this harness exists

Most agent workflows fail in one of three places:

1. **Scope drift** (the task changes silently).
2. **Missing evidence** (claims are not traceable to artifacts).
3. **Weak validation** (the same role implements and "approves" its own work).

NLAH-MoVE addresses these with:

- **Natural-language harness logic** in Markdown (roles, stages, recovery paths).
- **Deterministic scripts** for mechanical checks.
- **File-backed state** for durability and replay.
- **Verifier separation** between implementation and validation.
- **MoVE-style adversarial review** before release.

---

## Install into any Git repository

Use the setup script to install the harness into **any path inside any Git repo**.

```bash
bash /path/to/nlah-momoa-agent-harness/scripts/setup_harness.sh --target /path/to/your/repo
```

By default, this creates:

```text
<your-repo>/.nlah-move-harness/
```

### Setup script options

```bash
bash scripts/setup_harness.sh --help
```

- `--target PATH` path inside the target repository (default: current directory)
- `--install-dir NAME` destination folder name under repo root (default: `.nlah-move-harness`)
- `--force` overwrite an existing installation
- `--dry-run` preview actions without writing files

---

## Quick start (after installation)

```bash
python .nlah-move-harness/scripts/init_run.py \
  --task .nlah-move-harness/examples/simple-doc-task/TASK.md \
  --run-id demo-001

bash .nlah-move-harness/scripts/run_all_checks.sh runs/demo-001

python .nlah-move-harness/scripts/create_child_workspace.py \
  --run-dir runs/demo-001 \
  --child-id phase-1 \
  --task-contract runs/demo-001/PLAN.md
```

The run workspace includes copied templates, ledgers, an artifact manifest, and placeholders for evidence and release documentation.

---

## Lifecycle

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

---

## Repository layout

```text
harness/              Harness policy, stages, roles, rooms, skills, task-type catalog
templates/            Reusable run artifacts and task-type-specific templates
scripts/              Deterministic validation and workspace helper scripts
docs/                 Explanatory docs for architecture and execution flow
examples/             Example TASK.md inputs by task family
runs/                 Generated run workspaces, ignored except for .gitkeep
```

---

## Validation tiers

- **Tier 0 — Direct**: low-risk answers or small edits.
- **Tier 1 — Standard**: normal documentation, presentation, or analysis work.
- **Tier 2 — Critical**: code, architecture, migration, or high-impact design work.
- **Tier 3 — High Assurance**: security, vulnerability, compliance, or major production changes.
- **Tier 4 — Research / Benchmark**: controlled evaluations and harness experiments.

---

## Common task families

1. GitHub issue resolution (bug, enhancement, vulnerability, dependency upgrade).
2. Brownfield feature delivery.
3. Greenfield application delivery.
4. Presentation development (leadership, pitch, technical stakeholder).
5. Requirements-to-architecture (BRD analysis, HLD, LLD, ADR, traceability).

---

## Definition of done

A run is complete only when:

1. The scope contract is satisfied.
2. Required artifacts exist.
3. Validation gates pass.
4. Evidence is written.
5. Critical dissent is resolved.
6. The release packet is complete.
