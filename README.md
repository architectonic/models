# Models and Retrieval Policy

> **Status: experimental, pre-1.0.** Model and retrieval assessments are conditional on task, version, provider, date, parameters, evaluator, cost, latency, and evidence. Popularity and leaderboards are discovery signals, not universal capability proof.

This layer records:

- capability requirements and constraints;
- dated model and provider metadata;
- task-specific evaluations;
- primary and fallback routing policy;
- cost, latency, privacy, and availability boundaries;
- retrieval and reranking evidence when agents depend on corpora.

It may stand alone as a catalog or policy layer. Add agents only when model policy must be attached to concrete software actors.

Git/Markdown knowledge can be accompanied by lexical, vector, graph, or hybrid retrieval. Databases and indexes remain replaceable acceleration layers. Retrieval relevance, graph proximity, and generated summaries are not evidence by themselves.

See [`docs/RETRIEVAL_AND_ROUTING.md`](./docs/RETRIEVAL_AND_ROUTING.md).
