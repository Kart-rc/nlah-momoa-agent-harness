#!/usr/bin/env bash
set -euo pipefail

RUN_DIR="${1:-}"
if [[ -z "$RUN_DIR" ]]; then
  echo "Usage: bash scripts/run_all_checks.sh <run-dir>"
  exit 2
fi

python scripts/check_required_files.py "$RUN_DIR"
python scripts/validate_manifest.py "$RUN_DIR"
python scripts/validate_evidence.py "$RUN_DIR"
python scripts/validate_release_packet.py "$RUN_DIR"

echo "All checks passed"
