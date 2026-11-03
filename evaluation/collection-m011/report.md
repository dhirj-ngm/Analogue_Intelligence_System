# M011 collection expansion beyond the U.S. focus

**AI development checks, not independent human validation.** Human validation
remains deferred with zero human judgements; R01 was not contacted.

Three source-backed situations take the app from **17 to 20 cases**, from twelve
to fifteen companies: Marico's India business (2021), Kao's Japan/overseas consumer
products (2022), and South Africa-led Tiger Brands (2023). They add copra and
vegetable-oil benchmarks, petrochemical/paper cost pressure, and electricity-cut
operating costs alongside grain inflation. This is useful variety, not geographic
representativeness. Kao is not a Japan-only result; Tiger's gross margin is a group
measure. [Collection notes](../../../data/collection/m011/README.md) give original
links, exact pages, dates, source checks, scope and retention decisions.

## Freeze and comparison

Commit `98b8001` freezes [25 searches and comparison requirements](checks.json),
[17-case baseline observations](baseline.json) and [input hashes](freeze.json)
before adding records. Base: `13814c2`. The checks were chosen for geographic and
input gaps, counterexamples, insufficient evidence and publication boundaries,
not from expanded rankings. The small sample includes repeated/date-varied
descriptions; it is not 25 independent relevance observations.

Both cohorts use **the same M010 method** (`context_m010`), material vocabulary,
pressure-only representation, scoring formula, date/evidence rules and
self/continuation exclusions. Every existing case's eligibility is unchanged;
only new eligible candidates are added. Corpus statistics change BM25 scores;
scores across cohorts are not probabilities or calibrated quality comparisons.

| Frozen development check | 17 cases | 20 cases |
| --- | ---: | ---: |
| Queries with all expected useful targets in first five (16) | 2 | 14 |
| Expected-empty queries left empty (5) | 5 | 5 |
| Queries with forbidden/unexpected matches | 0 | 1 |

Twelve queries gain their expected targets. Fourteen of the 25 ranked lists change.
All three new source-day checks retrieve the new case; previous-day checks exclude
it. Searches about an actual airline, milk sales, absent oil inflation, falling
coffee and unsupported potatoes remain empty. Per-query outputs and failures,
eligible IDs, scores, coverage, comparisons and implementation hashes are in
[results.json](results.json). A successful reproduction check does **not** mean
every search expectation passed.

Useful gains include Marico for vegetable-oil/plastic costs, Kao for packaging/oil
pressure, and Tiger for combined wheat/maize and electricity-cost pressure. The
three can be selected together using `oil packaging grain energy`. Each remains
a partial comparison: Marico supports oil, Kao oil/packaging, Tiger grain/energy.
No combined situation or interchangeable financial measure is claimed.

## Regressions, misleading matches and gaps

Three frozen failures remain:

- **Copra alone:** empty despite Marico's disclosure. The material name has no
  family in the unchanged vocabulary; spelling out dried coconut kernel does
  not create a hidden scoring alias.
- **Paper/cardboard alone:** empty despite Kao's disclosure. These words are not
  mapped to fibre or packaging. The case can be found through its other pressures.
- **Diesel fuel:** Kao and Marico appear above Nestlé Waters through the broad
  oil family, although their natural/edible oils do not establish diesel pressure.
  These are misleading comparisons for that request, not successful new coverage.
  Source wording, related-word cautions and case differences expose the mismatch;
  those cautions do not fix ranking or establish exact-input support.

Among **186 historical query entries**, 51 ranked lists change. Ten entries have
a lower-ranked prior useful target; no prior labelled target leaves the first
five. These are older development labels, not fresh human assessments of new cases.
The three fuel-oriented entries `m006/food-scope`, `m009/charged-by-supplier` and
`m010/reverse-customer` move Nestlé Waters from first to third behind the two
natural-oil cases: a concrete regression. The other seven declines place Tiger
above existing grain/energy cases or add another partial electricity match;
the earlier target remains available. All ten are recorded, not averaged away.
Other old, unlabelled-as-target cases also leave the displayed five; complete
ranked lists preserve those changes.

Country names do not filter or boost results. A country-specific query can still
show another market's case. Geography labels and business-scope differences make
that visible. Bare input names, unlisted industries, indirect references and
M010's conservative clarification misses remain limited. Latin America, many
Asian/African markets, local commodity varieties and falling-cost episodes remain
underrepresented; isolated action effects and episode boundaries are unknown.
Hershey's earlier discrepancy is unchanged.

Next search work should freeze tests separating fuel from edible/natural oils
before changing family handling, and assess copra/paper terminology without broad
synonyms that invent input evidence. Further collection work should target other
local markets and genuinely distinct pressure directions, not these query ranks.

## Evidence and app verification

All three original PDFs were substantively read; dates, chart/table bases and
locators were checked. Temporary PDFs were inspected and their SHA-256 recorded.
Marico's first raw request returned 406; a browser User-Agent request returned
200. Kao/Tiger downloads succeeded without recorded status codes. All sources
remain external. The terms reserve content rights; no redistribution permission
is claimed and no document, image, brand artwork or verbatim excerpt is committed
or served. Offline validation does not check live remote availability.

The records preserve India versus group scope, original percentage/JPY/ZAR units,
market benchmarks versus consumed costs, issuer attribution, and explicit unknowns.
Kao's 2023 forecast bar is excluded from its 2022 pressure. Its negative JPY46.0
billion estimate is a year-on-year material headwind after Chemical price offsets,
not operating loss or a cumulative 2015 comparison. Tiger's reported 76/12/48
million rand cost bases are retained without inventing a reconciliation. Company
pricing/savings explanations and estimated action contributions are not independent
proof that actions caused results. Existing case records and frozen M001 files
are byte-identical.

98 Python and 17 JavaScript tests passed, including current HTTP behavior,
original-file hashes, each new case's dates/self/continuations, source timing,
future-response withholding, scope/unit checks and mutations proving that
geography, identity, actions, profit and figures cannot influence ranking.
Ruff/syntax, pilot/current collection validation, M005/M006/M007/M009/M010
historical reproductions, M011 paired observations and the original M008 audit/
optional packet checks passed. Earlier evaluations explicitly retain their original
cohorts. Their data and outputs are not rewritten; immutable Git blobs verify
historical runtime/UI hashes, with no data/evidence exemptions.

Desktop/375px Chrome passed **48 grouped checks and 40 delayed failure/retry
cycles**. Coverage includes real new-case searches/details/source links, all three
publication boundaries/self exclusions, geographic scope in comparisons, original
currency definitions, the unreconciled cost figures, partial coverage and empty
results. Screenshots of cards, comparisons and measures were inspected at both
sizes. This is local headless Chrome emulation, not physical-device or broad
browser testing. New check assertions initially needed correction for collapsed
method text, a row-header offset, and deterministic duplicate selection; no
ranking/date safeguard was relaxed to pass them.

Run `make test lint validate collection-check search-check search-check-m005 audit-check`.
`make collection-check-m011` reproduces this expansion alone. For the full current
UI use `node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20`; its audit
queries use the current M011 observations. `make audit-check` separately reproduces
the original M008 method/packet and confirms human validation remains deferred.
