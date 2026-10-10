# Domain/research reading sequence and inspection record

**Recorded:** 9 October 2026  
**Owner:** Domain and Research discussion  
**State:** Reading recommendation and bounded source inspection, not a systematic
review, reproduced experiment or accepted project design.

Use the [existing literature map](literature-map.md) as the inventory. This note
adds a learning sequence, questions for full reading and explicit inspection
depth. Read alongside the [analogue discussion draft](../domain/analogue-definition.md).
The suggested order is a Domain judgement about this project's needs, not a
finding from the papers. No new paper has been adopted as a dependency.

## Distinguish three levels of engagement

**Abstract inspection:** establish the source's stated task, broad approach and
reported result. This does not verify sampling, prompts, baselines, metrics or
statistical claims. An abstract's performance claim remains the authors' claim.

**Full-paper reading:** read the representation, assumptions, methods, data,
evaluation, results, limitations and relevant appendices. Record the paper
version, reconstruct the argument and identify what the result actually supports.
Selected full-text passages are useful inspection, but do not count as a completed
full-paper reading or proof audit.

**Reproduction:** execute a specified experiment under recorded versions,
data/splits, model configurations and metric conventions, compare the result
with the source and explain deviations. Running an AIS baseline is not reproducing
BEIR; inspecting code is not executing it. For theoretical claims, checking a
proof against its assumptions is a proof audit, distinct from computational
reproduction. An adapted FMCG experiment is a new transfer test.

**This assignment:** abstract/source-page inspection and targeted full-text
inspection only, as logged below. No completed full-paper reading, dataset/code
audit, proof audit or reproduction is claimed. Source access is not permission
to reuse every dataset or redistribute every document.

## Recommended sequence

| Order and source | Why read it now | Full-reading question and concrete output | Limit of transfer |
| --- | --- | --- | --- |
| 1. [Gentner (1983)](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf) | Establish relational alignment and connected structure before designing features | Map H-A and H-B onto the target; identify the relationship whose change breaks the comparison | A theory of analogy does not prove that a tag-overlap score implements it or improves FMCG retrieval |
| 2. [Puranam, Sen and Workiewicz (2025)](https://arxiv.org/abs/2505.00603v1) | Examine superficial matching and selection errors in strategic analogies | Read task design, hints, error coding and limits; write one positive and one misleading comparison independent of model tags | The source compares GPT-4 with business-school students on constrained story tasks; it does not establish results for current models or disclosure search |
| 3. [Chen et al., Analogical Deep Research (2026)](https://arxiv.org/html/2607.13602v1) | Inspect a close historical mechanism-matching precedent before making novelty claims | Read §§3–5 and theory/rubric appendices; distinguish retrieval, generation, foresight and hidden-factor inference | AIS preserves documented attributions; it does not infer hidden causes or adopt the paper's causal identification claim |
| 4. [Aamodt and Plaza (1994)](https://oak.conncoll.edu/parker/com316/papers/CBR.pdf) | Put case retrieval in its broader reuse/revision/retention setting | Read the cycle and retrieval sections; state which stages AIS supplies and which require separate validation | Showing responses is different from adapting and testing a strategy |
| 5. [Gavetti, Levinthal and Rivkin (2005)](https://faculty.wharton.upenn.edu/wp-content/uploads/2012/05/Strategy-in-Novel-Environments.pdf) | Question representation choice and rigid analogy transfer | Read the simulated world, agent behaviour and assumptions; identify a plausible FMCG condition outside the simulated setting | Agent-based simulation is not empirical validation of company mechanisms |
| 6. [BEIR (2021)](https://arxiv.org/abs/2104.08663v4) | Prepare a defensible retrieval comparison; move this earlier before M001-T05/T06 | Read datasets, judgement/metric conventions and system comparisons; write the pilot information-budget and per-query reporting checklist | Its reported robust BM25 baseline does not choose the best method for this corpus |
| 7. [FinCausal (2020)](https://aclanthology.org/2020.fnp-1.3/) | Study a bounded financial-language annotation task after the domain distinctions are understood | Read classification/relation guidelines and difficult examples; test whether “reported explanation” fits our evidence categories | Linguistic causal relations do not establish intervention effects; adopting this dataset needs label/access checks |

The first three support the immediate domain discussion. Aamodt/Plaza and Gavetti
help defend the product boundary and challenge assumptions. BEIR becomes practical
before evaluation execution. FinCausal becomes practical if later evidence supports
an extraction task; this ordering does not select the custom AI responsibility.

Read [HiSMatch](https://aclanthology.org/2022.findings-emnlp.542/) and
[AnRe](https://aclanthology.org/2025.acl-long.231/) when temporal/structural design
is considered: their source tasks predict entities/events in temporal knowledge
graphs. Ask whether the representation survives partial, attributed company
disclosures; their prediction results do not answer case-study relevance.

Read [GraphRAG](https://arxiv.org/abs/2404.16130v2) when discussing corpus-wide
questions: its source task is global query-focused summarization, rather than
episode ranking. Read [History Rhymes](https://arxiv.org/abs/2511.09754v2) when
discussing macro context: the authors describe macro-contextual retrieval for
financial forecasting, a different target and outcome from AIS. Neither is
mandatory infrastructure or a reason to expand M001.

## Primary-source observations that sharpen the discussion

**Strategic analogy study:** the full-text lab-design and conclusion passages
describe selecting between supplied source stories for target problems. Our
interpretation: distinguish finding candidates in a corpus from assessing a
supplied comparison. The abstract's precision/recall characterization should
not be presented as measured AIS retrieval performance. The limitations section
identifies business-school students as the human pool.
[Primary PDF, §3 and §5](https://arxiv.org/pdf/2505.00603v1).

**ADR:** the inspected text uses 15 target events, with historical and unfolding
subsets. Theorem 5 assumes conditional independence across confirming analogies.
Table 2 identifies an LLM judge for its analogy rubric, and §5.2 uses an LLM judge
for ADR scoring. These details limit how performance claims transfer: shared
shocks/sources may defeat independence, and model-judged alignment is not an
independent human assessment of reader usefulness. The numerical example about
two independent analogies depends on its stipulated probabilities; it is not
a universal minimum-evidence rule. These are inspection findings and Domain
interpretations, not a proof audit or a rejection of the work.
[Primary text, §3.3, Table 2 and §5.2](https://arxiv.org/html/2607.13602v1).

**Case-based reasoning:** §5 explicitly connects retrieval strategy to retrieval
purpose. Our interpretation: keep the investigation objective attached to each
query, rather than assigning one universal similarity meaning. The cycle also
separates case retrieval from reuse and testing/revision.
[Primary paper, §§3.1 and 5](https://oak.conncoll.edu/parker/com316/papers/CBR.pdf).

These implications supplement existing Q01/Q04/Q05/Q07 concerns. They do not
settle relevance grades, reviewer availability, splits, model choice or the
custom AI task. Multiple corporate recoveries still cannot prove a response's
causal effect simply by resembling one another.

## Inspection log for this assignment

All entries were accessed through primary-source links on 9 October 2026.
“Targeted text” means selected body passages were inspected, not all paper pages.

| Source/version | Depth reached | What supported the note | Remaining work |
| --- | --- | --- | --- |
| Gentner 1983 author-hosted PDF | Targeted text | Attribute/relational distinctions, mapping rules and systematicity discussion, pp. 156–163 | Complete paper and critically map business examples |
| Aamodt/Plaza 1994 PDF | Targeted text | Four-stage cycle and retrieval-purpose discussion, §§3.1/5 | Complete review; inspect adaptation/revision assumptions |
| Gavetti et al. 2005 author-hosted PDF | Abstract/introduction inspection | Agent-based simulation framing | Full model, results and limitations reading |
| Puranam et al. arXiv 2505.00603v1 | Abstract plus targeted text | Lab task, conclusion and limitations passages | Full methods/results/appendices; no raw-data or prompt audit yet |
| Chen et al. arXiv 2607.13602v1 | Abstract plus targeted HTML text | Benchmark definition, conditional-independence assumption, experiment/rubric descriptions | Full paper, theorem proofs, sampling/rubric audit and code/data access checks |
| BEIR arXiv 2104.08663v4 | Abstract inspection | Benchmark scope and reported baseline comparison | Full protocol/results; any reproduction would need exact datasets/configurations |
| FinCausal 2020 ACL source page | Abstract inspection | Binary classification and relation-extraction tasks | PDF and annotation guidelines, dataset terms and label-fit inspection |
| HiSMatch 2022 and AnRe 2025 ACL pages | Abstract inspection | Temporal KG prediction framing | Full representation/evaluation inspection if later relevant |
| GraphRAG arXiv 2404.16130v2 | Abstract inspection | Global summarization, graph index and community summaries | Full methods and evaluation if global questions become in scope |
| History Rhymes arXiv 2511.09754v2 | Abstract inspection | Macro-contextual forecasting framing | Full temporal protocol, vintages, availability and evaluation audit |

Paper availability was checked for reading. Dataset/code availability claims,
licences, empirical performance and relevance to our corpus have not been
independently verified. No experiment or paper reproduction was run.

## A reusable reading note

For a later full reading, record: exact version and depth; the research question;
input/output unit; evidence/representation; assumptions; source-reported findings;
baselines and information budgets; evaluation/judgement process; failure cases;
one possible AIS implication and one reason it may not transfer; and what would
be needed to reproduce or challenge the result. Keep these fields proportional
to useful reasoning, rather than create a new mandatory process for every link.
