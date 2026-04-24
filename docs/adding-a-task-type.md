# Adding a Task Type

A task type is a family of work the harness knows how to orchestrate end to
end: intake, planning, implementation, validation, and release. Adding a new
one should take about five minutes.

## 1. Scaffold

```bash
python scripts/new_task_type.py \
  --id my-task-type \
  --display-name "My Task Type" \
  --artifact MY_INTAKE.md \
  --artifact MY_PLAN.md \
  --artifact MY_REPORT.md \
  --keyword "my keyword" \
  --default-validation-tier 2
```

This creates:

- `harness/task-types/my-task-type/SKILL.md` — prose stub you edit.
- `harness/task-types/my-task-type/task-type.json` — machine-readable manifest.
- Appends an entry to `harness/task-types/registry.json`.

## 2. Edit the prose

Open `harness/task-types/my-task-type/SKILL.md` and replace the stub
workflow, role model, and validation gates with the real ones. Keep the
section headings — the task-family completeness check enforces them.

## 3. (Optional) Hand-written templates

By default every required artifact gets an auto-generated skeleton at
`init_run.py` time. If you want richer starter content, add:

```
templates/task-types/my-task-type/MY_INTAKE.md
templates/task-types/my-task-type/MY_PLAN.md
```

Then point `templates_dir` in the manifest to `"my-task-type"`.

## 4. Add an example

Create `examples/my-task-type-example/TASK.md` mirroring the shape of the
existing examples. The smoke test exercises examples, so this catches drift.

## 5. Verify

```bash
python scripts/validate_task_family_completeness.py
bash scripts/test_harness.sh
```

Both should pass.

## What actually drives behaviour

- `task-type.json` is the contract. `init_run.py` and
  `check_required_files.py` read it to materialise and enforce task-specific
  artifacts.
- `registry.json` is the enumeration. Routing logic reads it; the
  completeness check cross-references it with the on-disk directories.
- `SKILL.md` is prose for humans and agents. Scripts do not parse it beyond
  checking the required section headings exist.

Rule of thumb: if scripts need to know it, it goes in the JSON. If humans or
agents need to reason about it, it goes in the SKILL.md.
