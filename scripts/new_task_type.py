#!/usr/bin/env python3
"""Scaffold a new NLAH-MoVE task type.

Creates:

* ``harness/task-types/<id>/SKILL.md`` — prose skill document stub.
* ``harness/task-types/<id>/task-type.json`` — machine-readable manifest.
* Adds the new task type to ``harness/task-types/registry.json``.

Idempotent with ``--force``; otherwise fails if the task type already exists.
Running ``validate_task_family_completeness.py`` on the fresh scaffold must
pass — that's the acceptance test for this script.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _harness_lib import load_registry, task_types_root  # noqa: E402

SKILL_TEMPLATE = """# {display_name} Harness

## Purpose

{purpose}

## Required Inputs

- {input_hint}

## Required Artifacts

{artifacts_block}

## Workflow

1. Intake and scope contract
2. Plan and risk review
3. Implement or produce
4. Validate
5. Repair if needed
6. Prepare release evidence

## Validation Gates

- acceptance criteria are satisfied
- deterministic checks pass or are explicitly waived
- risks and tradeoffs are documented
- unrelated changes are avoided

## Role Model

- orchestrator: coordinate lifecycle and compliance gates
- planner: produce execution plan proportional to risk
- implementer: complete changes and evidence
- reviewer: challenge assumptions and quality
- independent validator: verify outcomes without implementer bias
- release certifier: confirm completion against scope contract

## End-to-End Flow Coverage

This task family executes all harness stages with scaled rigor:

1. classify scope and risk
2. resolve ambiguities that affect outcome
3. plan and execute
4. run validation and independent verification
5. repair if needed and certify release

## Release Expectations

Release must include what was produced, why, how validated, and known limitations.
"""


def build_skill(display_name: str, required_artifacts: list[str]) -> str:
    artifact_lines = "\n".join(f"- `{name}`" for name in required_artifacts)
    return SKILL_TEMPLATE.format(
        display_name=display_name,
        purpose=f"Execute {display_name.lower()} tasks with scope discipline and validation rigor.",
        input_hint="primary objective and acceptance criteria",
        artifacts_block=artifact_lines,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new NLAH-MoVE task type")
    parser.add_argument("--id", required=True, help="Task-type id (kebab-case)")
    parser.add_argument("--display-name", required=True, help="Human-readable name")
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Required artifact filename (can be passed multiple times)",
    )
    parser.add_argument(
        "--default-validation-tier",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
    )
    parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Routing keyword (can be passed multiple times)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite if exists")
    args = parser.parse_args()

    repo_root = SCRIPT_DIR.parent
    root = task_types_root(repo_root)
    task_dir = root / args.id

    if task_dir.exists() and not args.force:
        raise SystemExit(f"Task type already exists: {task_dir}. Re-run with --force to overwrite.")

    required_artifacts = args.artifact or [
        f"{args.id.upper().replace('-', '_')}_INTAKE.md",
        "IMPLEMENTATION_PLAN.md",
    ]

    task_dir.mkdir(parents=True, exist_ok=True)
    skill_text = build_skill(args.display_name, required_artifacts)
    (task_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")

    manifest = {
        "schema_version": "1.0",
        "id": args.id,
        "display_name": args.display_name,
        "default_validation_tier": args.default_validation_tier,
        "required_inputs": ["primary_objective"],
        "required_artifacts": required_artifacts,
        "templates_dir": None,
        "role_model": {
            "orchestrator": "coordinate lifecycle and compliance gates",
            "planner": "produce execution plan proportional to risk",
            "implementer": "complete changes and evidence",
            "reviewer": "challenge assumptions and quality",
            "independent_validator": "verify outcomes without implementer bias",
            "release_certifier": "confirm completion against scope contract",
        },
        "validation_gates": [
            "acceptance criteria are satisfied",
            "deterministic checks pass or are explicitly waived",
            "risks and tradeoffs are documented",
        ],
        "release_requirements": ["what was produced", "why", "how validated", "known limitations"],
    }
    (task_dir / "task-type.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    registry_path = root / "registry.json"
    registry = load_registry(repo_root=repo_root)
    existing_ids = {entry["id"] for entry in registry["task_types"]}
    entry = {
        "id": args.id,
        "display_name": args.display_name,
        "keywords": args.keyword,
        "variants": [],
        "default_validation_tier": args.default_validation_tier,
    }
    if args.id in existing_ids:
        registry["task_types"] = [
            entry if existing["id"] == args.id else existing
            for existing in registry["task_types"]
        ]
    else:
        registry["task_types"].append(entry)
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    print(f"Scaffolded task type '{args.id}' at {task_dir}")
    print("Next steps:")
    print(f"  1) Edit {task_dir}/SKILL.md prose.")
    print(f"  2) Adjust {task_dir}/task-type.json required_artifacts if needed.")
    print(f"  3) Add an example at examples/{args.id}-example/TASK.md.")
    print("  4) Run: python scripts/validate_task_family_completeness.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
