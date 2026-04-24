# Requirements to Multi-Option Prototyping Harness

## Purpose

Turn a problem statement into multiple candidate approaches, build lightweight prototypes for each, and use an AruBrix evaluation rubric across key parameters to select the best-fit approach.

## Required Inputs

- problem statement
- success criteria and constraints
- target users or stakeholders
- non-functional requirements and risk constraints, when known

## Required Artifacts

- `PROBLEM_DEFINITION.md`
- `OPTION_SET.md`
- `PROTOTYPE_PLAN.md`
- `PROTOTYPE_EVIDENCE.md`
- `ARUBRIX_MATRIX.md`
- `DECISION_SUMMARY.md`
- `RELEASE_PACKET.md`

## AruBrix Parameters

At minimum, score each option and prototype against:

1. correctness and requirement fit
2. feasibility and implementation complexity
3. scalability and performance headroom
4. security, reliability, and operational risk
5. cost, time-to-deliver, and maintainability
6. stakeholder or user impact

Use weighted scores, explicit assumptions, and confidence levels.

## Workflow

1. Define the problem and acceptance criteria
2. Generate at least three materially different options
3. Build focused prototypes for top candidates
4. Capture prototype evidence and failure cases
5. Score options with `ARUBRIX_MATRIX.md`
6. Run adversarial review on scoring and assumptions
7. Select recommended approach and fallback

## Validation Gates

- at least three options are explored
- prototype evidence exists for shortlisted options
- AruBrix scores are parameterized and weighted
- recommendation maps to evidence, not preference
- rejected options include clear rationale

## Role Model

- orchestrator: enforce option quality and rubric-based selection
- planner: define prototype scope, constraints, and evaluation design
- implementer: produce comparable prototype options with evidence
- reviewer: challenge option viability and hidden assumptions
- independent validator: verify rubric scoring and evidence fidelity
- release certifier: approve recommendation packet and caveats

## End-to-End Flow Coverage

This family maps across the complete lifecycle:

1. intake and decision context setup
2. ambiguity resolution for rubric and constraints
3. planning and prototype-option execution
4. comparative validation and scoring
5. repair/rework for weak options
6. release with final recommendation and rationale

## Release Expectations

Release must include option comparison, scoring rationale, recommendation confidence, and next-step experiment plan.
