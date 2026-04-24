#!/usr/bin/env python3
"""Create an isolated child workspace under an initialized run."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a child workspace for a run")
    parser.add_argument("--run-dir", required=True, help="Path to parent run directory")
    parser.add_argument("--child-id", required=True, help="Child workspace identifier")
    parser.add_argument(
        "--task-contract",
        required=True,
        help="Path to task contract file copied into child contracts/WORK_PHASE_TASK.md",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        raise SystemExit(f"Run directory does not exist: {run_dir}")

    orchestration_ledger = run_dir / "state" / "orchestration_ledger.jsonl"
    if not orchestration_ledger.exists():
        raise SystemExit(f"Run does not appear initialized (missing {orchestration_ledger})")

    task_contract = Path(args.task_contract)
    if not task_contract.exists():
        raise SystemExit(f"Task contract not found: {task_contract}")

    child_dir = run_dir / "children" / args.child_id
    if child_dir.exists():
        raise SystemExit(f"Child workspace already exists: {child_dir}")

    (child_dir / "contracts").mkdir(parents=True)
    (child_dir / "responses").mkdir()
    (child_dir / "artifacts").mkdir()
    (child_dir / "state").mkdir()

    shutil.copyfile(run_dir / "TASK.md", child_dir / "TASK.md")
    shutil.copyfile(task_contract, child_dir / "contracts" / "WORK_PHASE_TASK.md")

    metadata = {
        "schema_version": "1.0",
        "child_id": args.child_id,
        "parent_run_dir": str(run_dir),
        "created_at": now_utc(),
        "status": "initialized",
    }
    (child_dir / "state" / "child_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    append_jsonl(
        orchestration_ledger,
        {
            "timestamp": now_utc(),
            "event": "child_workspace_created",
            "child_id": args.child_id,
            "child_dir": str(child_dir),
            "task_contract": str(task_contract),
        },
    )

    print(f"Created child workspace: {child_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
