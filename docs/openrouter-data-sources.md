# OpenRouter Data Sources

## Primary metadata source

```text
GET https://openrouter.ai/api/v1/models
```

The live snapshot path is the primary source for:

- model id and name;
- context length;
- input and output modalities;
- supported parameters;
- provider/top-provider metadata;
- pricing;
- model descriptions;
- benchmark metadata when exposed by OpenRouter.

The bootstrap seed uses the same field shape but is not a substitute for a live snapshot.

## Future enrichment sources

```text
GET https://openrouter.ai/api/v1/datasets/rankings-daily
GET https://openrouter.ai/api/v1/classifications/task
```

These are identified but not yet wired into the bootstrap script. They should enrich:

- trailing popularity rank;
- weekly token totals;
- task-market fit signals;
- routing-change reports.

## Source hygiene

Provider metadata, usage popularity, and task classifications are signals. They are not proof that a model is good at a specific Workframe/autocorp task.

Eval-backed promotion requires stable fixtures and recorded results under future `evals/` and `reports/evals/` paths.
