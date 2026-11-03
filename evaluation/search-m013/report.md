# M013: final local prototype search pass

**AI development checks, not independent validation.** Twenty cases remain fixed;
no collection expansion or human-review effort. Human validation is deferred with
zero human judgements. R01 was not contacted.

## Freeze and small changes

Commit `871d4b4` freezes [44 queries/counterexamples](queries.json),
[M012 observations](baseline.json) and [input hashes](freeze.json) before editing
search. Base: `c0b8b32`. Both methods use identical eligible cases from the same
20-case collection. Each query's IDs/exclusions are checked, and the captured
M012 ranks, scores, coverage, readings and counts must reproduce. The paired
historical set has 275 entries: the previous 211 plus M012's 64. Variants and date
repeats are development checks, not independent samples or held-out human labels.

Two limited changes deliver the final pass:

1. **Reveal remaining compatible matches.** The first five stay ranked by BM25.
   A visible count and **Show more matching cases** expose the remainder in the
   same order, without another query or widening dates. Selection survives; focus
   moves to the newly added cards. All additional cases retain evidence, unknowns,
   partial-coverage cautions and comparison controls. This fixes access to the
   documented broad-query case without forcing its rank or inventing coverage.
2. **Recognize specific polymer names.** HDPE/high-density polyethylene and
   PET/polyethylene terephthalate get separate types using the existing grammar,
   material relations and BM25 formula. Adjacent definitions/generic labels are
   consumed once: “PVC resin” must not fall back to generic resin. LDPE, PVC and
   polypropylene also retain their own types; none has named pressure evidence
   in this collection. A source naming a polymer can support a broad plastic
   request; generic plastic cannot establish a particular polymer, and sibling
   polymers are not aliases. Pet-food/care and PET-scan wording is excluded from
   this material sense. Full names appear in cards and supported/missing inputs.

[Polymer rules](../../../src/ais/polymer_context.py) contain no company/query/case
exceptions. M012 helpers gain optional configuration with unchanged defaults;
original outputs still reproduce. Only pressure text enters ranking. Actions,
profit, metrics, business identity, geography and outcomes remain display-only.
Dates, earlier-period rules and self/continuation exclusions also apply to the
extra results. No case, source, M001 file or prior evaluation output was rewritten.

## Evidence checks

The unchanged pressure records already name the inputs. The original
[Marico update](https://marico.com/investorspdf/Information_Update_April_30_2021.pdf)
(30 April 2021), input-cost discussion and footnote (a), printed pp. 4/6, reports
HDPE market-price pressure; those benchmarks are not actual consumption costs.
[Coca-Cola Consolidated's 2022 10-K](https://www.sec.gov/Archives/edgar/data/317540/000031754023000009/coke-20221231.htm)
(22 February 2023), Item 7 Cost of Sales, printed p. 24, names PET resin within a
multi-input cost increase. It does not isolate PET's cost amount or an action's
causal effect. Both originals were re-opened; no document is stored or served.

Full-name equivalences were checked against primary material producers:
[Dow's HDPE description](https://www.dow.com/en-us/product-technology/pt-polyethylene/pg-polyethylene-hdpe.html)
and [Eastman's PET terminology](https://www.eastman.com/content/dam/eastman/corporate/en/literature/t/trs255.pdf).
These explain vocabulary only, not historical pressure, grades or company purchases.
The app's source attribution, dates, locations and definitions remain unchanged.

## Same-pool results

| Frozen development check | M012 | M013 |
| --- | ---: | ---: |
| All expectations met (44 queries) | 23 | 44 |
| All targets in first five (21 queries) | 8 | 21 |
| All targets accessible after optional expansion (24 queries) | 8 | 24 |
| Expected-empty searches left empty (18) | 16 | 18 |
| Queries with forbidden/unexpected results | 4 | 0 |

The first-five and accessible metrics have different declared target sets; they
must not be compared as a single recall measure. Thirteen first-five target queries
gain their targets, largely polymer wording/date variants. Sixteen gain accessible
targets, including three broad-query variants. Four misleading-result queries are
removed: HDPE/PET definitions no longer retrieve other polymers through “plastic”
or “resin,” and LDPE/PVC descriptions no longer fall back to generic plastic.
No frozen new-set target is lost or moves lower. These selected labels do not
establish precision, general accuracy or independent relevance.

For `natural oil packaging grain energy`, the first five remain Tiger, General
Mills, Kao, Colgate 2008 and Kimberly-Clark. **Marico appears ninth of ten, through
Show more**. It supports natural oil via its more specific rice-bran-oil evidence;
it does not establish grain, energy or packaging. Kao supports two of four named
pressures. The two cases can be compared, but neither establishes the whole
combination. M012 had ten matches internally but returned only five. This is a
visibility gain, **not** a top-five ranking improvement.

Eighteen new-set and **19 of 275 historical first-five lists change**. No previously
labelled historical target moves lower; Kao re-enters fifth for the ambiguous
`m011/japan-oil-packaging` query. Oil still requires clarification: this is partial
packaging retrieval, not oil identification. All 64 M012 frozen query first-five
lists are unchanged. Complete scores, coverage, reasons, extra ranks, eligibility,
changed lists and code hashes are preserved in [results.json](results.json).

Other changes must not be mistaken for universally improved ranking:

- Coca-Cola Consolidated moves fourth → fifth in four packaging/freight entries.
  In thirteen packaging-related entries Kao replaces it in fifth; Coca-Cola
  Consolidated remains available through expansion. These were not labelled
  targets, but the displacement is still recorded.
- For `Aluminum, PET resin and transport costs are rising`, Coca-Cola Consolidated
  remains first. Kimberly-Clark and Marico leave five; their generic/different
  plastic evidence no longer establishes PET. Remaining transport-only cases are
  explicitly partial, not evidence of the combined request.
- For `client-product`, Coca-Cola Consolidated moves third → second and Tiger
  second → third. Changes in material mentions affect BM25 lengths/statistics;
  the change does not demonstrate either case is a better analogue.

## Prototype check and limits

The complete flow runs the real local app on desktop and 375px Chrome. Checks
cover examples, source details/links and metric definitions, search, expansion,
comparison, selection/focus, date controls, publication boundaries, self exclusions,
clarification, insufficient evidence, stale/error states and delayed retry recovery.
Screenshots of broad-query and distinct-polymer comparisons were inspected at both
sizes. A concrete readability issue found during inspection—lowercase “pet” in
coverage—was fixed with full polymer names. No other concrete blocker remained.
This is headless Chrome emulation, not physical-device or multi-browser testing.

**116 Python / 19 JavaScript tests passed; 60 grouped browser checks and 40 delayed
failure/retry cycles passed.** Ruff check/format, syntax, frozen pilot/current
collection validation, M005/M006/M007/M009/M010/M011/M012 historical reproductions,
M013 paired evaluation and the original M008 AI audit/optional packet checks pass.
Historical runtime hashes verify Git blobs through `c0b8b32`; no evidence/data hash
is exempted. Reproduction success does not erase older documented search failures.

Known limits remain explicit: broad-query first-five ordering is not fixed;
viewing more results takes additional reading and is not a relevance guarantee.
Unlisted polymer names, indirect references, complex roles and ambiguous terms can
still miss or mislead. Generic oil needs clarification; related distribution costs
do not establish diesel. Search uses frozen pressure passages, not every fact in
a report. Country names do not filter, coverage remains small/U.S. weighted, and
company action effects, episode bounds, Tiger's cost reconciliation and Hershey's
source discrepancy remain unresolved. No independent human validation is claimed.

**The local prototype is complete with these limits.** No further collection,
search expansion or human review is initiated. Run `make app`; reproduce checks
with `make test lint validate collection-check search-check search-check-m005 audit-check`
and `node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20`.
