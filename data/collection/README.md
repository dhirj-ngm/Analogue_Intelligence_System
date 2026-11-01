# Additional case collection — M004

`cases.jsonl` contains three assistant-source-checked situations, added on
1 November 2026. They extend the reader app to 13 observations from eight
companies. They are not human-reviewed or independently validated. Frozen M001
case, evaluation and configuration files remain separate and unchanged.

| Case | Why selected | Evidence and comparison |
| --- | --- | --- |
| GIS-2007 | Earlier grain, dairy and energy pressure in a packaged-food business | [FY2007 10-K](https://www.sec.gov/Archives/edgar/data/40704/000089710107001522/gis072744s1_10k.htm), Item 7 p. 14: US$115 million input-cost increase. Item 6 p. 12: gross margin 36.1% versus 35.6%. Factory actions are the company's explanation; their separate effects are unknown. |
| NES-WATERS-2011-H1 | Oil-related distribution and packaging pressure in bottled water | [H1 2011 release](https://www.nestle.com/media/pressreleases/allpressreleases/half-year-results2011), Nestlé Waters section and Jan.–June table: trading operating margin 8.6%, down 140 basis points. A division's operating margin is different from whole-company gross margin. |
| HSY-2025-Q1 | Later cocoa pressure with a material accounting complication | [Q1 2025 10-Q](https://www.sec.gov/Archives/edgar/data/47111/000004711125000044/hsy-20250330.htm), MD&A pp. 30, 32, and [earnings release](https://hershey.gcs-web.com/news-releases/news-release-details/hershey-reports-first-quarter-2025-financial-results/), Consolidated Results and reconciliation: reported margin 33.7% versus 51.5%; adjusted margin 41.2%. Hedge revaluations and other drivers prevent a cocoa-only interpretation. |

The Hershey release states a decline of 1,780 basis points; the filing states
1,790. Both give the same rounded margin levels. Both stated changes are retained,
with their sources, and the discrepancy is visible in case details and comparison.
It has not been reconciled by guessing. A basis point is one hundredth of a
percentage point; the app explains the unit beside each number.

Each record includes reporting/publication dates, company and business scope,
claim attribution, figures with units/calculation/comparator, field-level source
locators, access/retention notes, continuation group, episode-boundary limits and
explicit unknowns. `figures` and `conflicts` supplement the primary metric. Only
`pressure.value` from these new records enters ranking; no actions, results,
supporting figures or conflicts enter the new similarity text. The adapter in
`ais.collection` supplies the existing search interface from one canonical record.

The periods are observation windows, not claims about the pressure's true start
or end. General Mills FY2008, Nestlé full-year 2011 and later updates are not
counted as additional situations. The Hershey release and filing support one
case; filing amendments are not new episodes. The inspected later Hershey
[amendment](https://www.sec.gov/Archives/edgar/data/47111/000004711125000061/hsy-20250330.htm)
describes trading-plan disclosure corrections without financial-statement changes;
it is not evidence used for this case's May 2025 ranking or figures.

Curation required opening four substantive primary documents, checking reporting
windows and public dates, tracing each claim to named passages, distinguishing
company explanations from figures, and checking units and competing definitions.
The General Mills filing index was unavailable through the web reader and a
direct request returned HTTP 403. Its report was readable; publication is supported
by the [official EDGAR directory](https://www.sec.gov/Archives/edgar/data/40704/)
entry dated 26 July 2007 and the report signatures. The Hershey EDGAR filing index
and release timestamp, and Nestlé's dated release, were inspected. Access methods
are recorded honestly: the web reader provided report text; its HTTP status is
unknown. Link accessibility may vary with bot controls or JavaScript requirements.

A [Danone FY2022 lead](https://www.danone.com/content/dam/corp/global/danonecom/medias/medias-en/2023/corporatepressreleases/pr-danone-full-year-results-22-02-23.pdf.coredownload.pdf)
was inspected but not added. Its aggregate inflation figure is already net of
productivity; that release does not justify inventing a milk-specific cost case.
General Mills FY2007 was selected over FY2008 for its explicit grain/dairy cost
passage. Nestlé Waters was selected for a specific business/cost mechanism rather
than treating the group's margin movement as a water-business result. These are
curation choices, not relevance labels or a representative industry sample.

No source document, PDF, image or HTML snapshot is retained or served. Sources
remain external links. Nestlé's [terms](https://www.nestle.com/info/tc) and
[copyright notice](https://www.nestle.com/info/copyright) describe proprietary
material and limited reproduction rights; its case uses factual paraphrases and
no verbatim excerpt. No open licence is assumed for issuer filings or releases.
Only two minimal evidence snippets (General Mills and Hershey) accompany facts
and locators. This records the retention choice, not permission to republish
documents.

Run `make collection-check` to validate records and reproduce the separate
[development query observations](../../evaluation/collection/results.json).
Inputs were written before running this batch's rankings and their hash is in the
results. Explicit cocoa, grain/dairy/energy and oil/packaging/distribution queries
retrieve the intended new cases first. The packaging regression query retains
Colgate 2022 first, but the enlarged corpus changes other scores/order.

Known misses are retained: milk/flour/electricity misses General Mills;
chocolate/ingredient inflation misses Hershey and returns General Mills on the
word “ingredient”; bottled-water/freight/fuel misses Nestlé. Actions such as lighter
bottles intentionally do not retrieve a case by themselves. These eight checks
are development examples, not a human benchmark, quality score or evidence that
any reported response worked. No synonym expansion or ranking-method change was
introduced in this module.

Final checks: 38 Python tests, 7 JavaScript tests, Ruff, syntax, pilot validation,
collection checks and 19 desktop/mobile browser flows passed. Screenshots were
inspected. Restricted local-socket runs failed in the sandbox and passed when
rerun with loopback access. One initial browser assertion incorrectly expected
zero results after choosing Hershey as a starting case; its broader commodity
wording can match older cases. The assertion now checks the actual requirement:
Hershey is excluded. No remaining test failures; no model experiment was rerun.

M005 preserves the records and historical M004 observations above. The current app
now uses related-input search; `make collection-check` explicitly reproduces the
old literal method. See the [M005 paired report](../../evaluation/search-m005/report.md)
for the three recovered cases and remaining misses/regressions. No new cases or
source documents were needed for those vocabulary gaps.
