#!/usr/bin/env bash
set -euo pipefail

print_usage() {
  cat <<'USAGE'
Usage: setup_harness.sh [--target PATH] [--install-dir NAME] [--force] [--dry-run] [--for-claude-code] [--claude-dir NAME]

Installs the NLAH-MoVE harness into a Git repository.

Options:
  --target PATH        Any path inside the target repository (default: current directory)
  --install-dir NAME   Directory name under the repo root (default: .nlah-move-harness)
  --force              Overwrite existing files in the install directory
  --dry-run            Print actions without writing files
  --for-claude-code    Also install the Claude Code skill, slash commands, and
                       subagent into the target repo's .claude/ directory.
  --claude-dir NAME    Name of the Claude directory (default: .claude). Only
                       used when --for-claude-code is set.
  -h, --help           Show this help
USAGE
}

TARGET_PATH="$(pwd)"
INSTALL_DIR_NAME=".nlah-move-harness"
FORCE=0
DRY_RUN=0
FOR_CLAUDE_CODE=0
CLAUDE_DIR_NAME=".claude"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET_PATH="$2"
      shift 2
      ;;
    --install-dir)
      INSTALL_DIR_NAME="$2"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --for-claude-code)
      FOR_CLAUDE_CODE=1
      shift
      ;;
    --claude-dir)
      CLAUDE_DIR_NAME="$2"
      shift 2
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      print_usage >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! REPO_ROOT="$(git -C "$TARGET_PATH" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "Error: --target must be inside a Git repository. Received: $TARGET_PATH" >&2
  exit 1
fi

INSTALL_DIR="$REPO_ROOT/$INSTALL_DIR_NAME"

if [[ -e "$INSTALL_DIR" && $FORCE -ne 1 ]]; then
  echo "Error: install directory already exists: $INSTALL_DIR" >&2
  echo "Re-run with --force to overwrite." >&2
  exit 1
fi

SOURCES=(
  "harness"
  "templates"
  "scripts"
  "docs"
  "examples"
  "runs/.gitkeep"
)

run_cmd() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

echo "Installing NLAH-MoVE harness"
echo "  Source: $SOURCE_ROOT"
echo "  Repo:   $REPO_ROOT"
echo "  Target: $INSTALL_DIR"

if [[ $FORCE -eq 1 ]]; then
  run_cmd rm -rf "$INSTALL_DIR"
fi
run_cmd mkdir -p "$INSTALL_DIR"

for rel_path in "${SOURCES[@]}"; do
  src="$SOURCE_ROOT/$rel_path"
  dst="$INSTALL_DIR/$rel_path"

  if [[ ! -e "$src" ]]; then
    echo "Warning: skipping missing source path: $src" >&2
    continue
  fi

  run_cmd mkdir -p "$(dirname "$dst")"
  run_cmd cp -a "$src" "$dst"
done

README_SRC="$SOURCE_ROOT/README.md"
README_DST="$INSTALL_DIR/HARNESS_README.md"
if [[ -f "$README_SRC" ]]; then
  run_cmd cp -a "$README_SRC" "$README_DST"
fi

if [[ $FOR_CLAUDE_CODE -eq 1 ]]; then
  CC_ARGS=(--target "$TARGET_PATH" --harness-dir "$INSTALL_DIR_NAME" --claude-dir "$CLAUDE_DIR_NAME")
  if [[ $FORCE -eq 1 ]]; then CC_ARGS+=(--force); fi
  if [[ $DRY_RUN -eq 1 ]]; then CC_ARGS+=(--dry-run); fi
  run_cmd bash "$SCRIPT_DIR/install_claude_code.sh" "${CC_ARGS[@]}"
fi

cat <<DONE

Install complete.

Next steps:
  1) Review harness docs at: $INSTALL_DIR/HARNESS_README.md
  2) Initialize a run from your repo root with:
     python $INSTALL_DIR/scripts/init_run.py --task $INSTALL_DIR/examples/simple-doc-task/TASK.md --run-id demo-001
DONE

if [[ $FOR_CLAUDE_CODE -eq 1 ]]; then
  cat <<DONE
  3) In Claude Code, try: /nlah-validate-catalog
DONE
fi
