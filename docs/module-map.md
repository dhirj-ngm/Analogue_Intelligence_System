# Module and task map

**Updated:** 9 October 2026  
**State:** M001 In Progress under D014/D015; T02 delivered for Domain review; M002–M008 remain proposed

Direction: [PROJECT_BRIEF.md](../PROJECT_BRIEF.md). Workflow and lifecycle:
[PROJECT_TRACK.md](../PROJECT_TRACK.md). Current work: [STATUS.md](../STATUS.md).

## Boundaries and dependencies

Separate modules around a reviewable outcome and an explicit input/output
contract. Technologies are choices within those boundaries. Create individual
specifications under `docs/modules/` as modules are taken up; do not specify
every future function before the data and interfaces are understood.

| ID | Responsibility | Reviewable outcome | Dependency |
| --- | --- | --- | --- |
| M001 | Data viability pilot | Ten reviewed episodes, five queries, initial baselines and a scope recommendation | Working contract/T01 authorized by D014; one-example T02 trial authorized by D015; later assignments at task checkpoints |
| M002 | Reproducible corpus pipeline | Source manifests, repeatable acquisition/parsing and validated records | Pilot evidence and schema findings |
| M003 | Evaluation and text baselines | Fixed eligibility/judgement/split protocol and reproducible BM25, dense and fusion runs | Reviewed corpus and pilot judgements |
| M004 | Structure-assisted retrieval | Inspectable features/scoring, ablations and failure analysis | M003 protocol established before tuning |
| M005 | Focused NLP learning experiment | A bounded evaluated model and integration audit | Suitable labels and demonstrated extraction/model task; conditional |
| M006 | Backend contracts | Tested search, episode, evidence and comparison interfaces | Stable core data/retrieval contracts |
| M007 | Case-study workspace | Readable case search, comparisons, evidence and dated follow-up | Backend and defined reader workflow |
| M008 | Reproduction and demonstration | Fresh setup, reliability checks, documentation and demonstration | Integrated scoped system |

The first specification is [M001 — Data viability pilot](modules/M001-data-viability-pilot.md).
Its lifecycle is **In Progress**: T01 is revised to trial guide v0.2, and T02
authoring/checkpoint delivery is complete with one real Colgate Asia Pacific Q4
2022 draft and author checks. Domain/Dheeraj case/revision review is pending;
human-reviewed episodes remain **0/10**, queries **0/5**, and T03–T08 unstarted.
D014 adopts the working contract and guide task; D015 records the explicit T02
trial. D011's startup gate is superseded, not reopened.
D012/D013 retain the product-first FMCG question and review ownership.
The specification owns M001 task/acceptance contracts; this map preserves the
proposed later-module boundaries without authorizing their execution.

M001 uses lightweight retrieval to obtain early feedback. M002/M003 promote
useful pilot work into repeatable pipelines; reuse working code and evidence.
Evaluation starts in the pilot and its formal protocol precedes M004 tuning.
Re-run affected checks after integrating extraction changes. M005 is a possible
location for custom AI work; a different model responsibility may need its own
module after discussion. The numbering is a proposed plan, not fixed dates.

### Module boundaries and later proposals

Retain M001–M008; no new module or renumbering is proposed. Clarify the following
contracts rather than split the small pilot into separate modules:

- **M001 owns a minimal evaluation protocol as well as data viability.** Eligibility,
  date rules, pre-ranking judgements, frozen inputs and reproducible paired runs
  are necessary to interpret its findings. M003 promotes/extends that protocol
  and baseline work; it does not establish fairness for the first time after M001.
- **M002 owns repeatable corpus preparation, not ranking or domain acceptance.**
  It receives the pilot's source access/retention findings, reviewed examples and
  schema issues. It must preserve provenance and reviewed meanings while making
  preparation reproducible; pilot utilities can be reused.
- **M003 owns text evaluation; M004 owns the incremental structural experiment.**
  Fusion is a later M003 comparison. Information-budget controls, ablations and
  tuning discipline are prerequisites to claims in M004, not M001 deliverables.
- **M005 is conditional, not a universal prerequisite to M006/M007.** M006 needs
  stable data and retrieval contracts; M007 needs M006 and an agreed reader flow.
  M004 or M005 becomes an interface dependency only if its output is explicitly
  included in the accepted product scope. M008 packages the accepted integrated
  scope and does not require an unapproved learning experiment.

These boundaries inform the adopted M001 working contract. Later module scope,
infrastructure, model tasks and parallel implementation remain unapproved.

## M001 task sequence

These IDs are defined as `M001-T01` through `M001-T08` in the specification.
T01 drafting/checks and T02 authoring/checkpoint delivery are recorded. The current
[T02 handoff](workflow/M001-T02-handoff.md) identifies the exact review targets;
Domain/Dheeraj review remains pending. T03–T08 are unstarted. Consult the
specification for scope, acceptance coverage, checks and dependencies.

| Task | Output | Completion evidence |
| --- | --- | --- |
| M001-T01: Define the episode contract | Trial guide v0.2; DOM-T01-01/02 author-applied following Domain recommendation | Original v0.1 review/hash preserved; revised meaning/curation freeze pending |
| M001-T02: Validate one complete example | Delivered one real draft, source manifest and walkthrough; human review pending | Author checks recorded and artifact hashes verified; 1 created real draft, 0 human-reviewed cases |
| M001-T03: Validate firms and windows | Source-access record and historical inventory | Actual source checks and justified diversity of firms/periods |
| M001-T04: Curate the pilot cases | Ten distinct reviewed episodes with supported contrasts | Record validation, provenance and documented differences |
| M001-T05: Define queries and judgements | Five queries, candidate eligibility and relevance grades/rationales | Rubric and judgements frozen before model rankings; self/duplicate exclusion explicit |
| M001-T06: Run BM25 and dense baselines | Paired rankings and versioned run records | Same admissible candidates and reproducible configuration |
| M001-T07: Review errors and effort | Per-query failures, missingness, disagreements and curation effort | Findings refer to actual evidence and measured work |
| M001-T08: Recommend next scope | Continue/narrow/revise report | Recommendation follows data quality, useful matches/nonmatches and effort |

The one-example task is an early learning checkpoint, not a substitute for ten
distinct cases. Shared firms/periods/shocks may still make distinct cases dependent.
T01 involves no acquisition; source work first occurs in T02 when authorized.
T02 may propose judgement examples; fix the evaluation rules and labels before
inspecting the baseline rankings in T06.

## Breaking a task into implementation work

For each task, specify its input, output, dependencies, allowed files, observable
behavior, completion checks and handoff. Then identify the relevant layers:
data/domain, core logic, interfaces and verification. Omit layers the task does
not need. Function/class boundaries follow those responsibilities.

For example, a candidate eligibility task might specify:

```text
Input: query cutoff, query episode ID, candidate evidence and duplicate groups.
Output: eligible candidate IDs plus reasons for excluded candidates.
Behavior: enforce the declared publication rule, exclude the query episode
and near duplicates, and apply the agreed unknown-date policy.
Checks: future publication, self-match, duplicates and ambiguous dates.
```

This is a behavior sketch, not a selected function signature or missing-date
policy. Tasks should produce useful reviewable artifacts; avoid splitting solely
by calendar days or creating a module for every technology.

## Ready and acceptance gates

Records drafts the specification, identifies the decisions needed for its first
task and keeps unresolved issues visible. Dheeraj agrees scope and completion
criteria before the module becomes `Ready`. Implementation proceeds through
assigned tasks and hands off reviewable checkpoints. Review checks code and
its specified behavior at code checkpoints under D012. Implementation retains
the required data, provenance, date and method checks; Domain/Dheeraj accepts
domain meaning and Dheeraj accepts the module outcome. T01's guide checkpoint
goes to Domain/Dheeraj with Implementation's checks, not independent code Review.

Use [Open questions](research/open-questions.md) and the
[Manager handoff](workflow/manager-direction-handoff.md) to distinguish accepted
direction from remaining operational choices. Do not reopen the questionnaire.
D014 resolved T01 startup. Resume from the delivered
[T01 checkpoint](workflow/M001-T01-handoff.md); T02 still requires guide review
and its own assignment. M001 stays In Progress during this task checkpoint.
