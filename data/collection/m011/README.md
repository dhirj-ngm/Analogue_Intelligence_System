# M011 collection notes — 3 November 2026

Three assistant-curated company situations broaden the seventeen-case collection.
They were selected for local evidence, geography and input/measurement variety,
before inspecting expanded search ranks. No human review or independent validation
occurred. [cases.jsonl](cases.jsonl) is separate from every existing case file.

| Situation / dates | Scope and evidence locations | Important distinction |
| --- | --- | --- |
| Marico, January–March 2021; published 30 April 2021 | India domestic FMCG. [Issuer update](https://marico.com/investorspdf/Information_Update_April_30_2021.pdf), cover exchange letter; printed p. 2 / PDF page 3 for India margin and actions; printed p. 4 / PDF page 5 for inputs; printed p. 6 / PDF page 7, footnote (a), for benchmarks. | Copra (dried coconut kernel), rice bran oil and HDPE (a plastic). The reported India operating margin is 17.6%, versus 22.8%. Market-price changes of 25%, 39% and 31% respectively are not actual inventory consumption costs. The India profit numerator is not reconciled to statutory profit in the update. |
| Kao, calendar 2022; published 2 February 2023 | Japan and overseas consumer products. [Issuer presentation](https://www.kao.com/content/dam/sites/kao/www-kao-com/global/en/investor-relations/pdf/presentations-fy2022-01.pdf), title date; printed/PDF pp. 13, 15 and 23 for income bridge, actions and material chart. | Natural fats/oils, petrochemical materials/packaging, paper/cardboard. Negative JPY46.0 billion is an estimated 2022-versus-2021 material-price effect, net of stated Chemical selling-price offsets. It is neither operating loss nor the chart's cumulative level versus 2015. JPY14.0 billion pricing contribution is company attribution. The separate 2023 forecast is excluded. |
| Tiger Brands, October 2022–March 2023; published 30 May 2023 | South Africa-led group, including exports/international activities. [Issuer booklet](https://www.tigerbrands-ir-digital.com/results/2023/interims-2023/pdf/booklet.pdf), printed p. 1 / PDF page 3 for costs, grains and gross margin; printed p. 3 / PDF page 5 for release date and outlook; printed p. 5 / PDF page 7 for income statement. | Wheat/maize inflation and operating with rolling power cuts. Group gross margin is 27.0%, versus 29.2%. Reported total outage costs of ZAR76 million versus ZAR12 million and incremental energy costs of ZAR48 million are separate stated bases with no reconciliation. Do not replace 48 with 64 or label all outage costs diesel. |

These are distinct companies and business situations, not independent global
economic shocks. Only one observation represents each continuing episode:
Marico's 2020–22 sequence, Kao's 2021–23 sequence, and Tiger's 2022–24 sequence.
Annual/quarterly updates are not added as further cases. Reporting windows do
not establish the true onset or end of pressure. Early HUL leads were not used:
the existing collection already contains Unilever's global 2022 observation,
making a subsidiary observation less useful for a focused distinct batch.

Marico contributes an India-specific cost and profit context; Tiger contributes
South African operating constraints. Kao is explicitly Japan **and overseas**,
not a Japan-only result. Existing global cases also cover several markets: the
old collection was U.S.-focused, not exclusively U.S. The added labels describe
scope; country names neither filter nor boost ranking.

## Source access and retention

All three substantive original PDFs were opened with the public web reader and
temporary local inspection copies. Their charts/tables and dates were inspected;
the SHA-256 of each inspected PDF is recorded without retaining the document in
Git or the app. Field-level locators distinguish printed pages from PDF positions.
The app links to the original documents; it does not serve PDFs, images or HTML.

Marico initially returned HTTP 406 to default curl, then HTTP 200 with an ordinary
browser User-Agent. Its actual successful status is recorded. Kao and Tiger
downloads succeeded, but their raw status codes were not captured, so those remain
null. A web-reader attempt at Tiger's terms returned 429; its ordinary direct PDF
download succeeded. These are actual access observations, not availability promises.

The [Marico terms](https://marico.com/india/terms-of-use),
[Kao legal statement](https://www.kao.com/global/en/terms-of-use/), and
[Tiger terms, clauses 4–6](https://www.tigerbrands.com/pdf/download-centre/policies-and-charters/policies/Tiger-Brands-Website-Terms-and-Conditions.pdf)
were read. They reserve source-content rights and do not supply an open
redistribution license. No such license or permission is asserted. This batch
keeps own-word factual notes and source locations, without source documents,
branding, verbatim passages or screenshots in the product/repository. Temporary
inspection files are not app assets. Offline checks do not re-fetch sources.

## Curation and remaining gaps

Curation involved candidate searches, substantive passage checks, release-date
verification, chart/table inspection, comparison of local and group scopes,
metric definitions, terms checks and rendered comparisons. No reliable timed
annotation measurement was collected. Kao's forecast energy increase was excluded
from the 2022 pressure passage after inspecting the chart; the exact component
amounts were not digitized. Source and schema unknowns were kept rather than filled.
Small schema additions support geography labels and original JPY/ZAR units.
They are display metadata; the search method and vocabulary remain unchanged.

The [frozen collection comparison](../../../evaluation/collection-m011/report.md)
records gains and failures. Bare copra and paper/cardboard queries miss useful new
cases. The broad oil family misleadingly connects fuel with natural/edible oils;
case differences and source wording flag the distinction, without claiming the
ranking issue is solved. No geographically representative coverage is claimed:
Latin America, many Asian/African markets, local commodity varieties, declining
costs and isolated action effects remain thin or absent. Human validation stays
deferred, with zero human judgements and no R01 contact.
