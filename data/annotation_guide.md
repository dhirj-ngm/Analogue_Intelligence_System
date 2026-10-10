# Episode and evidence annotation guide

**Version:** 0.2 — 9 October 2026  
**Task:** M001-T01 contract revised during assigned M001-T02  
**State:** Authorized for one-example trial; real example awaits Domain/Dheeraj review; not frozen for curation  
**Authority:** D003/D012/D013 requirements; D014 draft authority; explicit user T02 assignment  
**Checkpoint:** [T01 checks](../docs/workflow/M001-T01-handoff.md), [Domain findings](../docs/domain/M001-T01-guide-review.md) and [T02 handoff](../docs/workflow/M001-T02-handoff.md)

## Purpose and authority

Turn a public disclosure into an inspectable company case for the first
investigation: materials, packaging or logistics-cost margin pressure, relevant
earlier comparisons, documented responses/reasoning and later observations.
Pricing conditions and volume help when supported; neither is assumed.

Accepted requirements are preserved below. Operational field names, minimum-case
rules and boundary procedures are working proposals for Domain/Dheeraj review,
then a real-example check in T02. This guide defines no database, trained model,
ranking score or final evaluation policy. All worked examples are invented;
none may enter the real source manifest, episode count or benchmark.

## 1. Unit of annotation and stable identities

An **episode** is a company situation over a supported or uncertain interval.
An **update** adds dated evidence about that situation. A **case study** presents
the episode readably; an alternative presentation does not create a new episode.

Assign stable IDs to company, episode, document/version, evidence span, claim,
update, action and metric records when those records exist. IDs do not encode a
relevance grade or favourable outcome. References must resolve; do not renumber
existing identities when sorting, revising dates or changing a narrative.
The examples reserve `H-` IDs for hypothetical objects only.

An update references its episode, source document/version and claims. A claim
references the spans that support it, not merely a company's homepage. Multiple
documents can support one claim; one document can support multiple episodes if
the passages and business scope warrant it. Record duplicate documents and
reprints without counting them as independent evidence or new episodes.

## 2. Episode continuity, split and merge procedure

For each possible new episode or update:

1. Compare company and business scope, reported pressure, affected measures,
   interval, continuity language and any documented resolution or recurrence.
2. Link continuing reports to the same episode. Four quarters of one continuing
   challenge are one episode with four updates. A new action alone does not
   create a new challenge or end the old one.
3. A reporting gap triggers identity review. Silence is neither proof of
   resolution nor proof of continuity. Keep uncertain boundaries visible;
   use no automatic number-of-months split.
4. Propose a separate, linked episode when evidence supports a distinct situation,
   such as a new pressure after documented resolution or a separately supported
   business-scope change. Record overlaps; do not double-count the same situation.
5. For every split/merge, record affected IDs, supporting spans, reason, author,
   date and review state. Preserve retired IDs as aliases/references and retain
   the earlier record version. Do not silently delete provenance.

Unresolved identity gets `needs_identity_review` and does not count as an
additional reviewed episode. Different companies retain different episode IDs;
link a shared shock family only when supported, otherwise mark it unknown.
Shared companies, periods and shocks remain evaluation dependencies even when
episodes are distinct. No declaration of statistical independence follows.

## 3. Minimum case evidence and source records

**Proposed admission rule:** a lead becomes a draft case when evidence identifies
the company/business scope and reporting interval, supports a challenge relevant
to the investigation or a documented contrast, and contains locatable passages
with recorded publication-date information or an explicit date uncertainty.
For an input-cost/margin comparison, support both the pressure and the reported
margin effect. Claim a connection only when evidence supports that connection,
preserving management attribution. Co-occurrence alone is insufficient.

An incomplete lead may be retained with its gaps; it is not a reviewed positive
analogue. No fixed passage count can substitute for support. A reviewed case
requires record checks and Domain/Dheeraj meaning review, with unresolved issues
visible. Query eligibility remains a separate T05 decision, especially when
dates or historical ordering are uncertain.

For each source preserve issuer, type, URL, publication date and its basis,
reporting period, retrieval timestamp, document/version ID, content hash when
content is retained, and access/retention notes. Verify provider terms at T02;
public availability alone does not authorize redistribution. If retention is
restricted, record what locator/version metadata can be preserved and the
resulting reproduction limits rather than claim a nonexistent local snapshot.

For each evidence span preserve exact supported text, document/version reference,
section/page and paragraph, offsets or another reproducible locator. Keep enough
context for qualifications and negation. Record offset conventions if used.
A paraphrase is a claim summary, not a verbatim span. Later document revisions
receive distinguishable versions; they must not overwrite the original evidence.

## 4. Claim categories, attribution and review

| Claim kind | Store as | Do not convert into |
| --- | --- | --- |
| Disclosed observation or metric | What the source reports, with scope and basis | Independently established causal truth |
| Management attribution | Who attributes which effect to which pressure; preserve qualifiers | An unqualified causal edge |
| Forecast or announced intention | Expected/planned action or outcome and statement date | Implemented action or realized result |
| Documented implemented action | Source-supported implementation, timing and coverage | Proof that the action worked |
| Stated rationale | Management's documented reason linked to the action | A universal principle or an inferred motive |
| Analyst interpretation/hypothesis | Author, supporting evidence, reasoning and alternatives | A historical fact filling an evidence gap |

Use subject/relation/object fields only where useful; direction and attribution
must survive normalization. Start with the brief's vocabulary: cost increase,
logistics disruption, demand/volume change, margin change, pricing and productivity
actions. Do not add unsupported mechanisms to complete a graph.

Keep claim kind separate from review state. Record annotator, annotation method,
date and guide version; record technical/provenance checks separately from domain
review, including reviewer identity/role, findings, resolution and date. Do not
mark a claim human-reviewed because an assistant drafted or checked it. A record
can pass reference checks while its business interpretation remains unresolved.

Keep conflicting claims with their sources, compatible scopes and dates. First
check whether apparent contradictions concern different segments or periods.
If the conflict remains, flag it; the newest statement does not silently erase
the old one. Record any later adjudication and retain the conflicting evidence.

## 5. Unknowns and a compact record worksheet

Use an explicit missing value with a reason: `not_reported_in_checked_sources`,
`not_checked`, `unavailable_source`, `ambiguous` or `conflicting`. Record which
sources/sections were checked before saying something was not reported. Unknown
does not mean zero, false, no action, weak pricing power or proven mismatch.
Use `not_applicable` only with a reason. These are proposed annotation labels;
numeric penalties and treatment of unjudgeable pairs remain T05 work.

The worksheet below is a manual contract, not a selected serialization schema.
Sections may reference shared records instead of duplicating them.

| Section | Required contents or explicit uncertainty |
| --- | --- |
| Identity | Episode/company IDs, business scope, interval/precision, update and duplicate links, shared-shock ID or unknown |
| Sources and evidence | Document/version metadata, permitted locators and exact spans; claim-to-span references |
| Challenge/context | Supported pressure/effect, relevant conditions, contrary evidence and missing context |
| Claims | Summary, kind, attribution, dates, scope and evidence references |
| Responses | Action ID, announced/implemented/unknown status, dates, coverage, constraints and support |
| Reasoning | Source-stated rationale linked to action, or explicit unknown; separate interpretations |
| Follow-up | Dated later observations and other reported drivers, without a causal-success claim |
| Metrics | Name/value/unit, period, scope, accounting basis, vintage and evidence |
| Boundaries | Update/split/merge reasoning, affected IDs and identity-review state |
| Checks/review | Author, guide/record version, technical checks, domain review, findings and unresolved issues |
| Effort | Actual curation/review time where measured; distinguish estimates and missing measurements |

Completeness means each section is supported or explicitly unresolved. A response,
rationale, favourable outcome or quantified follow-up is not mandatory evidence
to invent. Whether a case is useful for a particular query is judged separately.

## 6. Dates, evidence availability and permitted use

Keep event interval, reporting period, publication time and retrieval time in
separate fields. Store date precision and source basis; use an uncertain interval
or unknown instead of inventing a day or timezone. An episode's first observed
report does not necessarily establish its actual onset. Missing follow-up does
not establish an end. Preserve original and restated metric vintages.

Every challenge summary or normalized tag must retain lineage to the claims and
spans that supplied it. Display eligibility and ranking eligibility are different.
For the first experiment, later response/outcome fields stay out of similarity
text, tags and derived features. Date-filtered text must not inherit a later
fact through a summary. Review contemporaneous response treatment at T05 before
any such material enters ranking; this guide does not silently allow it.

For a selected historical cutoff, evidence published after it cannot support the
query or candidate ranking features. A reporting-period end is not a publication
date. Publication before a cutoff alone also does not prove that a candidate is
historically earlier than the target. Unknown/conflicting dates, overlapping
episodes, retrospective/as-of mode and self/duplicate exclusions must be settled
in the T05 protocol before candidate sets are frozen. No retrieval run is
authorized to guess those policies from this draft.

## 7. Metrics and comparison limits

Preserve source-defined metric name, numeric value, unit/currency, level versus
change, period, group/segment scope, GAAP/adjusted basis, publication/vintage and
evidence. A gross margin is not interchangeable with an adjusted operating
margin; shipments are not automatically consumer demand. Retain the issuer's
price/volume/mix definitions rather than manufacture a decomposition.

Label derived quantities with formula, compatible inputs and their evidence.
Hypothetically, a gross margin falling from 30% to 27% changes by −3 percentage
points, or −300 basis points; the relative change is −10%. These are different
measures. Do not subtract figures with incompatible periods, scope or basis.
Later margin recovery alone does not identify an action's effect.

## 8. Worked boundary checks — entirely hypothetical

### H1 — Four continuing updates, one episode

Assume invented Company Cedar's four fictional disclosures each explicitly
describe the same continuing packaging-cost pressure in the same business scope.
The summaries below are teaching inputs, not real evidence spans or URLs.

| Update | Fictional document/span | Reporting period | Publication date | Assumed supported content |
| --- | --- | --- | --- | --- |
| H-U01 | H-D01 / H-S01 | 2020 Q1 | 2020-05-10 | Packaging costs rose; management attributes part of gross-margin pressure to them |
| H-U02 | H-D02 / H-S02 | 2020 Q2 | 2020-08-10 | Pressure continues; repricing announced, implementation not established |
| H-U03 | H-D03 / H-S03 | 2020 Q3 | 2020-11-10 | Pressure continues; source reports repricing implemented |
| H-U04 | H-D04 / H-S04 | 2020 Q4 | 2021-02-10 | Continuing challenge; later margin partly improves alongside several reported drivers |

Expected treatment: one episode `H-EP01`, four linked updates and four separately
dated document/span records. For example, claim `H-C01` links to `H-S01` as a
management attribution. Action `H-A01` has an announced statement at H-U02 and
an implementation statement at H-U03; retain both dates and supporting spans.
Rationale remains unknown unless a fictional statement explicitly supplies it.
The later observation at H-U04 does not establish repricing caused improvement.

H-U02's announcement statement became publicly available on 2020-08-10;
H-U03's implementation statement became publicly available on 2020-11-10.
These publication dates are not automatically the announcement event date or
the effective implementation date. The hypothetical content supplies no exact
action-event dates; preserve those as unspecified. Use an event interval only
if the statement supports it, and record that support separately from the
reporting period and publication date. Implementation status can be supported
while its effective date remains unknown (DOM-T01-02).

For a hypothetical cutoff of 2021-01-31, H-D04 is unavailable even though its
reporting period has ended. It cannot influence a cutoff summary. Its later
outcome is also excluded from first-experiment similarity features. These checks
illustrate the accepted controls, not selection of the pilot's actual date mode.

### H2 — A reporting gap is unresolved identity

Assume the next fictional Cedar report is published on 2022-05-10. It mentions
cost pressure but says nothing about intervening continuity, resolution or a new
shock. No intervening reports have been checked.

Expected treatment: keep the document and its supported claims as a pending
episode association; mark the interval `not_checked` and `needs_identity_review`.
Do not invent an end for H-EP01, append with asserted continuity, or count a
second reviewed episode. A curator checks intervening evidence. If later evidence
supports recurrence after resolution, propose a new linked ID and cite the
resolution/new-pressure spans in a split record. If it supports continuity,
attach the update with the reason. If inconclusive, preserve the uncertainty.

Another fictional company facing a documented shared shock would have a separate
episode and a shared-shock link. It is not an independent shock experiment.

### H3 — Clarifying the user leaves a historical unknown unknown

Assume the reader clarifies: “I want companies that faced a retailer-imposed
delay before raising prices.” Fictional Company Elm's checked release, H-D06,
mentions costs and margins, but its inspected operating-results section has no
pricing-constraint or implemented-response evidence.

Expected treatment: update the query objective. Keep Elm's constraint and action
as `not_reported_in_checked_sources`, naming H-D06 and the inspected section.
The reader's preference supplies no historical evidence. Do not infer a delay,
weak pricing power or inability to act. Explain the evidence gap; do not assign
a positive grade or a proven-mismatch label from it. Unknown-label handling is
deferred to T05, not improvised to force a comparison.

## 9. T02 real-example requirements and remaining decisions

After Domain/Dheeraj reviews this guide, Manager can assign one bounded real
example. T02 must verify source access/terms, construct the source and episode
records, and provide a passage-to-case walkthrough. Check every material claim,
date, unknown and metric definition. Record effort and contract failures. No
second real analogue, favourable outcome or benchmark label is required yet.
Revise this guide from that example and freeze a reviewed version before T04.

**Assigned first-example inclusion clarification (DOM-T01-01):** Select passages
supporting relevant input-cost pressure and a reported margin effect or headwind
in compatible business scope and periods, plus a supported relationship between
them. Qualified management attribution suffices; retain speaker and qualifiers.
Qualitative evidence is allowed: neither a quantified cost contribution nor a
net margin decline is mandatory. Differing scopes/periods require source support
for the linkage. Co-occurrence alone yields a partial lead with the relationship
unknown, not a demonstrated mechanism. This first-example preference does not
replace §3's broader admission rule for incomplete leads or contrasting cases.
A profit-only statement remains profit; it cannot substitute for margin.

**T02 serialization trial:** One JSONL source record and one episode record use
nested evidence/claims/actions/metrics with stable references and schema version
`m001-t02-trial-0.1`. This is a reversible worksheet representation, not the final
M002 schema. Evidence retains small exact excerpts with semantic section/row
locators and context hashes. If offsets are supplied, specify zero-based Unicode
character offsets, exclusive end, and the normalization used. Do not represent
short excerpts as complete paragraphs; retain qualifications in an attributed
summary and point readers to the full source context. A fetched-body hash identifies
the inspected current page, not proof of an unchanged historical publication.
No full-document archive or redistribution permission follows from access.

For metric tables, preserve column headings, period/scope and footnotes through
locators; mark unaudited and as-reported versus adjusted distinctions explicitly.
Rounded displayed values need not reproduce issuer-reported rounded changes
exactly. Record the reported change separately instead of manufacturing an exact
decomposition. A reported pricing benefit supports realized higher pricing, but
does not establish a particular pricing announcement, product coverage or effective
date. A programme-name attribution alone does not detail its implementation.

| When | Remaining decision or check |
| --- | --- |
| T01 checkpoint | Domain/Dheeraj reviews the proposed minimum-case rule, uncertain identities and claim/unknown distinctions; record agreement or concrete revisions |
| T02 | Confirm workable source locators, date evidence and record representation against one real example; revise fields without losing lineage |
| T03/T04 | Source sampling, firms/windows, review availability, diversity and effort; accept the curation version |
| Before T05 | Date mode/ordering, uncertain-date eligibility, relevance/unknown handling, no-match policy, judgements, information budget, contemporaneous responses and metric conventions |
| Before T06 | Model/dependencies, hardware feasibility and reproduction tolerances |

The guide is authorized for this one-example trial; human meaning review of the
real case and the T04 curation freeze remain pending. No evaluation policy is
selected by this revision. Actual acquisition/check results live in the T02 handoff.

## 10. Version and finding disposition

| Version | Changes and authority | Review limit |
| --- | --- | --- |
| 0.1 | T01 draft under D014; historical hash and checks in the T01 handoff | Domain review recommended a bounded trial with two Required clarifications |
| 0.2 | Explicit user T02 assignment; DOM-T01-01 resolved in §9, DOM-T01-02 in H1; added excerpt/context provenance, trial serialization, table rounding and observed-pricing limits from the real example | Author-applied resolutions; Domain/Dheeraj reviews the real example and revision; no human-reviewed case or final schema asserted |

The original Domain review and T01 hash remain unchanged as historical evidence.
The revised hash, actual source/record findings and next checkpoint are recorded
in the [T02 handoff](../docs/workflow/M001-T02-handoff.md).
