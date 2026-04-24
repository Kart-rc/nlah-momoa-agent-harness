"""Shared helpers for NLAH-MoVE harness scripts.

Keep this module dependency-free (stdlib only). It is imported by the other
scripts under ``scripts/`` to avoid re-implementing manifest loading, JSONL
append, and markdown section detection in three places.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

HARNESS_ROOT_NAME = "harness"
TASK_TYPES_DIR_NAME = "task-types"
REGISTRY_FILENAME = "registry.json"
MANIFEST_FILENAME = "task-type.json"
RUN_METADATA_FILENAME = "run_metadata.json"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def task_types_root(repo_root: Path | None = None) -> Path:
    root = repo_root or repo_root_from_script()
    return root / HARNESS_ROOT_NAME / TASK_TYPES_DIR_NAME


def load_registry(repo_root: Path | None = None) -> dict:
    path = task_types_root(repo_root) / REGISTRY_FILENAME
    if not path.exists():
        raise FileNotFoundError(f"Task-type registry not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_task_type_manifest(task_type_id: str, repo_root: Path | None = None) -> dict:
    path = task_types_root(repo_root) / task_type_id / MANIFEST_FILENAME
    if not path.exists():
        raise FileNotFoundError(
            f"Task-type manifest not found for '{task_type_id}': {path}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_run_metadata(run_dir: Path) -> dict | None:
    path = run_dir / "state" / RUN_METADATA_FILENAME
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_run_metadata(run_dir: Path, metadata: dict) -> None:
    path = run_dir / "state" / RUN_METADATA_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check_required_headings(text: str, required: list[str]) -> list[str]:
    """Return the headings in ``required`` that are not present in ``text``.

    Matching is line-anchored to reduce false positives from prose mentions of
    the same string. We intentionally keep this simple; swap for a markdown
    AST parser if stronger guarantees are needed.
    """
    lines = {line.strip() for line in text.splitlines()}
    return [heading for heading in required if heading.strip() not in lines]
