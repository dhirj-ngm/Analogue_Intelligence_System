# Historical Analogue Intelligence Engine

A small source-backed app for finding earlier company situations and comparing
their input costs, reported responses, differences and unknowns. It starts with
FMCG and has **17 assistant-checked observations from twelve companies**.
Company explanations do not establish that an action caused a result or would
work elsewhere. The collection has no independent human relevance validation.

## Run the app

Python 3.14 is tested. The app uses the Python standard library, local case files
and BM25. No package installation, model download, paid service or credentials
are needed:

```sh
make app
```

Open **http://127.0.0.1:8000**; stop with Ctrl+C. For another port:

```sh
PYTHONPATH=src python3 -m ais.app --port 8001
```

Describe a situation or choose an example. Open **Read the case and its sources**
for original links, figures, definitions, reported actions and unknowns. Select
**two or three cases**, then **Compare cases**. Phone comparisons stack vertically.

Each result and the first comparison row name the supported pressures and those
**not established here**. Partial cases do not document one combined situation.
Counts refer to identified named pressures, not every meaning of the description.
Missing evidence does not mean a cost did not change. Profit amounts, margins,
benchmarks and adjusted figures retain their own definitions and scope; basis
points are explained beside the numbers.

A food/water business can mention an airline or logistics supplier without becoming
an outside-industry query. A genuine airline/logistics business remains outside
this collection. A supplier's own costs are not automatically the reader's costs.
For **live animals**, the app asks whether you mean cattle or another animal.
**Edit the input description** selects the original phrase without changing text,
dates or submitting a search. Clarify what you buy and whether costs rose or fell.
Beef selling prices/sales remain separate from cattle purchase costs.

**Dates and a starting case** is optional. **Information available by** includes
reports published on or before that date; periods must end strictly before the
situation being compared. A starting case and known continuing reports are
excluded. Returning to **My own situation** restores your draft; resetting dates
keeps your own description. Invalid dates are explained and focused, never widened
silently to obtain results. Empty results describe a date, evidence, wording or
scope limit; they do not establish that no historical comparison exists.

**How this works** keeps method details and BM25 scores optional. The app binds
to loopback, does not persist searches, and fetches no sources or models. Original
reports open separately at the publisher/SEC; documents are not stored or served.

## Method, evidence and limits

BM25 scores named input families in **case pressure passages only**. The
[vocabulary](src/ais/related.py), [additional material names](src/ais/vocabulary.py)
and [reader-role rules](src/ais/reader_context.py) are small and explicit.
Responses, profit figures, business identity, later outcomes and rationale cannot
increase scores. Publication evidence, earlier periods and self/continuation
exclusions are shared across methods. Future responses are withheld.

Rules distinguish cost direction, negation and sales/demand roles. Opposite shared
input directions veto a partial match. Source pressure wording stays unchanged;
coverage is computed after scoring. Related words do not establish identical
purchases or a useful analogy. Unknown cost names do not become scoring synonyms.
Bare topic lists retain unspecified direction.

[M009 paired checks](evaluation/search-m009/report.md) freeze 37 development queries
before changes (`78abe11`). On identical eligible cases, expected-case retrieval
rises from 10/21 to 21/21; expected-empty queries from 15/16 to 16/16, with no
expected-case or target-rank regressions in that set. Only the intended supplier
failure changes ranks among 93 historical query entries. These case-informed
checks are **not independent validation or a general accuracy estimate**.

Unpunctuated alternative negation and comma-only opposing directions remain
[conservative misses](evaluation/search-m009/diagnostics.json). Unlisted industries,
complex roles and input phrases can still be misread. Collection coverage is narrow
and U.S. biased; episode bounds and action effects remain uncertain. Hershey's
existing source discrepancy remains visible and unresolved.

Additional cases live in `data/collection/cases.jsonl` and
`data/collection/m007/cases.jsonl`. All existing records and frozen M001 files are
unchanged. [Collection notes](data/collection/m007/README.md) explain source access,
precise locations, metric definitions, retention and continuation decisions.

**M008 human validation is deferred, with zero human judgements.** The withdrawn
154-pair packet remains optional; no R01 follow-up or resend is authorized. The
[small AI audit](evaluation/audit-m008/report.md) retains explicit AI provenance;
its original outputs still reproduce using the historical method. The user does
not need to grade anything.

## Checks

Python 3.14 and Node 22+ run the tests; the app itself does not need Node:

```sh
make test                # Python safeguards/HTTP checks and JavaScript reader tests
make lint                # Ruff check/format in the existing .venv
make validate            # Frozen pilot data and judgement coverage
make collection-check    # Current collection and historical M004 literal checks
make search-check        # M006/M007 historical and M009 paired evaluations
make search-check-m005   # Earlier literal/related comparison
make search-check-m009   # M009 alone
make audit-check         # Original M008 audit, optional packet and deferred human state
```

For minimal lint setup: `python3 -m venv .venv`, then
`.venv/bin/python -m pip install ruff==0.17.3`.
Older checks retain original cohorts/methods and verify original runtime/UI hashes
against Git at `1e4e6d3`; those checks need that history. No evidence/data hash is
exempted. The app itself adds no Git dependency.

Browser checks start and stop their own server and Chrome:

```sh
make browser-test
# Current M009 flow, historical audit searches and 40 delayed-response retry cycles:
node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20
# Override the default /opt/google/chrome/chrome if needed:
CHROME_BIN=/usr/bin/chromium make browser-test
```

Desktop/375px checks cover searches, sources, comparison, dates, self exclusions,
empty states, clarification and failure recovery. Screenshots are disposable in
`/tmp/ais-case-search-{desktop,mobile}.png`,
`/tmp/ais-m009-{partial,clarify}-{desktop,mobile}.png` and related comparison files.
The old audit flag uses recorded M009 expectations for the current UI; the audit
command separately reproduces M008. The optional archived review-form check is
`make review-browser`; its synthetic drafts are not human judgements.

## Earlier model pilot and project history

The [M001 report](evaluation/pilot/pilot-report.md) describes the frozen ten-case,
five-query BM25/MiniLM experiment. The app uses these records plus the additional
collection through an adapter, without rewriting pilot inputs/results. Detailed
Colgate evidence remains in `data/episodes.jsonl` and `data/source_manifest.jsonl`.
The five user grades do not form a complete human benchmark.

Only the earlier model pilot needs ML dependencies and an initial internet download:

```sh
make setup
make run
# After caching the model:
HF_HUB_OFFLINE=1 make run
```

Models/caches are ignored by Git. `make run` reproduces the earlier model pilot;
`make app` runs the reader. M002/M003 built the app/reader experience, M004/M007
expanded the collection, and M005/M006 introduced related-input/context checks.
[M008](evaluation/audit-m008/report.md) audited the app; M009 fixes the three
reader-facing failures. Next work should address the documented grammar limits
and broader realistic development samples. Development judgements stay labelled
honestly; human validation remains deferred.
