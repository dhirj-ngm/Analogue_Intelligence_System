# Historical Analogue Intelligence Engine

An evidence-based tool for finding earlier company situations that help explain
a current business challenge. Start with FMCG input costs and company responses.
The app lets readers describe a situation, inspect ranked historical cases and
compare up to three side by side, with sources, important differences and unknowns.
Issuer explanations remain distinct from independently identified effects.
A reported recovery does not establish that an action caused it.

The collection has ten assistant-checked observations from five companies.
These development records have limited evidence depth and independent validation.

## Run the case app

Python 3.14 is tested. The app uses only the Python standard library, existing
local case files and BM25 code. No package installation, model download, paid
service or credentials are needed:

```sh
make app
```

Open **http://127.0.0.1:8000**. Stop with Ctrl+C. For another port:

```sh
PYTHONPATH=src python3 -m ais.app --port 8001
```

Try **Packaging & logistics**, open a case's evidence panel, select two or three
cases and choose **Compare selected**. To investigate the existing Colgate Q4
2022 case, select **Colgate · CL-2022**: dates populate automatically and the case
and known continuations are excluded. Try `semiconductor shortages at a bank`
for an insufficient-evidence result.

**Only information published by** is an inclusive public-information cutoff.
Candidate reporting periods must end strictly before **Situation period end**,
which cannot be after that cutoff. Selecting a source case also limits candidates
to periods ending before its period end; its query evidence must be public by
the cutoff. Expand **Dates and exclusions** to see effective rules and counts.

The app binds to loopback for local use. Searches remain in memory for the
request; their text is neither logged nor persisted. The app does not fetch
models or sources. Source links visit the issuer's site in a separate tab.

## What ranking and comparisons mean

BM25 scores only the pilot's allowlisted `challenge` text. Responses, rationale,
later outcomes, comparison limits and review labels do not enter its scores.
Structured fields supply display evidence and a conservative pressure-match
gate. Unknown publication dates, post-cutoff challenge evidence, non-earlier
periods, the selected query case and its known duplicate/continuation group are
excluded. Other duplicate groups collapse to the earliest eligible publication
before scoring. Select a corpus source case when using its situation; free text
alone does not identify which case to exclude as self.

Up to five **partial pressure matches** require a positive BM25 score and at
least one specific shared pressure term. Generic cost/margin words alone do not
suffice. Explicitly negated/unknown clauses are skipped by this small lexical
gate. It can miss synonyms and mixed/complex descriptions. It does not establish
relevance, a useful analogy or confidence in a response's success. With no
eligible match, the app shows insufficient evidence. Unmatched query terms are
wording gaps, not documented contradictions. Dense retrieval remains in the
pilot; the app uses BM25 for an offline, inspectable implementation.

Responses appear after retrieval with their evidence. A response with a missing
publication date or a date after the cutoff is withheld. Comparisons retain
metric units, scope, accounting basis and reporting/comparison periods. The app
does not subtract incompatible measures. Missing verbatim excerpts are explicit
and retain their source locator. Episode boundaries, isolated response effects,
action-level reasoning and later outcomes remain limited.

## Checks

The deterministic suite includes local HTTP integration tests and needs no model:

```sh
make test
make validate
```

With the development environment installed, run `make lint` for Ruff checks and
format verification. For a minimal lint environment instead of the full model
setup: `python3 -m venv .venv`, then
`.venv/bin/python -m pip install ruff==0.17.3`.
JavaScript syntax: `node --check assets/app/app.js` and
`node --check scripts/check_app_browser.mjs`.

For the optional real-browser smoke check, use Node 22+ and Chrome/Chromium:

```sh
make browser-test
# If Chrome is installed elsewhere:
CHROME_BIN=/usr/bin/chromium make browser-test
```

The check starts/stops its own loopback server and temporary headless browser.
It covers search, source inspection, three-case comparison, self/date exclusions,
insufficient evidence, validation errors and a 375px mobile viewport. Screenshots
are written to `/tmp/ais-case-search-desktop.png` and
`/tmp/ais-case-search-mobile.png`; the temporary profile is removed. The default
browser path is `/opt/google/chrome/chrome`. The app itself needs neither Node
nor Chrome. Set `APP_PYTHON` to use a different Python executable.

## Reproduce the earlier model pilot

[The pilot report](evaluation/pilot/pilot-report.md) describes the ten-case,
five-query BM25/MiniLM experiment. The app reads `data/pilot/cases.jsonl` and
`data/pilot/cases-structured-v2.jsonl` without changing frozen inputs/results.
The detailed Colgate record and source manifest remain in `data/episodes.jsonl`
and `data/source_manifest.jsonl`.

Initial CPU model setup needs internet access and the larger ML dependencies:

```sh
make setup
make test
make lint
make validate
make run
```

After caching the model: `HF_HUB_OFFLINE=1 make run`. To try the pilot CLI:

```sh
PYTHONPATH=src .venv/bin/python -m ais.pilot search --text 'packaging costs and margin pressure' --cutoff 2023-01-27
```

Model caches are ignored by Git. Frozen v1/v2 files stay in `evaluation/pilot/`;
changes require a new benchmark version. `make run` reproduces the model pilot;
`make app` starts the reader app.

## Roadmap

M001 is closed as a development pilot; M002 delivers local search and comparison.
Next improve case depth and coverage. Later, evaluate with independent relevance
judgements, test structural comparison and consider task-specific training when
failures and labels justify it. Builder works end to end without user review
gates. Development findings must remain labelled honestly.
