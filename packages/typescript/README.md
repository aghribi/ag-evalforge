# ag-evalforge

Evaluation runner for LLM applications.

Scores model outputs against an evaluation dataset with exact match, regex, ROUGE-L, semantic similarity, LLM-as-judge or custom scorers, and compares two models on the same dataset.

## Install

```sh
pip install "ag-evalforge[all]"
npm install ag-evalforge
```

Extras: `openai`, `anthropic`, `semantic` (sentence-transformers), `all`.

## Usage

```python
from ag_evalforge import EvalCase, EvalDataset, ExactMatchScorer, run_eval

dataset = EvalDataset(cases=[
    EvalCase(input="Capital of France?", expected="Paris"),
    EvalCase(input="2 + 2?", expected="4"),
])
report = run_eval(dataset, ExactMatchScorer(), outputs=["Paris", "5"])
print(report.pass_rate, [r.case.input for r in report.failed])
```

Output:

```
0.5 ['2 + 2?']
```

Command line: `ag-evalforge run -d dataset.jsonl -s exact -o outputs.jsonl` and `ag-evalforge diff`. Datasets load from `.json`, `.jsonl` or `.csv`.

The TypeScript package `ag-evalforge` is a port of the core classes.

## Hosted API

`HostedScorer` runs the scoring in the hosted API, so no LLM provider key is needed locally. API keys are issued at https://ai.artifact-network.org. The default endpoint is `https://ai-api.artifact-network.org`; pass a different base URL to use your own deployment.

## Development

```sh
cd packages/python && pip install -e ".[all]" && pytest
cd packages/typescript && npm ci && npm test
```

## License

MIT, Copyright (c) 2026 Adnan Ghribi.
