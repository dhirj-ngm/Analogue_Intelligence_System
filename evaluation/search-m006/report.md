# M006 paired search checks

Assistant-authored development expectations frozen before changing the method; includes M005 failures and deliberately difficult context/negation examples. Useful cases are not exhaustive relevance grades; no independent validation. No independent validation or causal claims.

Across 33 useful-case queries, expected cases appeared in the first five in 27 old / 33 new results.
Across 32 expected-empty queries, unexpected candidates appeared in 16 old / 0 new results.
Queries returning explicitly forbidden cases: 5 old / 0 new.

| Query ID | Expected useful case(s) | Old rank(s) | New rank(s) | Unexpected candidates old → new |
| --- | --- | --- | --- | --- |
| milk-flour-electricity | GIS-2007 | 1 | 1 | — |
| chocolate | HSY-2025-Q1 | 1 | 1 | — |
| bottled-water | NES-WATERS-2011-H1 | 1 | 1 | — |
| literal-food | GIS-2007 | 1 | 1 | — |
| literal-cocoa | HSY-2025-Q1 | 1 | 1 | — |
| literal-oil | NES-WATERS-2011-H1 | 1 | 1 | — |
| literal-packaging | CL-2022 | 1 | 1 | — |
| literal-resin | KC-2011 | 1 | 1 | — |
| wheat-power | GIS-2007 | 1 | 1 | — |
| milk-powder | GIS-2007 | 1 | 1 | — |
| cacao | HSY-2025-Q1 | 1 | 1 | — |
| freight | NES-WATERS-2011-H1 | 1 | 1 | — |
| unsupported-chips | expect empty | — | — | False → False |
| unsupported-coffee | expect empty | — | — | False → False |
| unsupported-steel | expect empty | — | — | False → False |
| generic | expect empty | — | — | False → False |
| action-only | expect empty | — | — | False → False |
| negated-chocolate | expect empty | — | — | False → False |
| negated-milk | expect empty | — | — | False → False |
| mixed-clauses | CL-2022 | 3 | 3 | — |
| mixed-negation | CL-2022 | miss | 3 | — |
| falling-milk | expect empty | — | — | True → False |
| milk-sales | expect empty | — | — | True → False |
| airline | expect empty | — | — | True → False |
| oil-art | expect empty | — | — | True → False |
| early-food | expect empty | — | — | False → False |
| early-water | expect empty | — | — | False → False |
| early-chocolate | expect empty | — | — | False → False |
| inclusive-chocolate | HSY-2025-Q1 | 1 | 1 | — |
| self-cocoa | expect empty | — | — | False → False |
| self-food | expect empty | — | — | False → False |
| self-water | expect empty | — | — | False → False |
| period-boundary | expect empty | — | — | False → False |
| falling-dairy | expect empty | — | — | True → False |
| cheaper-milk | expect empty | — | — | True → False |
| sales-only | expect empty | — | — | True → False |
| demand-only | expect empty | — | — | True → False |
| aviation | expect empty | — | — | True → False |
| logistics-provider | expect empty | — | — | True → False |
| museum | expect empty | — | — | True → False |
| not-but | CL-2022 | miss | 3 | — |
| without-while | CL-2022 | 4 | 3 | — |
| no-and | CL-2022 | miss | 3 | — |
| down-and-up | HSY-2025-Q1 | 1 | 1 | — |
| unknown-but | CL-2022 | miss | 3 | — |
| costs-versus-sales | GIS-2007 | 1 | 1 | — |
| sales-and-costs | CL-2022 | 4 | 3 | — |
| costs-versus-profit | CL-2022 | 3 | 3 | — |
| changed | expect empty | — | — | True → False |
| either-direction | expect empty | — | — | True → False |
| contradiction | expect empty | — | — | True → False |
| no-longer | expect empty | — | — | False → False |
| not-declining | expect empty | — | — | False → False |
| topic-only | GIS-2007 | 1 | 1 | — |
| cost-topic | GIS-2007 | 1 | 1 | — |
| food-scope | NES-WATERS-2011-H1 | 1 | 1 | — |
| negative-sector | GIS-2007 | 1 | 1 | — |
| not-only | GIS-2007, CL-2022 | miss, miss | 1, 4 | — |
| positive-unknown | GIS-2007 | 1 | 1 | — |
| negative-alternative | GIS-2007 | miss | 1 | — |
| factory-scope | GIS-2007 | 1 | 1 | — |
| unknown-sector | expect empty | — | — | True → False |
| business-product | GIS-2007 | 2 | 1 | — |
| ambiguous-power | expect empty | — | — | True → False |
| split-costs | KC-2011 | 2 | 1 | — |

Changes (query IDs):
- retrieval improvements: mixed-negation, not-but, no-and, unknown-but, not-only, negative-alternative
- retrieval regressions: none
- rank regressions: none
- false positive regressions: none
- false positive improvements: falling-milk, milk-sales, airline, oil-art, falling-dairy, cheaper-milk, sales-only, demand-only, aviation, logistics-provider, museum, changed, either-direction, contradiction, unknown-sector, ambiguous-power
- top result changes: mixed-negation, falling-milk, milk-sales, airline, oil-art, falling-dairy, cheaper-milk, sales-only, demand-only, aviation, logistics-provider, museum, not-but, without-while, no-and, unknown-but, sales-and-costs, changed, either-direction, contradiction, not-only, negative-alternative, unknown-sector, business-product, ambiguous-power, split-costs
- remaining failures: none

Both methods use the same ordered eligible, deduplicated pool per query; IDs and matching pool hashes are recorded in results.json. The old method must reproduce every captured baseline rank and score. No cases or source records were added or changed.

M005 related_v1 is reproduced unchanged. M006 context_v1 retains its vocabulary and BM25 formula, reading only pressure passages. General clause rules separate inputs from sales/demand, identify rising/falling/unspecified directions, split contrast and independent assertions, remove denied/unknown statements, and recognize explicit non-consumer-goods business contexts. Product names in recognized business descriptions do not become input evidence. Opposite directions for any shared input veto a partial match on another input. Bare topic lists remain searches with unspecified direction; they are never labelled as increases in the query.

Packaging investigation: M005 discarded the negated milk clause, leaving one packaging term. Compressed passage lengths then favour CL-2008 (one input family) over CL-2022 (packaging plus transport), through BM25 length normalization. A packaging-only query cannot justify preferring the latter case; CL-2022 stays useful at rank 3. M006 restores mixed-negation searches without forcing this case upward. The broader packaging/logistics query retains CL-2022 first. Scores and every rank are recorded; rank is not analogy quality.
For the frozen mixed-clauses query, both methods give CL-2008 1.363102, CL-2015 1.056404, CL-2022 1.056404 and NES-WATERS-2011-H1 0.862371. CL-2015 and CL-2022 tie and are ordered by ID, not domain preference.

Limits: this explicit grammar and industry vocabulary are incomplete. Complex attachment, omitted subjects, unlisted word senses/sectors, predictions and long-distance negation can still fail. Ignored statements and the interpreted direction are visible in the app. Related inputs are not identical materials; unknown source facts and action effects remain unknown. A passing development query does not validate general understanding or response effectiveness.
Post-implementation diagnostics (diagnostics.json, excluded from frozen evaluation counts) still find safe but useful-case misses for unpunctuated 'rising not falling' and comma-linked opposite input changes. Mentioning a logistics supplier can also cause conservative industry rejection even when the business is a food maker. No frozen-query failures is not a claim of no remaining search failures.

The 65 query texts, expectations and M005 baseline were frozen in 234fab0; b1f85a7 corrected one mixed-direction expectation before implementation to exclude a case with explicitly opposite dairy costs. No labels changed after method edits. These queries were chosen with knowledge of M005 failures and are not held-out or human judgements. `make search-check` reproduces M006; `make search-check-m005` reproduces historical M005 ranks without rewriting its files. `PYTHONPATH=src python3 scripts/evaluate_search.py --write` records M006 outputs. No case records or model experiment changed.
