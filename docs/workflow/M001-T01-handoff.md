# M001-T01 — Annotation guide delivery and checks

**Recorded:** 9 October 2026  
**Authority:** D014, explicit user request to fix records/handoff and advance annotation rules  
**Delivered:** Guide v0.1; completeness inspection  
**Pending:** Domain/Dheeraj meaning review; no frozen curation contract  
**Module:** In Progress; T02–T08 not started

## Scope delivered

[Annotation guide v0.1](../../data/annotation_guide.md) defines stable identities,
episode/update/split handling, traceable claims, attribution, explicit unknowns,
dates, metric definitions, review states and one-real-example requirements.
It includes the three hypothetical checks required by the T01 specification.
No real company case, document download, query label or model result is supplied.

The current thread performed Records maintenance and T01 drafting sequentially
under D014. This is an author completeness check, not an independent reviewer
or a substitute for Dheeraj's business-meaning acceptance. New operational
rules in the guide are proposals for review; accepted D003/D012/D013 controls
remain requirements. AC01 also needs the later T02 real-example checkpoint.

## Completeness inspection

The checks below inspect whether the draft provides the required rule and a
reviewable example. They do not establish that a rule has passed real-source use.

| Required area | Guide location | Inspection result |
| --- | --- | --- |
| Stable IDs and linked updates | §§1–2; H1 | Episode, update, document/version, span and claim references distinguished; four continuing reports share H-EP01 |
| Splits, merges and shared shocks | §2; H2 | Written reasons/evidence and retained identities required; a reporting gap does not create a counted episode; shared shocks retain dependence |
| Source/span support | §3; worksheet | Exact spans and reproducible locators required; source versions and retention limits explicit |
| Claim categories and attribution | §4; H1 | Observations, management explanations, intentions, implementation and interpretation remain distinct |
| Action, rationale and follow-up | §§4–6; H1 | Announced and implemented statements retain separate support/dates; absent rationale stays unknown; recovery is not causal proof |
| Event/publication/reporting dates | §6; H1 | Separate dates and precision; H-D04 cannot inform a 2021-01-31 cutoff despite a 2020 reporting period |
| Unknown historical claims | §5; H3 | Reader clarification changes the query, not Elm's evidence; checked section and missing-field reason retained |
| Metric definitions | §7 | Units, basis, scope, period and vintage explicit; 30% → 27% distinguished as −3 pp, −300 bp and −10% relative |
| Ranking versus display | §6 | Later response/outcome exclusion covers summaries/tags and lineage; contemporaneous-response treatment remains a T05 decision |
| Review state and human acceptance | §4; §9 | Technical checks separate from domain review; no fabricated human reviewer or acceptance |
| Remaining policies and T02 handoff | §9 | Guide-review issues distinguished from later date/ranking/model choices; no numeric gap/ranking threshold selected |

**H1 outcome:** One hypothetical episode, four updates. Changed actions do not
inflate episode count; a later publication stays unavailable at the earlier cutoff.

**H2 outcome:** Unresolved association and identity-review flag, with an unchecked
gap. No invented resolution, automatic merge or second reviewed episode.

**H3 outcome:** A clarified query with an unchanged historical unknown. No
fabricated retailer constraint and no forced relevance label.

## Repository verification

A Python standard-library inspection covered all 18 Markdown files, including
untracked files that `git diff --check` does not cover:

- 111 local links and 20 local heading anchors resolve.
- UTF-8, final newlines, balanced code fences and whitespace checks pass;
  intentional two-space Markdown hard breaks are retained.
- All 14 decision IDs are unique; the eight M001 task IDs and eight acceptance
  IDs are preserved. No referenced decision ID is missing.
- H1 has four unique update/document/span identities with ordered publication
  dates; its fourth disclosure is after the example cutoff. The example margin
  arithmetic yields −3 percentage points, −300 basis points and −10% relative.
- Current M001 lifecycle statements agree. Every original project document is
  preserved; 12 existing documents changed and two artifacts were added.
- `git diff --check` passes for tracked changes. Inspection of remaining old-gate
  matches confirms that they are labelled history, not current assignments.

Guide v0.1 SHA-256:
`4aa38b15a7a0a2fc7160b8d2f86cf03a92c4bdd49756700a348ed21a16d56013`.
Recheck the hash if the guide changes; the review target is this artifact version.

Application tests/lint are not applicable: no runtime/test suite exists. No
acquisition, baseline or independent code review ran. These checks validate
document consistency and examples, not empirical source feasibility.

## Record repairs and scope limits

- D014 records the user's current authorization and supersedes the old T01
  startup gate. M001 moved Proposed → Ready → In Progress; it is not Done.
- The brief now agrees with M001 on the accepted pilot target, judgement-before-
  ranking order and unselected later AI task.
- Active thread prompts continue existing work, accept an assigned In Progress
  module, and route guide/data checkpoints to Domain/Dheeraj with Implementation
  checks. Independent Review owns code correctness at actual code checkpoints.
- Manager's handoff points here; Domain's earlier proposals retain their history
  with current-state pointers. No old setup assignment needs repeating.
- Exact companies, schema serialization, date mode, ranking policy, model and
  infrastructure remain open at their scheduled tasks. The working criteria are
  adopted under delegation, not falsely attributed to a line-by-line user review.

## Next owner and concrete review

**Domain/Dheeraj:** Inspect the guide's minimum-case rule (§3), identity procedure
(§2/H2) and unknown distinction (§5/H3). Record specific revisions or agreement
to try the contract on one real example. The accepted first objective and
continuing-update direction do not need another decision.

**Implementation/Records:** Apply concrete findings, record the reviewed version
and scope. Manager can then assign T02's one source-to-case walkthrough. T02 must
check access/terms, preserve locators/dates/metric basis, record unknowns and effort,
and revise the guide from actual evidence before the T04 curation freeze.

Resume message for the existing Domain conversation:

```text
Read STATUS.md, D014, data/annotation_guide.md v0.1 and
docs/workflow/M001-T01-handoff.md. Review the delivered T01 guide for minimum
case evidence, episode boundaries, attribution and historical unknowns using
the H1–H3 examples. Return concrete revisions or a recommendation for Dheeraj's
meaning review. Do not repeat initial orientation, reopen the D013 objective,
claim human acceptance, acquire sources or change module lifecycle state.
```

**Target:** `main`, base `3a6db3aef2eedad0c5f3d0dd96052099ef88dc1f`, plus the
current local documentation/guide changes. No new commit or remote check.
Read current files when resuming; a base commit alone does not contain this work.
