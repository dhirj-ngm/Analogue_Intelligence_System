# M008 AI development audit

**AI judgements by Builder, not independent human validation.** Human validation
is deferred at the user's request, with zero human judgements. Do not ask R01 to
complete the earlier packet or resend it. The frozen packet remains optional.

Eight case-informed searches were selected in `9fc5895` before these labels.
This is a deliberately small diagnostic sample, including known weaknesses, not
a held-out benchmark or a measurement of general search quality. Cases and
ranking rules are unchanged. [Selection](selection.json), [actual results](snapshot.json)
and [AI reasons](judgements.json) reproduce the scope: every displayed result
(ten pairs), plus four named non-displayed examples. Other eligible cases are
ungraded; no recall estimate is justified.

| Search | Actual displayed results, in order | AI assessment |
| --- | --- | --- |
| A01: food, rising milk/wheat/electricity | General Mills 2007; Kimberly-Clark 2011 | General Mills covers all three pressure families; Kimberly-Clark is energy-only. |
| A02: falling milk, price/profit context | Dean 2015 | Useful falling-cost comparison; benchmark and actual purchase price stay distinct. |
| A03: bottler, packaging/freight | Coca-Cola Consolidated 2022; Colgate 2022; Kimberly-Clark 2011; Nestlé Waters 2011; Colgate 2008 | First and fourth are useful bottler/water comparisons. Three others are narrower contrasts with business/material/metric differences. |
| A04: potato-cost situation | Empty | Honest gap in the recorded pressures; no claim that potato-cost history does not exist. |
| A05: coffee, information by 27 June 2011 | Empty | Chosen Smucker report is after cutoff. Earlier equivalent disclosure remains unknown. |
| A06: falling milk, rising energy | Dean 2015; Kimberly-Clark 2011 | Each supports only one side. Neither documents the joint situation. |
| A07: beef plant buys live animals | Empty | Wording limit; Tyson is a conditional lead if the animals are cattle. Clarification is needed. |
| A08: water bottler; freight supplier serves airlines | Empty | Concrete false abstention: supplier context triggers the global outside-industry veto. Nestlé Waters is a useful omitted case. |

Across the ten displayed pairs, **four AI labels are useful and six partly useful**.
None is judged wholly unrelated in this sample. Six partial matches carry possible
misinterpretation risk if treated as complete matches; that is an AI risk judgement,
not evidence of actual reader confusion. Current explanations identify matched
inputs, but do not plainly count the unsupported pressures. The A08 empty-state
message is misleading about the reader's industry. Outside this sample and the
four extra assessments, relevance is unmeasured.

## Failures and next fixes

1. **Supplier context (A08):** constrain outside-industry exclusions to the reader's
   business. The [water disclosure](https://www.nestle.com/media/pressreleases/allpressreleases/half-year-results2011)
   directly supports distribution/packaging pressure. Future checks must preserve
   abstention for a real airline query while allowing its FMCG supplier-context counterpart.
2. **Partial coverage (A01/A03/A06):** show which requested inputs are supported and
   missing in results/comparison. Two partial cases must not imply one joint episode.
   [Dean](https://www.sec.gov/Archives/edgar/data/931336/000093133616000031/df-20151231x10k.htm)
   supports falling dairy costs; [Kimberly-Clark](https://www.investor.kimberly-clark.com/news-releases/news-release-details/kimberly-clark-announces-third-quarter-2011-results)
   supports rising energy. Neither establishes both. Nestlé Waters below Kimberly-Clark
   in A03 is debatable on business fit, not a demonstrated numerical scoring bug.
3. **Input wording (A07):** offer clarification for live-animal purchases versus
   finished-product prices. [Tyson's cost bridge](https://www.sec.gov/Archives/edgar/data/100493/000010049324000014/tsn-20231230.htm)
   concerns cattle; do not make all beef price/sales statements match cattle costs.
4. **Source access:** preserve the verified Kimberly-Clark issuer HTML alternative
   in a future provenance update. The existing static-file fetch failed in this
   reader; that does not establish universal link failure. Frozen M001 files stay intact.

Nine assessed case sources were inspected: eight recorded URLs reopened directly;
Kimberly-Clark used the equivalent dated issuer HTML release after the static-link
cache miss. [Source checks](source-checks.json) preserve URLs, precise locations and
limits. Smucker's [accession directory](https://www.sec.gov/Archives/edgar/data/91419)
corroborates the chosen 28 June filing date; it does not establish first disclosure.
No original documents were retained. Issuer explanations of profit changes remain
attributed and do not establish isolated action effects.

Run `make audit-check` to verify snapshots, labels, source references, original
case/method hashes and the optional packet. This command is offline; source
availability was checked manually with the web reader. Full checks: 74 Python / 13 JavaScript
tests, Ruff/syntax, pilot/collection validation, M005/M006/M007 evaluations. The
desktop/375px browser flow also runs all eight audit searches with
`node scripts/check_app_browser.mjs --audit-m008`. Screenshots of mixed-direction results and the supplier-context empty state were
inspected on desktop/mobile. These checks reproduce behaviour;
they do not certify the AI relevance labels. No CodeRabbit or paid service was used.
