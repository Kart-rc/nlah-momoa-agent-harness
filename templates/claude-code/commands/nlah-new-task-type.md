---
description: Scaffold a new NLAH-MoVE task type
argument-hint: <id> "<Display Name>" [artifact1,artifact2,...]
---

Scaffold a new task type end-to-end.

Arguments: `$ARGUMENTS`

Interpretation:
- First token = task-type id (kebab-case). Must not collide with an existing
  id in `@@HARNESS_DIR@@/harness/task-types/registry.json`.
- Second token = quoted display name.
- Third token (optional) = comma-separated required artifact filenames.
- Fourth token onward = routing keywords (each in quotes).

Run:

```
python @@HARNESS_DIR@@/scripts/new_task_type.py \
  --id <id> \
  --display-name "<Display Name>" \
  --artifact <A1> --artifact <A2> ... \
  --keyword "<kw1>" --keyword "<kw2>" ...
```

Then validate:

```
python @@HARNESS_DIR@@/scripts/validate_task_family_completeness.py
```

Walk the user through the three follow-up edits:
1. Flesh out `@@HARNESS_DIR@@/harness/task-types/<id>/SKILL.md`.
2. Adjust required artifacts in `task-type.json` if the initial list is off.
3. Add an example task at `@@HARNESS_DIR@@/examples/<id>-example/TASK.md`.
