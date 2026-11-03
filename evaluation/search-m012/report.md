# M012: distinguish input materials

**AI development judgements, not independent validation.** Human validation
remains deferred with zero human judgements. R01 was not contacted.

Fuel no longer retrieves edible/natural-oil or petrochemical cases through a broad
oil synonym. Copra, dried coconut kernel, paper and cardboard now retrieve the
cases that name them. Results and comparisons distinguish a named input, a more
specific example within a requested category, and related costs that do **not**
establish the requested input. All twenty case records, evidence, dates and frozen
M001 files remain byte-identical; no sources or situations were added.

## Freeze and method

Commit `0241f27` freezes [64 searches and expectations](queries.json),
[M011 observations](baseline.json) and [input hashes](freeze.json) before changing
search. Base: `1630a79`. Queries cover purchased fuels, edible/natural oils,
petrochemicals, copra, paper/cardboard, misleading species/material substitutions,
sales, directions, negation, suppliers, dates and exclusions. Labels are selected,
case-informed AI development expectations; repeated variants are not independent
observations. Five clarification requirements overlap the other groups.

M011 (`context_m010`) and M012 (`context_m012`) run on **identical eligible cases
from the same twenty-case collection** for every query. M011 ranks, scores,
readings and coverage must reproduce the captured baseline. The paired historical
set has 211 entries: M006 65, M007 20, M008 8, M009 37, M010 56 and M011 25.
It includes prior publication boundaries, self/continuations and unsupported
requests. Older module commands separately reproduce their original cohorts.

[Explicit material rules](../../../src/ais/material_context.py) replace only the
broad oil family. They recognize bounded phrases, pass their material identity
through the existing sentence rules, and use directed comparison links:

- Named diesel/petrol belong to fuel; named rice bran oil can support a broader
  vegetable/edible/natural-oil request. Sibling fuels or oil species are not aliases.
- Generic natural fats/oils do not establish edible use, palm oil or coconut oil.
  Petrochemical raw materials/packaging are separate from fuel and natural oils.
- Bare oil prompts clarification. Unsupported named oils do not fall back to a
  broad category. Clearly identified other pressures can still yield partial cases.
- Explicit oil-related distribution costs can offer **related-only** fuel context.
  Neither diesel nor a named fuel is thereby established. Such coverage is removed
  from the supported-input count, with the limitation visible beside each result
  and in comparisons. Paper/cardboard do not establish pulp; copra is not coconut oil.
- Explicit descriptions of making/selling a product do not establish purchase
  pressure. Separately stated purchases or containers remain usable inputs.

BM25 retains k1=1.2 and b=0.75. Typed material links have half the term frequency
of named evidence; document length counts actual mentions, not generated links.
This avoids an alias-count length penalty that initially displaced a useful
freight result during development. Generic existing families retain their weights.
There are no query, company or case exceptions. Only pressure passages enter
ranking; responses, outcomes, identity, geography and numerical figures cannot
increase scores. Eligibility and opposite-direction safeguards are unchanged.

## Source checks and meaning

The original sources were re-opened, with no documents committed or served:

- [Nestlé, 10 August 2011](https://www.nestle.com/media/pressreleases/allpressreleases/half-year-results2011),
  final Waters bullet: oil-related costs in distribution and packaging. This
  passage does not name diesel; the result now says related costs only.
- [Marico, 30 April 2021](https://marico.com/investorspdf/Information_Update_April_30_2021.pdf),
  printed pages 4/6, input-cost discussion and footnote (a): copra, rice bran oil
  and HDPE plastic support the unchanged pressure record. The definition supports
  dried coconut kernel, not an inferred coconut-oil purchase. The source annex
  contains additional benchmarks outside the frozen pressure representation;
  absence from search is not absence from the full source.
- [Kao, 2 February 2023](https://www.kao.com/content/dam/sites/kao/www-kao-com/global/en/investor-relations/pdf/presentations-fy2022-01.pdf),
  printed page 23, FY2022 material-price chart: natural fats/oils, petrochemical
  raw materials/packaging and paper/cardboard. Natural does not specify edible
  use. Its separate 2023 energy forecast is not inserted into 2022 evidence.

Original locators, publication/reporting dates, metric definitions, attribution,
actions and unknowns are unchanged. Matching names does not establish identical
grades, purchase bases, useful analogy or response effectiveness.

## Paired results

| Frozen development check | M011 | M012 |
| --- | ---: | ---: |
| All declared expectations met (64 queries) | 25 | 64 |
| All expected useful or explicitly related targets in first five (38 queries) | 24 | 38 |
| Expected-empty searches left empty (26) | 19 | 26 |
| Queries with forbidden/unexpected results | 23 | 0 |
| Required material clarifications shown (5) | 0 | 5 |

Fourteen queries gain their expected targets; none of the new set loses one from
the first five. Named copra/paper checks and their source-day boundaries pass.
Diesel no longer shows Marico or Kao. Nestlé's remaining fuel connection is
explicitly qualified, not counted as exact-input retrieval. These figures are
not precision, accuracy, independent relevance grades or evidence of generalization.
[Full paired results](results.json) preserve eligible IDs, scores, ranking,
readings, coverage, reasons and implementation hashes.

**42 new-set ranked lists change.** Two target ranks decline: `plastic-not-fuel`
puts Marico second rather than first (Coca-Cola Consolidated rises to first);
`petrochemical-and-food` moves Kao first → second while Marico rises third → first.
Both targets remain displayed. Seven formerly nonempty searches become empty:
palm, olive, coconut oil, crude oil and three bare-oil descriptions. This is
intentional conservative handling, with recall costs recorded below.

**45 of 211 historical lists change.** Three previously labelled targets decline:
`m006/food-scope`, Nestlé third → absent, asks which oil;
`m011/japan-oil-packaging`, Kao first → absent from five, asks which oil while
showing partial packaging cases; `m011/japan-on`, Kao first → fifth with the same
clarification. The latter two previously relied on ambiguous oil wording; their
loss/rank drop is still a retrieval regression. Country names do not restore ranks.

### All ten targets that fell after M011

The first column of ranks is contextual history on seventeen cases. **The actual
method comparison uses twenty cases in both M011 and M012 columns.**

| Historical query | Target | Before M011 (17) | M011 (20) | M012 (20) |
| --- | --- | ---: | ---: | ---: |
| m006/wheat-power | General Mills | 1 | 2 | 2 |
| m006/food-scope | Nestlé Waters | 1 | 3 | Clarify; absent |
| m006/factory-scope | General Mills | 1 | 2 | 2 |
| m006/split-costs | Kimberly-Clark | 2 | 3 | 3 |
| m009/charged-by-supplier | Nestlé Waters | 1 | 3 | 1, related only |
| m009/mixed-directions | Kimberly-Clark | 2 | 3 | 3 |
| m010/comma-mixed | Kimberly-Clark | 2 | 3 | 3 |
| m010/reverse-customer | Nestlé Waters | 1 | 3 | 1, related only |
| m010/comma-with-negated-alternative | Kimberly-Clark | 2 | 3 | 3 |
| m010/different-negative-subject | Kimberly-Clark | 2 | 3 | 3 |

Two ranks are restored with qualified fuel evidence, seven remain lower after
Tiger's added grain/energy coverage, and one now asks for clarification. M012 does
not force old ordering or claim that a restored rank establishes usefulness.

## Remaining misses and next fixes

- No frozen pressure passage explicitly names diesel. An exact diesel comparison
  remains unsupported even when related distribution evidence is displayed.
- Vague oil loses previously expected targets. Naming the material helps, but
  a country, industry or response must not be used to guess its identity.
- A broad `natural oil packaging grain energy` query now omits Marico from the
  displayed five; naming copra brings it back. [Two post-freeze probes](diagnostics.json)
  record this browser-discovered recall limit separately, **excluded from all
  frozen summary counts**. General multi-pressure ranking still needs work.
- HDPE alone remains unrecognized despite its presence in the pressure; PET still
  needs resin/plastic wording. A future typed-polymer check set should cover these
  specific names without treating every polymer as interchangeable. This module
  does not claim to resolve all material names or facts outside the frozen passages.
- Indirect references, unlisted roles/materials and finite sentence rules remain
  limited. An empty search is a retrieval limit, not proof that no source or
  historical analogue exists. The collection remains small and geographically narrow.

## Verification

**109 Python / 18 JavaScript tests passed**, including all frozen new expectations,
historical pairing, material counterexamples, product-versus-input context,
direction/negation, publication/self/continuation rules, future-response withholding,
BM25/link-length checks, and mutations proving non-pressure fields cannot rank.
Ruff check/format, pilot/current collection validation, M005/M006/M007/M009/M010
historical evaluations, M011 comparison and M008 original audit/optional packet
checks passed. Reproduction success does not erase their documented search failures.
Historical runtime hashes verify immutable Git blobs; no prior case, evaluation
observation or manifest was rewritten or evidence hash exempted.

Desktop and 375px Chrome passed **54 grouped checks and 40 delayed failure/retry
cycles**. Searches, named/related/partial comparisons, source links/details, dates,
self exclusions, clarification edits, unsupported inputs and recovery were checked.
Screenshots of material comparisons and clarification were inspected at both sizes.
This is local headless Chrome emulation, not physical-device or broad-browser testing.

Run `make test lint validate collection-check search-check search-check-m005 audit-check`
and `node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20`.
`make search-check-m012` reproduces this paired evaluation alone.
