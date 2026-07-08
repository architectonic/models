# Architectonic Models

A repo-native model intelligence ledger for OpenRouter and adjacent model-provider routing.

The purpose is to turn a fast-changing model market into a maintained, machine-readable routing matrix that answers:

- which models are cheap enough for local development;
- which models are suitable as primary/fallback coding workers;
- which models deserve expensive high-reasoning review lanes;
- which models should be avoided for production or sensitive work;
- when pricing, context, popularity, or capability changes require routing changes.

## Current state

This repo is initialized with a bootstrap OpenRouter pipeline and seed matrix. The seed is intentionally conservative: it is a representative starter set, not a canonical top-50 list. The live catalog is produced by running the snapshot command against OpenRouter.

```bash
python scripts/openrouter_model_catalog.py seed
python scripts/openrouter_model_catalog.py validate
```

For live weekly/discretionary refreshes:

```bash
export OPENROUTER_API_KEY=...
python scripts/openrouter_model_catalog.py snapshot --sort top-weekly --output-modalities text
```

The public `/models` endpoint can run without an API key. Rankings and task-classification enrichment require an OpenRouter API key.

## Generated surfaces

```text
data/openrouter/generated/model-routing-matrix.csv
  CSV table for spreadsheet review and routing decisions.

data/openrouter/generated/model-routing-matrix.json
  Same rows in JSON for agent/runtime consumption.

data/openrouter/generated/model-router.generated.json
  Small route map grouped by use case and role.
```

## Operating model

This repo follows the same board-first heartbeat pattern used by the active Architectonic operator repos:

1. Fetch exact default-branch state.
2. Read `operations/board.json`, `operations/gates.md`, `operations/value-ledger.json`, today's daily state, and relevant ticket inputs.
3. Consume exactly one highest-priority ready ticket allowed by gates.
4. Produce an artifact or block/kill the ticket with evidence.
5. Run acceptance tests.
6. Update board, ledger, daily state, and log.

The first value path is:

```text
models-bootstrap-openrouter-catalog-001
-> models-live-openrouter-snapshot-001
-> models-routing-matrix-rank-top50-001
-> models-eval-harness-seed-001
```

## Boundary

This repo classifies and routes models. It does not execute production deployments, contact providers, change billing, transmit secrets, or claim model quality without metadata/eval evidence.
