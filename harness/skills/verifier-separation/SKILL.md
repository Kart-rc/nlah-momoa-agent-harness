# Skill — Verifier Separation

## Purpose

Prevent false completion by enforcing independent validation.

## Workflow

1. Implementer submits artifacts and evidence.
2. Independent validator reviews artifacts-only context.
3. Validator records findings and verdicts.
4. Repair is delegated back to implementation role.
5. Validator re-runs checks without inheriting repair reasoning.

## Prohibitions

- Validator must not silently patch and approve.
- Implementer confidence cannot replace validator evidence.
