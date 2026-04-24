#!/usr/bin/env python3
"""Data-driven markdown section validator.

All three legacy validators (scope contract, evidence, release packet) now
share this implementation. The section contracts live in one place so adding
a new section-driven validator is a data change, not new code.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _harness_lib import check_required_headings  # noqa: E402


SECTION_CONTRACTS: dict[str, dict] = {
    "scope-contract": {
        "target": "SCOPE_CONTRACT.md",
        "sections": [
            "# Scope Contract",
            "## In Scope",
            "## Out of Scope",
            "## Acceptance Criteria",
            "## Required Artifacts",
            "## Risks",
        ],
        "require_checklist": True,
    },
    "evidence": {
        "target": "IMPLEMENTATION_EVIDENCE.md",
        "sections": [
            "## Summary",
            "## Files Created or Modified",
            "## Claims and Evidence",
        ],
        "require_checklist": False,
    },
    "release-packet": {
        "target": "RELEASE_PACKET.md",
        "sections": [
            "## Release Verdict",
            "## Summary",
            "## Scope Satisfied",
            "## Artifacts",
            "## Validation Performed",
            "## Evidence References",
            "## Open Risks",
        ],
        "require_checklist": False,
    },
    "task-family": {
        "target": "SKILL.md",
        "sections": [
            "## Purpose",
            "## Required Inputs",
            "## Required Artifacts",
            "## Workflow",
            "## Validation Gates",
            "## Role Model",
            "## End-to-End Flow Coverage",
            "## Release Expectations",
        ],
        "require_checklist": False,
    },
}


def validate_file(path: Path, contract_name: str) -> int:
    contract = SECTION_CONTRACTS[contract_name]
    if not path.exists():
        print(f"Missing file: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    missing = check_required_headings(text, contract["sections"])
    if missing:
        print(f"{contract_name} missing required sections in {path}:")
        for heading in missing:
            print(f"- {heading}")
        return 1
    if contract.get("require_checklist"):
        if not any(token in text for token in ("- [ ]", "- [x]", "- [X]")):
            print(f"{contract_name} should include at least one checklist item in {path}")
            return 1
    print(f"{contract_name} check passed ({path})")
    return 0


def resolve_target(path_arg: str, contract_name: str) -> Path:
    """Accept either a direct file path or a run dir and resolve via target filename."""
    path = Path(path_arg)
    target_filename = SECTION_CONTRACTS[contract_name]["target"]
    if path.is_dir():
        return path / target_filename
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate markdown sections against a contract")
    parser.add_argument(
        "--contract",
        required=True,
        choices=sorted(SECTION_CONTRACTS.keys()),
        help="Section contract to apply",
    )
    parser.add_argument(
        "target",
        help="Run directory or file path. For 'task-family', pass the SKILL.md directly.",
    )
    args = parser.parse_args()

    target = resolve_target(args.target, args.contract)
    return validate_file(target, args.contract)


if __name__ == "__main__":
    raise SystemExit(main())
