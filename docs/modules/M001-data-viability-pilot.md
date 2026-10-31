# M001 — Data viability pilot

Owner: Builder. Authorized end to end by D017, 31 October 2026.

Deliver a small reproducible experiment showing whether public FMCG disclosures can support useful historical case retrieval. The original detailed contract is preserved in docs/archive/M001-original-contract.md; its task gates no longer govern execution.

## Deliverables

1. Evidence rules and one worked example (existing guide and corrected Colgate case).
2. Ten traceable observations across companies and periods, source/identity limitations and honest reviewer labels.
3. Five distinct queries, explicit candidate/date rules, pre-ranking relevance judgements and frozen inputs.
4. Paired BM25 and pretrained dense rankings, precision@5/nDCG@5, reproducible commands and meaningful tests.
5. A readable comparison with transfer limits, error analysis and continue/narrow/revise recommendation.

Builder owns all internal steps. No separate role handoff or permission is required. Preserve material scientific shortfalls rather than pad counts or invent reviews. Assistant checks support the development pilot; the original demand for ten human-reviewed cases and independent code review is not fulfilled by self-review. Report that distinction in the final evidence matrix. User acceptance remains separately recorded.

## Checks

Validate publication and reporting dates, self/duplicate exclusion, complete pair labels, ranking-text allowlist, source locators, units/accounting basis and frozen hashes. Both methods must rank identical candidates. Run tests and lint, rerun rankings to check reproducibility, inspect weak/no-match queries, and record actual failures. No minimum model improvement required.

The pilot does not include a chatbot, production backend, automatic source acquisition, structural retrieval, fine-tuning or a public corpus release. The final report, not another task assignment, closes Builder's work when these deliverables pass.
