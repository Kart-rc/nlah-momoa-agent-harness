# Getting Started

## Prerequisites

- Python 3.10+
- Bash shell

## 1) Initialize a run

```bash
python scripts/init_run.py --task examples/simple-doc-task/TASK.md --run-id demo-001
```

## 2) Review and refine scope

- Fill `runs/demo-001/SCOPE_CONTRACT.md`
- Fill `runs/demo-001/PLAN.md`
- Add traceability entries in `runs/demo-001/REQUIREMENT_TRACEABILITY.md`

## 3) Optionally create child workspaces

```bash
python scripts/create_child_workspace.py \
  --run-dir runs/demo-001 \
  --child-id phase-1-engineering \
  --task-contract runs/demo-001/PLAN.md
```

## 4) Run deterministic checks

```bash
bash scripts/run_all_checks.sh runs/demo-001
python scripts/validate_scope_contract.py runs/demo-001/SCOPE_CONTRACT.md
```

## 5) Close with release packet

- Ensure `IMPLEMENTATION_EVIDENCE.md` is complete.
- Ensure `VALIDATION_REPORT.md` includes gate outcomes.
- Ensure `RELEASE_PACKET.md` only contains true, evidence-backed claims.

## Suggested next steps

- Copy templates from `templates/task-types/github-issue/` when working issue flows.
- Add automated CI checks for script validators.
- Add schema checks as contracts mature.
