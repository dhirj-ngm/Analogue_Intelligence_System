# Project track and working guidelines

**Project:** Historical Analogue Intelligence Engine  
**Established:** 8 October 2026, Asia/Kolkata

**Updated:** 9 October 2026, Asia/Kolkata

## Direction and records

Build an evidence-based investigation system for business and supply chain
intelligence, starting with FMCG input cost pressure and company responses.
Serve analysts, researchers and students seeking curated historical case studies
from situation descriptions, hints or comparison questions. Preserve documented
responses and stated rationales; label interpretations and later observations.
Use [PROJECT_BRIEF.md](PROJECT_BRIEF.md) as the project direction. The first
implementation milestone is ten reviewed episodes and five investigation
queries, with lexical and semantic retrieval comparisons.

| Record | Responsibility | Consult when |
| --- | --- | --- |
| `PROJECT_BRIEF.md` | Purpose, scope, domain, experiment and intended deliverables | Starting substantive work, questioning scope, or finishing a module |
| `PROJECT_TRACK.md` | Working protocol and repository conventions | Starting a thread or checking workflow |
| `STATUS.md` | Verified progress, blockers and next concrete task | Starting or handing off substantive work |
| `DECISIONS.md` | Dated choices, reasons and unresolved alternatives | A relevant design choice arises or changes |
| `docs/project-overview.md` | Product and research objectives, records, output flow and model ambition | Understanding or explaining the system |
| `docs/module-map.md` | M001 task map and proposed later modules | Preparing module specifications |
| `docs/research/literature-map.md` | Paper notes, sources and research positioning | Assessing a research idea or novelty claim |
| `docs/research/open-questions.md` | Unresolved concerns and alternatives | Preparing a discussion or decision |
| `docs/workflow/thread-start-prompts.md` | Ordered role prompts and startup gates | Opening a working thread |
| `docs/workflow/manager-direction-handoff.md` | User responses, delegated first investigation and current handoff | Reconciling M001 with the accepted product direction |
| `data/annotation_guide.md` | Draft episode/evidence rules and hypothetical examples | Annotating or reviewing the T01 contract |
| `docs/workflow/M001-T01-handoff.md` | Delivered guide, completeness checks and next review | Resuming the current checkpoint |
| `docs/modules/` | Module specifications, tasks and acceptance criteria | Planning, implementing or reviewing a module |
| `docs/reviews/` | Review findings and resolution evidence | Reviewing a module or checking its completion |
| `docs/domain/` | Domain explanations, assumptions and investigated hypotheses | Domain interpretation affects implementation |

The linked knowledge documents, M001 specification and annotation guide exist;
the guide still needs domain review. The review directory is created when an
independent code checkpoint exists. Thread history supplies context;
repository records preserve the shared project state. Read the relevant brief
sections when uncertain or when moving to the next module. Do not infer
implementation from a planned feature or a prior conversation.

## Thread responsibilities

| Thread | Owns | Expected handoff |
| --- | --- | --- |
| AIS — Manager (designated coordination conversation) | Overall coordination, cross-module reasoning and Dheeraj's doubts | A scoped assignment or accepted direction, recorded in project files |
| Project Control / Records | Module breakdown, dependencies, specifications and authoritative module status | A bounded module specification with acceptance criteria and unresolved questions |
| Implementation / Status | Code and tests for the agreed module; evidence of progress | Changed files, checks and results, deviations, remaining issues and next action |
| Reviewer | Independent inspection against the specification and applicable guidelines | Findings classified as Blocking, Required or Suggested, with locations and evidence |
| Domain Discussion | Theory, terminology, assumptions, mechanism interpretation and experiments | Supported conclusions, uncertainties and proposed decisions for project records |

Dheeraj owns the project aim, domain acceptance and module acceptance. Codex
should explain material technical choices, challenge unsupported assumptions,
and distinguish evidence from judgement. Use direct professional discussion.

Manager coordinates the working threads; Records maintains specifications and
routine module transitions. Opening a thread does not start a background agent
or synchronize conversations. Handoffs through files and explicit assignments
carry the agreed work. Do not require Dheeraj to resolve all deferred research
concerns during thread setup; draft around them and identify only those needed
for the next assigned task.

D012/D013 now record Dheeraj's product-first direction and Manager's delegated
first FMCG question. Use the Manager handoff rather than the earlier blanket
assumption that all Q01–Q11 await answers. Independent Review starts with code
correctness at code checkpoints; Implementation retains record/provenance/date
checks and Domain/Dheeraj retains business-meaning acceptance. Records must
assign these checks explicitly, not remove them when narrowing review scope.

D014 records Dheeraj's later authorization to repair the records/handoff and
execute T01. For this bounded repair, the current thread performs Records
maintenance and guide drafting sequentially. This does not create new agents,
replace the existing working conversations or constitute independent review.
Resume from the latest task handoff rather than replay old startup prompts.

Use one implementation thread per active module. The reviewer inspects code
and runs relevant checks; fixes return to implementation unless explicitly
assigned to the reviewer. Domain discussion produces proposals; accepted
conclusions enter the decision record and relevant specification.

Project Control owns module transitions in `STATUS.md`. Implementation may
update progress, checks and blockers for its assigned module. Reviewers record
findings and communicate a handoff. Avoid concurrent edits to shared records;
use one writer per checkout, or separate Git worktrees when concurrent work
is needed. Record the branch or commit being reviewed when available.

## Module lifecycle

Use `Proposed -> Ready -> In Progress -> In Review -> Done`. A blocked module
retains its current state and records the blocker, responsible party and
condition required to proceed.

A module specification should contain:

- Module ID, objective and analyst value.
- Scope, non-goals, dependencies and prerequisites.
- Inputs, outputs, interfaces and relevant evidence/date constraints.
- Tasks grouped by layer: data/domain, core logic, interfaces and verification,
  including only layers relevant to the module.
- Observable acceptance criteria, required checks and review targets.
- Open questions, approved decisions and the next handoff.

Mark a module `Ready` when the scope and acceptance criteria are agreed and
no unresolved question prevents implementation. Work through the agreed tasks
without seeking approval for every routine step. Escalate changes affecting
scope, domain meaning or architecture, with evidence and a proposed decision.

Mark it `In Review` when implementation and its required checks are complete.
Mark it `Done` when acceptance criteria pass, Blocking and Required findings
are resolved, project records are updated, and Dheeraj accepts the outcome.
Suggested findings may be deferred with an explanation. An AI code review
does not establish the scientific validity of a business interpretation.

## Domain and evaluation rules

Follow the brief's scope, provenance and evaluation requirements, especially
sections 5, 8, 10, 11, 12 and 14:

- Retrieve both cross-company and own-company historical episodes from a
  deliberate, versioned corpus.
- Preserve source links, evidence spans, publication dates, reporting periods
  and review status. Keep event time separate from public-information time.
- Distinguish disclosed observations, management attributions, forecasts,
  implemented actions and analyst hypotheses. Do not claim identified causal
  effects or invent missing evidence, records, metrics or results.
- Enforce query cutoffs on query evidence, candidates and ranking features.
  For the first experiment, exclude later response and outcome fields from
  similarity features; display them as labelled follow-up observations.
- Exclude the query episode and near duplicates from analogue candidates.
  Account for shared companies, periods and shock families in evaluation.
- Establish relevance rules before inspecting model results. Compare methods
  on the same admissible candidates, and freeze evaluation rules and splits
  before tuning. Record failures and data limitations.
- Preserve metric units, periods, scope and accounting basis. Keep unknowns
  explicit and avoid comparing incompatible measures.
- Recheck provider access rules and reuse terms when implementing acquisition.
  The brief's research references describe earlier checkpoints.

Use the smallest implementation that meets the current milestone. Treat
candidate firms, SQLite, NetworkX, Flask, model checkpoints and feature weights
as proposals until justified and recorded. Add fine tuning or more complex
infrastructure when data and measured needs support it.

The later task-specific AI component is a user ambition. Its role, architecture
and checkpoint require evidence and a separate decision after the baselines.
The tool/method described as `jev` is unspecified; do not infer its identity.

## Repository conventions

Place production code in `src/`, automated tests in `tests/`, static resources
in `assets/`, developer utilities in `scripts/`, and architecture documentation
in `docs/`. Mirror source paths in tests where practical. Use `DECISIONS.md`
as the central decision register; link detailed design notes in `docs/` when
needed rather than maintaining contradictory decision logs.

Following brief section 17, use `data/` for curated records and annotation
guidance, `evaluation/` for queries, judgements and protocols, and `configs/`
for reproducible settings. Keep the root limited to entry documents and
necessary project configuration. Create directories only when they contain
useful work.

When adding a runtime, document a small stable command surface in `README.md`:
`make setup`, `make test`, `make lint` and `make run`, or equivalent conventional
commands. These commands are not implemented at project setup.

Use the standard formatter and linter for the selected language with committed
configuration. Default to spaces, UTF-8 and a final newline. Use descriptive
names: `snake_case` for Python files and functions, `kebab-case` for new
documentation other than established root records, and conventional
`PascalCase` for types. Keep modules focused and avoid hidden global state.

Add meaningful tests with behavior changes and bug fixes. Keep unit tests
deterministic and isolate network, hardware, time and filesystem dependencies
with fakes or fixtures. Name tests after observable behavior. Test provenance,
cutoffs, candidate eligibility and metric handling when those paths are added.
Run the project's documented test and lint commands before a pull request.

Preserve existing work. Do not commit generated output, caches, virtual
environments, local configuration, credentials, device identifiers or private
datasets. Use ignored environment files and sanitized `.env.example` values.
Validate external inputs and document required permissions or hardware access.

Use concise imperative commit subjects and separate unrelated changes. Pull
requests should explain the problem and solution, verification, relevant issues
and configuration or compatibility impact. Include logs or screenshots when
behavior or interface output changes.

## Progress, decisions and handoffs

After a meaningful milestone, update the applicable progress fields in
`STATUS.md` with actual files, checks, results, blockers and the next task.
Keep previous important milestones in a short history; avoid copying the
entire brief into the status record.

Append material choices to `DECISIONS.md` with a stable ID, recorded date,
status, basis, rationale and consequences. Distinguish imported confirmed
direction from proposed defaults. Supersede earlier entries by reference;
preserve the reasoning that led to them.

Keep explanations in the overview or domain notes, paper findings in the
literature map and unresolved alternatives in the question record. Record an
accepted choice in `DECISIONS.md`, reference its supporting note, then update
the affected brief/module/status fields. A drafted note or brainstorm is not
an accepted experimental design.

Every handoff should identify the module, scope delivered, relevant files,
verification performed, unresolved issues and next responsible thread.
When restarting, inspect the actual checkout and reconcile records with code.
Report unrun checks explicitly. Do not mark work complete because a document
or prompt describes the desired result.
