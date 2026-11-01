# Current status

Updated: 1 November 2026.

**M001: Closed as a development pilot.** Ten assistant-checked observations,
five queries and frozen BM25/MiniLM experiments remain unchanged. Five user grades
without rationales are not a complete human benchmark. See
[the pilot report](evaluation/pilot/pilot-report.md).

**M002–M005: Complete.** Local reader-friendly search/comparison and 13 observations
from eight companies run with `make app` at http://127.0.0.1:8000. Related inputs,
source inspection and reliable browser checks remain available. Historical
[M004 notes](data/collection/README.md) and [M005 report](evaluation/search-m005/report.md)
are unchanged.

**M006: Complete — context, direction and negation.** General clause rules separate
input costs from sales, preserve positive sides of mixed negation, compare cost
directions and set aside recognized outside industries. Opposite shared-input
directions veto partial matches. Ambiguous changes yield insufficient evidence;
bare input topics keep direction unspecified. The app shows what it read/ignored
and explains direction in results and comparison. Only pressure passages affect
ranking; dates and self/continuation exclusions are unchanged.

**Evaluation:** 65 query texts/expectations and M005 ranks frozen before method
edits (`234fab0`, expectation clarification `b1f85a7`). On identical eligible cases,
useful-case retrieval in the first five: 27/33 → 33/33; unexpected results on
expected-empty queries: 16/32 → 0/32; forbidden-case queries: 5 → 0. No useful-case
or target-rank regressions in this development set. Packaging-only Colgate 2022
remains third due to length normalization and an ID-ordered tie; the broader
packaging/logistics query remains first. See [actual comparisons](evaluation/search-m006/report.md).

**Verification:** 56 Python tests, 9 JavaScript tests, Ruff, syntax, pilot/collection
validation and M005/M006 evaluations passed. Desktop/375px phone browser flow passed
24 grouped checks, including 40 delayed-response failure/retry cycles; screenshots
inspected. All existing cases, source records, frozen M001 files and M004/M005
observations remain byte-identical. No source acquisition or model run was needed.

**Limits / next:** These are assistant-authored development checks, not independent
validation. [Additional diagnostics](evaluation/search-m006/diagnostics.json) record
remaining conservative misses in unpunctuated negation, comma-linked directions
and supplier-industry context. Improve those limits and test unlisted sectors/word
senses with independent judgements. Episode bounds, action effects and later
outcomes remain uncertain; Hershey's margin-source discrepancy is unresolved.
