# Current status

Updated: 3 November 2026.

**M001: Closed development pilot.** Ten observations and BM25/MiniLM experiments
remain frozen. Five earlier user grades are not a complete human benchmark.
See [pilot report](evaluation/pilot/pilot-report.md).

**M002–M011: Complete.** Local case search/comparison, sentence handling and
collection development. The app has twenty situations from fifteen companies,
including M011's India, Japan/overseas and South Africa-led additions. Earlier
evaluations retain their original cohorts and outputs. See
[M011 report](evaluation/collection-m011/report.md). Run `make app` at
http://127.0.0.1:8000.

**M008 human validation remains deferred: zero human judgements.** The withdrawn
packet is optional; no R01 contact, follow-up or resend. The
[AI audit](evaluation/audit-m008/report.md) is not independent validation.

**M012: Complete.** Search separates fuel, petrochemical and edible/natural oils;
recognizes copra/dried coconut kernel and paper/cardboard; and asks which material
bare “oil” means. Results/comparisons distinguish named inputs from broader related
costs. Nestlé's oil-related distribution disclosure does not establish diesel.
Sources were rechecked; all cases, attribution, dates and frozen M001 files remain
unchanged. Pressure-only ranking and publication/self/continuation rules are preserved.

**Development comparison:** `0241f27` freezes 64 queries before code changes.
Same eligible twenty-case pools: expected useful or explicitly related targets
at five in 24/38 → 38/38 queries; forbidden/unexpected results in 23 → 0 queries;
expected-empty in 19/26 → 26/26. New-set target retrieval has no loss, but two
target ranks decline. Of 211 historical entries, 45 lists change and three targets
rank lower, two leaving the five with oil clarification. Of M011's ten prior rank
losses: two restored with related-only fuel evidence, seven remain lower, one now
clarifies. These are AI development checks, not independent validation or accuracy
estimates. See [results, regressions and limits](evaluation/search-m012/report.md).

**Checks:** 109 Python / 18 JavaScript tests; Ruff check/format; pilot/current
collection validation; M005/M006/M007/M009/M010/M011 historical comparisons;
M012 paired evaluation; original M008 audit/optional packet checks passed.
Desktop/375px Chrome: 54 grouped checks, 40 delayed failure/retry cycles; named,
related and partial comparisons, clarification and source screenshots inspected.
Historical code/UI hashes verify against Git; no old observations/manifests rewritten.

**Limits / next:** No exact diesel disclosure; vague oil loses useful prior targets.
A broad multi-pressure query omits Marico from five; separate post-freeze probes
document this. HDPE alone and PET without resin/plastic wording still miss.
Next work should freeze checks for broad-query recall and specific polymer names.
Country names do not filter ranks; indirect references and collection geography
remain limited. Episode bounds, action effects, Tiger's cost-base reconciliation
and Hershey's source discrepancy remain unresolved. No response-effectiveness or
independent human-validation claim is made.
