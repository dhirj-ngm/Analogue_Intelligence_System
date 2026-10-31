# Pilot protocol v1 — frozen before rankings

Development demonstration, not an independent or held-out benchmark. Builder selected five distinct investigation objectives and hand-assigned grades before either baseline ran. No tuning or statistical superiority claim. Human labels are unavailable; D016 is bounded feedback on one case only.

Corpus: data/pilot/cases.jsonl, a compact projection/new pilot dataset preserving the original detailed Colgate worksheet unchanged. Ten observations from five issuers; true episode boundaries remain uncertain. No adjacent quarterly updates are counted twice. Different companies in 2021–22 share inflation conditions and are not independent shocks. Colgate observations are years apart but continuity remains a limitation.

Eligibility: known publication date <= query cutoff; candidate period ends strictly before target period end; exclude source ID and designated duplicate groups. Unknown dates excluded. Synthetic Q5 is an explicit out-of-corpus investigation, not a real company claim. Query text uses only challenge information. Ranking uses ONLY challenge text; responses, metrics, labels, rationale, company identity, tags and outcomes are excluded. BM25 IDF is computed on eligible candidates separately for each query; dense cosine uses the identical candidates and text. No external retrieval at ranking time.

Rubric: 3 directly useful shared driver; 2 useful partial comparison; 1 weak/background match with material mismatch; 0 unsupported mechanism/unrelated. Grades are task-specific, not strategy-success judgements. Every eligible pair has a pre-ranking grade, rationale and transfer limitation. Unknown evidence is not a documented mismatch.

Metrics: nDCG@5 with gain 2^grade-1, log2(rank+1), zero for zero ideal gain; P@5 uses relevance >=2 and denominator 5 even with fewer candidates. Report candidate counts and no-positive queries. Both methods always rank; no calibrated abstention threshold is claimed. Q5 tests the need to display insufficient evidence, not automatic detection of it. Stable ID resolves exact score ties; dense numeric tolerance 1e-5. Model fixed before runs; no train/test split, no tuning.

Freeze manifest hashes corpus, queries, all judgements, this protocol and model configuration. Changes require a new explicit benchmark version. The model may have seen public disclosures during pretraining; this experiment cannot prove historical model-training isolation.
