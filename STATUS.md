# Current status

Updated: 1 November 2026.

**M001: Closed as a development pilot.** Its ten observations, five queries and
frozen BM25/MiniLM experiments remain unchanged. Five user grades without
rationales are not a complete human benchmark. See [the pilot report](evaluation/pilot/pilot-report.md).

**M002–M006: Complete.** Reader-friendly local search/comparison, related inputs,
context/direction/negation rules and reproducible browser checks remain available.
Historical [M005](evaluation/search-m005/report.md) and
[M006](evaluation/search-m006/report.md) evaluations retain their original
thirteen-case collection and frozen observations.

**M007: Complete — focused collection expansion.** The app now has 17 situations
from twelve companies (`make app`, http://127.0.0.1:8000). Four distinct additions:
Smucker retail coffee FY2011, Dean's declining dairy costs in 2015, Tyson Beef
FY2024 Q1 cattle costs, and Coca-Cola Consolidated's 2022 packaging inputs.
[Collection notes](data/collection/m007/README.md) preserve original links,
publication/reporting dates, field-level locations, metric definitions, company
attribution, continuation boundaries and unknowns. Documents remain external;
existing case records and frozen M001 files are byte-identical.

**Development comparison:** Twenty checks and two comparison plans frozen in
`72d1611` before data/method edits. One fixed extended vocabulary on old/expanded
collections retrieves expected useful cases in 4/10 → 9/10 searches; all ten
expected-empty queries stay empty. No target-rank drops in this set. In an
additional probe of the older 65 queries, no previously expected cases leave the first five,
but General Mills for “milk costs” and Kimberly-Clark for falling milk/rising
energy each move first → second. See [ranks and limits](evaluation/collection-m007/report.md).

**Verification:** 63 Python and 10 JavaScript tests; Ruff and syntax; pilot and
collection validation; M005/M006 historical and M007 paired evaluations passed.
Desktop/375px phone flow passed 30 grouped checks with 40 delayed-response retry
cycles. Four new source documents opened; comparisons/screenshots inspected.
Benchmark/amount help now reflects units. See [actual checks](evaluation/collection-m007/verification.md).

**M008: AI development audit complete; human validation deferred.** The user
withdrew the 154-pair request: zero human judgements, no R01 follow-up or resend.
The frozen packet remains optional. [AI audit](evaluation/audit-m008/report.md):
eight searches selected in `9fc5895`, all ten displayed pairs plus four named
extra assessments; four AI useful / six AI partly useful displayed labels.
Nine source checks, including an issuer HTML fallback for Kimberly-Clark.
No independent human validation or general quality estimate is claimed.
Cases and ranking rules are unchanged. Checks: 74 Python / 13 JavaScript tests,
lint/syntax, validation, historical evaluations and desktop/375px audit flow.

**Limits / next:** Assistant curation and development checks, not independent
validation. Beef wording still misses cattle; PET alone is unrecognized. New
sources remain U.S. focused. Partial matches need not cover every named input;
complex grammar/industry limits, uncertain episode boundaries and unestablished
action effects remain. Hershey's earlier source discrepancy remains unresolved.
Next fix reader-versus-supplier industry context, expose partial pressure coverage
and clarify live-animal input wording. See the AI audit for proposed checks.
