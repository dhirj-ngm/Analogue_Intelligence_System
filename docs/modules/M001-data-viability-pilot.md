# M001 — Data viability pilot

**Updated:** 9 October 2026, Asia/Kolkata  
**Lifecycle:** In Progress  
**Execution:** T01 revised to guide v0.2; T02 artifact/check delivery complete, Domain/Dheeraj meaning review pending; T03–T08 not started  
**Coordinator:** AIS — Manager  
**Specification/status owner:** AIS — Records  
**Domain and module acceptance:** Dheeraj

## Authority and starting state

Read [PROJECT_TRACK.md](../../PROJECT_TRACK.md) for workflow and
[STATUS.md](../../STATUS.md) for verified progress. Direction comes from
[PROJECT_BRIEF.md](../../PROJECT_BRIEF.md), especially sections 8, 11, 12 and 14.
The [Manager direction handoff](../workflow/manager-direction-handoff.md) and
D012/D013 establish the current working objective and responsibilities. D014
adopts this M001 working contract under the user's delegated repair/guide
assignment; D015 records the later explicit one-example T02 trial assignment.
Later modules in the [module map](../module-map.md) remain proposals.
The [open questions](../research/open-questions.md) now distinguish Dheeraj's
recorded answers from remaining operational choices; they are not a questionnaire
to reopen before T01. A field or example below does not select a missing policy.

Relevant accepted decision references in [DECISIONS.md](../../DECISIONS.md):

| IDs | Requirement carried into this contract |
| --- | --- |
| D001, D008 | FMCG input cost investigation; readable cases for analysts, researchers and students |
| D002 | Curated cross-company and own-company public history |
| D003 | Evidence, two clocks, attribution, explicit unknowns and follow-up separation |
| D004 | Ten reviewed episodes, five queries, BM25/dense comparison and scope recommendation |
| D005 | Relevance and eligibility before results/tuning; retain negative findings |
| D006, D009 | File-based handoffs, Records transitions, human acceptance; plans are not execution |
| D010 | Later custom AI ambition; no selected task or architecture |
| D012 | Product usefulness first; continuing episode updates, historical unknowns and independent code-review remit |
| D013 | Delegated FMCG input-cost/margin investigation |
| D014 | Authorized record reconciliation and T01 execution; no repeated startup approval or automatic T02 acquisition |
| D015 | Explicit one-example T02 trial and applied guide clarifications; no human acceptance or T03 assignment |

D011 preserves the original proposal and is superseded by D014 for M001 startup.
Readiness and task start were recorded under D014; D015 then authorized the
bounded real-example trial. M001 remains In Progress. Neither authority asserts
that Dheeraj personally reviewed every criterion, accepted the real case's meaning
or approved final curation policy. The next checkpoint is Domain/Dheeraj review
of the real T02 case and revised guide; startup approval is not reopened.

The checkout remains on `main` at base `3a6db3a` with local changes. The
[annotation guide v0.2](../../data/annotation_guide.md), historical
[T01 checkpoint](../workflow/M001-T01-handoff.md) and current
[T02 checkpoint](../workflow/M001-T02-handoff.md) exist. One source manifest
record and one assistant-curated real episode were delivered; **created real
drafts: 1; human-reviewed episodes: 0/10; benchmark queries: 0/5**. T02's question
sketch is not an evaluation query. No retrieval runtime/results or human case
acceptance exist. T02 records actual access and unresolved operative terms; this
Records reconciliation did not refetch sources. The Domain [analogue notes](../domain/analogue-definition.md)
remain supporting discussion, not a separately authoritative annotation policy.

## Verified checkpoint and remaining acceptance

| Task / criterion | Actual evidence | Remaining disposition |
| --- | --- | --- |
| M001-T01 | v0.1 delivered under D014; Domain recommended a bounded trial with two Required clarifications; v0.2 applies both under D015 | Domain/Dheeraj assess revised meaning; freeze a reviewed curation version before T04 |
| M001-T02 | One real case `EP-CL-APAC-2022Q4-001`, one source, five spans/claims, two metrics and fourteen unknowns; authoring/checkpoint delivery complete | Domain/Dheeraj meaning/usability review; author-applied findings have not been human-accepted |
| M001-T03–T08 | Not started | Manager assigns later work after this checkpoint; no automatic T03 expansion |
| M001-AC01 | Guide and real-example check artifacts exist; local identities/references/version checks pass | Real-case/guide Domain disposition and required corrections remain; AC01 is not marked passed |
| M001-AC02 | One release accessible; operative terms unavailable; locators/hashes with no retained full-source archive | T03 coverage and source retention/reuse validation remain |
| M001-AC03–AC08 | No human-reviewed corpus, frozen evaluation, baseline runs or pilot recommendation | Full module criteria remain unmet; no In Review/Done transition |

Guide version history: v0.1's original review/hash remain in the T01 handoff and
Domain note. v0.2 applies DOM-T01-01 in §9 (compatible-scope/period cost–margin
support for the first example) and DOM-T01-02 in H1 (statement versus action
dates). It also records mixed-paragraph challenge/display lineage, excerpt/context
locators and current-page version limits, reversible trial JSONL, metric basis/
rounding and reported response effects versus unknown interventions. These
working clarifications do not select final schema, ranking text or date mode.

Records verified all four T02 handoff artifact hashes against the checkout and
locally checked counts, references, guide version, publication/reporting ordering,
unknowns and pending human-review state. Source-context matching and HTTP outcomes
remain Implementation-reported checks; inspection bodies were discarded, and no
independent live-source verification or business-meaning acceptance is claimed.
The measured 286-second assistant working envelope is not human curation time.

The brief itself now carries the reconciled rules: ten cases/five queries are
the accepted target; T05 freezes judgements before T06 rankings; and statement
detection is a candidate for later custom AI, not an adopted first learning task.

## Objective and analyst value

The first investigation is FMCG input-cost-driven margin pressure: find earlier
own-company and cross-company challenges involving reported materials, packaging
or logistics costs; inspect documented responses and reasoning; show later
observations; and explain relevant differences and evidence gaps. Pricing
flexibility and demand/volume are comparison dimensions when supported, not
assumptions or mandatory query filters. This is the accepted D013 scenario,
not a verified company case or a recommendation to copy an action.

Product usefulness comes first. A reader should be able to explain one supported
comparison, its documented response and reasoning where available, and a material
reason it may not transfer. Preserve evidence and reader feedback separately
from retrieval metrics. The pilot establishes this foundation through readable
cases and fixed queries; a chatbot or conversational interface is not required.

Determine whether public disclosures support that investigation with ten distinct
reviewed episodes and five queries. Compare BM25 and dense retrieval on the same
eligible cases without making structural superiority a delivery requirement.

The outcome is a feasibility assessment and a continue/narrow/revise
recommendation. Ten episodes and five queries cannot establish general retrieval
superiority, strategic effectiveness or the value of a future structural model.

## Working scope and non-goals

Scope: define an episode and a small annotation contract; validate one complete
real source-to-case example; check source access and historical coverage; curate
ten distinct reviewed episodes across multiple firms and at least two periods;
prepare five investigation queries, eligible candidates and relevance judgements;
run both text baselines; inspect errors, missingness, diversity and curation effort.
Seek distinct shock contexts and supported contrasting cases, rather than count
different companies in one shock as independent experiments. Record unsuccessful,
mixed or unresolved developments where supported; do not select only recoveries.

Manual annotation and small local utilities are sufficient. M001 includes enough
validation and reproducibility to inspect the pilot, not a production pipeline.
No database, graph library, framework, checkpoint, source provider or feature
weight is selected by this draft. Candidate seed firms remain Colgate-Palmolive,
Kimberly-Clark and Procter & Gamble; T03 may recommend alternatives with evidence.

Non-goals: automated collection at scale, full relation extraction, graph/hybrid
scoring or fusion experiments, fine tuning, custom AI, live internet search,
chatbot, backend/UI/deployment, forecasting, strategy recommendations and causal-effect
identification. M001 does not require every response, rationale or follow-up
metric to be observable; unsupported fields must remain explicitly unknown.

## Dependencies and interfaces

There is no predecessor implementation module. Execution requires an assigned
task and only the policy decisions needed at its checkpoint. D014 supplies
authority for the working contract and T01; D013 supplies the objective, so
neither startup decision is reopened. D015 supplies the completed T02 trial's
authority. Domain's existing analogue-definition and
mechanism notes provide discussion examples; they do not automatically fix
annotation or ranking policy.

| Interface | Input | Output/consumer |
| --- | --- | --- |
| Source to evidence | Permitted public documents, metadata and publication/reporting dates | Source manifest and locatable passages for annotation/review |
| Evidence to case | Reviewed claims, dates, company/period identity and unknowns | Episode records and readable case walkthrough; M002 schema findings |
| Case to ranking | Versioned, admissible challenge/context text with field lineage | Identical candidate IDs and declared text inputs for BM25/dense; M003 pilot assets |
| Query to judgement | Investigation objective, evidence/cutoff, exclusions and reviewed rubric | Candidate eligibility, grades, rationales and disagreements before rankings |
| Runs to recommendation | Rankings/configurations, errors, effort and limitations | Report for Manager/Dheeraj; proposed M002/M003 scope or revised direction |

Paths below are deliverable locations, not a fixed storage schema. The guide,
`data/source_manifest.jsonl`, `data/episodes.jsonl` and walkthrough exist. Later
task paths remain planned artifacts. T02 used nested records in the reversible
`m001-t02-trial-0.1` worksheet; this does not fix the M002 schema. Reuse T02's case
in T04 only if it qualifies after review; do not maintain competing canonical
copies. Keep machine-readable identities and references stable when promoting
pilot artifacts into M002/M003. Create directories only when useful artifacts exist.

## Draft episode and evidence contract

T01 must make these concepts operational with examples and boundary reasoning.
An episode is a bounded company situation supported by one or more documents;
passages and reporting updates are evidence, not automatically new episodes.
Under D012, four quarterly disclosures updating one continuing challenge form
one episode with four linked updates. Preserve each update's document, dates,
claims, actions and contradictions. A changed action alone does not establish
a new challenge.

Time gaps trigger identity review, not automatic splitting or assumed resolution.
Inspect company/business scope, pressure, affected metrics, evidence of continuity
or resolution, and a distinct recurrence/shock. A gap may mean missing coverage.
Retain a relationship and written reason for any split/merge; ambiguous continuity
gets a review-needed note. No numeric gap threshold is selected. Different
companies can have distinct episodes sharing a shock family and dependence.

| Record/view | Information to preserve; exact representation remains open |
| --- | --- |
| Identity | Stable episode/company IDs, company aliases, sector/category/geography, start/end or uncertain interval, shock-family and duplicate/update relationships |
| Source | Stable document ID, issuer/type/URL, publication date with basis, reporting period, retrieval time, content hash/version and access/retention notes |
| Evidence | Stable span ID, document reference, exact passage and section/page/offset or another reproducible locator; every material claim links to support |
| Challenge/context | Supported pressures, reported effects, small mechanism vocabulary, constraints, contrary evidence and explicit missing context |
| Claim/event/relation | Type, subject/relation/object where relevant, event interval, public-information date, evidence, attribution and review state |
| Response/rationale | Announced versus implemented action, dates/constraints, management's stated reasoning with support; separate labelled interpretation |
| Follow-up | Later developments and dated observations, with source/metric definitions and other reported drivers; no inferred proof of recovery or causation |
| Metric | Name/value/unit, period, group/segment scope, GAAP/adjusted or other accounting basis, publication/vintage and evidence; incompatible values remain distinct |
| Review | Annotator/reviewer identity or role, date, version, findings/resolution and unresolved disagreement; extraction status differs from domain acceptance |

A complete example means every section is supported or explicitly marked
unknown with an explanation of what was checked. It does not mean inventing
an implemented action, rationale, metric or favourable outcome. Initial vocabulary
from the brief: cost increase, logistics disruption, demand/volume change, margin
change, pricing and productivity actions. Additional labels need source evidence
and a documented contract change.

## Evidence, date and evaluation constraints

These carry accepted requirements; unresolved operational choices are listed later.

- Use traceable public sources. Recheck provider access and reuse/retention terms
  when source work begins, including T02's real example. Earlier brief references
  are leads, not current access validation. Retain originals only where permitted;
  document evidence reproducibility and any retention/redistribution limitation.
- Keep event time, reporting period, publication time and retrieval time separate.
  A year-end report published later is not evidence available at year-end. Preserve
  original/restated vintages and date uncertainty rather than backdating revisions.
- Declare retrospective versus as-of investigation and cutoff semantics before
  query construction. Apply the declared rules to query evidence, candidate
  evidence and every ranking feature. Unknown/conflicting dates need an agreed
  policy before eligibility runs; this draft selects none. Define what counts
  as an earlier episode, including overlapping/continuing periods, rather than
  treating publication by a cutoff as sufficient historical ordering by itself.
- Exclude the query episode and near duplicates. Keep an eligibility ledger with
  included/excluded IDs and reasons for each query. Same-company earlier history
  is allowed; shared company, period and shock are dependencies to report, not
  automatically independent evidence or silently forbidden candidates.
- Keep later response/outcome content out of the first similarity representation,
  including summaries, tags and derived features. Display dated follow-up
  separately. T05 defines permitted fields and checks lineage to source passages;
  it must settle how any contemporaneous response text is treated before T06.
- Distinguish observation, management attribution, forecast/intention, implemented
  action and analyst hypothesis. Missing evidence is not a documented mismatch.
  Missing pricing detail does not establish limited pricing power. Conversational
  clarification resolves the reader's situation/objective; only source/curation
  work can resolve historical evidence. It cannot fill an undocumented fact.
- Fix objective-specific relevance rules, labels, eligibility and evaluation use
  before rankings/tuning. The brief's 0–3 rubric is the starting proposal; T05 must
  operationalize it independently of model feature tags. Record reviewer
  availability, disagreements and any solo-review limitation.
- Both baselines receive the same frozen admissible candidate set and declared
  evidence information budget. T06 records text construction, tokenization,
  truncation/pooling/similarity and versions. Model choice does not supply extra
  unsupported facts or resolve pretrained-model hindsight limitations.
- At this size, inspecting all eligible candidates is practical. Do not promise
  five useful answers per query. Define handling of fewer than five candidates,
  no relevant cases and unjudged evidence before computing metrics. D012 requires
  “no sufficiently supported analogue found” when appropriate; show a nearest
  supported partial comparison only when defensible, labelled with its limits.
  No compulsory result when candidates are inadmissible or unrelated. Numeric
  thresholds/relevance cutoffs remain to be specified; no UI is added here.

## Stable task sequence and completion evidence

Use IDs `M001-T01` through `M001-T08` in assignments, progress and reviews.
T01 is revised to trial v0.2. T02's authoring and check handoff are delivered,
with Domain/Dheeraj review pending; T03–T08 are **Not started**.
The layers are data/domain (T01–T05), core retrieval (T06), and
verification/decision reporting (T07–T08). Every task
includes verification; no application interface layer is required in M001.

### M001-T01 — Define the episode and annotation contract

**Current checkpoint:** [Guide v0.2](../../data/annotation_guide.md) applies
DOM-T01-01/02 following the [v0.1 Domain recommendation](../domain/M001-T01-guide-review.md)
and authorized T02 trial. The [T01 handoff](../workflow/M001-T01-handoff.md)
preserves original completeness checks/hash; [T02](../workflow/M001-T02-handoff.md)
records the revised target. Resolutions are author-applied; real-example/revision
meaning review and the curation freeze remain pending.

- **Inputs/dependency:** D003/D012/D013, brief section 8, this reconciled task and
  existing Domain notes. Startup authority and readiness are recorded under D014;
  the objective is already supplied. Firm/model/split decisions are unnecessary.
- **Work/write scope:** Draft `data/annotation_guide.md` defining episode identity,
  update/split/merge rules, minimum evidence and unknowns, claim categories, IDs,
  dates/metrics and review states. Use clearly hypothetical boundary examples and
  the D013 question-purpose sketch; no real case claim or source download.
- **Artifact:** Versioned annotation contract with positive/boundary examples,
  unresolved policies and the proposed T02 example requirements.
- **Completion evidence:** Implementation records a completeness check covering
  IDs/linked updates, source/span support, event/publication/reporting dates,
  attribution, action/rationale/follow-up separation, metric definitions and
  explicit unknowns. Include three clearly hypothetical worked checks: four
  continuing quarterly reports share one episode ID; a reporting gap prompts
  review without an invented end/split; clarifying a user's question leaves a
  missing historical claim unknown. Record split/merge reasons, shared-shock
  dependence and undecided policies; select no numeric gap or ranking threshold.
- **Checkpoint/handoff:** Implementation sends the guide and check results to
  Domain/Dheeraj for meaning and boundary review, and Records for decision/status
  reconciliation. There is no independent Review checkpoint for this guide-only
  task. No automatic move to T02; Manager must assign it after the required
  contract/example prerequisites. Revise from the real example when authorized;
  freeze the curation version before T04.

### M001-T02 — Validate one complete source-to-case example

**Current checkpoint:** [T02 handoff](../workflow/M001-T02-handoff.md) delivered
under D015 with [source manifest](../../data/source_manifest.jsonl),
[episode record](../../data/episodes.jsonl) and
[walkthrough](../../data/pilot/example-walkthrough.md). Author checks pass;
Domain/Dheeraj case review is pending. The draft is Colgate Asia Pacific Q4 2022,
published 27 January 2023; actual episode onset/end remain unknown. No later
realized observation or retrieved analogue comparison has been demonstrated.

- **Inputs/dependency:** Reviewed T01 contract and agreed example inclusion rules.
  The Domain recommendation, explicit user assignment and author-applied required
  clarifications supplied this trial's authority; startup is not repeated.
  Access/terms were checked: release HTTP 200, terms wrapper HTTP 200, operative
  notice HTTP 404; full-source archival/public redistribution clearance remains
  unresolved. No full-source archive is retained. Candidate leads in the brief
  do not constitute an approved multi-firm sampling plan.
- **Work/write scope:** Populate `data/source_manifest.jsonl` and
  `data/episodes.jsonl` with one real example; write
  `data/pilot/example-walkthrough.md` mapping source passages to case sections,
  dates and allowed ranking versus follow-up content. Cache only permitted sources.
- **Artifact:** One supported case and its evidence, a proposed investigation
  question/comparison sketch, schema/annotation issues and recorded effort.
- **Completion evidence:** Material claims open at source locators; publication
  and reporting dates differ where appropriate; missing rationale/action/follow-up
  stays unknown; metric definitions and attribution survive the walkthrough.
  No second real analogue is required and the sketch is not yet a benchmark query.
- **Checkpoint/handoff:** Implementation records source/span, publication/reporting
  date, unknown and metric checks; Domain/Dheeraj review meaning and case usability.
  Return necessary contract changes to Records/T01 before
  T03/T04. One example does not establish viability or count as ten cases.

### M001-T03 — Validate candidate firms and historical windows

- **Inputs/dependency:** T02 evidence/schema findings and candidate firms/windows
  from the brief; available effort for a bounded source inventory.
- **Work/write scope:** Extend the source manifest; write
  `data/pilot/source-coverage.md` with actual access outcomes/date, access terms,
  usable evidence, gaps, firm/period/shock inventory and inclusion/rejection reasons.
- **Artifact:** Source-access and coverage record; proposed sampling plan for ten
  episodes across multiple firms and at least two periods, including contrasts.
- **Completion evidence:** Tested sources distinguished from leads; verified
  links/locators and date availability; inventory distinguishes reporting periods
  from independent shocks. Selection bias, inaccessible sources and expected
  curation effort are explicit. Do not fabricate diversity to meet the target.
- **Checkpoint/handoff:** Implementation records access/terms/coverage checks;
  Domain/Dheeraj assess evidence suitability. Manager/Dheeraj agree firms/windows and material sampling
  changes for T04. If coverage looks inadequate, record an early narrowing proposal
  rather than silently replacing the domain or launching broad acquisition.

### M001-T04 — Curate and review the ten pilot episodes

- **Inputs/dependency:** Reviewed example, curation contract and T03 sampling plan;
  agreed review responsibilities and evidence sufficiency rules.
- **Work/write scope:** Extend `data/episodes.jsonl` and source manifest; update
  annotation guidance and `data/pilot/curation-log.md`. Retain/replace the T02 case
  with an explained decision. Produce readable case sections within records.
- **Artifact:** Ten distinct reviewed cases, evidence, identity/duplicate/shock
  inventory, field missingness and effort/review log.
- **Completion evidence:** Ten unique episode identities, multiple firms and at
  least two periods; all material claims traceable; updates do not inflate counts;
  review findings resolved or visible. Supported contrasting mechanisms and
  important differences are identified for T05. No recovery-only requirement.
- **Checkpoint/handoff:** Implementation audits all ten at this scale for provenance,
  dates, record consistency and required fields, recording record-level results;
  Domain/Dheeraj accept meaning.
  If only fewer than ten defensible cases exist, report shortfall and proposed
  revision; do not pass the target by padding or quietly lower acceptance.

### M001-T05 — Define five queries, eligibility and frozen judgements

- **Inputs/dependency:** Reviewed T04 corpus; decisions on objective, date mode,
  unknown dates, duplicates, rubric and reviewer availability (Q01–Q07).
- **Work/write scope:** Create `evaluation/pilot/protocol.md`, `queries.jsonl`,
  `eligibility.jsonl`, `judgements.jsonl` and `freeze-manifest.json` under
  `evaluation/pilot/`. Corpus references and text/feature allowlist live in the
  protocol; the freeze manifest identifies exact artifact hashes/versions.
- **Artifact:** Five distinct investigation queries with objectives, admissible
  evidence/cutoffs, source episode IDs if any, all eligible/excluded candidates
  and reasons; pre-ranking grades, rationales/differences and review limitations.
- **Completion evidence:** Query evidence passes date checks; self/duplicates are
  excluded; own-company and cross-company eligibility are demonstrable or their
  coverage gaps explicit. Judge every eligible query/candidate pair at this scale.
  Useful/weak/misleading comparisons and insufficient-evidence situations are
  covered where evidence supports them; no fabricated positive or negative labels.
  Five paraphrases of one case do not count as five independent investigations.
- **Checkpoint/handoff:** Domain/Dheeraj agree rubric examples and judgement-process
  limits; Implementation records leakage, evidence-lineage and eligibility checks
  before rankings. Independent benchmark judgement availability remains a separate
  issue from code Review and reader feedback. Freeze labels,
  candidate sets, ranking text policy, metric conventions and any split/development
  use before T06. If five-query held-out separation is impractical, explicitly agree
  a descriptive pilot without tuning or held-out claims; this is not a chosen default.

### M001-T06 — Run BM25 and dense retrieval baselines

- **Inputs/dependency:** T05 frozen artifacts; checkpoint/licence/dependency and
  hardware feasibility choices recorded before runs. No structural model required.
- **Work/write scope:** Minimal retrieval/validation utilities in `src/` or
  `scripts/` as appropriate, meaningful tests in `tests/`, `configs/pilot/` and
  a documented conventional command surface in `README.md` when runtime is added.
  Save rankings and run manifests in `evaluation/pilot/baselines/`.
- **Artifact:** Paired rankings for all five queries, scores and candidate IDs,
  metrics/per-query counts, exact inputs/configuration/model revision and runtime.
  Record source revision/local-change state, corpus/protocol hashes and required
  generated caches without committing caches or environments.
- **Completion evidence:** Both methods rank identical eligible candidates from
  the declared information budget; rerun instructions reproduce rankings under
  documented numeric/tie tolerances; cutoff, self/duplicate exclusion, follow-up
  leakage and malformed-record checks pass. Record nDCG@5 and precision@5 per brief,
  using T05's agreed gain/relevance/denominator/zero-relevance conventions and
  limitations. No minimum improvement over either baseline is required.
- **Checkpoint/handoff:** Implementation records data/date/provenance checks,
  frozen input lineage and paired-ranking audits. Independent Review checks code
  correctness against the specified behavior, including date/eligibility code and
  meaningful tests, at this or an earlier code checkpoint. Code Review does not
  establish historical truth or benchmark relevance. Fix failed checks in Implementation;
  return scope/model infeasibility to Manager. Labels remain frozen.

### M001-T07 — Analyze errors, coverage and effort

- **Inputs/dependency:** T06 paired results and T02–T05 curation/review logs.
- **Work/write scope:** Write `evaluation/pilot/error-analysis.md` with per-query
  cases and references to actual records/ranks. Summarize time per usable episode,
  source failures, missingness, disagreements and firm/period/shock dependence.
  Record reader/Domain feedback on explaining supported comparisons and transfer
  limits separately from ranking metrics; identify actual participant/checker and
  any absence of reader feedback rather than inventing a usability result.
- **Artifact:** Error taxonomy and evidence-backed analysis of useful matches,
  superficial matches, documented mismatch versus unknowns, and corpus gaps.
- **Completion evidence:** Every conclusion cites a query/candidate or measured
  log; data/label issues distinguished from retrieval failures; wins and losses of
  both methods retained. Report effort sample sizes, estimates versus measurements,
  and reviewer/model limitations. No claim of structural improvement is possible.
- **Checkpoint/handoff:** Implementation verifies result/record references and
  measured logs; Domain/Dheeraj assess comparison meaning and product feedback.
  Label corrections require an explained new benchmark version
  and affected reruns, preserving the original results; no outcome-driven relabelling.

### M001-T08 — Recommend continue, narrow or revise

- **Inputs/dependency:** T07 findings, review resolutions, available hours and
  Dheeraj's constraints; unresolved limitations remain part of the recommendation.
- **Work/write scope:** Write `evaluation/pilot/pilot-report.md`. Implementation
  supplies evidence/next-task proposal; Records updates status and decision records
  after review and acceptance, without Implementation changing lifecycle state.
- **Artifact:** A bounded recommendation mapping each acceptance criterion to
  evidence, coverage/effort and risks; explicit proposed M002/M003 or revised scope.
- **Completion evidence:** Continue rests on traceable useful comparisons and
  meaningful nonmatches with feasible curation effort. Narrow explains why a
  comparison of reported margin drivers/responses is defensible if independent
  analogues are scarce. Revise identifies the contract/source/query changes and
  their revalidation needs. No numeric viability threshold is invented here.
- **Checkpoint/handoff:** Implementation supplies the data/method check record;
  Domain/Dheeraj review meaning, recommendation and product usefulness. Independent
  Review supplies Blocking/Required/Suggested findings for code checkpoints;
  Dheeraj accepts the module outcome. Records
  records the accepted choice by decision ID and only then marks M001 Done if
  all agreed criteria pass. A shortfall report is useful evidence, not automatic
  completion under the original ten-case/five-query criteria.

## Working acceptance criteria and required checks

D014 adopts this scope/acceptance package as the working contract under the
user's delegated repair and guide assignment. T01 execution is authorized.
Detailed later-task policies are settled at their checkpoints; the guide's
domain review and final module acceptance remain separate from startup authority.
Do not reopen Q01–Q11 or request the same T01 permission again.

The package is: (1) episode guide and real example; (2) ten traceable reviewed
episodes across multiple firms/at least two periods, counting continuing updates
once; (3) five queries with pre-ranking judgements and fair reproducible BM25/dense
runs; (4) evidence that a reader can explain one supported comparison and a
transfer limitation, with reasoning where documented and feedback distinct from
ranking metrics; (5) error/effort/limitation analysis and an evidence-led scope
recommendation. Required provenance/date checks remain with Implementation,
meaning with Domain/Dheeraj, and independent code Review at code checkpoints.
There is no required baseline gain, structural result or chatbot.

The table retains stable criterion IDs and names observable evidence for that
package. Exact schemas, metric conventions, thresholds and review staffing remain
task-level proposals where not recorded as agreed. Task completion or AI review
alone does not establish domain/module acceptance.

| ID | Observable criterion | Required evidence/checkpoint |
| --- | --- | --- |
| M001-AC01 | Episode identity, evidence status and unknown/date/metric rules are usable | T01 guide and T02 source-to-case review; contract changes resolved |
| M001-AC02 | Selected sources and coverage are actually validated | T03 access/terms/inventory record; permitted retention and source locators |
| M001-AC03 | Ten distinct reviewed cases across multiple firms and at least two periods | T04 identity/count/provenance/metric checks and human domain review; shock/selection limits reported |
| M001-AC04 | Five distinct queries have defensible eligibility and pre-ranking judgements | T05 protocol, full pair coverage, exclusions, rationale/review records and freeze hashes |
| M001-AC05 | Both baselines run fairly and can be reproduced | T06 paired candidate/input audit, manifests, documented commands, rankings and agreed metrics |
| M001-AC06 | Evidence/date protections survive the baseline implementation | Checks for publication versus event time, revised/unknown dates per agreed policy, self/duplicates and forbidden follow-up leakage; compatible metric handling when used |
| M001-AC07 | Product usefulness and error/effort findings are inspectable | T07/T08 reader or Domain/Dheeraj walkthrough: one supported comparison, documented response/reasoning where available and material transfer limit; feedback separate from metrics, with record-level errors/logs and negative findings |
| M001-AC08 | Recommendation and handoff follow evidence and accepted review | T08 evidence matrix, resolved Blocking/Required findings, recorded disposition of Suggested findings, Dheeraj acceptance and updated records |

Implementation owns documented contract/record, evidence/provenance, source-access,
date, metric, eligibility, input-lineage and result checks throughout T01–T08.
Data-only checkpoints use inspection/check logs, not artificial code tests.
Domain/Dheeraj owns business meaning, identity ambiguity, response/rationale
interpretation and comparison usefulness. Benchmark judgements are separately
specified before T05 freeze; reader dialogue/code review cannot replace them.

When code appears, Implementation adds deterministic tests for the required
behavior and runs documented test/lint commands, isolating network dependencies.
Independent Review inspects code correctness at those checkpoints, including
validation/cutoff/eligibility implementations when present, and writes findings
in `docs/reviews/M001-review.md` with target task/version/branch/base/local state,
checks, severity and resolution evidence. It is not assigned a separate historical
data or domain audit by this initial remit. Fixes return to Implementation.
Only after module implementation/checks finish does Records transition In Review;
Done still requires Dheeraj's module acceptance and resolution of required findings.

## Decisions by need, not all at startup

The concern record remains authoritative for questions; this table schedules
their effect without resolving them. Accepted answers must receive a decision
ID, supporting note and affected contract/protocol version.

| Needed by | Decision/input | Owner and affected task |
| --- | --- | --- |
| Startup — resolved | D014 adopts the working contract and authorizes T01; D012/D013 supply direction | Readiness and In Progress recorded under the delegated repair assignment; no repeated approval |
| T01 → T02 trial — assigned and delivered | D015 records the explicit one-example trial and DOM-T01-01/02 clarifications in v0.2 | Assignment resolved; Domain recommendation is not human acceptance; no repeated startup approval |
| Current T02 Domain checkpoint | Real-case scope/period/linkage, concurrent drivers, response/rationale/date unknowns, uncertain boundaries and guide v0.2 usability | Domain/Dheeraj reviews; Records records disposition/version; Implementation handles corrections; Manager assigns later work |
| Before broader source retention/public reuse | Operative terms unavailable; local trial uses minimal excerpts/locators and hashes, no full archive | Implementation needs a working notice or supported permission basis for such reuse; no clearance inferred from HTTP 200 |
| T03/T04 | Firms/windows, bounded source effort, sampling diversity and case-review availability | Implementation supplies access evidence; Domain/Dheeraj and Manager agree; Q05/Q08/Q11 |
| Before T05 freeze | Operational date/cutoff/ordering, unknowns and duplicate rules; query-specific rubric and judgement process; partial/no-match handling without forced results; evaluation use/metrics; ranking text budget and contemporaneous-response treatment | Implementation supplies evidence/checks, Domain/Dheeraj agrees meaning/policy, Manager coordinates material choices; settled D012/D013 direction is not reopened |
| Before T06 | Model/licence/configuration, compute constraints and reproducibility tolerances, using T05's frozen text policy | Implementation proposes/checks, independent Review inspects code, Manager coordinates material choices; no structural weights |
| T08 | Viability judgement and feasible next scope from evidence/available hours | Manager/Dheeraj; Q08/Q09 |
| Later modules | Structural information controls, custom AI task, `jev`, architecture, UI/deployment and optional extra review tools | Separate proposals after measured need; Q04/Q10/Q11 |

No fixed schedule, ranking missing-value policy, automatic abstention threshold, split,
model or reviewer availability is assumed. A deferred answer blocks only work
that actually depends on it. If a material ambiguity prevents the next task,
bring that precise question and the supporting artifact to Manager; continue
independent authorized work within the task.

## Current handoff and later assignments

**Now — T02 to Domain/Dheeraj:** Review the exact four artifacts/hashes in the
[T02 handoff](../workflow/M001-T02-handoff.md), guide v0.2 and the original Domain
findings. Assess compatible divisional cost–margin support and issuer attribution,
concurrent contributors, pricing/savings observations versus unknown interventions/
dates/rationale, uncertain actual episode boundaries and usable explanation. The
single Q4 observation is not proof of episode onset/end or recovery. Record
concrete findings/recommendation and any actual Dheeraj meaning acceptance;
an assistant Domain recommendation alone does not create a human-reviewed case.

**Next owners:** Records records that disposition and guide/case version; returned
corrections go to Implementation. Manager assigns subsequent work after the
checkpoint. Stop before T03; no source expansion or old T01 startup replay. No
independent code-review target exists, and M001 remains In Progress.

**At each implementation checkpoint:** Name task ID, delivered paths and artifact
versions, changes/deviations, checks and results (including unrun checks), branch/
commit/local state, unresolved decisions and next responsible thread. Include
review scope so Review does not infer completion from a target description.

**After accepted pilot:** M002 receives source/annotation/schema findings and
retention constraints. M003 receives frozen queries, judgements, eligibility,
configs, baseline utilities/results and limitations. Promote/reuse useful assets;
M003 establishes a larger reproducible evaluation before M004 tuning. M005 is
conditional and does not gate backend/workspace work unless its output becomes
an explicitly accepted dependency. Manager assigns the next module from findings.
