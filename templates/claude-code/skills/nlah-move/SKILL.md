---
name: nlah-move
description: Use when the user requests complex, multi-stage work that benefits from explicit scope contracts, durable artifacts, separated validator, and release certification. Typical triggers include "fix this GitHub issue", "add this feature", "scaffold a new application", "write this architecture doc", "build this presentation", or any request where silent scope drift or missing evidence would be unsafe. Not needed for trivial Q&A or one-line edits.
---

# NLAH-MoVE Agent Harness

Activate this skill to execute the task through the NLAH-MoVE harness, which
forces stage gates, file-backed state, and validator separation. The harness
lives at `@@HARNESS_DIR@@`.

## When to use
- Multi-stage tasks: intake → plan → implement → validate → release.
- Tasks that must produce traceable evidence.
- Work that spans multiple phases or child delegations.

## When not to use
- Trivial answers, one-liners, or purely conversational requests.

## Workflow

1. **Classify.** Read `@@HARNESS_DIR@@/harness/task-types/registry.json`; match
   the user request against `keywords`. Pick the most specific task type.
2. **Initialize.** Run:
   ```
   python @@HARNESS_DIR@@/scripts/init_run.py \
     --task <path-to-TASK.md> \
     --run-id <short-id> \
     --task-type <registry-id> \
     --runs-root runs
   ```
   The run directory is created under `runs/<run-id>/`, with common + task-
   type-specific artifacts staged from the manifest.
3. **Populate the scope contract.** Edit `runs/<run-id>/SCOPE_CONTRACT.md`
   with in-scope items, out-of-scope items, acceptance criteria, and risks.
   The scope contract is the frozen source of truth for later stages.
4. **Plan.** Edit `runs/<run-id>/PLAN.md` listing work phases, each with
   owner, output, and validation gate.
5. **Delegate work phases.** For isolated phases, run:
   ```
   python @@HARNESS_DIR@@/scripts/create_child_workspace.py \
     --run-dir runs/<run-id> \
     --child-id phase-N \
     --task-contract runs/<run-id>/PLAN.md
   ```
6. **Implement.** Populate each required artifact listed in the task-type
   manifest (`@@HARNESS_DIR@@/harness/task-types/<id>/task-type.json`) plus
   `IMPLEMENTATION_EVIDENCE.md`.
7. **Validate.** Run the validation gauntlet:
   ```
   bash @@HARNESS_DIR@@/scripts/run_all_checks.sh runs/<run-id>
   ```
   Failures produce repair tickets — fix, re-run, repeat.
8. **Release.** Populate `RELEASE_PACKET.md` and `RESPONSE.md`. Do not claim
   completion unless every required-files gate passes and every critical
   dissent in `state/dissent_log.jsonl` is resolved.

## Role discipline

The validator is never the implementer. If you wrote the evidence, you do not
sign off on it — launch a separate sub-agent (see
`@@HARNESS_DIR@@/harness/roles/`) for validation and release certification.

## References

- Entry point: `@@HARNESS_DIR@@/harness/SKILL.md`
- Stage definitions: `@@HARNESS_DIR@@/harness/stages/`
- Role definitions: `@@HARNESS_DIR@@/harness/roles/`
- Task-type catalog: `@@HARNESS_DIR@@/harness/task-types/registry.json`
- Failure taxonomy: `@@HARNESS_DIR@@/harness/failure-taxonomy.md`
- Adding a task type: `@@HARNESS_DIR@@/docs/adding-a-task-type.md`
