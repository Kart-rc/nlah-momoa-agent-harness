#!/usr/bin/env bash
set -euo pipefail

RUN_DIR="${1:-}"
if [[ -z "$RUN_DIR" ]]; then
  echo "Usage: bash scripts/run_all_checks.sh <run-dir>"
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python "$SCRIPT_DIR/check_required_files.py" "$RUN_DIR"
python "$SCRIPT_DIR/validate_manifest.py" "$RUN_DIR"
python "$SCRIPT_DIR/validate_sections.py" --contract scope-contract "$RUN_DIR/SCOPE_CONTRACT.md"
python "$SCRIPT_DIR/validate_sections.py" --contract evidence "$RUN_DIR"
python "$SCRIPT_DIR/validate_sections.py" --contract release-packet "$RUN_DIR"

echo "All checks passed"
