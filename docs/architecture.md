# NLAH-MoVE Architecture

## Goals

NLAH-MoVE provides a reusable harness for complex task execution with explicit contracts, stage gates, durable state, and validator separation.

## System Components

- **Policy layer (`harness/`)**
  - stage definitions
  - role definitions
  - room definitions
  - skill modules
  - task-type workflows
- **Deterministic scripts (`scripts/`)**
  - run initialization
  - child workspace creation
  - scope and structure validation
  - diff and evidence helpers
- **Contracts and templates (`templates/`)**
  - run-level artifacts
  - task-family artifacts
- **Run state (`runs/<run-id>/`)**
  - ledgers, evidence, child packets, integrated artifacts

## Runtime Model

1. Initialize run workspace from a task and template set.
2. Resolve ambiguity and lock scope contract.
3. Build plan and assign work phases to rooms.
4. Execute phases directly or via child workspaces.
5. Integrate outputs and update traceability.
6. Run validation gauntlet and repair loop if needed.
7. Produce release packet and response.

## State Surfaces

- `state/task_history.jsonl` — task and stage transitions.
- `state/orchestration_ledger.jsonl` — orchestration events and delegation decisions.
- `state/validation_ledger.jsonl` — gate verdicts and validation findings.
- `state/dissent_log.jsonl` — dissent points and resolution records.
- `artifacts/manifest.json` — tracked artifacts, ownership, and status.

## Child Workspace Pattern

Child workspaces isolate phase execution:

- `children/<child-id>/TASK.md`
- `children/<child-id>/contracts/WORK_PHASE_TASK.md`
- `children/<child-id>/responses/`
- `children/<child-id>/artifacts/`

Parent run integration only promotes explicit artifacts listed in promotion notes.

## Safety Invariants

- No release without validation evidence.
- No scope expansion without contract updates.
- No unresolved critical dissent at release.
- No validator self-repair for failed independent checks.
