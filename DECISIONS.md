# Project decisions

**Established:** 8 October 2026, Asia/Kolkata

This register records decisions and their reasons. `PROJECT_BRIEF.md` supplies
the project direction; `STATUS.md` supplies actual progress. Dates below are
recording dates, not inferred dates of the original discussions.

Use stable IDs. Status is `Accepted`, `Proposed` or `Superseded`. Append changes
with a reference to the earlier decision rather than erasing its reasoning.
An accepted project direction does not imply a feature is implemented.

## Accepted direction

### D001 — Analyst investigation in the FMCG input-cost domain

- **Recorded:** 8 October 2026.
- **Status:** Accepted; imported confirmed direction.
- **Basis:** Brief sections 2, 3 and 19.
- **Decision:** Build the Historical Analogue Intelligence Engine for business
  and supply chain investigation, initially FMCG input cost pressure, reported
  margin drivers and documented company responses.
- **Reason and consequence:** A bounded domain makes evidence collection and
  evaluation practical. Forecasting, simulation, broad policy intelligence and
  autonomous strategy recommendations remain outside the initial scope.

### D002 — Cross-company and own-company retrieval from a curated corpus

- **Recorded:** 8 October 2026.
- **Status:** Accepted; imported confirmed direction.
- **Basis:** Brief sections 5, 6 and 19.
- **Decision:** Search earlier episodes from multiple companies and the queried
  company's own public history using a deliberate, versioned corpus.
- **Reason and consequence:** Controlled evidence supports comparison and
  reproducible evaluation. Private records and live whole-web ingestion are
  unnecessary for the public-data project.

### D003 — Preserve provenance, dates and evidence meaning

- **Recorded:** 8 October 2026.
- **Status:** Accepted; imported design requirement.
- **Basis:** Brief sections 8, 10 and 11.
- **Decision:** Preserve evidence and publication dates; distinguish event time
  from public-information time and management explanations from established
  observations. The first similarity experiment excludes later response and
  outcome fields and displays them separately as follow-up.
- **Reason and consequence:** Historical comparisons must avoid hindsight and
  unsupported causal claims. Candidate and query eligibility require explicit
  rules; unknown values remain unknown and incompatible metrics stay distinct.

### D004 — Validate data viability before expanding the system

- **Recorded:** 8 October 2026.
- **Status:** Accepted; current milestone target from the brief.
- **Basis:** Brief opening, sections 12, 14 and 15.
- **Decision:** Begin with ten distinct reviewed episodes and five investigation
  queries. Compare BM25 and semantic retrieval, inspect errors and curation
  effort, and produce a continue/narrow/revise recommendation.
- **Reason and consequence:** Data quality and historical diversity determine
  whether the experiment is feasible. These are pilot targets, not statistical
  proof or a fixed deadline. Infrastructure and UI expansion follow the findings.

### D005 — Evaluate structural retrieval as a hypothesis

- **Recorded:** 8 October 2026.
- **Status:** Accepted; imported experimental requirement.
- **Basis:** Brief sections 3, 10 and 12.
- **Decision:** Test whether typed relationships and admissible context improve
  useful analogue retrieval over lexical and semantic baselines. Establish the
  relevance rubric, eligibility and evaluation split before tuning; compare the
  same candidates and record ablations and failure cases.
- **Reason and consequence:** Similarity is not a probability of strategic
  success. Retain negative results and report small-sample limitations. Fine
  tuning and learned ranking need a demonstrated task and suitable data.

### D006 — Repository records coordinate separate threads

- **Recorded:** 8 October 2026.
- **Status:** Accepted; user-requested workflow established during setup.
- **Basis:** Current conversation and brief section 17.
- **Decision:** Use Project Control / Records, module Implementation / Status,
  Reviewer and Domain Discussion threads. Share state through project files.
  Project Control owns module transitions; implementers record progress and
  reviewers supply independent findings. Dheeraj accepts domain and module results.
- **Reason and consequence:** Explicit specifications and handoffs allow work
  to resume without reconstructing conversations. Use one writer per checkout;
separate worktrees support simultaneous work. The protocol does not create
  threads or run a continuous reviewer automatically.

**9 October update:** D008 adds this existing conversation as Manager. Records
continues to own module specifications and routine status transitions.

### D007 — Name the working guidelines PROJECT_TRACK.md

- **Recorded:** 8 October 2026.
- **Status:** Accepted; naming arrangement implemented for the user's request.
- **Basis:** User request to keep the revised guidelines under another project
  tracking name; existing repository conventions and brief section 17.
- **Decision:** Put the full revised working guidelines in `PROJECT_TRACK.md`
  and retain a short `AGENTS.md` that explicitly directs Codex to read it.
- **Reason and consequence:** The requested project naming and the repository
  instruction entry point remain connected. Preserve applicable original
  repository guidelines in the working document. The original version remains
  available in Git commit `3a6db3a`.

### D008 — Manager coordination and a broader case-study audience

- **Recorded:** 9 October 2026.
- **Status:** Accepted; explicit user clarification, extending D001 and D006.
- **Decision:** Keep this conversation as Manager for coordination and doubts.
  Serve analysts, researchers and students seeking earlier company situations
  through descriptions, hints or comparison questions. Present readable curated
  case studies with documented responses, stated rationales, follow-up and limits.
- **Reason and consequence:** The user's central goal is learning from accessible
  precedents. Audience breadth does not expand the initial FMCG data domain.
  Principles inferred by a reader/system require labels; observed recovery is
  insufficient to establish an action's causal effect. Fixed queries remain
  adequate for the pilot; richer input interpretation follows the core.

### D009 — Preserve knowledge and provide bounded thread starters

- **Recorded:** 9 October 2026.
- **Status:** Accepted; explicit user request.
- **Decision:** Maintain the overview, proposed module map, literature notes,
  open questions and ordered prompts in `docs/`, routed from brief section 17.
  Preserve existing documents and record future accepted choices here.
- **Reason and consequence:** Project reasoning must remain available across
  threads. The proposed breakdown and experimental concerns await discussion;
  opening a thread does not mark its module `Ready` or approve all milestones.
  Dheeraj has deferred his responses to the concerns.

### D010 — Pursue a task-specific AI component after baselines

- **Recorded:** 9 October 2026.
- **Status:** Accepted ambition; implementation design remains open.
- **Decision:** Plan a later custom AI component after BM25/dense baselines;
  select a bounded task and training route using errors, labels and evaluation.
- **Reason and consequence:** Supports the user's AI learning and product goals.
  Extraction, query interpretation and reranking are candidates, not selections.
  The evidence store and deterministic eligibility rules remain explicit.
  The mentioned `jev` method/tool is unidentified and has not been adopted.

### D012 — Product-first conversational case-study direction

- **Recorded:** 9 October 2026.
- **Status:** Accepted; Dheeraj's explicit responses to Q01–Q11.
- **Decision:** Prioritize understanding historical FMCG challenges, documented
  responses/intended reasoning, outcomes and differences, not selecting a best
  strategy. Clarify unclear user situations, adapt explanation depth/style and
  let the reader assess usefulness. Include unsuccessful and unresolved cases.
  Continuing quarterly reports form one case with linked updates. Show the
  insufficient-analogue message and a nearest supported partial comparison when
  defensible. Select later custom AI from pilot weaknesses. Start independent
  review with checkpoint-based code correctness; domain issues belong with
  Dheeraj/Domain, and required data/provenance checks remain assigned work.
- **Reason and boundaries:** Conversation clarifies intent, not undocumented
  historical facts. A time gap flags identity review, not proof of resolution.
  Conversational structure does not select graph ranking; reader feedback does
  not resolve independent evaluation. Date mode, evidence policies, thresholds,
  labels, models, hours and reviewer availability remain open as applicable.
  Do not force an inadmissible/unrelated case merely to return one result.
- **Supporting handoff:** [Manager direction](docs/workflow/manager-direction-handoff.md).
  Extends D003–D005/D008/D010; does not approve all detailed M001 criteria or
  authorize chatbot implementation in the data pilot.

### D013 — Delegated first FMCG investigation and bounded next assignment

- **Recorded:** 9 October 2026.
- **Status:** Accepted working objective; selected by Manager under Dheeraj's
  explicit delegation to formulate the detailed first FMCG question.
- **Decision:** Investigate reported materials/packaging/logistics-cost margin
  pressure, compare relevant earlier own-company and cross-company episodes,
  inspect documented responses/reasoning and subsequent observations, and expose
  differences. Pricing conditions and volume are supported comparison dimensions,
  not assumed facts. The first demo should let a reader explain one supported
  comparison, its response and a material transfer limitation.
- **Original next action — startup superseded by D014:** Records reconciles
  M001 scope/criteria and review ownership;
  formal readiness remains its responsibility. Manager assigns M001-T01 after
  readiness: draft the annotation guide only, with hypothetical examples and
  unresolved policies visible. No automatic T02 acquisition or model/UI work.
- **Consequence:** Removes the need for Dheeraj to formulate the first scenario
  from scratch. The question is a working scenario, not a real case or benchmark
  label. Retrospective product learning is a proposed initial mode; the evaluation
  date policy remains to be agreed before T05.
- **Supporting handoff:** [Manager direction](docs/workflow/manager-direction-handoff.md).

### D014 — Reconcile current records and execute the annotation-guide task

- **Recorded:** 9 October 2026, after the repository assessment.
- **Status:** Accepted; explicit user authorization to repair inconsistencies,
  fix the initial handoff and use judgement to advance the annotation rules.
- **Basis:** Dheeraj requested these corrections after receiving the current
  M001 scope, readiness issue and T01/T02 sequence. This is delegated authority
  to perform the current repair and guide work, not a claim that he personally
  reviewed every criterion or accepted a completed module.
- **Decision:** Adopt the reconciled M001 scope and AC01–AC08 as the working
  contract for this assignment. Authorize this thread to perform the necessary
  Records maintenance and M001-T01 drafting sequentially. Record readiness and
  then In Progress when T01 starts; do not ask again for permission already
  supplied by this instruction. Supersedes D011's pending-package gate and
  D013's conditional T01 startup; D013's investigation objective is unchanged.
- **Deliverable:** `data/annotation_guide.md` v0.1 plus a completeness check and
  concrete handoff. The guide operationalizes accepted evidence requirements
  with hypothetical examples; new boundary/minimum-evidence proposals remain
  subject to Domain/Dheeraj review and revision with a real example.
- **Boundaries at issuance — later T02 assignment recorded in D015:** T01 drafting is not human domain acceptance, a frozen curation
  policy, completion of AC01, or completion of M001. T02–T08 remain unstarted;
  source acquisition still needs the T01 checkpoint and a scoped assignment.
  No model, ranking threshold, date mode, infrastructure or later module is
  selected here. No new agent or independent review is implied by role coverage.
- **Reason and consequence:** The old handoff repeatedly returned an already
  explained first task to a permission gate. Use the user's current instruction
  to produce its reviewable artifact, preserve evidence controls, and make the
  next handoff concern the actual guide rather than restart project setup.
- **Evidence:** [T01 checkpoint](docs/workflow/M001-T01-handoff.md),
  [annotation guide](data/annotation_guide.md) and [status](STATUS.md).

### D015 — Authorize the bounded real-example trial after the guide checkpoint

- **Recorded:** 9 October 2026, during Records reconciliation of T02.
- **Status:** Accepted; imported explicit Dheeraj assignment documented in
  [the T02 handoff](docs/workflow/M001-T02-handoff.md) and `STATUS.md`.
  This records existing authority, not a new Records authorization.
- **Basis:** Domain's [v0.1 guide recommendation](docs/domain/M001-T01-guide-review.md)
  proposed a bounded trial with DOM-T01-01/02 clarifications. Dheeraj then
  authorized use of the reviewed guide for one real example, applying necessary
  clarifications and executing M001-T02; stop before T03.
- **Decision:** Use guide v0.2 for this one-example trial. The first example
  requires source-supported input-cost pressure, margin effect/headwind and
  linkage in compatible scope/period; qualified management attribution and
  qualitative evidence suffice. Co-occurrence alone remains a partial lead.
  Separate action-statement publication from announcement/implementation event
  dates. These are trial instructions, not a universal corpus-admission rule.
- **Delivery evidence:** Guide v0.2 contains author-applied DOM-T01-01/02
  resolutions. The source manifest, `EP-CL-APAC-2022Q4-001` and walkthrough
  provide one Colgate Asia Pacific Q4 2022 draft with author checks. Artifact
  hashes are in the T02 handoff and match the checkout inspected by Records.
- **Limits and consequences:** Assignment and authoring/check delivery are
  established; Domain/Dheeraj meaning review remains pending. No human-reviewed
  case, final guide freeze, definitive episode boundaries, response-effect
  finding, query eligibility or module acceptance follows. Nested trial JSONL,
  excerpt/context locators and metric rounding rules are reversible working
  clarifications, not accepted final architecture. Operative source terms were
  unavailable; full-source retention and public redistribution remain unverified.
  M001 stays In Progress. Domain/Dheeraj is next, Records records disposition,
  Implementation handles returned corrections, and Manager assigns later work.
  T03–T08 are unstarted; startup approval is not repeated.

## Superseded proposal and unresolved choices

### D011 — Pilot task contracts and cross-module handoffs

- **Recorded:** 9 October 2026.
- **Status:** Superseded by D014 for the M001 working contract and T01 startup.
  The proposal and earlier reconciliation below are preserved as history;
  M002–M008 remain a proposed roadmap.
- **Basis:** Current Records assignment, D003–D006/D009/D010, brief sections
  8/11/12/14 and the checkout inspected at base `3a6db3a` with local changes.
- **Proposal:** Retain M001–M008. Specify M001-T01–T08 from episode definition
  and one real example through source coverage, ten cases, five queries with
  pre-ranking judgements, paired BM25/dense runs, errors/effort and recommendation.
  Include minimal reproducibility and eligibility in M001; promote useful assets
  into M002/M003. Keep structural experiments in M004 and custom AI conditional
  in M005; M005 does not automatically gate backend/workspace delivery.
- **Rationale and consequences:** A baseline pilot needs evidence/date controls
  before its results can be interpreted. Separate later production/research
  outcomes without recreating pilot work. The draft identifies decisions at
  their needed checkpoints and selects no missing-date policy, split, model,
  reviewer, companies/windows or architecture. The existing milestone target
  remains D004; its presence does not approve this module's detailed criteria.
- **Reviewable proposal:** [M001 specification](docs/modules/M001-data-viability-pilot.md)
  and [module boundary review](docs/module-map.md).
- **Original acceptance request — superseded by D014:** Dheeraj agrees
  scope/criteria and the first task's
  working investigation objective; Records then records readiness. Preserve this
  proposal's reasoning if it is revised or superseded.

**Historical reconciliation after D012/D013, before D014:** The working objective, product
priority, linked continuing updates, gap-triggered identity review and initial
independent code-review remit are now accepted direction. They no longer require
selection under this proposal. Records has revised M001 accordingly: Implementation
owns the required data/provenance/date/method checks, Domain/Dheeraj owns meaning,
and independent Review starts at code checkpoints. The acceptance package now
explicitly includes explaining one supported comparison and a transfer limit,
with product feedback separate from ranking metrics. D011 remains Proposed for
the detailed scope/acceptance package; no agreement to that package is recorded
by D012/D013. The only readiness agreement still needed is the reconciled package
and T01's concrete guide-only completion checks. Later operational policies do not
block T01 drafting. Records has not marked Ready or executed a pilot task.

## Current unresolved choices

The following choices remain unselected or unvalidated. D014/D015 authorize
guide work and the one-example trial, not later experimental policy selection.

| Choice | Current proposal or uncertainty | Evidence needed to resolve it |
| --- | --- | --- |
| Seed firms and historical windows | Colgate Asia Pacific Q4 2022 supplied one draft example; multi-firm/window selection is unstarted; Kimberly-Clark and Procter & Gamble remain leads | T03 source coverage, diversity and sampling evidence |
| Record schema and missing values | Guide v0.2 and nested `m001-t02-trial-0.1` worksheet tested on one real draft; final schema, curation freeze and ranking treatment remain open | Domain/Dheeraj review of the real example/revision and subsequent schema findings |
| Source retention and public reuse | Official release was accessible; operative terms notice unavailable; no full-source archive or general redistribution clearance | Working operative notice or another supported permission basis before broader retention/reuse |
| Storage, graph tools and backend | SQLite, NetworkX and Flask are suggested defaults | Actual workload and implementation requirements |
| Semantic model and structural weights | No checkpoint, licence or weights selected | Baseline quality, model terms, local benchmarks and development data |
| Judgements and evaluation split | Brief's 0–3 rubric; separation needs definition | Query/candidate inventory, shock families and reviewer availability |
| NLP learning experiment | Statement detection, extraction, query interpretation and reranking are candidates; no first task selected | Label definitions, baseline errors, sufficient data and held-out documents |
| Schedule, compute and budget | Brief's 80–120 hours is an estimate | Available hours, measured pilot effort and verified hardware capacity |
| UI and deployment | No framework or hosting route selected | Analytical core results and a bounded analyst workflow |
| Later custom AI task and tooling | User ambition recorded in D010; `jev` unspecified | Exact tool/method identity, measured baseline gap, labels and evaluation |

When resolving one of these, append an accepted decision with its evidence,
alternatives considered and consequences. Update the relevant module and status
record; change the brief when the project direction itself changes.

Detailed concerns and Dheeraj's responses, with remaining operational questions, are preserved in
[Open questions](docs/research/open-questions.md). Research precedents are
maintained in [Literature map](docs/research/literature-map.md); their inclusion
does not constitute replication or acceptance of a model architecture.
