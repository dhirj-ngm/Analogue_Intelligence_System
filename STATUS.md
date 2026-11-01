# Current status

Updated: 1 November 2026.

**M001: Closed as a development pilot.** Ten assistant-checked observations,
five queries and frozen BM25/MiniLM experiments remain unchanged. Five user grades
without rationales are not a complete human benchmark. See
[the pilot report](evaluation/pilot/pilot-report.md).

**M002: Complete.** Local case search, source inspection and comparison run with
`make app` at http://127.0.0.1:8000.

**M003: Complete — reader-friendly experience.** Plain labels and explanations
cover shared pressures, company reports, differences, actions and unknowns.
Scores and detailed date/exclusion checks sit in optional “How this works”.
Examples run a search; starting-case switching restores the reader's own draft;
optional dates explain their meaning and errors focus the field to fix. Empty
states distinguish date restrictions from a collection gap. Phone comparisons
stack vertically. Visible cautions preserve uncertainty and attribution.

**Verification:** 29 Python tests and 6 JavaScript tests, Ruff, syntax and pilot
validation passed. Thirteen real-browser checks covered the complete flow on
desktop and a 375px phone viewport, plus connection-failure recovery. Screenshots
were inspected. Four regression queries retained identical rankings/scores; all
case, evaluation and configuration hashes were unchanged. No model run or new
source acquisition was needed.

**Limits / next:** Literal pressure matching can miss synonyms or complex
situations; these cases are starting points, not validated analogues or evidence
that a response worked. Episode boundaries, later outcomes and source reuse
rights remain limited. Improve case depth/coverage before further ranking claims.
Use [README.md](README.md) for run instructions and checks.
