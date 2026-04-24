#!/usr/bin/env python3
"""Validate that implementation evidence is present enough for release review."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = ["## Summary", "## Files Created or Modified", "## Claims and Evidence"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate implementation evidence")
    parser.add_argument("run_dir")
    args = parser.parse_args()

    evidence_path = Path(args.run_dir) / "IMPLEMENTATION_EVIDENCE.md"
    if not evidence_path.exists():
        print(f"Missing evidence file: {evidence_path}")
        return 1
    text = evidence_path.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing:
        print(f"Evidence file missing sections: {missing}")
        return 1
    print("Evidence structure check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
