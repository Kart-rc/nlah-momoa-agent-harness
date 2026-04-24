#!/usr/bin/env python3
"""Check required NLAH-MoVE run files."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED = [
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
    missing = [path for path in REQUIRED if not (run_dir / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("Required file check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
