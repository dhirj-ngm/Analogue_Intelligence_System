# Project explanation and intended experience

**Updated:** 9 October 2026  
**Direction:** [PROJECT_BRIEF.md](../PROJECT_BRIEF.md)  
**State:** Product explanation and design intent; no implemented application

## Purpose and audience

The Historical Analogue Intelligence Engine is a place where analysts,
researchers and students investigate company situations through curated
historical case studies. A reader supplies a situation, partial hints or a
comparison question and explores whether related incidents happened before,
how companies responded, their documented reasoning and subsequent observations.

Start within business and supply chain intelligence: FMCG input cost pressure,
reported margin drivers and company responses. The audience can be broad while
the initial evidence domain remains bounded. Search earlier cases at other
companies and the current company's own public history.

The reader draws inferences for their own study or work. Show differences,
unknowns and contrary evidence alongside useful similarities. A historical
response is evidence to investigate; its later outcome does not establish that
the response caused a recovery or will transfer to another company.

## Product and research objectives

**Product objective:** make useful historical company cases easier to find,
understand, compare and challenge. A case should be readable and its important
claims traceable to source passages. Later feedback can examine time to useful
evidence, understanding of differences and ability to recognize a weak match.
These are proposed evaluation dimensions, not measured benefits.

Product usefulness is now Dheeraj's current priority (D012). The intended
experience is conversational: ask relevant clarifications, structure the
situation, adapt explanation depth/style, then follow the reader's interests
through supported case details. Fixed pilot queries can establish retrieval
before that interface is built. Dialogue does not complete missing historical
evidence or establish independent retrieval accuracy.

**Research objective:** test whether explicitly representing business mechanisms,
typed relationships and admissible context improves analogue retrieval beyond
keyword and semantic search. Improvements are hypotheses. A useful case-study
workspace and a better retrieval metric are separate outcomes.

The technical experiment must distinguish gains from better curated information
from gains due to a structural representation. See
[Open questions](research/open-questions.md) for the proposed controls.

## An investigation, step by step

1. The user describes a situation or asks a comparison question. A pilot query
   can be a fixed case or structured form; open-ended conversational parsing
   can follow once retrieval works.
2. Identify the investigation objective, known conditions and information cutoff.
   Clarify missing information that materially changes eligibility or meaning.
3. Select admissible earlier episodes, excluding the query case and near duplicates.
4. Rank the eligible cases using the chosen baseline or experimental method.
5. Show readable cases, supporting passages, similarity components and differences.
6. Let the reader inspect responses, rationales and dated follow-up observations.
7. Preserve the query, corpus version and ranking configuration for reproducibility.

An unsupported or weak comparison should remain visibly weak. A corpus with no
adequate case should return that limitation rather than fabricate a case study.
Offer the nearest supported partial comparison when defensible, explicitly
labelled as limited and not sufficiently supported. If no admissible related
case exists, return no case. The operational support policy remains to be designed.

## Case-study presentation

Each case should organize supported information into:

- **Identity:** company, period, sector/category and source publication dates.
- **Challenge:** conditions and pressures established by the evidence.
- **Reported mechanism:** how the disclosure relates pressures to effects,
  preserving attribution and uncertainty.
- **Response:** announced or implemented actions and any documented constraints.
- **Rationale or principles:** the company's stated reasoning, with a passage;
  separately labelled analyst/system interpretation where relevant.
- **Follow-up:** later developments and compatible metrics, with dates.
- **Comparison:** useful similarities, material differences and missing evidence.
- **Evidence:** passages and source locations for the supported claims.

Do not require every case to end in recovery. Unsuccessful responses, mixed
outcomes and incomplete follow-up also belong in a useful corpus. Avoid
selecting only success stories and calling their responses proven principles.

### Illustrative comparison

This is a hypothetical explanation, not a dataset entry or a real-company claim:

> A consumer-products company reports higher packaging costs and falling gross
> margin. An earlier company episode reports similar cost pressure, but its
> disclosures describe greater pricing flexibility. That episode may illuminate
> cost exposure while offering a limited comparison for response selection.

The same candidate can be more useful for studying margin drivers than for
studying pricing actions. Relevance must be tied to the query's purpose.

## Records and what they preserve

An episode is a bounded company situation supported by one or more documents.
Multiple passages or quarterly updates can describe one episode. The following
are conceptual records from brief section 8; exact schemas follow real examples.

Four reports updating the same continuing pressure are one case with four
linked updates (D012). A time gap is an identity-review signal, not a fixed
split rule; continuity, business scope and resolution/recurrence evidence matter.

| Record | What it preserves | Contribution to the output |
| --- | --- | --- |
| Company | Canonical identity, aliases, sector, geography and source identifiers | Company identification and supported filters |
| Source document | URL, issuer, type, publication date, reporting period, retrieval time and content hash | Traceability and evidence version |
| Evidence span | Document link, exact passage, section/page and offsets when available | Inspectable support for a claim |
| Episode | Company, bounded period, context, mechanism tags, shock family and evidence IDs | The historical case being retrieved |
| Event | Type, entity, event time/interval, publication date and evidence | Dated developments in a timeline |
| Relationship | Directed subject/relation/object, dates, attribution and review status | Qualified mechanism representation |
| Action | Type, announcement date, implementation status, constraints and evidence | Documented company response |
| Metric | Value, unit, period, scope, accounting basis, publication date and source | Compatible quantitative context |
| Rationale/principle annotation | Sourced management statement or explicitly labelled interpretation | Explanation of a response; proposed annotation, not a fixed new schema |
| Follow-up observation | Later developments, metrics, evidence and confounders | Separately dated subsequent observations |
| Retrieval judgement | Query/candidate IDs, grade, rationale, reviewer and date | Independent assessment of usefulness |
| Experiment | Corpus/split/config versions, seed, metrics and runtime | Reproducible comparison of methods |

Keep unknown values explicit. Missing pricing information does not establish
limited pricing power. Group and segment metrics, gross and operating margin,
and adjusted and GAAP figures require their own definitions and scope.

## Preparation and query responsibilities

Preparation jobs acquire permitted sources, preserve originals, extract passages,
construct/review episodes, validate records and build versioned indexes.
Queries operate on that prepared corpus. Acquisition is separate from interactive
ranking, making evidence review and experiments reproducible.

Event time and public-information time are distinct. A report published in
February describing the previous year was not available in December. Enforce
cutoffs for the query evidence, candidates and ranking features. For the first
experiment, keep later response/outcome fields out of similarity features and
display them as follow-up, per brief section 11.

## Baselines and later custom AI

Begin with BM25 for lexical retrieval and dense embeddings for semantic
similarity. Text fusion and an inspectable structural/context score are candidate
next comparisons. Score scales, weights and missing-value handling remain open.

Dheeraj intends to build a later task-specific AI component. The corpus can
support training examples and features, but its records do not all need to be
fed into one model. Model tasks may include statement detection, relation
extraction, query interpretation or reranking. Select the task after the pilot
reveals a measurable gap and sufficient labels.

The evidence store, date checks, eligibility, source access and versioning remain
explicit system responsibilities. A learned component must be evaluated on held-out
data and compared with the retained baselines. An external pretrained model's
historical knowledge is a potential hindsight limitation if it generates facts;
do not present unsupported model knowledge as contemporaneous source evidence.

The term `jev` in discussion is unresolved. Confirm the exact method/tool,
purpose and documentation before adding a dependency or committing to a design.

## Delivery and knowledge routing

The current milestone is ten reviewed episodes and five investigation queries,
with baseline rankings, an error review and a continue/narrow/revise decision.
M001 is In Progress under D014: [guide v0.1](../data/annotation_guide.md) is
drafted and checked, awaiting Domain/Dheeraj review through the
[T01 handoff](workflow/M001-T01-handoff.md). Real episodes, queries and runs
remain unstarted; the eventual conversational experience is not implemented.
This is a feasibility pilot. The later system adds reproducible corpus handling,
evaluation, structure, a conditional learning experiment, backend, case-study
workspace and reproduction instructions.

See [Module map](module-map.md) for proposed boundaries,
[Literature map](research/literature-map.md) for precedents, and
[Thread starter prompts](workflow/thread-start-prompts.md) for execution roles.
Accepted choices belong in [DECISIONS.md](../DECISIONS.md), and actual progress
in [STATUS.md](../STATUS.md). This explanation does not approve an architecture
or imply any experiment has been completed.
