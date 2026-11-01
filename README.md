# Historical Analogue Intelligence Engine

An evidence-based tool for finding earlier company situations that help explain
a current business challenge. Start with FMCG input costs and company responses.
The app lets readers describe a situation, inspect ranked historical cases and
compare up to three side by side, with sources, important differences and unknowns.
Issuer explanations remain distinct from independently identified effects.
A reported recovery does not establish that an action caused it.

The collection has **13 assistant-checked observations from eight companies**.
The latest batch adds General Mills' 2007 grain/dairy/energy costs, Nestlé Waters'
2011 oil-related packaging/distribution costs, and Hershey's 2025 cocoa costs.
These development records have not had independent human validation.

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

Describe the problem, or choose an example to run a search straight away.
Open **Read the case and its sources** to see what the company reported,
where to find it, how the situation differs, and what we do not know. Choose
**two or three cases**, then **Compare cases**, to read them together. On a
phone, comparisons stack vertically without a sideways-scrolling table.

**Dates and a starting case** is optional. Choose a case such as Colgate's period
ending 31 Dec 2022 to fill in its description and dates. Switching back to
**My own situation** restores your earlier description and date choices.
**Use my situation and today's dates** resets the dates without losing your own
text. Changing the information date also updates an end date that is still linked
to it; a separately chosen end date is kept.

**Information available by** includes reports published on or before that date.
Cases must cover periods ending before **End of the situation you are comparing**.
A chosen starting case and its known continuing reports are excluded. Date errors
open the controls and focus the field to fix; dates are never silently widened to
produce results.

If the app cannot support a comparison, it explains whether the dates ruled out
all cases or the description has no supported connection through the input vocabulary.
You can check the dates, edit the description, or try an example. `Semiconductor shortages at a bank`
shows a collection gap. Empty results are not evidence that no historical
comparison exists elsewhere.

**How this works** contains the method, date/exclusion counts and optional BM25
scores. Each result shows the words connected in your description and the report,
with sources, differences and unknowns. Related terms do not establish a useful
analogy or that the report measured your exact input. Reported actions do
not prove what caused a result. Metric definitions and exact source locators
remain available beside the company-reported figures.

Try **Cocoa costs** or **Food ingredients & energy** for the new cases.
Case details and comparisons explain basis points beside the disclosed numbers.
**More company-reported figures** keeps supporting amounts and adjusted measures
with their own definitions and sources. Hershey's release and filing disagree
about the margin decline; the app shows both claims and the unresolved difference.
Reported and adjusted margins remain separate.

The app binds to loopback for local use. Searches remain in memory for the
request; their text is neither logged nor persisted. The app does not fetch
models or sources. Source links visit the issuer's site or SEC EDGAR in a separate tab.

## Safeguards and limits

BM25 now scores named input families in the source-backed pressure passages
only. A small [readable vocabulary](src/ais/related.py) connects milk/dairy,
flour/grains, electricity/energy, chocolate/cocoa and freight/transport, alongside
other related inputs. It applies to all queries and eligible cases, with no case
IDs or query-specific rules. Responses, profit figures, rationale, later outcomes
and business descriptions do not affect these scores. Unknown or post-cutoff
challenge dates, self cases, known duplicates/continuations and non-earlier
periods stay excluded. A response unknown by the selected date is withheld.
Explicit no/not/unknown clauses are skipped before term matching. General words
such as ingredient or commodity cannot establish a match. The vocabulary can miss
unlisted words and does not reliably check industry, sales versus input costs,
direction of change or mixed negation. Numerical comparisons retain
units, scope and the company's accounting definition. No incompatible amounts
are subtracted. The new records live in `data/collection/cases.jsonl`; the frozen
M001 source records, cases and experiments are unchanged. No source documents are
stored or served by the app; readers follow links to original reports.

See [collection notes](data/collection/README.md) for source selection, precise
locations, access/retention limits, continuation decisions and curation work.
The three M004 misses now retrieve their intended case first: milk/flour/electricity
finds General Mills, chocolate ingredient inflation finds Hershey, and bottled-water
freight/fuel finds Nestlé Waters. The [paired M005 evaluation](evaluation/search-m005/report.md)
uses 33 queries and expectations frozen in Git before search changes, on identical
eligible cases. Expected useful cases appear in the first five for 7/15 old versus
14/15 new queries. Unexpected candidates on expected-empty queries increase from
3/18 to 4/18: broader terms introduce falling-milk-cost, booming-milk-sales and
airline-fuel false positives, while removing two old false-positive results. One
packaging query drops from rank 1 to 3; mixed negation still misses a useful case.
These are assistant-authored development checks, not independent quality claims.
The [M004 observations](evaluation/collection/results.json) remain reproducible
with the old literal method; their files and all case records remain unchanged.

## Checks

Python 3.14 and Node 22+ run the full development suite; running the app itself
needs no Node installation:

```sh
make test       # Python safeguards/HTTP tests and JavaScript reader-state tests
make validate   # Existing pilot data and judgement coverage
make collection-check # Collection validation and historical M004 literal results
make search-check # Frozen M005 paired evaluation, including misses and regressions
make lint       # Ruff, using the existing .venv development environment
```

For a minimal lint environment: `python3 -m venv .venv`, then
`.venv/bin/python -m pip install ruff==0.17.3`.
JavaScript syntax: `node --check assets/app/app.js`,
`node --check assets/app/reader.mjs` and `node --check scripts/check_app_browser.mjs`.

The optional browser checks use Node 22+ and installed Chrome/Chromium:

```sh
make browser-test
# Full flow with 20 failure/retry cycles on each screen size:
node scripts/check_app_browser.mjs --retry-rounds=20
# For another browser installation:
CHROME_BIN=/usr/bin/chromium make browser-test
```

They start and stop their own local server and browser. Real control clicks cover
search, case/source details, comparison, date recovery and insufficient-evidence
results on desktop and a 375px phone viewport. They also check that technical
information stays optional, a personal draft survives source-case switching,
and a failed connection preserves the description for retry. New-case checks
cover the source disagreement, accounting definitions, publication boundary,
self exclusion, related terms, negation and comparison on both screen sizes. Screenshots go to
`/tmp/ais-case-search-{desktop,mobile}.png`,
`/tmp/ais-reader-comparison-{desktop,mobile}.png` and
`/tmp/ais-reader-case-mobile.png`; the temporary browser profile is removed.
Default Chrome path: `/opt/google/chrome/chrome`. Set `APP_PYTHON` to use another
Python executable.

Additional screenshots: `/tmp/ais-collection-{conflict,comparison,figures}-{desktop,mobile}.png`
and `/tmp/ais-related-search-{desktop,mobile}.png`.

The intermittent retry failure was in the browser check: queued focus scrolling
could move its coordinate target, so the click hit nearby text, and an old idle
flag was mistaken for a finished retry. Clicks now wait for stable, hit-tested
positions; searches must have a fresh submission before completion. Default
checks repeat delayed-response recovery three times per screen size. See the
[browser findings](evaluation/search-m005/browser-check.md) for the reproduction
and the 40-cycle stress result.

## Reproduce the earlier model pilot

[The pilot report](evaluation/pilot/pilot-report.md) describes the ten-case,
five-query BM25/MiniLM experiment. The app combines `data/pilot/cases.jsonl` and
`data/pilot/cases-structured-v2.jsonl` with the new collection through an adapter,
without changing frozen inputs/results. The pilot CLI still uses only its frozen
ten cases.
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

M001 is closed as a development pilot. M002 delivers local search/comparison;
M003 makes the reader experience simpler, with optional technical detail.
M004 adds three distinct source-backed cost situations. M005 fixes browser-check
timing and adds explainable related-input search with a frozen paired evaluation.
Next address context/direction errors and mixed negation, then evaluate with
independent relevance judgements, test structural comparison and consider training when
failures and labels justify it. Builder works end to end without user review
gates. Development findings must remain labelled honestly.
