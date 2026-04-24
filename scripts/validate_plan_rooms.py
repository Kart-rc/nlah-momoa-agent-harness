#!/usr/bin/env python3
"""Validate PLAN.md work-phase room assignments.

Enforces that work phases explicitly declare a room and role pair, matching the
stage-05 contract that non-trivial phases must include room metadata.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADER_PATTERN = re.compile(r"^\|(.+)\|$")


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def parse_table_line(line: str) -> list[str] | None:
    match = HEADER_PATTERN.match(line.strip())
    if not match:
        return None
    return [cell.strip() for cell in match.group(1).split("|")]


def load_known_rooms(repo_root: Path) -> set[str]:
    rooms_dir = repo_root / "harness" / "rooms"
    known: set[str] = set()
    for room_file in sorted(rooms_dir.glob("*-room.md")):
        slug = room_file.stem.removesuffix("-room")
        known.add(slug)
        text = room_file.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("# Room"):
                label = line.split("—", 1)[-1].strip()
                known.add(normalize(label))
                break
    return known


def resolve_plan_path(target: str) -> Path:
    path = Path(target)
    if path.is_dir():
        return path / "PLAN.md"
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PLAN.md room usage")
    parser.add_argument("target", help="Run directory or PLAN.md path")
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository root used to load known rooms",
    )
    args = parser.parse_args()

    plan_path = resolve_plan_path(args.target)
    if not plan_path.exists():
        print(f"Missing plan file: {plan_path}")
        return 1

    known_rooms = load_known_rooms(args.repo_root)
    lines = plan_path.read_text(encoding="utf-8").splitlines()

    in_work_phases = False
    headers: list[str] | None = None
    data_rows: list[list[str]] = []

    for line in lines:
        if line.strip() == "## Work Phases":
            in_work_phases = True
            headers = None
            continue
        if in_work_phases and line.startswith("## "):
            break
        if not in_work_phases:
            continue

        cells = parse_table_line(line)
        if cells is None:
            continue
        if headers is None:
            headers = cells
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if any(cell.strip() for cell in cells):
            data_rows.append(cells)

    if not headers:
        print(f"PLAN missing Work Phases table header: {plan_path}")
        return 1

    normalized_headers = [normalize(cell) for cell in headers]
    required = ["phase", "room", "role pair", "owner", "output", "validation"]
    missing_headers = [h for h in required if h not in normalized_headers]
    if missing_headers:
        print("PLAN work phases table missing required columns:")
        for header in missing_headers:
            print(f"- {header}")
        return 1

    if not data_rows:
        print("PLAN work phases table must include at least one phase row")
        return 1

    idx = {name: normalized_headers.index(name) for name in required}
    failures: list[str] = []
    for row_num, row in enumerate(data_rows, start=1):
        padded = row + [""] * (len(normalized_headers) - len(row))
        room = normalize(padded[idx["room"]])
        role_pair = padded[idx["role pair"]].strip()
        if not room:
            failures.append(f"row {row_num}: room is empty")
        elif room not in known_rooms:
            failures.append(f"row {row_num}: room '{padded[idx['room']]}' not in harness/rooms")
        if not role_pair:
            failures.append(f"row {row_num}: role pair is empty")

    if failures:
        print("PLAN work phase room checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PLAN room checks passed ({plan_path})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
