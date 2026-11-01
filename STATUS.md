# Current status

Updated: 1 November 2026.

**M001: Closed as a development pilot.** Ten assistant-checked observations,
five queries and frozen BM25/MiniLM experiments remain unchanged. Five user grades
without rationales are not a complete human benchmark. See
[the pilot report](evaluation/pilot/pilot-report.md).

**M002–M004: Complete.** Local reader-friendly search/comparison, source inspection
and 13 observations from eight companies run with `make app` at
http://127.0.0.1:8000. Company claims, measurement scope and unknowns stay visible;
source documents remain external. See [collection notes](data/collection/README.md).

**M005: Complete — related-input search and reliable browser checks.** The retry
fault was a moving coordinate target plus acceptance of an old idle flag in the
check. Stable hit-tested clicks and fresh-submission waits fix it; the app's request
lifecycle needed no change. New search uses an explicit input vocabulary and BM25
on pressure passages only. Results show query/report term connections and caution
that related inputs need not be identical. Dates, self/continuation exclusions and
response/outcome isolation remain enforced. No cases or source records were added.

**Evaluation:** 33 queries/expectations and the old baseline were frozen in commit
`cb1b37c` before changing search. Both methods use identical eligible cases. All
three M004 misses now retrieve the intended case first. Useful-case retrieval in
the first five: 7/15 old → 14/15 new. Unexpected results on expected-empty queries:
3/18 → 4/18; new false positives concern falling milk costs, booming milk sales and
airline fuel. One packaging query drops 1 → 3, and mixed negation still misses a
useful case. These assistant-authored checks are not independent relevance grades.
See [actual comparisons](evaluation/search-m005/report.md).

**Verification:** 46 Python tests, 8 JavaScript tests, Ruff, syntax, pilot/collection
validation and paired evaluation passed. The full desktop/375px phone browser flow
passed with 20 grouped checks, including 40 delayed-response failure/retry cycles;
screenshots inspected. All 16 frozen M001 hashes and M004 case/result files remain
unchanged. See [browser findings](evaluation/search-m005/browser-check.md).

**Next:** Improve context/direction handling and mixed negation; extend vocabulary
only with explicit relationships and evaluate with independent judgements. True
episode bounds, isolated response effects and later outcomes remain limited;
Hershey's two stated margin declines remain unreconciled. Run/check via README.md.
