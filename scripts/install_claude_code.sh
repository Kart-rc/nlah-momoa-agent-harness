#!/usr/bin/env bash
# Install the NLAH-MoVE Claude Code integration (skill, slash commands,
# subagent) into a target repository's .claude/ directory.
#
# The installer substitutes @@HARNESS_DIR@@ in every file with the path where
# the harness assets live, so the generated files work regardless of install
# location.
set -euo pipefail

print_usage() {
  cat <<'USAGE'
Usage: install_claude_code.sh --target PATH [--harness-dir PATH] [--claude-dir NAME] [--force] [--dry-run]

Installs NLAH-MoVE as a Claude Code skill, slash commands, and subagent.

Options:
  --target PATH        Path inside the target repository (default: current directory)
  --harness-dir PATH   Path to the installed harness, relative to repo root
                       (default: .nlah-move-harness)
  --claude-dir NAME    Name of the Claude directory under repo root (default: .claude)
  --force              Overwrite existing files in the Claude Code surface
  --dry-run            Print actions without writing files
  -h, --help           Show this help
USAGE
}

TARGET_PATH="$(pwd)"
HARNESS_DIR=".nlah-move-harness"
CLAUDE_DIR_NAME=".claude"
FORCE=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET_PATH="$2"; shift 2 ;;
    --harness-dir) HARNESS_DIR="$2"; shift 2 ;;
    --claude-dir) CLAUDE_DIR_NAME="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) print_usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; print_usage >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! REPO_ROOT="$(git -C "$TARGET_PATH" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "Error: --target must be inside a Git repository. Received: $TARGET_PATH" >&2
  exit 1
fi

CLAUDE_DIR="$REPO_ROOT/$CLAUDE_DIR_NAME"
TEMPLATES_DIR="$SOURCE_ROOT/templates/claude-code"

if [[ ! -d "$TEMPLATES_DIR" ]]; then
  echo "Error: Claude Code templates missing at $TEMPLATES_DIR" >&2
  exit 1
fi

run_cmd() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

# Copy a file from the templates dir to the claude dir, substituting
# @@HARNESS_DIR@@. Refuses to overwrite unless --force.
install_templated_file() {
  local src="$1"
  local dst="$2"
  if [[ -e "$dst" && $FORCE -ne 1 ]]; then
    echo "Skipping existing file (use --force to overwrite): $dst"
    return 0
  fi
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] install $src -> $dst (substitute @@HARNESS_DIR@@=$HARNESS_DIR)"
    return 0
  fi
  mkdir -p "$(dirname "$dst")"
  # Use Python for portable, safe replacement (sed escaping is fragile).
  python - "$src" "$dst" "$HARNESS_DIR" <<'PY'
import sys
src, dst, harness_dir = sys.argv[1], sys.argv[2], sys.argv[3]
with open(src, encoding="utf-8") as f:
    content = f.read()
content = content.replace("@@HARNESS_DIR@@", harness_dir)
with open(dst, "w", encoding="utf-8") as f:
    f.write(content)
PY
}

echo "Installing NLAH-MoVE Claude Code integration"
echo "  Repo:        $REPO_ROOT"
echo "  Claude dir:  $CLAUDE_DIR"
echo "  Harness dir: $HARNESS_DIR"

# Skill
install_templated_file \
  "$TEMPLATES_DIR/skills/nlah-move/SKILL.md" \
  "$CLAUDE_DIR/skills/nlah-move/SKILL.md"

# Commands
for cmd_src in "$TEMPLATES_DIR/commands/"*.md; do
  cmd_name="$(basename "$cmd_src")"
  install_templated_file "$cmd_src" "$CLAUDE_DIR/commands/$cmd_name"
done

# Subagents
for agent_src in "$TEMPLATES_DIR/agents/"*.md; do
  agent_name="$(basename "$agent_src")"
  install_templated_file "$agent_src" "$CLAUDE_DIR/agents/$agent_name"
done

cat <<DONE

Claude Code integration installed.

Try:
  /nlah-validate-catalog
  /nlah-init demo-001 generic-documentation
  /nlah-check runs/demo-001

Or have Claude Code launch the independent validator:
  "Use the nlah-independent-validator subagent to validate runs/demo-001"
DONE
