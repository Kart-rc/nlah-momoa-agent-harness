#!/usr/bin/env python3
"""Initialize a file-backed NLAH-MoVE run workspace."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_TEMPLATES = [
    "SCOPE_CONTRACT.md",
    "PLAN.md",
    "IMPLEMENTATION_EVIDENCE.md",
    "VALIDATION_REPORT.md",
    "REQUIREMENT_TRACEABILITY.md",
    "RELEASE_PACKET.md",
    "RESPONSE.md",
]

LEDGERS = [
    "task_history.jsonl",
    "orchestration_ledger.jsonl",
    "validation_ledger.jsonl",
    "dissent_log.jsonl",
]


def write_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a NLAH-MoVE run workspace")
    parser.add_argument("--task", required=True, help="Path to a TASK.md file")
    parser.add_argument("--run-id", required=True, help="Run identifier under runs/")
    parser.add_argument("--runs-root", default="runs", help="Runs directory")
    args = parser.parse_args()

    repo_root = Path.cwd()
    task_path = Path(args.task)
    if not task_path.exists():
        raise SystemExit(f"Task file not found: {task_path}")

    run_dir = repo_root / args.runs_root / args.run_id
    if run_dir.exists():
        raise SystemExit(f"Run already exists: {run_dir}")

    (run_dir / "state").mkdir(parents=True)
    (run_dir / "children").mkdir()
    (run_dir / "scratch").mkdir()
    (run_dir / "evidence").mkdir()
    (run_dir / "artifacts").mkdir()

    shutil.copyfile(task_path, run_dir / "TASK.md")

    templates_dir = repo_root / "templates"
    for name in REQUIRED_TEMPLATES:
        source = templates_dir / name
        if not source.exists():
            raise SystemExit(f"Missing template: {source}")
        shutil.copyfile(source, run_dir / name)

    for ledger in LEDGERS:
        (run_dir / "state" / ledger).touch()

    manifest = {
        "schema_version": "1.0",
        "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": [],
    }
    (run_dir / "artifacts" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    write_jsonl(
        run_dir / "state" / "orchestration_ledger.jsonl",
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "run_initialized",
            "run_id": args.run_id,
            "task": str(task_path),
        },
    )

    print(f"Initialized run workspace: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
