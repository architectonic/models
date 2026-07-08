# Models Value Gates

## Purpose

The Models loop converts provider metadata, pricing, usage signals, and local eval results into a useful routing matrix. It must not become a spreadsheet-shaped pile of guesses.

The board of record is `operations/board.json`. Daily ledgers are audit trails.

## Promotion ladder

```text
provider metadata snapshot
-> normalized model matrix
-> use-case routing roles
-> seeded router config
-> local eval harness
-> eval-backed role promotion
-> weekly/discretionary refresh loop
```

## Done definition

A Models ticket is done only if it:

- fetches or preserves provider metadata;
- normalizes pricing/capability fields into machine-readable rows;
- produces or validates a routing matrix;
- creates a useful router config grouped by use case;
- adds eval tasks or eval results that can falsify metadata-only rankings;
- detects and records material pricing/context/capability changes;
- kills or blocks a weak model route with evidence.

Status-only updates and generic model commentary are low value.

## Safety gates

- Do not send secrets, credentials, private customer data, unpublished code, or sensitive financial data to free/opportunistic models.
- Do not call Gmail, Vercel, Netlify, Stripe, DNS, broker, wallet, exchange, or other external mutation tools from this repo.
- Do not claim verified quality unless backed by local eval results or explicit benchmark evidence.
- Do not claim OpenRouter popularity means model quality.
- Do not use a free route as production primary unless a human explicitly approves and the route is reviewed.

## Supervisor authority

The Portfolio Supervisor may:

- block production routing if the matrix is stale or metadata-only;
- require local evals before promoting fallback models to primary;
- require scope narrowing if live OpenRouter fetches fail repeatedly;
- mark price-only updates low value unless routing changes materially;
- require manual review for free/opportunistic lanes.
