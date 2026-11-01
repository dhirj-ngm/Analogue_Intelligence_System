# M005 paired search checks

Assistant-authored development checks, selected with knowledge of M004 misses. Expected useful cases are not exhaustive relevance grades; no independent validation or causal claims.

Across 15 useful-case queries, expected cases appeared in the first five in 7 old / 14 new results.
Across 18 expected-empty queries, unexpected candidates appeared in 3 old / 4 new results.

| Query ID | Expected useful case(s) | Old rank(s) | New rank(s) | Unexpected candidates old → new |
| --- | --- | --- | --- | --- |
| milk-flour-electricity | GIS-2007 | miss | 1 | — |
| chocolate | HSY-2025-Q1 | miss | 1 | — |
| bottled-water | NES-WATERS-2011-H1 | miss | 1 | — |
| literal-food | GIS-2007 | 1 | 1 | — |
| literal-cocoa | HSY-2025-Q1 | 1 | 1 | — |
| literal-oil | NES-WATERS-2011-H1 | 1 | 1 | — |
| literal-packaging | CL-2022 | 1 | 1 | — |
| literal-resin | KC-2011 | 1 | 1 | — |
| wheat-power | GIS-2007 | miss | 1 | — |
| milk-powder | GIS-2007 | miss | 1 | — |
| cacao | HSY-2025-Q1 | miss | 1 | — |
| freight | NES-WATERS-2011-H1 | 1 | 1 | — |
| unsupported-chips | expect empty | — | — | False → False |
| unsupported-coffee | expect empty | — | — | False → False |
| unsupported-steel | expect empty | — | — | False → False |
| generic | expect empty | — | — | True → False |
| action-only | expect empty | — | — | False → False |
| negated-chocolate | expect empty | — | — | False → False |
| negated-milk | expect empty | — | — | False → False |
| mixed-clauses | CL-2022 | 1 | 3 | — |
| mixed-negation | CL-2022 | miss | miss | — |
| falling-milk | expect empty | — | — | False → True |
| milk-sales | expect empty | — | — | False → True |
| airline | expect empty | — | — | False → True |
| oil-art | expect empty | — | — | True → True |
| early-food | expect empty | — | — | False → False |
| early-water | expect empty | — | — | False → False |
| early-chocolate | expect empty | — | — | True → False |
| inclusive-chocolate | HSY-2025-Q1 | miss | 1 | — |
| self-cocoa | expect empty | — | — | False → False |
| self-food | expect empty | — | — | False → False |
| self-water | expect empty | — | — | False → False |
| period-boundary | expect empty | — | — | False → False |

Changes (query IDs):
- retrieval improvements: milk-flour-electricity, chocolate, bottled-water, wheat-power, milk-powder, cacao, inclusive-chocolate
- retrieval regressions: none
- rank regressions: mixed-clauses
- false positive regressions: falling-milk, milk-sales, airline
- false positive improvements: generic, early-chocolate

Both methods use the same ordered eligible, deduplicated pool per query; IDs and matching pool hashes are recorded in results.json. The old method must reproduce every captured baseline rank and score. No cases or source records were added or changed.

The old method uses literal BM25 on allowlisted challenge text plus a shared pressure-word gate. The new method uses the same BM25 formula on named families from pressure passages only. A fixed vocabulary joins related inputs; generic ingredient/commodity words do not rank a case. This changes both the vocabulary and scoring representation, not the eligibility rules. No responses, outcomes or business identity are used to build concepts.

Remaining limits: related inputs are not identical materials. The vocabulary does not reliably understand industry, sales versus input costs, direction of change or mixed negation. Falling milk costs, booming milk sales and airline fuel can produce misleading candidates; oil paintings already misled the old method. The mixed-negation query can still lose a useful packaging match. Explicitly negative/unknown clauses remain excluded. The app displays its term links and cautions; this is not a general relevance model.

Inputs and expected cases were frozen in commit cb1b37c before search changes, from M004 base bd2046f. The 33 queries were deliberately chosen development examples, not a held-out benchmark. Run `make search-check` to verify the freeze, reproduce the literal baseline, and compare the new results without network access. `PYTHONPATH=src python3 scripts/evaluate_search.py --write` records outputs. No model experiment was rerun.
