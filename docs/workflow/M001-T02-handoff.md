# M001-T02 — Checkpoint and correction handoff

## Current correction to Records — 31 October 2026

**Task/finding:** M001-T02 / DOM-T02-01, applied under the explicit correction
assignment and D016. No T03 work or lifecycle transition.

The Colgate Asia Pacific Q4 2022 episode is now **record version 2**. Added
SP-CL-APAC-006, CL-CL-APAC-006 and MET-CL-APAC-003/004: as-reported and organic
volume each changed **−1.0% versus Q4 2021**, in the same division. Source: the
[official release](https://investor.colgatepalmolive.com/news-releases/news-release-details/colgate-announces-4th-quarter-and-full-year-2022-results),
Fourth Quarter Sales Growth By Division, Asia Pacific row, its two volume
columns and quarter heading; corroborated by quarterly Table 6 and notes.

The worksheet replaces `volume_demand` with evidenced `disclosed_volume` references
and a separate `underlying_consumer_demand` unknown. The issuer's volume columns
do not establish consumer demand or a volume contribution to margin decline.
Source labels, comparison periods and the difference from sales are preserved;
no extra definition/weighting formula is invented. The new claim stays display-only
pending T05. Existing margin attribution and initial evidence/IDs remain intact.

**Source checks:** Web reader opened the same release and exposed the relevant
headings, volume cells, footnotes and Table 6. Direct `curl` returned HTTP 403
(exit 22). A new raw body/hash was not obtained. The new locator hashes rendered
row cells, with normalization and column positions declared; this is not a raw
HTML hash or a revalidation of the old HTML offsets. The manifest adds a dated
inspection without replacing the original retrieval/hash. Terms were not
rechecked; full-source retention/public-reuse limits remain unresolved.

**Local checks passed:** One source/episode, six unique spans/claims, four metrics,
fourteen explicit unknowns; claim/update/action/metric references resolve. Both
volume values, division, units, reporting/comparison quarters and publication
date agree with the inspected table. The stored excerpt matches the rendered-row
cell-pair fixture, offsets and context hash. Original five spans/claims, both
margin metrics, source retrieval metadata, guide 0.2, canonical review flags and
original effort measurement are unchanged. JSONL parsing, Markdown local links,
UTF-8/newlines/whitespace and `git diff --check` passed. No application code was
introduced; application tests/lint are inapplicable. No ranking or model run.

**Records disposition requested:** D016 already records Dheeraj's bounded
acceptance of the case's limited usefulness. Record the correction/version and
reconcile canonical human-review flags/counts with that limited decision. Those
flags/counts were deliberately not promoted by Implementation; no final guide,
episode-boundary, response-effectiveness or ten-case corpus acceptance follows.
Earlier specification reconciliation is already complete and is not reopened.
Manager decides any subsequent assignment. No new user decision is needed merely
to disposition this correction.

Changed artifacts: episode JSONL, source manifest (additive inspection and excerpt
count), walkthrough, this handoff, factual STATUS progress and the linked checksum
ledger. The guide, Domain review and pre-existing D016 changes are preserved.

**Exact target:** `main` at base
`0f5ff4426489e98cd9f10d51c54096c46fd79f26`, plus this local correction and
pre-existing `DECISIONS.md` / Domain-review work. No new commit or remote check.

| Current artifact | SHA-256 |
| --- | --- |
| Guide 0.2, unchanged | `0ec2551848436aec85c2f42ddf58f3f3827d46a8e302436325820ab338b9ac4c` |
| Source manifest, additional volume inspection | `918911af5ddcc37c943e96436ac887d372e1fd67d749855262e244c040310e05` |
| Episode record version 2 | `117be571db6674549af0d7255dae363898b58fd4818cd3208efa5820ff104618` |
| Revised walkthrough | `91341b90728c332ea03363a8cbff8c0c145d31d73d4706d8b5e357f944c93348` |

The [correction checksum ledger](../../data/pilot/M001-T02-correction.sha256)
also records final hashes for this handoff and STATUS, avoiding a self-hash cycle
inside either document. Verify from the repository root with
`sha256sum -c data/pilot/M001-T02-correction.sha256`.

The original handoff SHA-256 before this correction was
`6cdef0a07f777b09d19e80a56a91ac0d3ae5fff69d1718f91a72fdb6429e8a83`.
The historical target table below is preserved unchanged; it identifies the
pre-correction checkpoint, not the current files. The episode revision history
also preserves its original hash and committed snapshot reference.

## Historical delivery to Domain — 9 October 2026

The remainder preserves the original checkpoint, its checks, scope and target
hashes. Its pending-review/repair instructions describe that earlier state;
D016 and the current Records handoff above govern resumption.

**Recorded:** 9 October 2026, Asia/Kolkata  
**Task:** M001-T02 — one source-to-case example; stop before T03  
**Authority:** Dheeraj's explicit current user assignment: use the reviewed guide
for a one-example trial, resolve needed findings and execute T02  
**Module:** In Progress; no formal transition or module acceptance  
**Next owner:** Domain/Dheeraj for case meaning and usability; Records for disposition

## Delivered scope and target

One official Colgate-Palmolive results disclosure and one draft episode:
`EP-CL-APAC-2022Q4-001`, Asia Pacific materials-cost operating-margin pressure.
The observed interval is Q4 2022; publication is 27 January 2023. The source
attributes lower divisional operating margin primarily to materials/packaging
costs and preserves partial offsets and other contributors. No isolated response
effect, recovery, second analogue or historical episode boundary is invented.

The [walkthrough](../../data/pilot/example-walkthrough.md) maps every case section
to record references, explains selection and limitations, and gives a proposed
question. Five small exact excerpts retain semantic locators, context hashes and
offsets; two reported metrics preserve unit, period, scope, basis and vintage.
Fourteen missing-value objects preserve reasons and bounded checks. The example
remains assistant-curated: **human review pending; reviewed cases 0/10**.

Files changed for this assignment:

- [Annotation guide](../../data/annotation_guide.md): 0.1 → 0.2, with finding
  disposition and real-example contract clarifications.
- [Source manifest](../../data/source_manifest.jsonl): one inspected release,
  publication/retrieval metadata, access outcomes and retention limits.
- [Episode record](../../data/episodes.jsonl): one canonical nested trial worksheet.
- [Example walkthrough](../../data/pilot/example-walkthrough.md): source-to-case
  map, question sketch, unknowns, schema problems, effort and check record.
- This handoff and [STATUS.md](../../STATUS.md): factual progress and next owner.

No persistent utility, application code, dependency, runtime or test suite was
introduced. Temporary standard-library authoring/inspection scripts are not
project deliverables. Existing project work, original Domain review and T01
checkpoint were preserved; no commit, push, remote fetch or new thread created.

## Required guide findings resolved for the trial

| Finding | Author-applied resolution | Real-case evidence / review limit |
| --- | --- | --- |
| DOM-T01-01 | Guide §9 requires compatible-scope/period cost pressure, margin effect and supported linkage for this first example; qualitative headwinds remain allowed; partial leads are distinguished | Divisional introduction, Asia Pacific driver bullet and operating-margin row map to claims 001/002; issuer attribution and offsets retained. Domain must assess meaning. |
| DOM-T01-02 | H1 separates announcement/implementation statement publication from action-event dates | Real pricing/savings observations have Q4 effect context and January statement availability; effective intervention dates remain explicit unknowns. |

Guide 0.2 additionally records mixed-paragraph lineage separation, excerpt/context
locators, current-page version limits, table basis/rounding and realized-response
versus detailed-action distinctions. The nested JSONL version is a reversible
trial representation, not a final schema/architecture decision or curation freeze.

## Checks and actual results

| Check | Actual result |
| --- | --- |
| Official release access | Direct HTTPS GET succeeded, HTTP 200, no credentials; web-tool open timed out. The successful body was inspected. |
| Provider access/retention terms | Footer terms wrapper HTTP 200; its actual notice HTTP 404 (`curl` exit 22). Indexed official-page text is a lead, not verified current operative terms. Full archive/public redistribution clearance unresolved. |
| Evidence text/version/locator | All five stored excerpts matched the inspected normalized HTML elements, hashes and offsets; 23 quoted words total. Current-body SHA-256 recorded; historical immutability unverified. |
| Record/reference/scope checks | One source, one episode, five unique spans/claims; source/claim/action/update/metric references resolve; selected claims have matching divisional period/scope. |
| Dates and metrics | Publication follows Q4 reporting end; heading/dateline/metadata date agree; two reported metrics preserve definitions, scope, period, units and unaudited segment presentation; −220 bp converts to −2.2 pp. |
| Unknowns and feature boundary | Fourteen missing-value objects carry reasons; checked-but-unreported values name sections. Challenge/display claim sets are disjoint; no ranking text or response/outcome inclusion authorized. |
| Review and retention status | No human reviewer or accepted-corpus claim; no full-source repository archive. Temporary inspection bodies discarded after checks. |
| Repository records | UTF-8/final newline, whitespace, balanced fences and local-file links checked across Markdown including untracked files; `git diff --check` passed for tracked changes. JSONL parsed successfully. |
| Unrun / inapplicable | No application tests/lint: no persistent code/runtime introduced. No ranking/evaluation/model run, independent code review or human case review. No T03 coverage work. |

Failures retained accurately: a notice-body inspection also failed because the
404 request created no file; an authoring assertion initially expected 24 excerpt
words and was corrected to the actual 23 before records were written. Subsequent
record checks passed. No notice-content inspection or archival permission is
claimed from those failed requests. Measured effort is the bounded 286-second
working envelope in the walkthrough, not active human annotation time.

## Unresolved issues and disposition

There is no remaining example-meaning issue requiring a new user answer before
this handoff. Domain should assess the attribution, unknown boundaries and partial
responses on the supplied evidence. A single example tests contract usability;
it does not establish data viability or a useful retrieved comparison.

The provider's operative notice is unavailable. No full document is archived;
the local trial retains factual annotation and minimal attributed excerpts with
links/hashes. General redistribution and durable full-source retention remain
unverified and need a working notice or another supported basis before such use.
Refetching can produce a changed page; no immutable historical snapshot is claimed.

The specification's execution summary and earlier handoffs still describe the
pre-T02 checkpoint. The current assignment and STATUS supply actual progress;
Records should reconcile those snapshots after disposition. Implementation has
not edited the specification, decision register, domain review or lifecycle.
T03–T08 remain unstarted; no sampling/model/date-mode policy has been selected.

## Exact review target and next handoff

Branch/worktree: `main`, base commit
`3a6db3aef2eedad0c5f3d0dd96052099ef88dc1f`, plus existing uncommitted work and
these six changed/new files. No target commit exists; the base alone does not
contain the deliverables. Exact artifact SHA-256 values:

| Artifact | SHA-256 |
| --- | --- |
| Guide 0.2 | `0ec2551848436aec85c2f42ddf58f3f3827d46a8e302436325820ab338b9ac4c` |
| Source manifest | `c5d27ff6d609859d0d504ba043d6e8cbe3ea1ac87d471404041655992f98f756` |
| Episode record | `7b6a3f5ca739f6698eadc43ec446b3aed9f9219e1e0ba795b8d04eaea89d1684` |
| Walkthrough | `536faa9c1328b5dbaaa2716a9863d511bc79f509d41ca944f392a6b23ee83e15` |

Domain resume prompt:

```text
Review M001-T02 using STATUS.md, data/annotation_guide.md v0.2,
docs/domain/M001-T01-guide-review.md, data/source_manifest.jsonl,
data/episodes.jsonl, data/pilot/example-walkthrough.md and this handoff.
Inspect EP-CL-APAC-2022Q4-001 against the linked release's divisional introduction,
Asia Pacific driver bullet and operating-margin table. Assess compatible scope
and period, issuer attribution and concurrent contributors, reported pricing/
savings versus unknown interventions/dates/rationale, uncertain episode boundaries
and usable explanation. Return concrete findings or a recommendation to Dheeraj;
an AI Domain inspection alone does not establish human review. Preserve source,
metric and retention limits; do not acquire a second case, run rankings or start
T03. Records then records disposition/version; Manager assigns subsequent work.
```

Next proposed work is this Domain/Dheeraj checkpoint and any returned corrections.
T03 is a later Manager assignment after that checkpoint; it has not begun.
