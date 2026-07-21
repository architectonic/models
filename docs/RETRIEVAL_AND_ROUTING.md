# Retrieval and Routing

## Separate concerns

```text
canonical corpus       sources, claims, uncertainty, contradictions
retrieval index        replaceable access path
model policy           which capabilities and constraints a task requires
agent attachment       which policy a concrete agent may use
```

## Candidate retrieval paths

- lexical search for exact language and identifiers;
- vector search for semantic similarity;
- graph traversal for declared or inferred relationships;
- structured queries for datasets and operational stores;
- hybrid retrieval and reranking for task-specific combinations.

No path is universally best. Evaluate representative questions, source recall, unsupported-answer rate, latency, cost, and failure behavior.

## Routing record

Record task class, required capabilities, model and provider version, context policy, primary, fallback, review gate, cost and latency bounds, privacy constraints, evaluation date, and evidence.

Re-evaluate when providers change aliases, quantization, context behavior, pricing, availability, or safety controls.
