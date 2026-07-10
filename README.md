# models

`models` maintains source-backed metadata, evaluations, constraints, and routing policy for computational models used by an Architectonic system.

Install it with:

```bash
npx architectonic add models
```

Its purpose is to help a concrete system decide:

- which models meet a task's capability requirements;
- which models are suitable as primary or fallback workers;
- where additional review is justified;
- which models should be excluded from sensitive or production work;
- when pricing, availability, context limits, or measured behavior require routing changes.

Model assessments are conditional on task, evidence, cost, latency, provider, date, and evaluation method. A temporary leaderboard is not a general statement of model quality.

## Canonical records and generated views

The repository may retain:

```text
provider metadata
model and provider identifiers
dated evaluation definitions
measured results and failures
capability requirements
cost and latency observations
routing rules and review thresholds
known uncertainty and unresolved questions
```

Generated tables, summaries, rankings, and route maps are derived views. The inputs and rules required to reproduce them should remain recoverable.

## Current implementation

The repository includes an OpenRouter catalog pipeline and seed matrix:

```bash
python scripts/openrouter_model_catalog.py seed
python scripts/openrouter_model_catalog.py validate
```

For a current snapshot:

```bash
export OPENROUTER_API_KEY=...
python scripts/openrouter_model_catalog.py snapshot --sort top-weekly --output-modalities text
```

The public `/models` endpoint can run without an API key. Provider-specific rankings and enrichment may require one.

## Generated surfaces

```text
data/openrouter/generated/model-routing-matrix.csv
data/openrouter/generated/model-routing-matrix.json
data/openrouter/generated/model-router.generated.json
```

## Evaluation principles

- Separate provider metadata from measured behavior.
- Record model version, provider, date, parameters, task set, and evaluator.
- Treat popularity and promotional claims as signals rather than capability evidence.
- Prefer task-specific evaluations over one aggregate score.
- Record variance, failures, and known limitations.
- Re-evaluate when providers change aliases, quantization, context policy, availability, or pricing.
- Keep routing policy replaceable and independent from agent identity.
- Require stronger evidence and review for higher-risk actions.

## Maintenance

A maintenance cycle should:

1. fetch current provider and repository state;
2. select one bounded update or evaluation;
3. preserve evidence, assumptions, and dates;
4. validate generated outputs;
5. record the resulting change and unresolved uncertainty.

Operational artifacts should exist only when they change future work, preserve evidence, or define a necessary review boundary.

## Relationship to the ensemble

```text
constitution      = composes the ensemble
doctrine          = governs acceptable use and risk
identity          = defines who may select, approve, or override routing
project           = supplies task and operating context
skills            = supplies evaluation and routing procedures
knowledge         = retains reviewed claims and evidence
models            = maintains model metadata, evaluations, constraints, and route candidates
agents            = consumes capability requirements and routing policy
living-knowledge  = may maintain changing model knowledge through reviewed campaigns
meta              = defines refresh, drift, audit, and revision policy
```

## Boundary

This repository records and evaluates model capabilities. It does not execute production deployments, contact providers, change billing, transmit secrets, or claim model quality without dated metadata or evaluation evidence.