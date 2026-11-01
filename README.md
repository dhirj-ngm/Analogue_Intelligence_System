# Historical Analogue Intelligence Engine

An evidence-based tool for finding earlier company situations that help explain
a current business challenge. Start with FMCG input costs and company responses.
The app lets readers describe a situation, inspect ranked historical cases and
compare up to three side by side, with sources, important differences and unknowns.
Issuer explanations remain distinct from independently identified effects.
A reported recovery does not establish that an action caused it.

The collection has **17 assistant-checked observations from twelve companies**.
M007 adds Smucker's 2011 coffee inputs, Dean Foods' 2015 falling milk costs,
Tyson Beef's early-2024 cattle costs, and Coca-Cola Consolidated's 2022 packaging
inputs. These are distinct situations, not successive reports of one episode.
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
all cases, the collection lacks a matching pressure, or the wording does not support
a comparison. It explains a direction conflict, a sales statement, an outside
industry or an unclear change. You can edit the description, check dates or try
an example. `Semiconductor shortages at a bank`
shows a collection gap. Empty results are not evidence that no historical
comparison exists elsewhere.

**How this works** contains the method, date/exclusion counts and optional BM25
scores. Each result shows the words connected in your description and the report,
with sources, differences and unknowns. Related terms do not establish a useful
analogy or that the report measured your exact input. The app shows which pressures
it read and which parts it left out. Direction appears beside each match and in
comparison; topic lists are labelled “direction not specified”. Reported actions
do not prove what caused a result. Metric definitions and exact source locators
remain available beside the company-reported figures.

Try **Coffee costs** or **Falling milk costs**, or describe rising cattle or aluminum
costs. A bare “milk” search can show both rising and falling costs: read the direction.
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
other related inputs. [M007's material names](src/ais/vocabulary.py) add coffee,
cattle/livestock and aluminum/aluminium. They apply to all queries and eligible cases, with no case
IDs or query-specific rules. Responses, profit figures, rationale, later outcomes
and business descriptions do not affect these scores. Unknown or post-cutoff
challenge dates, self cases, known duplicates/continuations and non-earlier
periods stay excluded. A response unknown by the selected date is withheld.
M006 adds [explicit clause rules](src/ais/context.py) for input role, cost direction,
negation and business context. Falling costs cannot match a report of rising costs
for the same input, even if another shared input fits. Sales/demand statements do
not become input costs. Contrasts preserve the positive side of “not milk but
packaging”; “not only” is treated as additive. Recognized outside industries such
as airlines are set aside. Product names in recognized business descriptions do
not become purchased inputs. Ambiguous changes and denied/unknown directions are
not filled in. Bare input-topic lists remain useful searches with unspecified
direction. These are limited language rules, not a complete industry or sentence
classifier. General words such as ingredient or commodity are still insufficient. Numerical comparisons retain
units, scope and the company's accounting definition. No incompatible amounts
are subtracted. Additional records live in `data/collection/cases.jsonl` and
`data/collection/m007/cases.jsonl`; the frozen
M001 source records, cases and experiments are unchanged. No source documents are
stored or served by the app; readers follow links to original reports.

See [M007 collection notes](data/collection/m007/README.md) and
[earlier notes](data/collection/README.md) for source selection, precise
locations, access/retention limits, continuation decisions and curation work.
The three M004 related-term searches still find their intended cases first.
The historical [M006 paired report](evaluation/search-m006/report.md) compares M005 and M006
on 65 queries frozen before implementation, using the original thirteen-case collection.
Useful-case retrieval in the first five rises from 27/33 to 33/33; unexpected
results on expected-empty queries fall from 16/32 to 0/32, and queries returning
explicitly forbidden cases fall from 5 to 0. No useful-case or target-rank
regressions occurred in this set. These assistant-authored examples were chosen
with knowledge of M005 failures; they are not independent validation.

The packaging-only query still puts Colgate 2022 third: BM25 favours a shorter
packaging-only passage, and Colgate 2015 ties with 2022 and precedes it by ID.
Adding logistics still puts Colgate 2022 first. A score does not establish which
case is the better analogy. [Post-implementation diagnostics](evaluation/search-m006/diagnostics.json),
excluded from the 65-query metrics, record remaining misses with unpunctuated
negation, comma-linked cost directions and supplier-industry context. Unlisted
sectors, word senses and complex attachments can still mislead or cause abstention.

The [M004 observations](evaluation/collection/results.json) and
[M005 report](evaluation/search-m005/report.md) remain unchanged and reproducible
with their historical methods. All existing cases and frozen M001 files are unchanged.

The [M007 comparison](evaluation/collection-m007/report.md) uses twenty new checks
frozen before adding records. With one fixed method, expected useful cases appear
in the first five for 4/10 searches on the old collection and 9/10 on the expanded
one; all ten expected-empty searches stay empty. Beef wording still misses Tyson's
cattle case, and PET alone is unrecognized. An additional probe of the older 65
queries finds no useful-case retrieval losses but two target-rank drops: General
Mills for “milk costs” and Kimberly-Clark for falling milk plus rising energy both
move from first to second. These development checks are not independent validation.
The added sources remain U.S. focused; episode boundaries and action effects are
still uncertain. More records do not establish reliable search quality.

## Checks

Python 3.14 and Node 22+ run the full development suite; running the app itself
needs no Node installation:

```sh
make test       # Python safeguards/HTTP tests and JavaScript reader-state tests
make validate   # Existing pilot data and judgement coverage
make collection-check # Collection validation and historical M004 literal results
make search-check # Historical M006 evaluation plus frozen M007 old/expanded checks
make collection-check-m007 # M007 alone, including older-query rank-change probe
make search-check-m005 # Reproduce historical M005 ranks without rewriting its files
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
self exclusion, related terms, cost direction, sales/industry checks, mixed negation,
ambiguous wording and comparison on both screen sizes. Screenshots go to
`/tmp/ais-case-search-{desktop,mobile}.png`,
`/tmp/ais-reader-comparison-{desktop,mobile}.png` and
`/tmp/ais-reader-case-mobile.png`; the temporary browser profile is removed.
Default Chrome path: `/opt/google/chrome/chrome`. Set `APP_PYTHON` to use another
Python executable.

Additional screenshots: `/tmp/ais-collection-{conflict,comparison,figures}-{desktop,mobile}.png`
and `/tmp/ais-related-search-{desktop,mobile}.png`. M006 adds
`/tmp/ais-context-{empty,mixed}-{desktop,mobile}.png`. M007 adds
`/tmp/ais-m007-{dairy,comparison,measures}-{desktop,mobile}.png`, including
benchmark units and different profit measures. Price and dollar-amount help stays
separate from margin-percentage explanations.

The intermittent retry failure was in the browser check: queued focus scrolling
could move its coordinate target, so the click hit nearby text, and an old idle
flag was mistaken for a finished retry. Clicks now wait for stable, hit-tested
positions; searches must have a fresh submission before completion. Default
checks repeat delayed-response recovery three times per screen size. See the
[browser findings](evaluation/search-m005/browser-check.md) for the reproduction
and the 40-cycle stress result.

## M008 AI development audit

Human validation is deferred, with zero human judgements. The earlier 154-pair
packet remains an optional frozen artifact; no further R01 review request or
resend is authorized. The user does not need to grade anything.

The [small AI audit](evaluation/audit-m008/report.md) assesses eight selected
searches, all ten displayed results and four named non-displayed examples, with
reasons and nine source checks. These are Builder AI judgements, not independent
human validation or a general quality estimate. It identifies a supplier-industry
false abstention, unclear partial coverage and a live-animal wording limit.
Ranking rules and case records are unchanged; next fixes are proposed in the report.

Run `make audit-check` (also `make review-check`) to reproduce the audit and
verify the optional human packet and deferred state. Run
`node scripts/check_app_browser.mjs --audit-m008` for the full desktop/mobile flow
plus these searches. Original sources stay external. No paid review service is used.

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
timing and adds explainable related-input search. M006 adds conservative context,
direction and negation checks, visible interpretations and a frozen comparison.
M007 adds four source-backed situations and compares the old and expanded collections.
M008 completes a small AI development audit; human validation is deferred.
Next address supplier-context and partial-coverage limits using the recorded
failure cases. Broader comparison, collection and model work needs evidence
that justifies it. Builder works end to end without user review gates;
development judgements remain labelled honestly.
