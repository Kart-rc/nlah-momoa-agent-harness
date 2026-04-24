#!/usr/bin/env python3
"""Initialize a file-backed NLAH-MoVE run workspace.

When ``--task-type`` is supplied, the task-type manifest at
``harness/task-types/<id>/task-type.json`` drives which task-specific
artifacts are materialised in the run directory. Task-specific artifacts
that have a hand-written template under ``templates/task-types/<dir>/``
are copied; anything else gets a minimal auto-generated skeleton so the
artifact list in the manifest stays the single source of truth.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _harness_lib import (  # noqa: E402
    append_jsonl,
    load_task_type_manifest,
    now_utc_iso,
    write_run_metadata,
)

COMMON_TEMPLATES = [
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


def filename_to_title(name: str) -> str:
    stem = name.rsplit(".", 1)[0]
    parts = stem.replace("-", "_").split("_")
    return " ".join(part.capitalize() for part in parts if part)


def materialise_artifact(
    artifact: str,
    run_dir: Path,
    task_type_templates_dir: Path | None,
    task_type_id: str | None,
) -> str:
    """Copy template if present, otherwise write a minimal skeleton.

    Returns the source description for logging.
    """
    destination = run_dir / artifact
    if task_type_templates_dir is not None:
        candidate = task_type_templates_dir / artifact
        if candidate.exists():
            shutil.copyfile(candidate, destination)
            return f"template:{candidate}"

    title = filename_to_title(artifact)
    hint = (
        f"_Auto-generated skeleton. Populate per "
        f"`harness/task-types/{task_type_id}/SKILL.md`._"
        if task_type_id
        else "_Auto-generated skeleton._"
    )
    destination.write_text(f"# {title}\n\n{hint}\n", encoding="utf-8")
    return "skeleton"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a NLAH-MoVE run workspace")
    parser.add_argument("--task", required=True, help="Path to a TASK.md file")
    parser.add_argument("--run-id", required=True, help="Run identifier under runs/")
    parser.add_argument("--runs-root", default="runs", help="Runs directory")
    parser.add_argument(
        "--task-type",
        default=None,
        help=(
            "Task-type id (see harness/task-types/registry.json). When set, task-specific "
            "artifacts from the manifest are also materialised."
        ),
    )
    parser.add_argument(
        "--validation-tier",
        type=int,
        default=None,
        help="Override validation tier. Defaults to the task-type's default tier.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    task_path = Path(args.task)
    if not task_path.exists():
        raise SystemExit(f"Task file not found: {task_path}")

    run_dir = repo_root / args.runs_root / args.run_id
    if run_dir.exists():
        raise SystemExit(f"Run already exists: {run_dir}")

    manifest = None
    task_type_templates_dir: Path | None = None
    if args.task_type:
        try:
            manifest = load_task_type_manifest(args.task_type, repo_root=SCRIPT_DIR.parent)
        except FileNotFoundError as exc:
            raise SystemExit(str(exc)) from exc
        templates_dir_name = manifest.get("templates_dir")
        if templates_dir_name:
            candidate = repo_root / "templates" / "task-types" / templates_dir_name
            if candidate.exists():
                task_type_templates_dir = candidate

    (run_dir / "state").mkdir(parents=True)
    (run_dir / "children").mkdir()
    (run_dir / "scratch").mkdir()
    (run_dir / "evidence").mkdir()
    (run_dir / "artifacts").mkdir()

    shutil.copyfile(task_path, run_dir / "TASK.md")

    templates_dir = repo_root / "templates"
    for name in COMMON_TEMPLATES:
        source = templates_dir / name
        if not source.exists():
            raise SystemExit(f"Missing common template: {source}")
        shutil.copyfile(source, run_dir / name)

    materialised_task_specific: list[dict] = []
    if manifest is not None:
        for artifact in manifest.get("required_artifacts", []):
            if artifact in COMMON_TEMPLATES or artifact == "RELEASE_PACKET.md":
                # Common templates already copied above.
                continue
            if (run_dir / artifact).exists():
                continue
            source = materialise_artifact(
                artifact, run_dir, task_type_templates_dir, manifest["id"]
            )
            materialised_task_specific.append({"artifact": artifact, "source": source})

    for ledger in LEDGERS:
        (run_dir / "state" / ledger).touch()

    validation_tier = args.validation_tier
    if validation_tier is None and manifest is not None:
        validation_tier = manifest.get("default_validation_tier")

    run_metadata = {
        "schema_version": "1.0",
        "run_id": args.run_id,
        "created_at": now_utc_iso(),
        "task_path": str(task_path),
        "task_type": args.task_type,
        "validation_tier": validation_tier,
    }
    write_run_metadata(run_dir, run_metadata)

    artifact_manifest = {
        "schema_version": "1.0",
        "run_id": args.run_id,
        "created_at": now_utc_iso(),
        "task_type": args.task_type,
        "artifacts": [],
    }
    (run_dir / "artifacts" / "manifest.json").write_text(
        json.dumps(artifact_manifest, indent=2) + "\n", encoding="utf-8"
    )

    append_jsonl(
        run_dir / "state" / "orchestration_ledger.jsonl",
        {
            "timestamp": now_utc_iso(),
            "event": "run_initialized",
            "run_id": args.run_id,
            "task": str(task_path),
            "task_type": args.task_type,
            "validation_tier": validation_tier,
            "task_specific_artifacts": materialised_task_specific,
        },
    )

    print(f"Initialized run workspace: {run_dir}")
    if args.task_type:
        print(f"  task_type: {args.task_type}")
        print(f"  validation_tier: {validation_tier}")
        if materialised_task_specific:
            print("  task-specific artifacts:")
            for entry in materialised_task_specific:
                print(f"    - {entry['artifact']} ({entry['source']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
