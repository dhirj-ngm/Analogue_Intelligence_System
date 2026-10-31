# M001 development pilot

Closed 31 October 2026. Ten assistant-checked source-linked observations across
five issuers and multiple periods, five fixed queries, 33 assistant-labelled
eligible pairs, and paired BM25/MiniLM runs. Results are descriptive; the labels
and most cases have no independent human review.

| Method | Mean P@5 | Mean nDCG@5 |
| --- | ---: | ---: |
| BM25 | 0.400 | 0.6253 |
| MiniLM dense | 0.360 | 0.6561 |

Means include one query with no relevant case. Candidate counts by query were
7, 5, 2, 9 and 10. Dense has slightly higher nDCG and lower P@5, but five
assistant-labelled queries cannot establish superiority. The Q3 nDCG of 1.0
reflects only two eligible candidates and a partial match. Q5 asks for an
export-embargo case absent from this corpus; both methods still rank unrelated
cases because no calibrated abstention rule exists.

The ten records were purposively selected from accessible official releases and
filings: Colgate 2008/2015/2020/2022, Kimberly-Clark 2011/2018, Clorox
2021/2023, P&G 2022 and Unilever 2022. The Colgate 2020 source lead redirected
to the wrong quarter during curation, so its unsupported cost narrative was
removed before the v1 benchmark froze. The retained Q1 official release supports
a contrasting demand-growth case. The same company and the 2021–22 inflation
window recur; ten observations are not ten proven independent shocks.

For the Colgate Asia Pacific Q4 2022 question, Colgate Q3 2008 is a useful
partial own-company comparison: both discuss materials/packaging pressure and
pricing/savings offsets. The 2008 metric is adjusted global gross margin;
the 2022 metric is regional operating margin. Their levels cannot be compared
as the same measure. Clorox Q4 2021 is a cross-company partial comparison with
shipment normalization and fixed-cost absorption as additional contributors.
Neither comparison isolates response effectiveness.

A later structured view separates pressure, reported margin/profit change,
other drivers and response. It keeps responses out of ranking text. Five
user-entered grades of 2 (A–E) were recorded without reasons. On those pairs,
BM25 positions were 4, 2, 1, 2, 9 and MiniLM positions were 1, 2, 1, 2, 5.
Those grades cover only five pairs; full-list human P@5/nDCG@5 cannot be
calculated. Pair E (P&G commodity costs against an embargo query) has no
recorded explanation for relevance. Preserve the grade as entered and do not
infer a reason or an embargo mechanism.

Verification: eight tests, Ruff checks, frozen-input and candidate audit, and
offline rerun passed. Rank order and metrics reproduced, with scores within
1e-5. See run manifests and frozen protocols in `evaluation/pilot/`. Source
URLs, locators, dates and metric bases live in the case records. Full-source
archival/public redistribution permission, precise episode boundaries, later
realized outcomes, human review of all ten cases, and independent full-query
labels remain unverified. The original detailed Colgate case had limited
usefulness accepted by Dheeraj after its volume correction; this does not
validate the whole corpus. No causal or strategy-success conclusion follows.

Recommendation: continue with a narrow evidence-based comparison experience.
Expand supported case detail and handle insufficient evidence before training
or adding complex structural ranking. No model improvement claim is accepted
from this tiny pilot.
