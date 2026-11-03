# Current status

Updated: 3 November 2026.

**M001: Closed development pilot.** Ten observations and BM25/MiniLM experiments
remain frozen. Five earlier user grades are not a complete human benchmark.
See [pilot report](evaluation/pilot/pilot-report.md).

**M002–M010: Complete.** Local reader-friendly case search/comparison, collection
and sentence-handling development. Earlier evaluations retain original cohorts and
outputs. See [M010 report](evaluation/search-m010/report.md).

**M008 human validation remains deferred: zero human judgements.** The withdrawn
packet is optional; no R01 follow-up/resend. The historical
[AI audit](evaluation/audit-m008/report.md) is not independent validation.

**M011: Complete.** The app now has twenty situations from fifteen companies:
Marico's India input costs (2021), Kao's Japan/overseas consumer materials (2022),
and Tiger Brands' South African electricity/grain pressure (2023) add geographic
and input variety. New location labels and currency explanations preserve domestic
versus group scope, market benchmarks, estimates and unknowns. Sources remain
external; existing records and frozen M001 files are unchanged. See
[collection notes](data/collection/m011/README.md). Run `make app` at
http://127.0.0.1:8000.

**Development comparison:** 25 searches/comparison checks frozen in `98b8001`
before records, plus 186 historical entries. Same M010 method and eligible-case
rules on 17/20 cases: expected useful targets at five in 2/16 → 14/16 queries;
all five expected-empty searches stay empty. Fourteen new-set and 51 historical
ranked lists change; ten prior targets rank lower, none leaves the first five.
Copra/paper queries miss, and edible oils misleadingly match diesel. These are
AI development judgements, not independent validation or an accuracy estimate.
See [actual results, regressions and limits](evaluation/collection-m011/report.md).

**Checks:** 98 Python / 17 JavaScript tests; Ruff/syntax; pilot/current collection
validation; M005/M006/M007/M008/M009/M010 historical and M011 paired reproductions
passed. Desktop/375px: 48 grouped checks, 40 delayed failure/retry cycles; source
and app screenshots inspected. Original PDFs, dates, definitions, terms and links
checked; no documents served. Historical code/UI hashes verify against Git;
no prior case, observation or manifest was rewritten.

**Limits / next:** Freeze tests to distinguish fuel from edible/natural oils and
assess copra/paper names before changing search. Country names do not filter ranks.
Indirect references still need clarification. Geographic coverage remains narrow,
with many local markets missing; episode bounds, action effects, Tiger's cost-base
reconciliation and Hershey's earlier discrepancy remain unresolved. No human
validation or response-effectiveness claim is made; no R01 contact occurred.
