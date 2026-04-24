# Adversarial Review — NLAH-MoVE Agent Harness

This review was performed against the state of `main` as of April 2026 with the
explicit goal of reducing friction when adding new task types and cleaning up
duplication across markdown policy, Python scripts, and templates.

## TL;DR

The harness has strong *policy* (clear stage/role/room separation, explicit
prohibitions, file-backed state) but weak *mechanics* (no single source of
truth for task-type metadata, three near-identical heading validators, no
task-type-aware init, github-issue is the only task type with specialised
templates).

Net effect: adding a new task type today requires touching **four** files in
non-obvious order, none of which are machine-readable. A new contributor has
to read prose in `task-router.md`, edit prose in `task-types/README.md`, copy
a SKILL.md, and remember to add both templates and an example. Nothing
enforces consistency between them.

## Findings

### 1. No single source of truth for task-type metadata
Each task type is declared as prose in `harness/task-types/<id>/SKILL.md`,
re-listed in `harness/task-types/README.md`, re-listed again in
`harness/task-router.md`, and (partially) reified in `templates/task-types/`.
The list has already drifted: `task-types/README.md` lists nine families,
`task-router.md` lists ten, and `task-router.md` refers to
`github-issue/vulnerability` and `github-issue/dependency-upgrade`
subdirectories that don't exist.

### 2. `init_run.py` is task-type-blind
It always copies the same eight generic templates regardless of the declared
task type. A github-issue run therefore starts without `ISSUE_INTAKE.md`,
`ROOT_CAUSE_ANALYSIS.md`, `PATCH_PLAN.md`, `PR_SUMMARY.md`, or
`VALIDATION_EVIDENCE.md` — all of which the task-type's SKILL.md declares
required. The required-artifacts contract is declarative but never enforced.

### 3. `check_required_files.py` is task-type-blind
It hardcodes the same eight generic files. A github-issue run can pass the
required-files gate while missing every task-specific artifact declared in
its own SKILL.md.

### 4. Three validators duplicate a single pattern
`validate_scope_contract.py`, `validate_evidence.py`, and
`validate_release_packet.py` all do "read file, assert substring for each
required heading, fail otherwise." The list of headings is the only
difference. One data-driven validator would remove ~60 lines of code and a
drift vector.

### 5. Ledger helpers are duplicated
`init_run.py` defines `write_jsonl`; `create_child_workspace.py` defines
`append_jsonl`; both do the same thing. `datetime.now(timezone.utc).isoformat()`
is open-coded in both.

### 6. Asymmetric task-type template support
Only `github-issue` ships with task-specific templates. The other eight
families silently fall through to the generic templates, and nothing flags
this.

### 7. Substring-based markdown validation is fragile
Headings are checked with `"## Section" in content`. Re-formatting, adding a
leading space, or changing header level silently breaks validation. A
markdown-aware check (at minimum: line-anchored + case-folded) is cheap and
removes a surprise.

### 8. `setup_harness.sh` uses `eval "$@"`
`run_cmd` in `scripts/setup_harness.sh` concatenates with `eval`, which
breaks on paths containing spaces or shell metacharacters and adds a small
injection surface. Arrays would be both safer and simpler.

### 9. Inconsistent executable bits
Four of ten Python scripts are `chmod +x`; six are not. Invocations in the
README use `python <path>` which hides the problem, but the inconsistency is
noise.

### 10. `compute_diff_summary.py` is dead weight
It is not referenced from any other script, template, stage, or doc. Either
hook it into `run_all_checks.sh` (as an artifact producer for evidence) or
remove it.

### 11. `BATCH_COMMIT_NOTE.md` is a stale implementation note
A single sentence at the repo root telling future commits to batch files.
That is commit-message / PR-description content, not a tracked artifact.

### 12. Validation tiers are declared but not wired
`validation-tiers.md` specifies different gate sets per tier, but
`run_all_checks.sh` runs the same checks for every run.

### 13. No smoke test
Nothing exercises `init_run.py` → `run_all_checks.sh` end-to-end. Schema
changes can break existing examples with no signal.

### 14. `RESPONSE.md` + `REQUIREMENT_TRACEABILITY.md` are mandatory for all runs
These make sense for Tier 2+ but are ceremony for Tier 0 / Tier 1 runs. The
required-files list should itself be tier-aware or task-type-aware.

## Response (what this PR changes)

The changes in this branch are additive and backwards-compatible; nothing
deletes or renames an existing markdown contract.

1. **`harness/task-types/registry.json`** — machine-readable list of task
   types with ids, variants, keywords, default tier. Replaces the two prose
   lists as source of truth.
2. **`harness/task-types/<id>/task-type.json`** — per-task-type manifest
   declaring required artifacts, templates dir, default tier, role model,
   validation gates. SKILL.md stays as human-readable prose; the manifest is
   the contract scripts consume.
3. **`scripts/_harness_lib.py`** — shared helpers (manifest loader, JSONL
   append, markdown heading check). Kills duplication across scripts.
4. **`scripts/init_run.py`** — accepts `--task-type`; when set, copies the
   task-type's templates in addition to common ones, writes
   `state/run_metadata.json` so downstream scripts can recover the type.
5. **`scripts/check_required_files.py`** — reads `run_metadata.json` +
   the task-type manifest; validates task-specific required artifacts in
   addition to the common set.
6. **`scripts/validate_sections.py`** — one data-driven section validator
   replacing three near-identical ones. The three old scripts stay as
   1-line shims for backwards compatibility.
7. **`scripts/new_task_type.py`** — scaffolds a new task type end-to-end:
   creates the directory, writes a SKILL.md stub + task-type.json, adds an
   entry to `registry.json`, and optionally creates a template directory.
8. **`scripts/test_harness.sh`** — exercises the pipeline against every
   example. Catches schema drift.
9. **`setup_harness.sh`** — `eval "$@"` replaced with a small wrapper that
   uses arrays.
10. **`docs/adding-a-task-type.md`** — one-page extension guide, pointing
    at `new_task_type.py`.
11. **`BATCH_COMMIT_NOTE.md`** — removed.
12. Executable bit normalised across `scripts/*.py` and `scripts/*.sh`.

Items deliberately **not** changed:

- Stage, role, and room markdown — they're fine as policy documents; no
  duplication worth the churn.
- Validation-tier gating in `run_all_checks.sh` — needs a product decision
  about which gates are tier-scoped; flagged in this review for follow-up.
- Ledger compaction — flagged, not solved.
- Markdown AST parsing — flagged, not solved. Line-anchored substring
  matching is "good enough" until we need structural validation.
