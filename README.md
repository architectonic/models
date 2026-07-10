---
type: Entry Point
title: models
description: Evidence-backed model metadata, evaluations, capability requirements, and routing policy.
tags: [models, routing, evaluation, openrouter, architectonic, okf]
okf_version: "0.2"
status: draft
---

# models

```bash
npx architectonic add models
```

`models` maintains source-backed metadata, evaluations, constraints, and routing policy for computational models used by an Architectonic system.

It helps a concrete system decide which models meet a task's capability requirements, which are suitable as primary or fallback workers, where additional review is justified, and when pricing, availability, or measured behavior require routing changes.

Model assessments are conditional on task, evidence, cost, latency, provider, date, and evaluation method. A temporary leaderboard is not a general statement of model quality.

## In the ensemble

```text
constitution      composition contract for the ensemble
doctrine          purpose, principles, ontology, epistemology, ethics, governance, incentives
identity          actors, roles, authority, delegation, incentives, privacy
project           operating-unit context, sources, decisions, risks, continuity
skills            reusable procedures, verification, failure handling
knowledge         claims, sources, evidence, uncertainty, known unknowns
models            model metadata, evaluations, capability requirements, routing policy
agents            software actors composed from identity, skills, models, knowledge, permissions
living-knowledge  optional: governed maintenance of frequently changing corpora
meta              audit, upkeep, drift review, revision policy
```

Agents consume capability requirements and routing policy from this layer. Model selection remains implementation policy, not identity.

## Commands

```bash
npx architectonic add models
npx architectonic add models --source npm
npx architectonic init
npx architectonic list
npx architectonic doctor
```

CLI: https://github.com/architectonic/architectonic

## Canonical records and generated views

The repository may retain provider metadata, evaluation definitions, measured results, capability requirements, routing rules, and known uncertainty.

Generated tables, summaries, rankings, and route maps are derived views. The inputs and rules required to reproduce them should remain recoverable.

## Catalog pipeline

```bash
python scripts/openrouter_model_catalog.py seed
python scripts/openrouter_model_catalog.py validate
```

For a current provider snapshot (optional API key):

```bash
python scripts/openrouter_model_catalog.py snapshot --sort top-weekly --output-modalities text
```

Generated surfaces:

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
- Re-evaluate when providers change aliases, quantization, context policy, availability, or pricing.
- Keep routing policy replaceable and independent from agent identity.

## Boundary

This repository records and evaluates model capabilities. It does not execute production deployments, contact providers, change billing, transmit secrets, or claim model quality without dated metadata or evaluation evidence.
