# Current status

Updated: 1 November 2026.

**M001: Closed as a development pilot.** Ten assistant-checked observations,
five queries and frozen BM25/MiniLM experiments remain unchanged. Five user grades
without rationales are not a complete human benchmark. See
[the pilot report](evaluation/pilot/pilot-report.md).

**M002 / M003: Complete.** Local, reader-friendly search, source inspection and
comparison run with `make app` at http://127.0.0.1:8000. Technical details remain
optional; date, self/continuation and evidence safeguards remain enforced.

**M004: Complete — deeper case collection.** Three distinct situations add
General Mills FY2007 grain/dairy/energy costs, Nestlé Waters H1 2011 oil-related
packaging/distribution costs and Hershey Q1 2025 cocoa costs. The app now has 13
observations from eight companies. New records include source passages/locators,
publication/reporting dates, scope, units/basis, company attribution, actions,
unknowns and access/retention notes. Supporting figures and Hershey's unresolved
source disagreement are available in details and comparison. Basis points are
explained beside numbers. Original documents remain external links.

**Verification:** 38 Python tests, 7 JavaScript tests, Ruff, JavaScript syntax,
pilot validation and collection checks passed. Nineteen real-browser checks
covered desktop and a 375px phone, new-case comparisons, source links, dates,
self exclusion, empty results and connection recovery; screenshots inspected.
Four substantive primary documents were readable through the web reader; a
General Mills index request returned 403, with publication corroborated through
the official EDGAR directory/report. All 16 frozen pilot artifact hashes match
the starting checkpoint. No model experiment was rerun.

**Limits / next:** Eight recorded development queries include three useful-case
misses; these are not a human relevance benchmark. See
[collection notes](data/collection/README.md) and
[actual query results](evaluation/collection/results.json). Improve coverage and
literal-matching failures next. Cases remain assistant-checked; true episode
bounds, isolated action effects and later outcomes are unknown. Hershey's two
stated margin declines remain unreconciled. Use [README.md](README.md) to run/check.
