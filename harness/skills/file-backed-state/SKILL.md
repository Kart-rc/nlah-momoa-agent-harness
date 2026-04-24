# Skill — File-Backed State

## Purpose

Maintain durable, path-addressable run state to support replay, audits, and child-agent coordination.

## Workflow

1. Write material events to JSONL ledgers.
2. Register produced artifacts in `artifacts/manifest.json`.
3. Store child contracts and child responses under `children/`.
4. Promote only approved child artifacts into parent artifact paths.

## Rules

- Never rely solely on hidden chain-of-thought memory.
- Keep append-only event history where possible.
- Include UTC timestamps for all state events.
