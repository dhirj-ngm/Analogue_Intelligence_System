# M007 verification — 1 November 2026

Assistant development checks and self-inspection only. No human case review,
independent relevance validation or evidence of response effectiveness is claimed.

| Check | Actual result |
| --- | --- |
| `make test` | 63 Python tests and 10 JavaScript tests passed. Includes real HTTP requests, new-case dates/self/continuations, metric attribution, original-file hashes and pressure-only ranking invariance. |
| `make lint` | Ruff check and format passed for 19 Python files. |
| `node --check` on app.js, reader.mjs and check_app_browser.mjs | All three passed. |
| `make validate` | Original pilot valid: 10 cases, 5 queries, 33 eligible judgements. |
| `make collection-check` | Seven additional canonical situations valid; original M004 literal observations reproduce on their thirteen-case cohort. Current app catalog: 17 situations, twelve companies. |
| `make search-check` | Historical M006 baseline/eligibility reproduced; M007 frozen checks reproduced. Same extended method on both collection cohorts; original eligible IDs preserved. |
| `make search-check-m005` | Historical M005 baseline/eligibility reproduced on its original thirteen cases. |
| `make collection-check-m007` | Reproduced results.json, including hashes, twenty frozen queries, two comparison record sets and the 65-query legacy rank probe. |
| `make browser-test` | Full desktop/375px phone flow passed, including six delayed-response failure/retry cycles. |
| `node scripts/check_app_browser.mjs --retry-rounds=20` | Final full flow passed 30 grouped checks and 40 delayed-response failure/retry cycles, using trusted control clicks. No browser runtime exceptions. |
| New original source links | All four substantive SEC-hosted filings opened and read through the web reader; key figures, definitions and publication corroboration inspected. Raw HTTP statuses unavailable, recorded as null. |
| Frozen-file checks / `git diff --check` | Historical data, M001 pilot and earlier evaluation artifacts match frozen hashes; diff whitespace check passed. |

Browser coverage includes all four additions, old related-term searches, visible
source locators, definitions, Hershey's retained conflict, comparisons, source-case
switching, date boundaries/validation, unknowns, direction/negation, insufficient
evidence, preserved drafts and connection recovery. Declining milk now returns
Dean; the previous falling-milk empty check was replaced by uncovered falling
coffee. Mixed falling-milk/rising-energy searches show two partial matches, rather
than asserting the old single result was permanent.

Screenshots inspected in `/tmp` include the desktop three-company comparison and
its measures, the phone comparison/measures, and the phone milk benchmark definition.
The layout retains readable stacked cells without page overflow. The benchmark
inspection exposed generic margin help below a price figure; unit-specific help
replaced it and is covered by JavaScript and browser checks. These are emulated
viewports in local headless Chrome, not physical-device or broad browser testing.
Screenshots are disposable local artifacts, not source documents or committed data.

Initial local-server attempts were blocked by the filesystem sandbox's socket
restriction; successful full tests/browser runs used the permitted execution mode.
Two new browser assertions initially failed: requiring the literal phrase “printed
p.” even where a precise “p.” locator existed, and expecting a raw signed amount
to be visible inside a closed definition panel. They were corrected to check
the actual visible loss wording and then open its definition. Full flows were
rerun after fixes. No unresolved test failures remain.

Offline checks do not fetch sources. Original source passages and SEC reuse
guidance were inspected manually; older case documents were not reacquired.
No ML model run was needed: BM25 and existing context rules remain the method,
with the frozen material-name extension. No independent review was performed.
The remaining beef-wording miss, two legacy target-rank drops, corpus bias and
coverage limits are recorded in [report.md](report.md), not graded away.
