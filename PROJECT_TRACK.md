# Project working rules

The project helps readers find source-backed historical comparisons for business
situations. Start with FMCG input costs and company responses. Preserve important
differences, uncertainty, and the evidence for each reported action or result.

Use two conversations: **Discussion** for ideas and explanations, **Builder** for
complete implementation. Builder chooses routine methods, researches sources,
updates data and code, runs checks, and records results without handoffs or user
review gates. Ask only for essential missing access, paid services, destructive
external actions, or a material change to the user's objective. The user asked
Builder to complete the project autonomously.

Read this file and STATUS.md when starting. Keep README.md current for purpose,
setup, commands and roadmap. Keep STATUS.md short and factual. Each module can be
tracked in STATUS.md; do not create module specs, role prompts, handoffs, decision
logs or review documents unless their content is necessary to reproduce a result.
Use Git history for old discussions and superseded plans.

For every case, preserve a source URL and locator, publication and reporting
dates, scope, metric units/basis, review provenance and unknowns. Separate issuer
attribution, observed figures, forecasts and analyst interpretation. Never infer
that a response caused an outcome. Do not count continuing reports as independent
cases. Check source reuse terms before archiving or redistributing documents.

For retrieval experiments, enforce the public-information cutoff, exclude the
query episode and known duplicates, and keep responses and later outcomes out
of first-stage similarity text. Freeze evaluation inputs before rankings. Compare
methods on identical eligible candidates. Assistant labels and self-review are
valid for development but must be labelled honestly; do not claim human or
independent validation that did not happen.

Keep code in src/, tests in tests/, tools in scripts/, source-linked records in
data/, and experimental inputs/results in evaluation/. Use meaningful tests for
behavior changes. Keep caches, environments and secrets out of Git. Commit
completed work and push when the current session authorizes it.
