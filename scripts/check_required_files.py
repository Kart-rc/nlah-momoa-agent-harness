#!/usr/bin/env python3
"""Check required NLAH-MoVE run files.

The common run-level artifact list is enforced for every run. If the run was
initialised with a task type (recorded in ``state/run_metadata.json``), the
task-type manifest's ``required_artifacts`` list is also enforced.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _harness_lib import load_run_metadata, load_task_type_manifest  # noqa: E402

COMMON_REQUIRED = [
    "TASK.md",
    "SCOPE_CONTRACT.md",
    "PLAN.md",
    "IMPLEMENTATION_EVIDENCE.md",
    "VALIDATION_REPORT.md",
    "REQUIREMENT_TRACEABILITY.md",
    "RELEASE_PACKET.md",
    "RESPONSE.md",
    "artifacts/manifest.json",
    "state/orchestration_ledger.jsonl",
    "state/validation_ledger.jsonl",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check required run files")
    parser.add_argument("run_dir", help="Run directory to validate")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    required = list(COMMON_REQUIRED)

    metadata = load_run_metadata(run_dir)
    task_type_id = metadata.get("task_type") if metadata else None
    if task_type_id:
        try:
            manifest = load_task_type_manifest(task_type_id, repo_root=SCRIPT_DIR.parent)
        except FileNotFoundError as exc:
            print(f"Task-type manifest error: {exc}")
            return 1
        for artifact in manifest.get("required_artifacts", []):
            if artifact not in required:
                required.append(artifact)

    missing = [path for path in required if not (run_dir / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1
    print(
        f"Required file check passed ({len(required)} files, task_type={task_type_id or 'none'})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
