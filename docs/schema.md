# Model Routing Matrix Schema

## Canonical raw input

```text
data/openrouter/raw/YYYY-MM-DD/models.json
```

Raw provider snapshots must remain unedited. Generated routing opinions are derived from raw snapshots and seed data by `scripts/openrouter_model_catalog.py`.

## Generated outputs

```text
data/openrouter/generated/model-routing-matrix.csv
data/openrouter/generated/model-routing-matrix.json
data/openrouter/generated/model-router.generated.json
```

## Role values

Use-case role columns must use one of:

```text
primary
fallback
high_reasoning
cheap
free
avoid
unknown
candidate
```

## Trust tiers

```text
free      opportunistic/free route; not production primary by default
paid      normal paid provider route
premium   expensive/high-reasoning provider route
```

## Cost columns

OpenRouter pricing is represented as per-token decimal values. The builder converts these into per-million-token values.

```text
pricing_prompt_per_mtok     = pricing.prompt * 1,000,000
pricing_completion_per_mtok = pricing.completion * 1,000,000
```

Use-case weighted cost columns use these mixes:

```text
documentation = 85% input + 15% output
coding        = 55% input + 45% output
testing       = 60% input + 40% output
review        = 90% input + 10% output
agent         = 50% input + 50% output
planning      = 70% input + 30% output
```

## Routing rule

Generated roles are advisory. Promotion from metadata-backed routing to eval-backed routing requires repo-local eval results.
