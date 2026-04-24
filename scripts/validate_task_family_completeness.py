#!/usr/bin/env python3
"""Validate task-family SKILL docs and manifests.

For each task type under ``harness/task-types/*/``:

* ``SKILL.md`` must contain the required section headings.
* ``task-type.json`` must parse and expose the fields scripts depend on.

Also verifies ``harness/task-types/registry.json`` lists every task type and
that every registry entry has a matching directory and manifest.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _harness_lib import load_registry, load_task_type_manifest, task_types_root  # noqa: E402
from validate_sections import SECTION_CONTRACTS, check_required_headings  # noqa: E402

REQUIRED_MANIFEST_KEYS = {
    "schema_version",
    "id",
    "display_name",
    "default_validation_tier",
    "required_artifacts",
    "role_model",
    "validation_gates",
}


def main() -> int:
    repo_root = SCRIPT_DIR.parent
    root = task_types_root(repo_root)
    skill_paths = sorted(root.glob("*/SKILL.md"))
    if not skill_paths:
        print("No task-family SKILL.md files found.")
        return 1

    failures: list[str] = []
    skill_sections = SECTION_CONTRACTS["task-family"]["sections"]

    for skill_path in skill_paths:
        text = skill_path.read_text(encoding="utf-8")
        missing_headings = check_required_headings(text, skill_sections)
        if missing_headings:
            failures.append(
                f"{skill_path.relative_to(repo_root)}: missing headings {missing_headings}"
            )
        manifest_path = skill_path.parent / "task-type.json"
        if not manifest_path.exists():
            failures.append(f"{manifest_path.relative_to(repo_root)}: missing manifest")
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{manifest_path.relative_to(repo_root)}: invalid JSON ({exc})")
            continue
        missing_keys = REQUIRED_MANIFEST_KEYS - set(manifest)
        if missing_keys:
            failures.append(
                f"{manifest_path.relative_to(repo_root)}: missing keys {sorted(missing_keys)}"
            )
        if manifest.get("id") != skill_path.parent.name:
            failures.append(
                f"{manifest_path.relative_to(repo_root)}: id mismatch with directory"
            )

    try:
        registry = load_registry(repo_root=repo_root)
    except FileNotFoundError as exc:
        failures.append(str(exc))
    else:
        registry_ids = {entry["id"] for entry in registry.get("task_types", [])}
        dir_ids = {path.parent.name for path in skill_paths}
        for missing in dir_ids - registry_ids:
            failures.append(f"registry.json: task type '{missing}' is present on disk but not registered")
        for missing in registry_ids - dir_ids:
            failures.append(f"registry.json: task type '{missing}' is registered but has no directory")
        for entry in registry.get("task_types", []):
            tier = entry.get("default_validation_tier")
            if tier is None:
                failures.append(f"registry.json: entry '{entry.get('id')}' missing default_validation_tier")
            try:
                load_task_type_manifest(entry["id"], repo_root=repo_root)
            except FileNotFoundError as exc:
                failures.append(str(exc))

    if failures:
        print("Task family completeness validation failed:")
        for line in failures:
            print(f"- {line}")
        return 1

    print(
        f"Validated {len(skill_paths)} task families: "
        f"SKILL.md sections, manifests, and registry all consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
