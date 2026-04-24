---
description: Validate the NLAH-MoVE task-type catalog (registry + manifests + SKILL.md headings)
---

Validate that every task type under `@@HARNESS_DIR@@/harness/task-types/` is
self-consistent: SKILL.md has the required section headings, `task-type.json`
has the required keys, and `registry.json` lists exactly the on-disk set.

Run:

```
python @@HARNESS_DIR@@/scripts/validate_task_family_completeness.py
```

If any entry fails, report the failing task type and which check failed (missing
heading, missing manifest key, registry drift, etc.). Do not mutate the catalog
without explicit confirmation from the user.
