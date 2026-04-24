# Task Router

## Purpose

Classify a user task into a task family and load the matching task-type
harness.

## Source of truth

The task-type catalog is [`harness/task-types/registry.json`](./task-types/registry.json).
Each entry declares `id`, `display_name`, `keywords`, `variants`, and
`default_validation_tier`. Routing logic should consume the registry rather
than hardcoding a list.

## Routing Rules

Match the user request against the `keywords` of each registry entry. When
multiple entries match, prefer the most specific (longest keyword match wins;
tie-break to the entry appearing first in the registry). Variants listed in
the registry (e.g., `github-issue` `variants: [vulnerability, dependency-upgrade, ...]`)
let the router capture a subclass without requiring a separate task type.

## Output Contract

Write `TASK_CLASSIFICATION.md` with:

- selected task type (matches a registry `id`)
- selected variant if applicable
- confidence score
- routing rationale
- missing inputs
- required artifacts (copied from the task-type manifest)
- suggested validation tier (defaults to the task-type's `default_validation_tier`)
- ambiguity triggers

## Ambiguity Trigger

Before planning, trigger ambiguity resolution if a missing input could
materially change architecture, implementation, cost, risk, or audience fit.
