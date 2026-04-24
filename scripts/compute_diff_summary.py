#!/usr/bin/env python3
"""Compute a deterministic git diff summary for changed files."""
from __future__ import annotations

import argparse
import json
import subprocess


def run_git(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], check=True, capture_output=True, text=True)
    return completed.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute git diff summary")
    parser.add_argument("--base", default="HEAD", help="Base ref for diff (default: HEAD)")
    parser.add_argument(
        "--output",
        default="",
        help="Optional output file path. When omitted, writes JSON to stdout.",
    )
    args = parser.parse_args()

    names = run_git(["diff", "--name-only", args.base]).splitlines()
    numstat_raw = run_git(["diff", "--numstat", args.base]).splitlines()

    files = []
    total_added = 0
    total_removed = 0
    for line in numstat_raw:
        if not line:
            continue
        added_s, removed_s, path = line.split("\t", 2)
        added = 0 if added_s == "-" else int(added_s)
        removed = 0 if removed_s == "-" else int(removed_s)
        total_added += added
        total_removed += removed
        files.append({"path": path, "added": added, "removed": removed})

    payload = {
        "base": args.base,
        "changed_files": [name for name in names if name],
        "files": files,
        "totals": {
            "file_count": len([name for name in names if name]),
            "added": total_added,
            "removed": total_removed,
        },
    }

    serialized = json.dumps(payload, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(serialized)
    else:
        print(serialized, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
