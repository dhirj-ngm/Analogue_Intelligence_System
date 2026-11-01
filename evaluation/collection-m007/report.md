# M007 collection expansion checks

Assistant-authored development checks, not independent validation. Source scouting
preceded the provisional labels. Twenty query texts, expected useful/empty cases,
two comparison plans and proposed material aliases were frozen in commit `72d1611`
before new records or search edits. Base: `78e9446`. No expectations were changed
after observing ranks; no case was added to satisfy the remaining miss.

## What was compared

The old collection has 13 observations from eight companies; the expanded one has
17 from twelve. Four new situations cover coffee, declining dairy costs, live
cattle and aluminum beverage packaging. See [curation and sources](../../data/collection/m007/README.md).

Both collections use `context_m007`, the same BM25 formula, date/period safeguards,
self/continuation exclusions and pressure-only representation. A small vocabulary
extension recognizes coffee, cattle/livestock and aluminum/aluminium. M006 sentence
rules and existing material families are unchanged. Only source-backed pressure
enters ranking; company identity, responses, profit figures and later outcomes do
not. The original `context_v1` on the old collection also reproduces the frozen
baseline exactly. On these twenty queries its displayed ranks equal those of the
extended vocabulary on the old collection, isolating the collection addition.

Eligible old-case IDs are identical in both cohorts: new admissions add eligible
new IDs, without changing the treatment of existing cases. BM25 corpus frequencies
and length normalization are recalculated over each eligible collection, so scores
can change even when rank order does not. Comparing absolute scores across these
collections is not a confidence comparison.

## Frozen twenty-query observations

| Development measure | Original M006 / old 13 | Fixed extended method / old 13 | Same method / expanded 17 |
| --- | ---: | ---: | ---: |
| Expected useful case in first five (10 queries) | 4 | 4 | 9 |
| Expected-empty queries returning cases (10 queries) | 0 | 0 | 0 |
| Queries returning an explicitly forbidden case | 0 | 0 | 0 |

Five searches gain their proposed useful case: coffee, falling raw-milk costs,
cattle, aluminum, and aluminum/resin/transport. There are no useful-case retrieval
losses or target-rank regressions in this twenty-query set. Seven displayed lists
change, including two existing-pressure controls:

- The packaging/logistics target, Colgate 2022, remains first. Coca-Cola Consolidated
  enters fourth, Dean is absent, Colgate 2015 moves fifth, and P&G leaves the first
  five. Those additional cases have no exhaustive relevance grades.
- Packaging-only mixed negation retains Colgate 2022 third and excludes both dairy
  records. The bottler is a fifth result. The earlier length/tie ordering persists.
- The aluminum/resin/transport search moves the new bottler first, moving four
  existing displayed cases down and Unilever out of the first five. This is a
  displacement observation, not an independently judged quality improvement.

Rising milk excludes the declining Dean situation. Falling coffee, milk/cattle
sales, airline fuel, steel smelting, potato inputs and four pre-publication queries
remain insufficient evidence. Publication-day inclusion, prior-day exclusion,
reporting-end limits and self/continuation exclusions are also checked for the
new records. Unsupported searches do not widen dates or use profit to find a match.

**Remaining frozen miss:** “Beef input costs are rising” does not retrieve Tyson's
cattle situation. Beef output prices and live-cattle inputs are not automatically
equated. The source record is not changed to make this query pass. PET-only wording
also remains outside the vocabulary; “PET resin” uses the established resin family.

## Older-query rank probe

The existing 65 M006 query texts were also run on both collections with the same
extended method. Their original input files and historical evaluation remain
unchanged. Twenty displayed lists change. None loses an originally expected useful
case from the first five, but **two targets rank lower**:

| Query | Existing target | Old → expanded rank | Interpretation requiring inspection |
| --- | --- | --- | --- |
| Milk costs | General Mills 2007 | 1 → 2 | Dean's shorter declining-milk passage ranks first for an unspecified direction. The app shows the differing directions. |
| Milk costs fell while energy bills rose | Kimberly-Clark 2011 | 1 → 2 | Dean matches falling milk only and precedes the energy-only case. Neither is evidence for the complete two-input situation. |

Four old expected-empty texts now return cases: rising arabica-coffee costs and
three declining-milk descriptions. Those labels described gaps in the old corpus;
they cannot simply be reused as false-positive labels for the larger collection.
Smucker supports green coffee, **not a verified arabica species**; that distinction
remains unknown. Dean supports falling inputs and company-reported profit, not
independent proof of a recovery mechanism. No new relevance grade is asserted here.
All changed lists, old labels and target ranks are recorded in
[results.json](results.json), alongside the main paired observations.

## Comparison and verification

The frozen comparison plans were read in the app on desktop (1280px) and phone
(375px). Dairy comparison keeps rising/falling directions visible and exposes the
milk benchmark's units and exclusion of purchase premiums. The three-company
comparison clearly distinguishes annual coffee-segment margin, quarterly beef
operating loss, and annual bottler gross margin. Sources, accounting definitions,
reported actions, other drivers and unknowns remain attached to individual cases.
These are inspection observations, not independent acceptance or effectiveness
grades. Browser automation checks controls, layout, source link targets, quantities,
definitions, comparison clearing, dates, empty states and connection recovery.

Reproduce without fetching sources/models:

```sh
make collection-check
make collection-check-m007
make search-check
make search-check-m005
make test
make lint
make validate
make browser-test
```

The source documents were opened and read manually, not fetched by these offline
commands. Machine observations include fingerprints of frozen inputs, new records
and implementation. Full current verification and browser results are in
[verification.md](verification.md). Coverage is still narrow and U.S. biased;
complex sentence/industry limits from M006, incomplete episode boundaries and the
absence of independently established action effects remain. No independent
validation or general search-quality gain is claimed.
