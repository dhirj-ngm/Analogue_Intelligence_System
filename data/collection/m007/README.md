# M007 collection notes

Assistant curation and development checks on 1 November 2026; no human or independent
validation. Four situations supplement the original thirteen. The canonical records
are [cases.jsonl](cases.jsonl); existing records and frozen M001 files are unchanged.

Selection followed evidence gaps: a named coffee input, falling rather than rising
dairy costs, live-animal processing costs, and metal beverage packaging. It did not
follow observed search ranks. Search/comparison expectations and the proposed material
names were committed in `72d1611` before records or method changes. The four additional
companies and reporting periods add useful variety, but all four businesses are U.S.
focused. This does not resolve geographic bias or establish representative coverage.

| Situation | Reporting window / chosen source date | Why it is distinct; precise locations |
| --- | --- | --- |
| J.M. Smucker retail coffee | May 2010–April 2011 / 28 June 2011 | [Annual report, Exhibit 13](https://www.sec.gov/Archives/edgar/data/91419/000095012311062373/l42203aexv13.htm), MD&A pp. 24–25; Note E pp. 48–49. Green-coffee costs; a division's segment-profit calculation, revised with prior years conformed. Profit growth and a declining margin coexist. |
| Dean Foods dairy | Calendar 2015 / 22 February 2016 | [10-K](https://www.sec.gov/Archives/edgar/data/931336/000093133616000031/df-20151231x10k.htm), MD&A pp. 21, 24; raw-milk table/footnotes p. 24; Note 1, Shipping and Handling Fees, p. F-8. Falling raw-milk costs; the quoted milk benchmark is explicitly not Dean's purchase price. |
| Tyson Beef | 1 October–30 December 2023 (FY2024 Q1) / 5 February 2024 | [10-Q](https://www.sec.gov/Archives/edgar/data/100493/000010049324000014/tsn-20231230.htm), market environment p. 25, cost bridge p. 27, Beef results p. 29; Note 6 Plant Closures p. 10. Cattle inputs in a meat-processing division; operating loss includes inventory, legal and closure items. |
| Coca-Cola Consolidated | Calendar 2022 / 22 February 2023 | [10-K](https://www.sec.gov/Archives/edgar/data/317540/000031754023000009/coke-20221231.htm), MD&A Executive Summary p. 22, Net Sales p. 23, Cost of Sales p. 24. Aluminum and bottle resin at a U.S. bottler, distinct from the global brand/concentrate company and Nestlé's water division. |

Each record has field-level URLs, printed-page/section locators, publication and
reporting dates, metric basis/comparator/scope, assistant provenance, a short evidence
snippet, and unknowns. Figures and actions are company reports, not independently
established causes. None of these records claims underlying consumer demand or an
isolated effect of pricing, closures or efficiency work.

The primary measures deliberately differ: segment profit as a share of sales,
gross margin, and quarterly operating loss in dollars. Dean's supplemental milk
benchmark uses dollars per U.S. hundredweight (100 pounds). Tyson's estimated cattle
cost bridge is not total consolidated cost growth or an isolated profit impact;
Coca-Cola Consolidated's aggregate input-cost estimate cannot be assigned entirely
to aluminum. The app retains those definitions rather than subtracting incompatible
measures. Cost-of-sales treatment of delivery also differs between companies.

## Access, dates and retention

All four substantive original SEC-hosted reports were accessible through the web
reader and inspected; all four were reopened at the end of curation. No raw HTTP
status was exposed by that reader, so records use `http_status: null`, not an
invented 200. Printed page numbers plus headings remain useful if HTML layout changes.

Tyson's [filing index](https://www.sec.gov/Archives/edgar/data/100493/000010049324000014/0000100493-24-000014-index.html)
provided its publication date. Other filing-index fetches were unavailable through
the reader. The accession entries in the SEC company directories for
[Smucker](https://www.sec.gov/Archives/edgar/data/91419),
[Dean](https://www.sec.gov/Archives/edgar/data/931336/), and
[Coca-Cola Consolidated](https://www.sec.gov/Archives/edgar/data/317540/)
provided dated corroboration, recorded in each source's metadata. The Smucker annual
report is a conservative chosen source date: an earlier June earnings-release lead
could not be substantively opened. The record does not assert these facts first
became public on 28 June. Tyson's period start is the day after its disclosed prior
fiscal year end, not an inferred start of cost pressure.

The [SEC Webmaster FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions)
says public filing content is free to access and reuse. Its
[Website Dissemination policy](https://www.sec.gov/about/privacy-information)
allows distribution without SEC permission, requests attribution and restricts
logos/artwork. Both were read on 1 November 2026. We retain factual summaries,
locators and minimal snippets; no original HTML, PDF, images or logos are archived
or served. Company explanations remain attributed to the company, not to the SEC.
Offline validation does not recheck remote availability.

## Curation decisions and limits

Curation required scouting candidate disclosures, opening substantive passages,
corroborating publication dates, reading metric/accounting footnotes, separating
reported numbers from issuer explanations, and manually checking rendered comparisons.
No reliable timed annotation measurement was collected. Rejected leads included
generic Reckitt deflation without enough named-input detail, broader Pepsi commodity
inflation with less variety, and Tyson feed inflation overlapping existing grain
coverage. Coca-Cola HBC was explored; Consolidated supplied the clearer cost bridge.

Only one observation represents each chosen continuing situation. Coffee quarters
and FY2012 follow-ups, Dean's 2015–16 sequence, Tyson's subsequent FY2024 quarters,
and the bottler's 2021–23 reports are not counted as additional independent cases.
Duplicate groups express these curation boundaries; true onset/end remains unknown.

Schema changes were small: the loader combines a separate M007 file, and a metric
may use `USD per 100 lb`. The existing measure fields preserve company estimates
and benchmark definitions; no new outcome or effectiveness field was inferred.
Named coffee, cattle/livestock and aluminum/aluminium families are in a versioned
vocabulary used identically on both evaluation collections. No company exceptions
or first-stage response/outcome features were added. Historical methods retain
their original vocabulary and their thirteen-case cohort.

The [frozen development comparison](../../../evaluation/collection-m007/report.md)
records both gains and misses. Beef wording still misses the cattle case; PET
without resin/plastic is not recognized. Potato and falling-coffee situations
remain uncovered. Outside-industry/complex-negation limitations from M006 persist.
There are still few independent episodes per commodity, no well-established
action effects, limited emerging-market coverage, and no complete human benchmark.
