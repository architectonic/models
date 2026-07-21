# Models

> **Status: experimental, pre-1.0.** Model records and routing outputs are dated evidence, not universal rankings or guarantees.

`models` stores provider metadata, evaluation definitions, measured results, capability requirements, routing constraints, and known uncertainty for computational models used by an Architectonic organization.

Use this layer only when agents need model-level granularity: task requirements, primary and fallback selection, cost, latency, availability, provider differences, or review thresholds.

## Evidence rules

- separate provider metadata from measured behavior;
- record model version, provider, date, parameters, task set, and evaluator;
- treat popularity and promotional claims as signals, not capability evidence;
- prefer task-specific evaluations over one aggregate score;
- re-evaluate when aliases, quantization, context policy, availability, or pricing change;
- keep routing policy replaceable and independent from agent identity;
- preserve the inputs and rules needed to reproduce generated tables and routes.

## Install

```bash
npx architectonic@latest add models --source npm
npx architectonic@latest verify
```

This package does not deploy models, contact providers, change billing, transmit credentials, or authorize an agent to act.
