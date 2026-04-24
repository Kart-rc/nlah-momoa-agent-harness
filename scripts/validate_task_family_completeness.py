#!/usr/bin/env python3
"""Validate task-family SKILL docs for end-to-end NLAH-MoVE coverage."""

from pathlib import Path
import sys

REQUIRED_HEADINGS = [
    "## Purpose",
    "## Required Inputs",
    "## Required Artifacts",
    "## Workflow",
    "## Validation Gates",
    "## Role Model",
    "## End-to-End Flow Coverage",
    "## Release Expectations",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    task_types_dir = root / "harness" / "task-types"
    skill_paths = sorted(task_types_dir.glob("*/SKILL.md"))

    if not skill_paths:
        print("No task-family SKILL.md files found.")
        return 1

    missing = {}
    for skill_path in skill_paths:
        text = skill_path.read_text(encoding="utf-8")
        missing_headings = [h for h in REQUIRED_HEADINGS if h not in text]
        if missing_headings:
            missing[skill_path] = missing_headings

    if missing:
        print("Task family completeness validation failed:")
        for path, headings in missing.items():
            print(f"- {path.relative_to(root)}")
            for heading in headings:
                print(f"  * missing: {heading}")
        return 1

    print(f"Validated {len(skill_paths)} task families: all required sections present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
