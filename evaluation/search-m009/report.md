# M009 reader context, partial coverage and live-animal clarification

Builder-authored development checks, not independent human validation or a held-out
relevance benchmark. Human validation remains deferred with zero human judgements;
no further R01 contact occurred. Cases and frozen M001 files are unchanged.

**Freeze:** `78abe11`, before implementation, captures 37 new query texts and
expected behaviours, plus M008 outputs for those queries and 93 historical query
entries. Base: `1e4e6d3`. The historical entries come from M006 (65), M007 (20) and
M008 (8), with some repeated descriptions. Both methods run on the **same current
17-case collection and identical eligible IDs/exclusion counts for every query**.
Historical original-cohort evaluations also remain reproducible separately.

| Frozen development check | M008 | M009 |
| --- | ---: | ---: |
| Expected useful-case targets in first five (21 queries) | 10 | 21 |
| Expected-empty queries left empty (16 queries) | 15 | 16 |
| Live-input clarification offered where expected (4 queries) | 0 | 4 |
| Queries meeting all expectations, including coverage fields (37) | 14 | 37 |

All frozen expectations pass. Eleven queries gain their expected case; none loses
an expected useful case or worsens its target rank. A genuine logistics-business
query changes from results to empty: an intended outside-scope correction, not
a useful-case retrieval regression. Of 93 historical entries, only M008 A08 changes
its ranked list, from empty to results led by Nestlé Waters. These targeted gains
do not establish general relevance accuracy or response effectiveness.
See [actual paired results](results.json) and [frozen inputs](queries.json).

## What changed

- **Reader versus supplier:** explicit supplier/customer descriptions and purchasing
  relations no longer define the reader's industry. Charges to the reader are kept;
  a supplier's own operating costs are set aside. An explicit outside reader
  business still blocks results, even if it mentions a food supplier. Rules are
  generic sentence/role patterns, with no query IDs or company exceptions.
- **Per-case coverage:** results and the first comparison row show supported and
  not-established pressures. Unknown cost names and unresolved inputs prevent full
  coverage claims. Missing evidence is not a claim that a cost did not change.
  Two partial cases never stand in for one documented joint situation. Counts refer
  to identified named pressures, not every possible meaning of the description.
- **Live animals:** ambiguous purchase/input wording asks whether the reader means
  cattle or another animal. The edit button focuses/selects the original phrase;
  it changes neither text nor dates and submits nothing. Explicit cattle-input text
  can find Tyson; beef selling prices/sales and cattle sales do not become input
  pressure. No live-animal/beef synonym was added.

The BM25 formula, material families and case-pressure representation are unchanged.
Only query-role handling changes first-stage terms. Coverage is computed after
scoring; responses, profit figures, business identity and later outcomes remain
excluded from ranking. Dates, strict earlier-period limits, self/continuations,
future-response withholding, attribution and source links remain intact.

## Verification and remaining failures

82 Python and 16 JavaScript tests passed; Ruff/syntax, pilot/collection validation,
M005/M006/M007 historical evaluations, the historical M008 audit/optional packet and
M009 paired evaluation passed. Desktop/375px Chrome passed 38 grouped checks,
including all audit searches, date/source controls, per-case comparison coverage,
unknown inputs, editable clarification, output-price counterexamples and 40 delayed
failure/retry cycles. Screenshots were inspected. One new browser assertion was
corrected: selecting a starting case changes the query, so self-exclusion does not
require every other eligible case to disappear.

[Rechecked M006 diagnostics](diagnostics.json) retain conservative misses for
unpunctuated alternative negation and comma-only opposing directions. The old
supplier diagnostic now returns cases. Complex role attachments, unlisted industries
and multiword/unrecognized inputs remain limited by the small grammar; coverage
counts only pressures it can identify. No automatic animal-species inference or
general natural-language understanding is claimed.

Older methods still use the unchanged original grammar and reproduce captured
outputs. Historical verification checks original runtime/UI hashes against immutable
Git blobs at `1e4e6d3`; the optional packet renders with its original reader helper.
**No case/evidence hash is exempted and no old manifest or observation was rewritten.**
Historical development checks need that Git history; running the app adds no Git,
package, model or paid-service dependency.

Run `make test lint validate collection-check search-check search-check-m005 audit-check`.
Use `make search-check-m009` for the paired evaluation alone, and
`node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20` for the full
current UI flow. The old audit flag uses recorded M009 expectations for those
historical queries; `make audit-check` separately reproduces the original M008 method.
