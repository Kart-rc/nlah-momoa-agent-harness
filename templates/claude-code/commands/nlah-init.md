---
description: Initialize a new NLAH-MoVE run workspace for the task at hand
argument-hint: <run-id> <task-type> [path-to-TASK.md]
---

Initialize an NLAH-MoVE run workspace.

Arguments: `$ARGUMENTS`

Interpretation:
- First token = `run-id` (short, kebab-case).
- Second token = `task-type` (must match an id in
  `@@HARNESS_DIR@@/harness/task-types/registry.json`).
- Third token (optional) = path to a `TASK.md`. If omitted, write a minimal
  `TASK.md` into `runs/<run-id>/TASK.md` from the current conversation's task
  description before running init (see
  `@@HARNESS_DIR@@/templates/TASK.md` for the shape).

Steps:
1. If no TASK.md path is supplied, create one at
   `runs/.pending/<run-id>/TASK.md` populated from the user's request.
2. Run:
   ```
   python @@HARNESS_DIR@@/scripts/init_run.py \
     --task <task-md-path> \
     --run-id <run-id> \
     --task-type <task-type>
   ```
3. Echo the run directory and the list of task-specific artifacts that were
   materialised.

If the task type is unknown, list the valid ids from `registry.json` and
ask the user to confirm one.
