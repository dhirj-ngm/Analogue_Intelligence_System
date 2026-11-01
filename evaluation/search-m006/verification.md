# M006 verification and limits

The 65 queries and M005 rankings were frozen before method edits in `234fab0`.
`b1f85a7` corrected one expectation before implementation: an explicit opposite
dairy-cost direction must exclude General Mills even if its energy input overlaps.
No query labels were adjusted after the method changed. `freeze.json` fingerprints
all existing data files, M001 artifacts and M004/M005 evaluations; they remain
byte-identical. `related_v1` is unchanged and reproduces captured M005 scores.
The paired report records the same ordered eligible pool for both methods.

Final checks passed: 56 Python tests, 9 JavaScript tests, Ruff, JavaScript syntax,
pilot validation, collection validation/historical M004 output, historical M005
evaluation and the paired M006 evaluation. The full browser flow passed on a
1280px desktop and 375px phone with 24 grouped checks, including 20 connection
failure/retry cycles per screen size with delayed responses. Screenshots were
inspected; no sideways overflow was observed. The final default browser run also
checks the simplified empty-state copy and clears stale query interpretations on
connection failure. A legacy test initially expected a semiconductor query to
have the old word-gap reason; that query now has an industry-context reason.
The word-gap test uses coffee beans, while context reasons have dedicated tests.

All 33 useful-case queries retrieve their expected cases in the first five; all
32 expected-empty queries abstain. Five M005 queries returned explicitly forbidden
cases; M006 returns none. There are no target-rank regressions in this selected
set. The packaging-only Colgate 2022 rank of 3 is retained and explained, rather
than promoted based on the expected label. Its score ties Colgate 2015, behind a
shorter packaging-only passage. The broad packaging/logistics query remains first.

These are assistant-authored development labels selected with knowledge of prior
failures, not independent or held-out validation. Unit grammar probes are not
added to the 65-query metrics. Post-implementation observations in
`diagnostics.json` still show useful-case misses: “rising not falling” without
punctuation, comma-linked opposite changes, and a food maker mentioning its
logistics supplier. The rules abstain in these examples. No frozen-query failures
does not mean no remaining search failures. Complex syntax, unlisted industries,
other meanings of input words and price/sales attachment can still mislead.

Cases and original source evidence have not been rewritten. Scope classification
uses query wording and a visible, limited industry vocabulary; case identity,
responses, figures and later outcomes cannot supply ranking concepts or direction.
Tests demonstrate that a synthetic declining-cost pressure can match a declining
query, and that unknown source direction is not filled in. Reported action effects
and later outcomes remain unknown.

Reproduce with `make test`, `make lint`, `make validate`, `make collection-check`,
`make search-check`, `make search-check-m005` and `make browser-test`. For the stress
flow: `node scripts/check_app_browser.mjs --retry-rounds=20`. Screenshots are under
`/tmp/ais-context-{empty,mixed}-{desktop,mobile}.png`, alongside the existing case,
source and comparison screenshots. No paid services, model downloads or external
source acquisition were used.
