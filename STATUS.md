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

**M009: Complete.** Supplier/customer context, per-case pressure coverage and
live-animal clarification remain available. See [M009 report](evaluation/search-m009/report.md).

**M010: Complete.** Ordinary denied alternatives (“rising not falling”), comma-linked
cost directions and explicit buying/third-party roles are handled before ranking.
Ambiguous directions or reader roles ask for clarification; edits keep text/dates
without submitting. Case-pressure scoring, publication dates, earlier periods,
self/continuation exclusions and withheld future actions are preserved.

**Development evaluation:** 56 queries/counterexamples frozen in `e858102` before
method changes. Same seventeen-case eligible pools for M009/M010: expected useful
cases found in 9/33 → 33/33 queries; misleading-result queries 9 → 0; required
clarifications 1/9 → 9/9. All 56 expectations pass. Thirty-two ranked lists change;
no expected-target retrieval/rank regressions. All 130 historical entries retain
ranks and scores. See [paired results and limits](evaluation/search-m010/report.md).

**Checks:** 90 Python / 16 JavaScript tests; Ruff/syntax; pilot/collection validation;
M005/M006/M007/M008 historical and M009/M010 paired checks passed. Desktop/375px:
42 grouped checks and 40 delayed-response retry cycles; screenshots inspected.
Existing cases, frozen M001 files and previous evaluation artifacts are unchanged;
original runtime/UI hashes are checked against Git history.

**Limits / next:** Builder development judgements, not independent validation.
Negated antecedents (“Milk prices aren't rising; they are falling”) and indirect
cost references (“costs of milk … those of energy”) still ask for clarification.
Unlisted sectors, complex roles and input phrases remain limited. Next: improve
reference handling conservatively and broaden realistic development checks.
Coverage, episode bounds, action effects and Hershey's source discrepancy remain
unresolved. Human validation stays deferred; no R01 contact occurred.
