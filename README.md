# NLAH-MoVE Agent Harness

NLAH-MoVE is a **markdown-first, contract-first agent harness** that combines Natural-Language Agent Harness structure with MoMoA-style validation, context isolation, work phases, dissent handling, and release certification.

It is designed for human+agent workflows where process and quality gates are explicit in version-controlled files.

---

## Why this harness exists

Most agent workflows fail in one of three places:

1. **Scope drift** (the task changes silently).
2. **Missing evidence** (claims are not traceable to artifacts).
3. **Weak validation** (the same role implements and "approves" its own work).

NLAH-MoVE addresses these with:

- **Natural-language harness logic** in Markdown (roles, stages, recovery paths).
- **Deterministic scripts** for mechanical checks.
- **File-backed state** for durability and replay.
- **Verifier separation** between implementation and validation.
- **MoVE-style adversarial review** before release.

---

## Install

The harness installs into any path inside any Git repository. There are two
installation modes: standalone (scripts only) and Claude Code (scripts plus a
Claude Code skill, slash commands, and a subagent).

### Standalone

```bash
bash /path/to/nlah-momoa-agent-harness/scripts/setup_harness.sh \
  --target /path/to/your/repo
```

Creates:

```text
<your-repo>/.nlah-move-harness/
  harness/      policy (stages, roles, rooms, task-type catalog)
  templates/    run-level + task-type-specific artifact templates
  scripts/      init, check, new-task-type, validators, smoke test
  docs/         architecture + extension guide
  examples/     example TASK.md per task family
```

### Claude Code

Install the harness *and* a Claude Code skill + slash commands + subagent in
one step:

```bash
bash /path/to/nlah-momoa-agent-harness/scripts/setup_harness.sh \
  --target /path/to/your/repo \
  --for-claude-code
```

This adds the following under your repo's `.claude/` directory:

```text
.claude/
  skills/nlah-move/SKILL.md             activates the harness on matching tasks
  commands/nlah-init.md                 /nlah-init <run-id> <task-type> [task.md]
  commands/nlah-check.md                /nlah-check <run-dir>
  commands/nlah-new-task-type.md        /nlah-new-task-type <id> "Display" ...
  commands/nlah-validate-catalog.md     /nlah-validate-catalog
  agents/nlah-independent-validator.md  independent validator subagent
```

Already have the harness installed and just want the Claude Code surface?

```bash
bash .nlah-move-harness/scripts/install_claude_code.sh --target .
```

### Claude Code quickstart (setup → install → run)

Use this when your goal is to run the harness primarily from Claude Code.

1) **Open a terminal at your repository root**

```bash
cd /path/to/your/repo
```

2) **Install the harness with Claude Code integration**

```bash
bash /path/to/nlah-momoa-agent-harness/scripts/setup_harness.sh \
  --target . \
  --for-claude-code
```

3) **Confirm the install**

```bash
test -f .nlah-move-harness/scripts/init_run.py && echo "Harness installed"
test -f .claude/skills/nlah-move/SKILL.md && echo "Claude skill installed"
test -f .claude/commands/nlah-init.md && echo "Slash commands installed"
```

4) **Start Claude Code in this repo**

```bash
claude
```

5) **Initialize a run from Claude Code**

In Claude Code, run:

```text
/nlah-init demo-001 generic-coding
```

If you already have a task file, provide it explicitly:

```text
/nlah-init demo-001 generic-coding path/to/TASK.md
```

6) **Do the implementation work, then run checks**

```text
/nlah-check runs/demo-001
```

If checks fail, address the reported artifact gaps and run `/nlah-check` again
until all gates pass.

7) **(Optional) Ask for an independent validation pass**

```text
Use the nlah-independent-validator subagent to validate runs/demo-001.
```

The validator writes `VALIDATION_REPORT.md` with a release verdict.

### Antigravity + Windsurf quickstart

Antigravity and Windsurf do not currently have a dedicated installer in this
repo (like `--for-claude-code`), but you can use the harness reliably with a
shared setup:

1) **Install the harness into your repository**

```bash
cd /path/to/your/repo
bash /path/to/nlah-momoa-agent-harness/scripts/setup_harness.sh --target .
```

2) **Run from repo root so relative paths resolve**

```bash
pwd
# should be /path/to/your/repo
```

3) **Create and initialize a run**

```bash
python .nlah-move-harness/scripts/init_run.py \
  --task path/to/TASK.md \
  --run-id demo-001 \
  --task-type generic-coding
```

4) **In Antigravity or Windsurf, instruct the agent to follow the harness**

Use this as your first message in a task:

```text
Use .nlah-move-harness/harness/SKILL.md as the operating workflow.
Work only inside runs/demo-001/.
Keep SCOPE_CONTRACT.md and PLAN.md updated before implementation.
Write evidence to IMPLEMENTATION_EVIDENCE.md and VALIDATION_EVIDENCE.md.
Before finalizing, run:
bash .nlah-move-harness/scripts/run_all_checks.sh runs/demo-001
```

5) **Validate deterministically before you accept output**

```bash
bash .nlah-move-harness/scripts/run_all_checks.sh runs/demo-001
```

6) **(Optional) add helper aliases for parity with Claude Code commands**

```bash
alias nlah-init='python .nlah-move-harness/scripts/init_run.py'
alias nlah-check='bash .nlah-move-harness/scripts/run_all_checks.sh'
```

Then you can use:

```bash
nlah-init --task path/to/TASK.md --run-id demo-001 --task-type generic-coding
nlah-check runs/demo-001
```

### Setup script options

```bash
bash scripts/setup_harness.sh --help
```

| Flag | Default | Effect |
|---|---|---|
| `--target PATH` | cwd | Any path inside the target repository |
| `--install-dir NAME` | `.nlah-move-harness` | Folder name under repo root |
| `--for-claude-code` | off | Also install the Claude Code skill/commands/agent |
| `--claude-dir NAME` | `.claude` | Claude directory name |
| `--force` | off | Overwrite an existing installation |
| `--dry-run` | off | Print actions without writing files |

---

## Invocation examples

All examples assume the harness was installed at `.nlah-move-harness/` and
that you're running commands from the repo root.

### A. Generic task (no task type)

```bash
# Point at any TASK.md; the harness creates runs/demo-001/ with common templates.
python .nlah-move-harness/scripts/init_run.py \
  --task .nlah-move-harness/examples/simple-doc-task/TASK.md \
  --run-id demo-001

# Run the full validation gauntlet (required files, manifest, sections).
bash .nlah-move-harness/scripts/run_all_checks.sh runs/demo-001
```

### B. Task-type-aware run (recommended)

```bash
# Materialises task-specific artifacts (ISSUE_INTAKE.md, ROOT_CAUSE_ANALYSIS.md,
# PATCH_PLAN.md, PR_SUMMARY.md, etc.) and records task-type + default tier
# in state/run_metadata.json so downstream checks enforce the right contract.
python .nlah-move-harness/scripts/init_run.py \
  --task .nlah-move-harness/examples/github-issue-bug/TASK.md \
  --run-id gh-214 \
  --task-type github-issue

ls runs/gh-214/
# TASK.md  SCOPE_CONTRACT.md  PLAN.md  IMPLEMENTATION_EVIDENCE.md ...
# ISSUE_INTAKE.md  ISSUE_CLASSIFICATION.md  ROOT_CAUSE_ANALYSIS.md
# PATCH_PLAN.md  VALIDATION_EVIDENCE.md  PR_SUMMARY.md

# Populate SCOPE_CONTRACT.md, PLAN.md, and the task-type artifacts.
# Then:
bash .nlah-move-harness/scripts/run_all_checks.sh runs/gh-214
```

### C. Delegating an isolated phase

```bash
python .nlah-move-harness/scripts/create_child_workspace.py \
  --run-dir runs/gh-214 \
  --child-id phase-1-reproduce \
  --task-contract runs/gh-214/PLAN.md

# Child gets its own contracts/, responses/, artifacts/, state/ under
# runs/gh-214/children/phase-1-reproduce/.
```

### D. Adding a new task type

```bash
python .nlah-move-harness/scripts/new_task_type.py \
  --id bug-bash \
  --display-name "Bug Bash" \
  --artifact BUG_BASH_INTAKE.md \
  --artifact BUG_BASH_FINDINGS.md \
  --artifact BUG_BASH_REPORT.md \
  --keyword "bug bash" \
  --keyword "hackathon" \
  --default-validation-tier 1

python .nlah-move-harness/scripts/validate_task_family_completeness.py
bash .nlah-move-harness/scripts/test_harness.sh
```

See [`docs/adding-a-task-type.md`](docs/adding-a-task-type.md) for the full
extension guide.

### E. Smoke-testing the whole pipeline

```bash
bash .nlah-move-harness/scripts/test_harness.sh
```

Exercises task-family completeness, `init_run.py` with and without a task
type, skeleton generation for task types without hand-written templates,
`new_task_type.py` scaffolding, and the Claude Code install. Suitable for CI.

---

## Using the harness from Claude Code

After installing with `--for-claude-code`, the following are available inside
a Claude Code session rooted at your repo:

### Recommended day-to-day flow in Claude Code

1. Create a run with `/nlah-init <run-id> <task-type> [task.md]`.
2. Complete artifacts in `runs/<run-id>/` (`SCOPE_CONTRACT.md`, `PLAN.md`,
   implementation evidence, plus task-type artifacts).
3. Run `/nlah-check runs/<run-id>` to execute the deterministic gauntlet.
4. Fix any failed gates and re-run `/nlah-check`.
5. Before release, invoke `nlah-independent-validator` for a separated verdict.

### Slash commands

| Command | What it does |
|---|---|
| `/nlah-init <run-id> <task-type> [task.md]` | Initialise a run workspace for the task at hand. If no `TASK.md` is supplied, Claude writes one from the current conversation. |
| `/nlah-check <run-dir>` | Run the validation gauntlet. Reports the first failing gate and classifies it against the failure taxonomy. |
| `/nlah-new-task-type <id> "Display" [artifacts] [keywords]` | Scaffold a new task type and validate the catalog. |
| `/nlah-validate-catalog` | Validate the task-type catalog (registry + manifests + SKILL.md headings). |

Example session:

```
User:   /nlah-init gh-214 github-issue
Claude: Writes a TASK.md from the conversation, runs init_run.py, reports:
          runs/gh-214/ with 6 task-specific artifacts materialised from templates.

User:   Fix issue #214 per runs/gh-214/TASK.md.
Claude: (activates the nlah-move skill, populates SCOPE_CONTRACT, PLAN,
         implements, fills IMPLEMENTATION_EVIDENCE and PATCH_PLAN)

User:   /nlah-check runs/gh-214
Claude: Reports any failing gates and proposed repair tickets.
```

### Skill (auto-activates)

The `nlah-move` skill activates on prompts that match multi-stage, evidence-
heavy work (bug fixes, features, architecture, presentations, research). You
don't invoke it directly — describe the task and Claude decides whether the
harness is appropriate. The skill's description is intentionally specific so
it doesn't fire on trivial requests.

### Subagent

The `nlah-independent-validator` subagent reads an in-progress run and
produces an honest verdict without editing artifacts. Invoke it explicitly:

```
Use the nlah-independent-validator subagent to validate runs/gh-214.
```

The subagent runs the deterministic checks, verifies each acceptance
criterion is traced to evidence, flags unresolved dissent, and writes
`VALIDATION_REPORT.md` with a `PASS` / `PASS_WITH_CONDITIONS` / `FAIL`
verdict.

---

## Lifecycle

```text
Task Router
  -> Intake
  -> Ambiguity Resolution
  -> Scope Contract
  -> Planning
  -> Plan Review
  -> Work Phase Selection
  -> Work Phase Execution
  -> Integration
  -> Validation Gauntlet
  -> Repair Loop
  -> Release Certification
```

---

## Repository layout

```text
harness/              Harness policy, stages, roles, rooms, skills, task-type catalog
templates/            Reusable run artifacts, task-type templates, Claude Code surface
scripts/              Deterministic validation and workspace helper scripts
docs/                 Explanatory docs for architecture and execution flow
examples/             Example TASK.md inputs by task family
runs/                 Generated run workspaces, ignored except for .gitkeep
```

---

## Validation tiers

- **Tier 0 — Direct**: low-risk answers or small edits.
- **Tier 1 — Standard**: normal documentation, presentation, or analysis work.
- **Tier 2 — Critical**: code, architecture, migration, or high-impact design work.
- **Tier 3 — High Assurance**: security, vulnerability, compliance, or major production changes.
- **Tier 4 — Research / Benchmark**: controlled evaluations and harness experiments.

---

## Task families

The machine-readable catalog lives in
[`harness/task-types/registry.json`](harness/task-types/registry.json). At the
time of writing:

1. `github-issue` (bug, enhancement, vulnerability, dependency-upgrade, build/test-failure, perf, docs)
2. `brownfield-feature`
3. `greenfield-application`
4. `presentation` (leadership, pitch, technical-stakeholder, roadmap, architecture-review, incident-review)
5. `requirements-to-architecture`
6. `research-analysis`
7. `generic-documentation`
8. `generic-coding`
9. `requirements-to-prototype-options`

Each has a sibling `task-type.json` manifest declaring required artifacts,
default validation tier, role model, and validation gates. This manifest is
what scripts consume; the prose `SKILL.md` is what humans and agents read.

---

## Definition of done

A run is complete only when:

1. The scope contract is satisfied.
2. Required artifacts exist (common + task-type-specific).
3. Validation gates pass.
4. Evidence is written.
5. Critical dissent is resolved.
6. The release packet is complete.
