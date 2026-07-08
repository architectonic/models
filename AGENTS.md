# Agent Instructions

## Mission

Maintain a model-routing intelligence ledger that helps Workframe/autocorp choose models by use case, price, capability, and trust tier.

## Board-first protocol

Every operator pass must:

1. Resolve `architectonic/models` through GitHub.
2. Fetch exact default-branch state and record inspected ref/SHA.
3. Read `operations/board.json`, `operations/gates.md`, `operations/value-ledger.json`, today's daily state, `operations/log.md`, and ticket inputs.
4. Select the highest-priority `ready` ticket allowed by gates.
5. Consume exactly one ticket.
6. Produce the required artifact or mark the ticket blocked/killed with direct evidence.
7. Run the acceptance tests explicitly.
8. Update board, value ledger, daily status/queues, and log.
9. Report files changed, resulting commit SHA, value delta, blockers, and next ticket.

## Anti-slop rule

Status-only updates are low value unless they repair missing state, remove a blocker, promote/block/kill a ticket, or preserve a material model/pricing/routing change.

## Safety

- Never send secrets or private customer data to free/opportunistic models.
- Never let model-ranking output become financial advice, trading advice, or production deployment authority.
- Never claim a model is best without metadata, benchmark, or local-eval evidence.
- Treat OpenRouter descriptions and popularity as signals, not proof.
- Treat generated router files as advisory until validated by use-case evals.
