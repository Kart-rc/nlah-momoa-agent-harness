#!/usr/bin/env bash
# End-to-end smoke test for the harness scripts.
#
# Exercises: task-family completeness, `init_run.py` with and without a task
# type, `new_task_type.py` scaffolding, and `check_required_files.py` for a
# task-type-aware run. Intended to run in CI or locally before pushing.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

TMP_RUNS="$(mktemp -d)"
trap 'rm -rf "$TMP_RUNS"' EXIT

echo "[1/5] validate_task_family_completeness"
python scripts/validate_task_family_completeness.py

echo "[2/5] init_run (no task-type)"
python scripts/init_run.py \
  --task examples/simple-doc-task/TASK.md \
  --run-id smoke-generic \
  --runs-root "$TMP_RUNS"
test -f "$TMP_RUNS/smoke-generic/SCOPE_CONTRACT.md"
test -f "$TMP_RUNS/smoke-generic/state/run_metadata.json"

echo "[3/5] init_run (github-issue, with hand-written templates)"
python scripts/init_run.py \
  --task examples/github-issue-bug/TASK.md \
  --run-id smoke-gh \
  --runs-root "$TMP_RUNS" \
  --task-type github-issue
for f in ISSUE_INTAKE.md ISSUE_CLASSIFICATION.md ROOT_CAUSE_ANALYSIS.md PATCH_PLAN.md VALIDATION_EVIDENCE.md PR_SUMMARY.md; do
  test -f "$TMP_RUNS/smoke-gh/$f" || { echo "Missing $f"; exit 1; }
done

echo "[4/5] init_run (research-analysis, skeleton generation)"
python scripts/init_run.py \
  --task examples/simple-doc-task/TASK.md \
  --run-id smoke-research \
  --runs-root "$TMP_RUNS" \
  --task-type research-analysis
for f in RESEARCH_QUESTION.md SOURCE_LOG.md HYPOTHESES.md ANALYSIS_NOTES.md FINDINGS_SUMMARY.md LIMITATIONS.md; do
  test -f "$TMP_RUNS/smoke-research/$f" || { echo "Missing $f"; exit 1; }
done
python scripts/check_required_files.py "$TMP_RUNS/smoke-research"

echo "[5/5] new_task_type scaffolding"
SCAFFOLD_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_RUNS" "$SCAFFOLD_DIR"' EXIT
cp -a harness "$SCAFFOLD_DIR/"
cp -a scripts "$SCAFFOLD_DIR/"
(
  cd "$SCAFFOLD_DIR"
  python scripts/new_task_type.py \
    --id smoke-task-type \
    --display-name "Smoke Task Type" \
    --artifact SMOKE_INTAKE.md \
    --artifact SMOKE_PLAN.md \
    --keyword smoke
  python scripts/validate_task_family_completeness.py
)

echo "Harness smoke test passed."
