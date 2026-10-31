# M001 pilot report — 31 October 2026

**Delivery:** working development pilot, with scientific validation shortfalls explicitly retained. **Recommendation: narrow** the next build to evidence-backed comparisons of reported pressures and responses. Do not yet claim strategy learning, independently reviewed analogues or an effective conversational advisor.

## Delivered

Ten compact source-linked observations across five issuers and multiple years; five fixed investigations; 33 eligible pre-ranking assistant judgements; publication/self/duplicate controls; BM25 and pinned MiniLM dense retrieval; tests, commands, results and offline reproducibility evidence. Original corrected Colgate worksheet and D016 feedback preserved.

| Method | Mean P@5 | Mean nDCG@5 |
| --- | ---: | ---: |
| BM25 | 0.400 | 0.6253 |
| MiniLM dense | 0.360 | 0.6561 |

Means include the zero-relevance query. Candidate counts Q1–Q5 are 7, 5, 2, 9 and 10. Dense has slightly higher mean nDCG but lower P@5; five assistant-labelled questions cannot establish superiority. No split, tuning, independent relevance review or statistical testing was performed.

## Readable comparison

For the Colgate Asia Pacific Q4 2022 investigation, CL-2008 is a supported partial own-company comparison: both disclosures identify materials/packaging cost pressure and describe pricing and savings as offsets. The 2008 observation concerns global gross margin excluding restructuring; the 2022 example concerns regional operating margin. Those measures include different costs and scopes, so their levels cannot be compared directly. Neither source isolates the effect of a response or supplies a transferable best strategy. Exact implementation detail and later outcomes remain unknown in the pilot.

Clorox 2021 is a cross-company comparison with a material difference: alongside input/logistics inflation, shipment normalization and manufacturing absorption contributed to the margin decline. That is useful context, but it cannot establish that the same mechanism operated in Colgate. This walkthrough is assistant-authored; D016 supplies human feedback only on the original example's limited usefulness. No new reader-usability result is claimed.

## Original acceptance matrix

| Criterion | Evidence / disposition |
| --- | --- |
| AC01 usable rules/example | Existing guide, corrected T02 record and D016; compact pilot schema documented. Definitive boundaries remain uncertain. |
| AC02 source coverage | source-coverage.md records inspected sources, redirects and access limits. Full archive/public reuse clearance remains unverified. |
| AC03 ten reviewed cases | Ten assistant-checked bounded observations. Original ten human-reviewed, distinct-episode criterion is **not satisfied**. |
| AC04 five queries/judgements | Five queries and 33 frozen eligible-pair grades; assistant-only descriptive evaluation. |
| AC05 reproducible baselines | Paired rankings, pinned model/config, dependency lock, run manifest and offline rerun evidence. |
| AC06 protections | Seven tests plus saved-candidate/hash/metric audit; no response/outcome fields in ranking text. |
| AC07 usefulness/errors/effort | Concrete comparison above, per-query errors and explicit missing effort/reader evidence. No new human usability test. |
| AC08 recommendation/review | Narrow recommendation and Builder self-review delivered; independent review and user module acceptance are not claimed. |

D017 removes task-start handoffs and authorizes whole-module execution; it does not turn assistant checks into human validation. This is complete as a reproducible development implementation under the compact module specification, with the original research acceptance shortfalls above. It is not marked scientifically validated or human-accepted.

## Next practical scope

Reuse the existing runner and records. Improve evidence depth and case readability before adding graph ranking or custom training. In particular, collect dated response implementation and follow-up evidence, clarify episode continuity, and obtain a small independent relevance review when feasible. A modest case-search/comparison interface can be built on the current data with visible source and uncertainty labels; its usefulness must then be tested with readers.

Per-case human curation time and a reliable scaling estimate remain unknown. Avoid projecting the old assistant T02 timing into a corpus budget. No paid service or additional MCP is needed for the current pilot.

## Verification

`make test lint validate` passes. `scripts/audit_results.py` verifies frozen hashes, both methods, exact eligible sets and metrics. Two CPU runs produced identical ranks and metrics; score differences were below 1e-5, with the second run offline. See baselines/reproducibility.json and run-manifest.json. No deployment, commit or publication performed.
