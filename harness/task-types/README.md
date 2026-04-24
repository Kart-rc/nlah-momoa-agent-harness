# Task-Type Catalog

Task types route common work into purpose-built workflows, artifacts, and
validation gates.

## Source of truth

The machine-readable catalog lives in [`registry.json`](./registry.json). Each
task type has a directory here containing:

- `SKILL.md` — prose skill document for humans and agents.
- `task-type.json` — machine-readable manifest consumed by scripts.

Scripts such as `init_run.py`, `check_required_files.py`, and
`validate_task_family_completeness.py` read the manifest and registry. To add
a new task type, see [`docs/adding-a-task-type.md`](../../docs/adding-a-task-type.md)
or run `python scripts/new_task_type.py --help`.

## Contract

Every task type must declare:

- purpose
- required inputs
- required artifacts
- workflow
- validation gates
- role model
- release expectations
