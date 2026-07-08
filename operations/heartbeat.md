# Models Heartbeat Protocol

## Operator loop

Every scheduled Models heartbeat must:

1. Resolve `architectonic/models` through GitHub.
2. Fetch exact default-branch state and record inspected ref/SHA.
3. Fetch `operations/board.json`, `operations/gates.md`, `operations/value-ledger.json`, today's daily status/queues, `operations/log.md`, generated model matrix, and relevant ticket inputs.
4. Select the highest-priority `ready` board ticket allowed by `operations/gates.md`.
5. Produce the ticket output artifact or mark the ticket blocked/killed with evidence.
6. Run ticket acceptance tests.
7. Update `operations/board.json` ticket status and next ticket state.
8. Append one value event to `operations/value-ledger.json`.
9. Update today's status/report/log with concise evidence.
10. Report inspected SHA, ticket consumed, sources/files reviewed, files changed, commit SHA, value delta, blockers, and next ticket.

## Anti-slop rule

If a run only changes status, reports, or queues, it must mark itself `low_value_status_only` unless it repaired missing state, removed a blocker, promoted/blocked/killed a board ticket, or preserved a material routing/pricing change.

## Current priority

```text
models-bootstrap-openrouter-catalog-001
-> models-live-openrouter-snapshot-001
-> models-routing-matrix-rank-top50-001
-> models-eval-harness-seed-001
```

No production routing claim is valid until metadata is validated and use-case evals are added.
