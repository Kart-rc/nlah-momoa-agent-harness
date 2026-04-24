#!/usr/bin/env python3
"""Validate artifacts/manifest.json for a run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate run artifact manifest")
    parser.add_argument("run_dir")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    manifest_path = run_dir / "artifacts" / "manifest.json"
    if not manifest_path.exists():
        print(f"Missing manifest: {manifest_path}")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid manifest JSON: {exc}")
        return 1

    required_keys = {"schema_version", "run_id", "created_at", "artifacts"}
    missing = required_keys - set(manifest)
    if missing:
        print(f"Manifest missing keys: {sorted(missing)}")
        return 1
    if not isinstance(manifest["artifacts"], list):
        print("Manifest 'artifacts' must be a list")
        return 1

    print("Manifest check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
