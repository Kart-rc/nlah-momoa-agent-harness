#!/usr/bin/env python3
"""Validate minimal structure and quality markers in SCOPE_CONTRACT.md."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "# Scope Contract",
    "## In Scope",
    "## Out of Scope",
    "## Acceptance Criteria",
    "## Required Artifacts",
    "## Risks",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SCOPE_CONTRACT.md")
    parser.add_argument("scope_contract", help="Path to SCOPE_CONTRACT.md")
    args = parser.parse_args()

    scope_path = Path(args.scope_contract)
    if not scope_path.exists():
        print(f"Missing scope contract: {scope_path}")
        return 1

    content = scope_path.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in content]
    if missing:
        print("Scope contract missing required sections:")
        for item in missing:
            print(f"- {item}")
        return 1

    has_checklist = "- [ ]" in content or "- [x]" in content or "- [X]" in content
    if not has_checklist:
        print("Scope contract should include at least one checklist item for acceptance tracking")
        return 1

    print("Scope contract check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
