#!/usr/bin/env python3
"""Validate IMPLEMENTATION_EVIDENCE.md (thin shim over validate_sections.py)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_sections import resolve_target, validate_file  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate implementation evidence")
    parser.add_argument("run_dir")
    args = parser.parse_args()
    return validate_file(resolve_target(args.run_dir, "evidence"), "evidence")


if __name__ == "__main__":
    raise SystemExit(main())
