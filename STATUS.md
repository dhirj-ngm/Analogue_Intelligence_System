# Current status

Updated: 3 November 2026.

**Local prototype complete — M013 delivered.** Search, evidence inspection and
comparison run locally over the unchanged twenty FMCG situations from fifteen
companies. No production rollout, collection expansion or human-review effort is
underway. Run `make app`, then open http://127.0.0.1:8000. See [README](README.md).

**Final search pass:** HDPE and PET alone find their own named-input cases;
sibling polymers and generic plastic do not establish one another. Full names are
visible in results/comparisons. **Show more matching cases** exposes compatible
results below five, preserving ranking, selection, evidence and partial-coverage
limits. The documented broad query can now reach Marico, still ranked ninth.
Dates, earlier reporting periods, self/continuation exclusions and pressure-only
ranking apply to all results. Cases, sources and frozen M001 files are unchanged.

**Development evidence:** `871d4b4` freezes 44 searches before code changes;
M012/M013 use identical eligible twenty-case pools. First-five target queries:
8/21 → 21/21; accessible targets after expansion: 8/24 → 24/24. Expected-empty:
16/18 → 18/18; forbidden/unexpected-result queries: 4 → 0. Among 275 historical
entries, 19 first-five lists change; no previously labelled target moves lower.
Other cases do move down or leave five; all are recorded. These are selected AI
development checks, not independent validation or accuracy estimates. See
[M013 results and limits](evaluation/search-m013/report.md).

**Verification:** 116 Python / 19 JavaScript tests; Ruff check/format and syntax;
pilot/current collection validation; original M005–M012 evaluations and M008 AI
audit/optional packet checks; M013 paired comparison passed. The real app passed
60 desktop/375px Chrome grouped checks and 40 delayed failure/retry cycles.
Expansion, source details, date controls, distinct-polymer/partial comparisons,
empty states and recovery were exercised; screenshots inspected at both sizes.
The final inspection's lowercase polymer-label issue was fixed. No concrete
prototype blocker remains; this is not multi-browser/physical-device testing.

**Known limits:** First-five broad-query recall still misses useful cases; expanding
results is not a relevance guarantee. Unlisted materials, complex roles and indirect
references can still miss or mislead. Bare oil needs clarification; related costs
do not establish diesel. Country names do not filter. Coverage remains small and
U.S. weighted; episode bounds, action effects, Tiger's cost reconciliation and
Hershey's source discrepancy remain unresolved. These limits do not trigger more
modules under the current prototype scope.

**History / human review:** M001 remains a closed, frozen model pilot; five earlier
user grades are not a complete human benchmark. M002–M013 implementation is complete.
M008 human validation stays deferred, with zero human judgements. The withdrawn
packet remains optional; no R01 contact, follow-up or resend. Historical methods,
cohorts, hashes and observations remain reproducible without rewriting old evidence.
