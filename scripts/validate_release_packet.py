#!/usr/bin/env python3
"""Validate release packet structure."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Release Verdict",
    "## Summary",
    "## Scope Satisfied",
    "## Artifacts",
    "## Validation Performed",
    "## Evidence References",
    "## Open Risks",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release packet")
    parser.add_argument("run_dir")
    args = parser.parse_args()

    release_path = Path(args.run_dir) / "RELEASE_PACKET.md"
    if not release_path.exists():
        print(f"Missing release packet: {release_path}")
        return 1
    text = release_path.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing:
        print(f"Release packet missing sections: {missing}")
        return 1
    print("Release packet structure check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
