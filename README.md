# Historical Analogue Intelligence Engine

An evidence-based tool for finding earlier company situations that help explain
a current business challenge. The first domain is FMCG input-cost pressure and
company responses. Search should compare both the company's own past and other
companies, show why an earlier case helps, show important differences, and link
to source passages. Issuer explanations and later observations must remain
separate from the system's interpretation. A reported recovery is not proof that
a particular action caused it.

The current deliverable is a reproducible **development pilot** with ten
assistant-checked observations, five queries, BM25 keyword retrieval and MiniLM
semantic retrieval. [The pilot report](evaluation/pilot/pilot-report.md) contains
results and limitations. `data/pilot/cases-structured-v2.jsonl` separates
pressure, measure, other drivers, response and unknowns. The original detailed
Colgate record remains in `data/episodes.jsonl` with its source manifest.

## Run

Python 3.14 and an internet connection are needed for initial CPU model setup.
No paid API, credentials or MCP are required.

```sh
make setup
make test
make lint
make validate
make run
```

After the model is cached: `HF_HUB_OFFLINE=1 make run`. To try a keyword query:

```sh
PYTHONPATH=src .venv/bin/python -m ais.pilot search --text 'packaging costs and margin pressure' --cutoff 2023-01-27
```

Results are uncalibrated candidates; inspect source evidence and differences.
Model caches are ignored by Git. Frozen v1 and v2 experiment files stay under
`evaluation/pilot/`; changes to them require a new version.

## Roadmap

M001 is closed as a development pilot. Next build the case-search and comparison
experience and improve evidence depth. Later, expand the corpus, evaluate with
independent relevance judgements if available, test structural comparison, and
consider task-specific model training only when failures and labels justify it.
Builder works end to end without user review gates. Development findings must
not be presented as independently validated business advice.
