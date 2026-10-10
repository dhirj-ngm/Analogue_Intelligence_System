# Initial literature map and research position

**Recorded:** 9 October 2026  
**Basis:** Primary sources consulted in the Manager discussion on 8 October,
with the recent analogy abstracts rechecked on 9 October 2026.

This is a maintained starting map, not a systematic review, replication or
endorsement of a paper's performance claims. Separate what a source reports
from our interpretation of its relevance. Detailed paper discussions can add
notes here or linked files; accepted project choices enter
[DECISIONS.md](../../DECISIONS.md).

## Foundations

### Gentner (1983): Structure-Mapping

The framework distinguishes analogy through shared relational structure from
general overlap of object attributes. Our interpretation: the comparison should
represent supported relationships among pressures, constraints and reported
effects. It does not establish that the brief's proposed feature score implements
the full theory or improves retrieval.
[Primary paper](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf)

### Aamodt and Plaza (1994): Case-Based Reasoning

The case-based reasoning cycle includes retrieval, reuse, revision and retention.
Our initial product emphasizes retrieving and inspecting evidence; adapting a
historical strategy or testing its effectiveness is a distinct further task.
This precedent rules out claiming that using past cases is itself novel.
[Primary paper](https://oak.conncoll.edu/parker/com316/papers/CBR.pdf)

### Gavetti, Levinthal and Rivkin (2005): Strategy Making in Novel and Complex Worlds

An agent-based simulation examines how representation, experience and adherence
to analogies affect strategy search. The authors report advantages of relevant
representations and risks of rigid transfer. Our interpretation: show meaningful
differences and allow readers to challenge a comparison. Simulation results are
not empirical validation of this company's disclosures or our engine.
[Primary paper](https://faculty.wharton.upenn.edu/wp-content/uploads/2012/05/Strategy-in-Novel-Environments.pdf)

## Retrieval, extraction and temporal structure

| Work | Source's task or finding | Relevance and boundary |
| --- | --- | --- |
| FinCausal 2020 | Binary classification and relation extraction in financial documents | Task-design precedent for reported explanations; financial language does not establish causal effects. [Paper](https://aclanthology.org/2020.fnp-1.3/) |
| BEIR 2021 | Diverse retrieval benchmark; BM25 is reported as a robust baseline | Compare fairly with lexical retrieval; embedding superiority in FMCG is unproven. [Paper](https://arxiv.org/abs/2104.08663) |
| HiSMatch 2022 | Matching query/candidate historical structures for temporal KG reasoning | Relevant representation precedent; entity prediction differs from case usefulness. [Paper](https://aclanthology.org/2022.findings-emnlp.542/) |
| GraphRAG 2024 | Entity graph/community summaries for corpus-wide query-focused summarization | Useful graph/text precedent; global summaries differ from episode ranking. [Paper](https://arxiv.org/abs/2404.16130) |
| AnRe 2025 | Analogical replay and historical context for temporal KG forecasting | Relevant historical-pattern precedent; forecasting results do not validate our comparison task. [Paper](https://aclanthology.org/2025.acl-long.231/) |

## Closer analogy and financial precedents

### Puranam, Sen and Workiewicz (2025): LLMs and Strategic Analogical Reasoning

The study reports high recall but lower precision from GPT-4 analogy selection,
with superficial matches, while human participants selected fewer analogies
with stronger alignment. The findings apply to the studied model and setting.
Our interpretation: broad candidate discovery and critical comparison may need
different checks; changing model/version does not establish the same result.
[Primary preprint](https://arxiv.org/abs/2505.00603)

### Chen and colleagues (July 2026): Analogical Deep Research

This close precedent studies historical analogies for foresight, proposing
mechanism alignment, structural decomposition and cross-analogy confirmation.
The paper describes fifteen target events in ADR-bench and reports improvements
for its CANA framework. The arXiv record describes an ongoing project; we have
not reproduced it or independently verified performance.

Our interpretation: historical mechanism matching is prior art. Study its
representation and evaluation, but preserve our FMCG focus, sourced attributions
and bounded retrieval objective. The paper's causal/foresight framing does not
authorize our system to infer unobserved causes from company reports.
[Abstract](https://arxiv.org/abs/2607.13602),
[Paper text](https://arxiv.org/html/2607.13602v1)

### Khanna and colleagues (2025): History Rhymes

The work uses macroeconomic context and text to retrieve historical regimes for
financial forecasting and reports out-of-distribution results. Our interpretation:
contextual retrieval is a relevant comparator idea. Its market prediction task,
data and outcomes differ from curated company case-study relevance, and we have
not validated its empirical results.
[Primary preprint](https://arxiv.org/abs/2511.09754)

## Defensible project contribution

The project can contribute an evidence-linked, dated FMCG episode corpus; an
explicit relevance and candidate-eligibility protocol; controlled comparisons
of text and structural/context representations; and a workspace exposing both
similarities and limits. Broader novelty requires more literature review and
stronger evaluation. Negative retrieval results should be preserved.

These sources establish research interest, not society-wide consensus or demand
for this specific product. Reader usefulness requires task-based feedback.
Commercial product descriptions from the brief show adjacent workflows, not
independent evidence of effectiveness or validation of our design.

## Suggested first reading discussions

Start with Gentner, the 2025 strategic-decision study and the 2026 Analogical Deep
Research paper. For each, examine the problem, representation, data, baselines,
evaluation, assumptions, errors and possible transfer to disclosures. Then use
BEIR for evaluation discipline and FinCausal for a bounded extraction task.

Capture at least one design implication and one reason the finding might not
transfer. Keep full-text reading, abstract inspection and replication distinct.
Record access and reuse terms before adopting datasets or code.

The Domain discussion's [reading sequence and inspection log](reading-sequence.md)
adds a recommended order, source-linked questions and targeted primary-text
observations. It records abstract versus selected full-text inspection explicitly;
no completed full-paper reading or reproduction is claimed for that assignment.
Its implications are proposals, not adopted evaluation or annotation policy.
