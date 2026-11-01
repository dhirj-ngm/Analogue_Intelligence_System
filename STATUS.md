# Current status

Updated: 2 November 2026.

**M001: Closed development pilot.** Ten observations and original BM25/MiniLM
experiments remain frozen. The five user grades are not a complete human benchmark.
See [pilot report](evaluation/pilot/pilot-report.md).

**M002–M007: Complete.** Reader-friendly local case search/comparison, with seventeen
situations from twelve companies: `make app`, http://127.0.0.1:8000. Source evidence,
metric definitions, unknowns and original observations are unchanged. See
[M007 collection notes](data/collection/m007/README.md) and the earlier reports.

**M008: AI audit complete; human validation deferred.** Zero human judgements.
The withdrawn 154-pair packet remains optional; no R01 follow-up or resend.
The [AI audit](evaluation/audit-m008/report.md) is historical development evidence,
not independent validation. Its method and original observations still reproduce.

**M009: Complete.** Explicit supplier/customer roles no longer define the reader's
industry; genuine outside reader businesses remain excluded. Results and the first
comparison row identify supported/missing pressures and unresolved inputs. Partial
cases cannot imply a combined situation. Live-animal purchases prompt an explicit
edit/clarification, with no cattle synonym or change to the reader's text/dates.
Beef output prices/sales remain separate from cattle input costs.

**Development evaluation:** 37 queries/expectations frozen in `78abe11` before code
edits. Same seventeen-case eligible pools for M008/M009: expected-case retrieval
10/21 → 21/21; expected-empty queries 15/16 → 16/16; clarification 0/4 → 4/4.
All 37 behaviour checks pass, without expected-case or target-rank regressions.
Of 93 historical entries, only the intended M008 supplier failure changes ranks.
See [paired results and limits](evaluation/search-m009/report.md).

**Checks:** 82 Python / 16 JavaScript tests; Ruff/syntax; pilot/collection validation;
M005/M006/M007/M008 historical and M009 paired checks passed. Desktop/375px flow:
38 grouped checks and 40 delayed-response retry cycles; screenshots inspected.
All case records and frozen M001 inputs are byte-identical. Historical code/UI
hashes are verified against Git; no old observation or manifest was rewritten.

**Limits / next:** These are Builder development checks, not independent human
validation. Unpunctuated alternative negation, comma-only mixed directions,
unlisted sectors and complex role/input phrases can still be missed. Counts cover
identified pressures. Episode bounds, action effects and Hershey's source discrepancy
remain unresolved; collection coverage is still narrow. Prioritize grammar diagnostics
and broader realistic development queries while human validation remains deferred.
