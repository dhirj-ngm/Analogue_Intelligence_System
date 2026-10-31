# Project status

Updated: 31 October 2026. Two threads: **Discussion** and **Builder** (D017).

## M001 — development implementation delivered

Builder completed the authorized end-to-end pilot: evidence inventory, ten compact observations, five queries, 33 pre-ranking pair judgements, frozen inputs, BM25/MiniLM comparison, tests, self-review and final report.

Start with [the pilot report](evaluation/pilot/pilot-report.md). Run instructions are in [README.md](README.md).

- Cases: five issuers, ten assistant-checked observations; original detailed Colgate data and applied volume correction preserved.
- Mean P@5: BM25 0.400, dense 0.360. Mean nDCG@5: BM25 0.6253, dense 0.6561. Descriptive results only.
- Checks: seven tests, Ruff lint/format, validation and saved-result audit pass. Offline rerun reproduced ranks/metrics within 1e-5 score tolerance.
- Recommendation: narrow the next scope to readable, evidence-backed pressure/response comparisons. Improve evidence depth before structural retrieval or training.

## Limits and acceptance

Original human-review/independent-review criteria are not fulfilled. Ten bounded observations are not ten proven independent episodes. Labels and expanded data review are assistant-only; no new human usability study. Full-source archival/public reuse rights, precise episode boundaries and later outcomes remain unresolved. These shortfalls are explicit in the report's AC01–AC08 matrix.

D016 accepted only the original Colgate case's limited usefulness subject to its now-applied volume clarification. User acceptance of the complete module has not been recorded. Development delivery does not imply scientific validation.

## Working arrangement

Use Discussion for questions and direction; Builder for complete modules. Start with PROJECT_TRACK.md and this file. Older role handoffs are history and do not create permission gates. No separate Manager, Records, Reviewer or Domain thread is needed. Existing user changes were preserved. Dheeraj authorized committing the delivered work; Git history records the commit. No push or deployment requested.

M002–M008 remain proposals. No additional MCP or paid API is required. Next module choice can be discussed from the delivered pilot results, without reopening M001's old task-start gates.

## Active follow-up — structured cases and reader review

Builder created `data/pilot/cases-structured-v2.jsonl` with separate pressure, measure, other drivers, response, unknowns and evidence locators for all ten cases. Source/date/metric/review fields passed a local completeness check. The five-pair `evaluation/pilot/relevance-review-v2.md` is ready for Dheeraj's grades and reasons; no human judgements or new model results are claimed. Frozen v1 inputs/results remain unchanged. After feedback, record the actual judgements, define/freeze a v2 comparison and rerun methods on the same eligible candidates.
