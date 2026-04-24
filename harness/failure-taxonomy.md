# Failure Taxonomy

Use this taxonomy to classify validation failures, execution problems, and repair triggers.

| Failure | Meaning | Default Recovery |
|---|---|---|
| `format_error` | Output does not match required format or schema | Repair artifact and rerun deterministic check |
| `missing_artifact` | Required file or evidence is absent | Create missing artifact; rerun artifact gate |
| `wrong_path` | Artifact exists outside expected path | Move or relink artifact; update manifest |
| `test_failure` | Deterministic test failed | Targeted repair; rerun failed tests |
| `evidence_gap` | Claim lacks evidence | Add evidence or downgrade claim |
| `scope_mismatch` | Work does not satisfy agreed scope or changed unrelated scope | Replan or repair against scope contract |
| `security_failure` | Security gate failed | Escalate to security reviewer; require Tier 3 release |
| `context_drift` | Agent lost original objective or assumptions | Reopen scope contract; replan |
| `tool_error` | Tool call failed or returned unusable output | Retry once; then use tool-repair wrapper |
| `timeout` | Work exceeded budget | Overseer decides reduce scope, replan, or abort |
| `local_success_global_failure` | Local check passed but overall task objective remains unmet | Independent validation and targeted repair |
| `unresolved_dissent` | Critical reviewer objection remains open | Paradox resolution or human input |

## Severity

- **low**: does not block release if documented.
- **medium**: blocks release until repaired or accepted as known risk.
- **high**: blocks release and requires independent validation.
- **critical**: blocks release and requires overseer decision or human input.
