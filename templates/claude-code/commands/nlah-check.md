---
description: Run the NLAH-MoVE validation gauntlet on a run directory
argument-hint: <run-dir>
---

Run the validation gauntlet on an NLAH-MoVE run directory.

Arguments: `$ARGUMENTS`

If no argument is supplied, default to the most recently modified directory
under `runs/`.

Execute:

```
bash @@HARNESS_DIR@@/scripts/run_all_checks.sh <run-dir>
```

Report the first failing gate verbatim. Do not paper over failures — classify
each failure using `@@HARNESS_DIR@@/harness/failure-taxonomy.md` and either
open a repair task or escalate per the taxonomy.

On success, also recap:
- task type and validation tier (from `<run-dir>/state/run_metadata.json`),
- number of artifacts listed in `<run-dir>/artifacts/manifest.json`,
- unresolved entries in `<run-dir>/state/dissent_log.jsonl`.
