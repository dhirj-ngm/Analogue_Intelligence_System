# M010 ordinary sentence wording

**AI development checks, not independent human validation.** Human validation
remains deferred with zero human judgements. No R01 contact occurred. All seventeen
case records, source evidence, frozen M001 files and previous evaluation artifacts
are unchanged.

Freeze commit `e858102` precedes method changes; base is `d63b3c3` (M009).
[Queries and expectations](queries.json), [captured M009 outputs](baseline.json)
and [input hashes](freeze.json) cover 56 new descriptions/counterexamples and 130
historical entries: M006 (65), M007 (20), M008 (8), M009 (37). Some historical
descriptions repeat. This is a case-informed diagnostic sample, not held-out
relevance evidence or a general accuracy estimate.

## Paired results

Both methods use identical eligible IDs and exclusion counts per query, on the
same seventeen-case collection. The evaluator verifies that M009 still reproduces
its captured ranks, scores, query reading, coverage and clarification.

| Frozen development expectation | M009 | M010 |
| --- | ---: | ---: |
| All expected useful targets in first five, by query (33) | 9 | 33 |
| Expected-empty queries left empty (23) | 17 | 23 |
| Queries returning a forbidden case or unexpected results | 9 | 0 |
| Required clarification kind shown (9) | 1 | 9 |
| Queries meeting every expectation (56) | 19 | 56 |

Twenty-four queries gain their expected useful cases; none loses an expected
target or worsens a target's rank. Thirty-two ranked lists change. Six change
from nonempty to empty: conflicting same-input directions, unresolved time periods,
customer purchase prices (two descriptions), reader selling prices, and an “up and
down” input list. The other misleading matches corrected are wrong-direction
dairy cases for “we pay more/less” and a supplier's own milk costs overriding the
reader's purchase. All 130 historical ranked lists **and scores** are unchanged.
Full paired observations and per-query failures are in [results.json](results.json).

Concrete examples:

- “Milk costs are rising not falling” now finds General Mills; a denial alone
  (“milk costs are not falling”) still establishes no rise.
- “Milk costs fell, energy bills rose” finds Dean Foods and Kimberly-Clark as
  separate **partial** comparisons. General Mills' rising milk costs are excluded.
  Neither displayed case is presented as evidence for the combined situation.
- A bottled-water business using a logistics firm whose customers include airlines
  can find Nestlé Waters; an actual airline remains outside the collection.
- “Our supplier's milk costs fell, but we pay more for milk” now searches rising
  reader costs. Customer payments, reader selling prices and supplier own costs
  do not become purchased-input pressure.
- “Milk costs fell, prices rose” and “we are an airline supplier” ask for an edit
  instead of assigning the unnamed price or guessing the reader's industry.

## Method and safeguards

`context_m010` applies small local query rules before the unchanged pressure-only
BM25 method. Named input lists stay together; distinct comma/coordination clauses
keep their own subjects and directions. Explicit opposite denied alternatives are
removed only when a positive direction is stated. Neither absence, uncertainty
nor a denial alone supplies a direction. Ordinary directional forms (raised,
lowered, risen, climbed, dipped) are normalized; no material synonym was added.

Explicit purchasing and third-party relationships are separated from business
identity, output prices and another actor's own bills. A discarded cost clause
cannot erase an explicit outside reader identity. A single immediate purchase
reference can resolve a following price statement; an intervening subject clears
that reference. Conflicting directions, ambiguous business roles and unresolved
ownership through “its/their” request clarification. The edit control preserves
words/dates, focuses the search box and submits nothing; live-animal clarification
continues to require an explicit reader edit.

Case pressure profiles, vocabulary families, scoring formula and tie-breaking are
unchanged. Responses, profit/metric fields, business identity and later outcomes
cannot affect scores; coverage is computed after scoring. Publication/evidence
cutoffs, strict earlier periods, self/continuation grouping, duplicate exclusion
and future-action withholding are shared across methods. The existing M009 method
and original grammar remain available for historical reproduction. Earlier hashes
are verified against immutable Git code/UI at `d63b3c3` and `1e4e6d3`; no evidence
or data hash is exempted and no prior manifest/observation was rewritten.

## Checks and remaining failures

90 Python and 16 JavaScript tests passed, including HTTP behavior, frozen pairs,
direction binding, partial coverage, ownership/output counterexamples and mutation
checks proving response/outcome/metric/business fields cannot change rankings.
Ruff, JavaScript syntax, pilot/collection validation, M005/M006/M007 historical
evaluations, M009/M010 paired evaluations and the original M008 audit/optional
packet checks passed. Historical M005 and M007 reports retain their documented
old-method misses; passing reproduction is not a claim that those methods solve them.

Desktop/375px Chrome passed 42 grouped checks, including sources/details,
comparison, dates/self exclusion, clarification, historical audit searches and
40 delayed connection-failure/retry cycles. Screenshots of direction and business
clarification and per-case comparison coverage were inspected on both sizes.
An initial browser assertion expected the superseded sales warning; it was updated
to assert the current output/input distinction, then the full flow passed.
The initial sandbox test run could not open its HTTP socket; the complete rerun
with local sockets enabled passed. A delivery-price wording regression found by
an existing M009 test was fixed before final checks.

Post-freeze probes, excluded from the 56-query metrics, retain two conservative
misses: “Milk prices aren't rising; they are falling” and “The costs of milk were
lower, but those of energy were higher.” Both return insufficient evidence with
direction clarification, even though a reader may resolve the reference. Follow-up:
freeze explicit negated-antecedent and indirect-reference tests before extending
binding. Do not simply carry the nearest input across clauses or infer a direction
from a denial. Post-freeze tests also prevent a milk cooperative's product identity
from becoming purchased milk, and prevent a pronoun from crossing an intervening
supplier subject. Feed/veterinary costs remain unsupported inputs.

Unlisted industries, longer role attachments, word senses and unrecognized predicates
can still be misread by this finite grammar. Unknown input names are display-only;
coverage counts only identified pressures. The small collection, episode bounds,
action effects and Hershey's source discrepancy remain limitations. No general
language understanding, independent relevance validation or response effectiveness
is claimed.

Reproduce with `make test lint validate collection-check search-check search-check-m005 audit-check`;
`make search-check-m010` runs this paired evaluation alone. Use
`node scripts/check_app_browser.mjs --audit-m008 --retry-rounds=20` for the full
current UI flow. The audit flag uses recorded M010 expectations for the current
UI; `make audit-check` separately reproduces M008's original method and packet.
