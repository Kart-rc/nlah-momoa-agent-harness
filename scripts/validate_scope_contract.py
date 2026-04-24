#!/usr/bin/env python3
"""Validate SCOPE_CONTRACT.md (thin shim over validate_sections.py)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_sections import resolve_target, validate_file  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SCOPE_CONTRACT.md")
    parser.add_argument("scope_contract", help="Path to SCOPE_CONTRACT.md or run dir")
    args = parser.parse_args()
    return validate_file(resolve_target(args.scope_contract, "scope-contract"), "scope-contract")


if __name__ == "__main__":
    raise SystemExit(main())
