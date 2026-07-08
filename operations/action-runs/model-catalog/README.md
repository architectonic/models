# Model Catalog Action Runs

`latest.json` is written by `.github/workflows/model-catalog.yml` after every workflow run.

It records:

- GitHub run id and source SHA;
- snapshot and validation outcomes;
- whether the raw OpenRouter models snapshot exists;
- raw model count;
- generated matrix row count;
- next ChatGPT/operator action.
