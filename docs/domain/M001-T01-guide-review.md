# M001-T01 — Domain review of annotation guide v0.1

**Recorded:** 9 October 2026  
**Reviewer role:** Domain and Research discussion  
**Scope:** Only rules and examples affecting one real M001-T02 source-to-case
walkthrough. This is a review recommendation, not Dheeraj's acceptance or a T02
assignment. The accepted investigation is unchanged.

**Target:** [Annotation guide v0.1](../../data/annotation_guide.md), on `main` at
base `3a6db3aef2eedad0c5f3d0dd96052099ef88dc1f` plus local, uncommitted work.
The inspected SHA-256 matches the [T01 handoff](../workflow/M001-T01-handoff.md):
`4aa38b15a7a0a2fc7160b8d2f86cf03a92c4bdd49756700a348ed21a16d56013`.
Locations below refer to that version; later revisions need their own hash.

## Recommendation

**Ready for a bounded real-example trial once the two clarifications below are
recorded in the reviewed guide or the T02 assignment.** No blocking design defect
was found. Both findings are Required clarifications for the recommended example,
not requests to redesign the guide or settle later evaluation policy.

The contract supports an honest partial case, source-linked attribution and
uncertain chronology. One real example is the appropriate next test of whether
those rules are usable. This review does not establish source feasibility,
freeze the curation guide, complete AC01 or accept M001. Dheeraj's meaning
acceptance remains separate; Records records the disposition/version and Manager
assigns T02 through the existing checkpoint.

## Findings and proposed corrections

### DOM-T01-01 — Clarify evidence for the first cost–margin walkthrough

**Severity:** Required clarification of T02 inclusion instructions.  
**Locations:** Guide §3, lines 67–79; §5, lines 147–149; §9, lines 248–253.

**Evidence:** The admission rule allows a draft case with supported pressure
and a reported margin effect, and correctly prohibits claiming a connection
from co-occurrence. It does not explicitly distinguish that permissible partial
draft from the preferred first walkthrough of the accepted cost–margin mechanism.
The specification requires agreed example inclusion rules before T02.

**Effect on the example:** A curator could select a group-wide freight-cost
statement and a segment margin decline, record both accurately, and still lack
support that they describe the same situation. That would test source capture
but leave the central relationship untested. Conversely, “margin effect” should
not inadvertently require a numerical driver estimate or a headline margin
decline when the source reports cost pressure offset by other contributors.

**Proposed wording for the T02 instructions:**

> Select source passages that support relevant input-cost pressure and a reported
> margin effect or headwind, with compatible business scope and periods, plus a
> supported relationship between them. A qualified management attribution is
> sufficient; preserve its speaker and qualifications. Qualitative support is
> allowed: neither a quantified cost contribution nor a net margin decline is
> mandatory. If scopes or periods differ, require source support for the linkage.
> If only co-occurrence is supported, retain a partial lead with the relationship
> unknown; do not present it as a demonstrated input-cost/margin mechanism.

This is a recommendation for selecting the **first example**, not a new universal
corpus-admission rule. Contrasts and incomplete leads remain valid records under
the guide. Responses, rationale, pricing constraints, volume detail and follow-up
may remain explicitly unknown; no successful outcome is required.

**Resolution evidence:** The revised instructions state this distinction. The
eventual walkthrough separately maps pressure, reported effect and attributed
relationship to passages, with their scope/period and claim kind. It preserves
other reported drivers and does not turn an attributed explanation into causal
proof. A profit-only statement remains labelled as profit; it cannot silently
substitute for a margin measure under §7.

### DOM-T01-02 — Make H1's action-date distinction explicit

**Severity:** Required clarification of the worked example.  
**Locations:** Guide §6, lines 153–157; H1, lines 198–206.

**Evidence:** H1 supplies reporting periods and publication dates and places an
announcement statement at H-U02 and an implementation statement at H-U03. Its
instruction to retain both dates does not explicitly identify these as statement
availability dates. No effective implementation date appears in the teaching
content. The general two-clock rule is already correct; the example needs to
demonstrate it unambiguously.

**Effect on the example:** Copying H1 into an action worksheet could wrongly use
2020-11-10 as the effective implementation date, or assign implementation to Q3
solely because the report covers Q3. The real example may likewise report that
pricing was implemented without saying when it took effect.

**Proposed addition after H1's action paragraph:**

> H-U02's announcement statement became publicly available on 2020-08-10;
> H-U03's implementation statement became publicly available on 2020-11-10.
> These publication dates are not automatically the announcement event date or
> the effective implementation date. The hypothetical content supplies no exact
> action-event dates; preserve those as unspecified. Use an event interval only
> if the statement supports it, and record that support separately from the
> reporting period and publication date.

**Resolution evidence:** H1 explicitly separates statement availability from
action-event timing. The real action record either cites an effective date or
supported interval, or records an unknown with the checked passage. Implementation
status may be supported while its effective date remains unknown.

## Areas needing no correction for this example

| Reviewed area | Assessment and practical limit |
| --- | --- |
| Episode/update boundaries — §2 and H1 | Correctly keeps four explicitly continuing disclosures in one episode and preserves separate updates. An action change alone does not split the episode. A first real case need not have four quarterly reports; the number is illustrative. |
| Reporting gaps — §2 and H2 | Correctly retains pending association and identity review without inventing continuity, resolution or a second reviewed episode. If a gap appears in the selected example, record the bounded sources checked and remaining uncertainty; an inconclusive check need not become an unrestricted history search. |
| H2's unknown reason | `not_checked` fits its stated unchecked gap. After a bounded check, update the reason to reflect the actual result, such as `ambiguous` continuity or `unavailable_source`, while retaining unresolved identity. §§2/5 already permit this. |
| Claim attribution — §4 | Separates observation, management attribution, intention, implementation, stated rationale and analyst interpretation. One source passage can support multiple separately typed claims; retain qualifiers and scope. No new claim category is needed to try T02. |
| Historical unknowns — §5 and H3 | Correctly distinguishes checked-but-unreported evidence from unexamined evidence. H3 changes the query objective without inventing a retailer constraint or action for Elm. No ranking label is needed for T02. |
| Dates and metrics — §§6–7 and H1 | Keeps reporting/publication/event time and metric scope/basis distinct. H-D04 is unavailable at the example cutoff despite its completed reporting period. The illustrative −3 pp/−300 bp/−10% arithmetic is correct. The action-date clarification above closes the example's remaining ambiguity. |
| Responses, rationale and follow-up | Their absence is explicit rather than filled with plausible facts. Stated reasoning remains separate from interpretation; subsequent recovery does not establish response effectiveness. An example can be complete as a worksheet while these sections remain unknown. |

These are guide-level assessments, not claims that the hypothetical inputs have
real source support. H1–H3 remain teaching examples and contribute no pilot cases.

## Bounded next handoff and verification

**Implementation/Records:** Incorporate or explicitly disposition DOM-T01-01/02,
record the reviewed guide version/hash and return any remaining example-specific
ambiguity. For T02, retain the existing access/terms checks, exact passages and
locators, date basis, metric definitions, checked-source unknowns and effort log.
If the selected lead lacks the recommended relationship support, report the
shortfall rather than add an inferred causal claim. No second analogue is needed.

**Manager/Dheeraj:** Use this recommendation for the existing guide-meaning
checkpoint and the scoped T02 assignment. This document does not record a user
answer, authorize acquisition or change module lifecycle state.

Read PROJECT_TRACK.md, STATUS.md, the current M001 specification, the guide and
T01 handoff; consulted the relevant D012–D014 entries and Manager handoff.
Verified the branch/base and guide hash; inspected H1–H3 against the stated rules
and checked the hypothetical date ordering and margin arithmetic. Checked this
review's local document links and Markdown formatting. No acquisition, live
source inspection, empirical domain validation, application tests or code review
was performed. Only this review note was added; the guide, specification,
decision register and module status remain unchanged.
