# Task Router

## Purpose

Classify a user task into a task family and load the matching task-type harness.

## Supported Task Families

1. GitHub Issue
2. Brownfield Feature
3. Greenfield Application
4. Presentation / Deck Creation
5. Requirements to Architecture
6. HLD / LLD / ADR Creation
7. Research / Analysis
8. Generic Documentation
9. Generic Coding Task
10. Requirements to Prototype Options

## Routing Rules

If the task references:

- GitHub issue, ticket, bug, failing test, stack trace: use `github-issue`.
- CVE, vulnerability, dependency risk, or security fix: use `github-issue/vulnerability`.
- library version, framework upgrade, or dependency upgrade: use `github-issue/dependency-upgrade`.
- existing codebase, brownfield, add feature, or modify existing app: use `brownfield-feature`.
- new app, new service, MVP, scaffold, or from scratch: use `greenfield-application`.
- slides, presentation, pitch, leadership, or stakeholders: use `presentation`.
- BRD, business requirement, architecture, HLD, LLD, or ADR: use `requirements-to-architecture`.
- benchmark synthesis, literature review, landscape comparison, or exploratory analysis: use `research-analysis`.
- docs rewrite, runbook, README cleanup, tutorials, or knowledge-base articles: use `generic-documentation`.
- implementation request without a tighter family match: use `generic-coding`.
- problem statement asks for multiple approach proposals, quick prototyping, and rubric-based selection: use `requirements-to-prototype-options`.

## Output Contract

Write `TASK_CLASSIFICATION.md` with:

- selected task type
- confidence score
- routing rationale
- missing inputs
- required artifacts
- suggested validation tier
- ambiguity triggers

## Ambiguity Trigger

Before planning, trigger ambiguity resolution if a missing input could materially change architecture, implementation, cost, risk, or audience fit.
