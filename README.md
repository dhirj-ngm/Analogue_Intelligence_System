# Historical Analogue Intelligence Engine

An evidence-linked FMCG case retrieval pilot. Two threads: **Discussion** for ideas and decisions; **Builder** for whole-module delivery. Read PROJECT_TRACK.md and STATUS.md to resume. Older handoffs are history.

## Run locally

Python 3.14 was used for this pilot. CPU inference; initial setup and model download require internet access. No paid API, credentials or MCP required.

```sh
make setup
make test
make lint
make validate
make run
# After the first model download, run without network:
HF_HUB_OFFLINE=1 make run
```

The model cache lives in ignored `models/`. Frozen benchmark inputs are checked before execution. Results are written to `evaluation/pilot/baselines/`. `requirements.txt` records the tested dependency environment.

For a lexical investigation:

```sh
PYTHONPATH=src .venv/bin/python -m ais.pilot search --text 'packaging costs and margin pressure' --cutoff 2023-01-27
```

This returns uncalibrated candidates with evidence and limitations; a rank is not proof of relevance. No automatic insufficient-evidence threshold is implemented. Inspect source passages before interpreting cases.

## What is here

- `data/pilot/cases.jsonl`: ten compact assistant-checked observations, including contrasts; original detailed Colgate evidence remains in `data/episodes.jsonl`.
- `evaluation/pilot/`: fixed queries, pre-ranking assistant judgements, protocol, input hashes and measured comparisons.
- `src/ais/pilot.py`: date/candidate validation, BM25, dense retrieval and metrics.
- `tests/`: leakage, dates, eligibility, invalid inputs and metric checks.

The pilot is descriptive and has no independent relevance labels, held-out claims, causal findings or trained custom model. Evidence review and user acceptance are separate from software delivery.

Read [the completed development pilot report](evaluation/pilot/pilot-report.md) for results and the unmet original human-validation criteria.
