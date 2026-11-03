# Historical Analogue Intelligence Engine

**Complete local prototype:** search and compare twenty source-backed FMCG
input-cost situations from fifteen companies. Intended for analysts, researchers
and students exploring historical comparisons. Cases and search checks were
prepared with AI; there is no independent human relevance validation. A company
saying it took an action does not establish that the action caused a result.

## Run locally

Python 3.14 is tested. The app uses the standard library and local files; no
installation, model download, credentials or paid service is needed:

```sh
make app
```

Open **http://127.0.0.1:8000**; stop with Ctrl+C. To use another port:

```sh
PYTHONPATH=src python3 -m ais.app --port 8001
```

Describe purchased inputs and whether costs rose or fell, or choose an example.
Open **Read the case and its sources** for original links, locations, dates,
figures, company-stated actions and unknowns. The first five matches are a starting
point: **Show more matching cases** reveals the rest in the same ranked order.
Select two or three cases and **Compare cases**. Phone comparisons stack vertically.
Each case names the pressures supported and **not established here**; combining
partial cases does not document a situation with every requested pressure.

**Dates and a starting case** is optional. Reports must be public on or before
**Information available by**, with reporting periods ending strictly before the
situation being compared. The starting case and known continuations are excluded
from all results, including additional matches. Invalid dates are explained,
never silently widened. Resetting dates preserves your personal description.

HDPE (high-density polyethylene) and PET (polyethylene terephthalate) match their
own named evidence, not one another or generic plastic reports. Fuel,
petrochemical materials and edible/natural oils stay separate; bare **oil** asks
which material you buy. Live-animal wording also asks for clarification. The edit
button preserves your description and dates without submitting it. Empty results
show a search/evidence limit, not proof that no historical analogue exists.

**How this works** holds method details and scores. The app binds to loopback,
does not persist searches and fetches no sources or models. Original documents
remain external links; the app does not store or serve them.

## Search and known limits

BM25 uses **pressure passages only**, with explicit
[material](src/ais/material_context.py), [polymer](src/ais/polymer_context.py) and
[sentence rules](src/ais/language_context.py). Responses, profit figures, outcomes,
company identity and geography cannot increase scores. Simple rules separate
cost direction, negation, input purchases, sales and supplier/customer context.
Related input words do not establish identical purchases or useful analogies.
Metric units, scope, basis points, attribution and uncertainties remain visible.

[M013's report](evaluation/search-m013/report.md) compares the unchanged twenty-case
collection with M012 using 44 searches frozen in `871d4b4` plus 275 historical
entries. Expected targets in the first five improve from 8/21 to 21/21 queries;
targets accessible after expansion improve from 8/24 to 24/24. Forbidden/unexpected
matches fall from four queries to zero. Nineteen historical first-five lists
change, with no previously labelled target ranking lower. These are **AI development
checks, not independent validation or accuracy estimates**.

The broad `natural oil packaging grain energy` query still puts Marico below five;
**Show more** makes it accessible without claiming an improved top-five rank.
Generic oil needs clarification. Nestlé's related distribution-cost evidence does
not name diesel. Unlisted material names, indirect references and complex business
roles can still be misread; search does not index every fact in the original
report. Country names do not filter results. Coverage is small and U.S. weighted;
episode boundaries, action effects, Tiger's cost-base reconciliation and Hershey's
source discrepancy remain unresolved. The prototype is complete with these limits;
no collection expansion or human-review effort is underway.

**Human validation remains deferred, with zero human judgements.** The withdrawn
M008 packet is optional; R01 must not be contacted or sent the packet again.
[Prior AI audit](evaluation/audit-m008/report.md) labels retain AI provenance.

## Checks and history

Python 3.14 and Node 22+ run tests; Node is not needed to use the app:

```sh
make test lint validate collection-check search-check search-check-m005 audit-check
make search-check-m013  # M012/M013 paired evaluation alone
node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20
```

Lint uses the existing `.venv` with `ruff==0.17.3`; minimal setup:
`python3 -m venv .venv` then `.venv/bin/python -m pip install ruff==0.17.3`.
Browser checks start/stop their own app and Chrome. Override the browser with
`CHROME_BIN=/usr/bin/chromium make browser-test`. Desktop/375px checks cover
search, all matches, evidence, comparisons, dates, exclusions, empty states and
failure recovery. Disposable screenshots include
`/tmp/ais-m013-{broad,polymers}-{desktop,mobile}.png`.

Cases live in the frozen pilot and `data/collection/{cases.jsonl,m007/,m011/}`;
[M011 notes](data/collection/m011/README.md) explain the latest source selection.
Existing records, evidence and prior observations remain unchanged. Historical
commands retain original methods/cohorts and verify code/UI hashes against Git
commits through `c0b8b32`; that history is needed for checks, not for running the app.
Earlier reports remain under `evaluation/`.

Only the archived [M001 model pilot](evaluation/pilot/pilot-report.md) needs ML
packages/downloads: `make setup` then `make run`. Its frozen ten-case experiment
and five earlier user grades are not a complete human benchmark. Models and caches
are ignored by Git. The delivered local app uses no model service.
