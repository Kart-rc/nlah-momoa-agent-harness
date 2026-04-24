# Runtime Charter

## Purpose

Define the shared runtime semantics for executing natural-language harness logic without hiding task policy in controller code.

## Runtime Responsibilities

The runtime is responsible for:

- reading harness markdown and task contracts
- creating durable run workspaces
- invoking deterministic scripts and adapters
- enforcing stop conditions and budgets
- preserving state in files, ledgers, and manifests
- isolating validation context from implementation context
- recording major decisions in the orchestration ledger

## Harness Responsibilities

The harness is responsible for:

- stage order and allowed transitions
- artifact contracts
- role boundaries
- validation gates
- failure classification
- repair and release policy
- task-family-specific behavior

## Agent Call Contract

Every delegated call should have:

- task objective
- required inputs
- allowed paths
- allowed tools
- required outputs
- evidence expectations
- maximum attempts or budget
- completion condition

## State Semantics

State must be externalized, path-addressable, and compaction-stable. Important state must be written to `runs/<run-id>/state/*.jsonl` or promoted into `runs/<run-id>/artifacts/manifest.json`.

## Permission Boundary

A child or phase may only modify files explicitly included in its task contract unless the orchestrator updates the scope contract and records the reason.

## Release Boundary

The runtime must not release a run if required validation artifacts are missing or if critical dissent is unresolved.
