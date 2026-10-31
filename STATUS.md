# Current status

Updated: 1 November 2026.

**M001: Closed as a development pilot.** Ten assistant-checked observations,
five queries, frozen BM25/MiniLM experiments and structured fields remain
unchanged. Five user-entered grades have no rationales and are not a complete
human benchmark. See [the pilot report](evaluation/pilot/pilot-report.md).

**M002: Complete — local case search and comparison.** `make app` opens a
Python standard-library app at http://127.0.0.1:8000. Readers describe a situation,
inspect ranked partial pressure matches with source locators, responses,
differences and unknowns, and compare up to three cases. Source-case selection
sets historical dates and excludes self/known continuations. Cutoffs apply to
challenge evidence and displayed responses; BM25 uses challenge text alone.
Insufficient evidence is explicit when no eligible specific pressure match exists.
The app preserves frozen pilot artifacts and does not persist search text.

**Verification:** 26 deterministic tests, including loopback HTTP integration;
Ruff check/format; pilot validation (10 cases, 5 queries, 33 eligible judgements);
JavaScript syntax checks; and seven headless-Chrome flows passed. Browser checks
covered evidence/unknowns, three-case comparison, self/date exclusions, unsupported
queries, date errors and a 375px viewport. Desktop/mobile screenshots were
inspected; missing-excerpt and comparison-focus behavior were corrected.
No model rerun or new source acquisition was needed.

**Limits / next build:** The pressure gate uses literal terms and simple negation
handling; partial matches are not validated analogues. Ten bounded observations
do not establish episode diversity, response effectiveness or retrieval superiority.
Case boundaries, later outcomes and source reuse rights remain limited. Improve
case depth and coverage before further ranking claims. Builder proceeds without
routine user review gates. Use [README.md](README.md) for commands and safeguards.
