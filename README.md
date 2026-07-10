# Architectonic Models

`models` is a repository for maintaining evidence-backed model metadata and routing policy.

Its purpose is to help a concrete system decide:

- which models meet a task's capability requirements;
- which models are suitable as primary or fallback workers;
- where additional review is justified;
- which models should be excluded from sensitive or production work;
- when changes in pricing, availability, context limits, or measured behavior require routing changes.

Model rankings are conditional on task, evidence, cost, latency, provider, date, and evaluation method. This repository should not present a temporary leaderboard as a general statement of model quality.

## Current state

The repository includes a bootstrap OpenRouter pipeline and a seed matrix. The seed is a representative starting set, not a canonical ranking. A current catalog is produced by running the snapshot command against OpenRouter.

```bash
python scripts/openrouter_model_catalog.py seed
python scripts/openrouter_model_catalog.py validate
```

For live refreshes:

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
  Equivalent rows in JSON for software consumption.

data/openrouter/generated/model-router.generated.json
  Compact route map grouped by use case and role.
```

Generated files are derived views. The inputs, evaluation definitions, dates, and routing rules needed to reproduce them should remain recoverable.

## Evaluation principles

- Separate provider metadata from measured behavior.
- Record model version, provider, date, parameters, task set, and evaluator.
- Treat popularity and marketing claims as signals, not capability evidence.
- Prefer task-specific evaluations over one aggregate score.
- Record variance, failures, and known limitations rather than only successful examples.
- Re-evaluate when providers silently change aliases, quantization, context policy, or pricing.
- Keep routing policy replaceable and independent from agent identity.
- Require stronger evidence and review for higher-risk actions.

## Operating model

Maintenance may use a board, ledger, or another explicit queue. The durable requirements are simpler:

1. fetch current source state and provider data;
2. select one bounded update or evaluation;
3. preserve evidence and assumptions;
4. validate generated outputs;
5. record the resulting change and unresolved uncertainty.

Operational artifacts should not multiply unless they change future work, preserve evidence, or define a necessary review boundary.

## Relationship to the stack

```text
doctrine   = governs acceptable use and risk
identity   = defines who may select, approve, or override routing
project    = supplies task and operating context
skills     = supplies evaluation and routing procedures
knowledge  = retains reviewed model claims and evidence
meta       = defines refresh, drift, and revision policy
agents     = consumes capability requirements and routing policy
models     = maintains model metadata, evaluations, and route candidates
```

## Boundary

This repository classifies and routes models. It does not execute production deployments, contact providers, change billing, transmit secrets, or claim model quality without metadata or evaluation evidence.
