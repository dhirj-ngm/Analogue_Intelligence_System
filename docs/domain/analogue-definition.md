# What counts as a useful historical analogue?

**Recorded:** 9 October 2026  
**Owner:** Domain and Research discussion  
**State:** Discussion draft v0.1 — proposed terminology and comparison reasoning.
**Not an approved annotation guide, relevance rubric, evaluation policy or module
specification.** Hypothetical examples are not dataset entries or judged pairs.

Basis: [PROJECT_BRIEF.md](../../PROJECT_BRIEF.md), accepted D001–D005/D008,
the [M001 draft](../modules/M001-data-viability-pilot.md), and Q01–Q09 in
[open questions](../research/open-questions.md). See also
[mechanism notes](input-cost-margin-mechanisms.md) and
[Manager/Records handoff](manager-records-handoff.md).

**Current use:** D013 subsequently selected the first investigation. The
[annotation guide v0.1](../../data/annotation_guide.md), drafted under D014,
turns these discussions into a reviewable T01 contract. This note remains
supporting reasoning, not a competing guide or a request to reselect the objective.

## Proposed working definition

A historical analogue is an earlier company episode whose supported relationships
and relevant conditions help investigate a specified question about a target
situation. The comparison must explain the match, consequential differences,
unknowns and evidence limits. Usefulness belongs to the question–candidate pair,
not permanently to the candidate company or case.

“Earlier” requires an agreed historical-ordering rule. Publication by a query
cutoff alone does not prove an episode preceded the target. Overlapping episodes,
continuing pressures and unknown dates remain unresolved under Q07.

An analogue can help organize a question, locate evidence, identify an alternative
explanation or illustrate a documented trade-off. It does not imply identical
conditions, identical responses, identified causality or predictable success.
No shared outcome or recovery is required.

The theoretical motivation is relational comparison: Gentner distinguishes
mapping relationships from merely sharing attributes, and emphasizes connected
systems of relations. This motivates inspecting supported patterns in this
domain; it does not validate our labels, scoring method or causal claims.
[Gentner (1983), especially pp. 156–163](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf).

## Terminology for critique

| Term | Proposed meaning | Boundary or caution |
| --- | --- | --- |
| Investigation question | What the reader wants the comparison to illuminate | “Find similar firms” does not specify which mechanism or trade-off matters |
| Target situation | Company conditions supported by the query's admissible evidence | Hints may leave important conditions unknown; do not silently complete them |
| Episode | A bounded company situation and its linked evidence across a stated interval | A passage, document or quarter is not automatically one episode |
| Case study | A readable presentation of an episode's supported challenge, response, reasoning and follow-up | A section may be unknown; presentation does not add evidence |
| Shock/pressure | A change or burden potentially affecting the firm | Distinguish external price movement, firm exposure and recognized expense |
| Mechanism | A proposed or reported relationship connecting conditions and effects | Store attribution; a plausible explanation is not a demonstrated cause |
| Context | Conditions that affect interpretation of the relationship | Category, geography and firm identity matter when they alter the question |
| Constraint | A documented limit on a feasible response in that period | Missing action evidence is not constraint evidence |
| Response | An announced or implemented company action | Preserve announcement, timing, scope and implementation evidence separately |
| Stated rationale/principle | Management's sourced reasoning or expressed operating commitment | A statement is not proof it governed every decision; silence is not lack of reasoning |
| Inferred principle | An analyst/system interpretation of a pattern | Separate its author, evidence and alternatives from stated management reasoning |
| Follow-up observation | A dated subsequent development or metric | “Observed after” does not mean “caused by” |
| Useful analogue | A supported comparison relevant to the particular question | Can be partial and can have materially different responses/outcomes |
| Superficial match | Shared wording, attributes or symptoms with little support for the relevant relationship | May still help a terminology search or a different investigation |
| Contrast case | Supported alternative mechanism or constraint that helps discriminate explanations | Educational value is distinct from positive analogue relevance |
| Insufficient evidence | Available admissible sources do not support a needed comparison claim | It is not evidence of incompatibility or absence of an action |

This vocabulary is conceptual. It does not require a new database table or an
expanded label inventory. M001-T01/Records should translate accepted distinctions
into the smallest usable annotation contract.

## Preserve the kind of claim

| Claim kind | Hypothetical illustration | What it establishes |
| --- | --- | --- |
| Source-reported metric/observation | An annual report discloses gross margin of 28% | What the source reports under its period/scope/basis; not necessarily independently audited at this claim level |
| Management attribution | Management says packaging costs contributed to the decline | A sourced management explanation, not an independently identified cause |
| Forecast/intention | Management plans a price increase next quarter | A stated plan, not implementation or realized price |
| Documented implemented action | A later release reports the increase took effect | Source support for implementation; magnitude/coverage may still be unclear |
| Analyst interpretation | A reader interprets delay as protecting retailer relations | A labelled interpretation requiring evidence and alternatives |
| Hypothesis | Delayed pricing may explain part of margin pressure | A proposition to investigate; not a factual relationship to fill into the graph |
| Accepted project choice | D003 separates later outcomes from first-experiment similarity | A design requirement, not a business-world finding |

“Sourced” describes provenance, not automatic truth. Annotator review and
automatic extraction status are separate from these claim kinds. Preserve
contrary passages and source scope; later contradictory evidence should not
overwrite what was stated at an earlier date.

## Comparison dimensions

No fixed weights or mandatory completeness threshold is proposed. Choose which
dimensions matter from the investigation objective and available evidence.

| Dimension | What to compare | Why a match can fail |
| --- | --- | --- |
| Pressure and exposure | Input basket, magnitude/direction, purchased versus benchmark costs | Both mention inflation but only one has material exposure |
| Reported effect | Gross/operating margin or profit; recognized cost and attributed contributors | Same symptom comes from demand, mix or exceptional charges |
| Demand/volume | Shipment definition, category demand, availability, channel inventory | One has stockouts; another has weak sell-through |
| Pricing conditions | Realized pricing, contracts, promotions, competitors, affordability | One can reprice promptly; another documents a delay |
| Productivity/operations | Programme status, savings basis, capacity and implementation costs | “Savings” refer to different baselines or different expense scopes |
| Other constraints | Supplier qualification, cash, regulatory/product or retailer limits | Response options are materially different despite similar cost pressure |
| Company/business context | Category, channels, geography, integration and business scope | Own-company history predates a portfolio change; group aggregates hide a segment |
| Timing | Shock onset, recognition lag, pricing lag, duration, seasonal/fiscal comparators | Annual averages hide sequencing; overlapping cases may not be earlier |
| Metric basis | Units, percent/basis-point changes, period, GAAP/adjusted, group/segment | Gross and adjusted operating margin are not interchangeable |
| Evidence | Passage support, publication date, review status, disagreement and missingness | Attractive narrative is unsupported or available only after the cutoff |
| Responses/rationales/follow-up | What the historical company did, said and subsequently reported | Useful display evidence can be forbidden ranking evidence; recovery proves no response effect |

Own-company and cross-company episodes follow the same evidence standards.
Identity alone is insufficient to declare either useful. Separate company cases
within one broad shock may be valid comparisons while remaining dependent
observations. Ten company episodes need not be ten independent shock experiments.

## Three hypothetical examples — entirely invented

The target is **Company Cedar**, a packaged household-products business. At the
query cutoff it reports increased resin/packaging costs, a gross-margin decline
from 30% to 27%, and little shipment-volume change. Management attributes part
of the decline to those costs and says a retailer agreement delays net pricing
changes. Assume these statements have contemporaneous passage support. No
response success is known or assumed.

### H-A: a useful historical analogue

Earlier **Company Birch** sells packaged personal-care products. Its disclosures
report resin-cost pressure, a gross-margin decline, broadly stable shipments and
a contractual delay before repricing. Management attributes part of the pressure
to packaging costs and timing. Historical follow-up separately reports a net
price change and a waste-reduction programme, a stated aim of limiting disruption
to customer agreements, and subsequent margin improvement alongside lower resin
costs. Every assertion is hypothetical and assumed to have dated support.

Birch is useful for investigating how reported input exposure and delayed price
realization coexist with margin pressure. Different category, packaging intensity
and customer arrangements limit transfer. The later improvement cannot identify
the programme's effect because prices, input costs and other conditions changed.

An earlier **Cedar** episode with the same supported pattern could also be useful.
Before preferring it, check whether Cedar's portfolio, channels and pricing
agreements have changed. Own history does not remove the need for comparison.

### H-B: a superficial match, potentially a useful contrast

Earlier **Company Ash** also reports “inflation,” “margin pressure” and “cost
savings.” Its comparable-scope disclosure says its material input costs were
stable; management instead attributes margin pressure mainly to sharply lower
shipments and factory underutilization. Its disclosed pricing conditions differ
from Cedar's delay.

For a question about packaging inflation with stable shipments, the shared
wording hides a different reported relationship. Ash is a weak analogue but a
useful contrast for checking alternative margin drivers. For a question about
how lower volume affects fixed-cost absorption, Ash may be more useful than
Birch. Stable inputs do not prove demand is the only driver; retain qualifiers.

### H-C: insufficient evidence

Earlier **Company Elm** reports “challenging cost conditions” and a lower
adjusted operating margin. It provides no supported input breakdown, comparable
gross margin, volume detail, repricing constraints or implemented response in
the admissible sources examined.

Elm is a source lead. Its wording does not establish Cedar's cost pathway,
pricing power or action history. The correct explanation is that the needed
evidence is unavailable, specifying sources/fields checked. It is not a proven
nonmatch, and its adjusted operating margin cannot stand in for gross margin.
Later documents might improve the evidence for a retrospective study; they
cannot be backdated into the original query representation.

### Usefulness changes with the question

| Investigation objective | H-A: Birch | H-B: Ash | H-C: Elm |
| --- | --- | --- | --- |
| Understand input-cost pressure with a repricing lag | Useful relationship/context comparison with explicit differences | Weak analogue; supported alternative-driver contrast | Insufficient evidence for the relationship |
| Inspect responses taken under a documented pricing delay | Useful dated response catalogue after challenge-based retrieval; transfer remains limited | Reported conditions do not support the same response constraint | Implementation/constraint unknown |
| Investigate volume-led fixed-cost absorption | Limited by stable-volume context | Useful for its reported volume/utilization relationship | Volume/utilization unknown |
| Establish that a response caused recovery | Follow-up does not establish the counterfactual | Follow-up would not establish it either | Evidence inadequate even for describing the proposed response |

This table contains discussion judgements, not 0–3 benchmark grades. The response
catalogue question does not change D003's first-experiment feature restrictions.
An action-conditioned retrieval experiment would require a separate task and
information-budget decision. No candidate proves causal effectiveness here.

## Disqualifying evidence, differences and unknowns

Separate three issues before proposing a relevance grade:

1. **Admissibility failure:** the query episode itself, a near duplicate, evidence
   unavailable under the chosen cutoff, or a candidate that fails the agreed
   historical ordering. These are eligibility matters under accepted direction;
   their operational rules remain to be agreed in M001-T05.
2. **Documented incompatibility for this claim/question:** comparable evidence
   contradicts a required exposure, mechanism or response constraint. H-B's
   stable inputs disqualify the assertion that its packaging-cost pathway matches
   Cedar's, while leaving its value as a contrast. If a question requires a
   documented pricing delay, evidence of immediate repricing defeats that match
   dimension. Incompatibility need not exclude the whole case for every purpose.
3. **Insufficient support:** missing dates, missing driver evidence, mismatched
   metric basis or missing constraint detail can prevent a defensible comparison.
   Missing information does not become a documented contradiction. Unknown dates
   require a chosen eligibility policy; none is adopted here.

Different firm sizes, commodities or geographies are not automatic disqualifiers.
Explain whether they affect the question. Contradiction must concern compatible
scope/time; group and segment statements can differ without contradicting one
another. An unsourced analyst summary cannot establish a missing mechanism.

Display unknown/not reported, conflicting evidence and documented mismatch
distinctly. Describe what was checked before saying “not found.” Do not substitute
zero, an average or a guessed constraint. Numeric scoring penalties, relevance
labels for unjudgeable cases and abstention thresholds remain Q03/Q06 decisions.

## Proposed episode-boundary reasoning for M001-T01

An episode is company-specific and bounded by the situation being investigated,
not by paragraph counts. Preserve explicit source intervals and uncertainty.
Do not invent a precise onset when the earliest report only describes ongoing
pressure. A shared shock identifier groups related episodes without merging
different companies into one company record.

Hypothetical boundary examples for critique:

- Cedar's quarterly update reports continuing resin pressure and progress on
  the same response. Candidate treatment: append evidence to the same episode;
  keep the evidence/publication sequence rather than create another case.
- Cedar starts implementing repricing during the continuing pressure. Candidate
  treatment: an action within the episode; a changed response alone need not split it.
- A later plant shutdown introduces a materially different capacity/volume
  situation. Candidate treatment: consider a linked episode or subepisode if it
  answers a distinct question and can be supported separately. Record the reason,
  overlap and shared context; do not count independence by fiat.
- A later new cost shock follows a documented interval of changed conditions.
  Candidate treatment: consider a new linked episode. No fixed quiet-period or
  quarter threshold is selected.
- Birch and Cedar face the same resin shock. Candidate treatment: distinct company
  episodes, shared shock dependence. Different companies alone do not justify a
  held-out independence claim.

These are proposed heuristics requiring real-example revision at T02. Records
should settle identity, split/merge/update rules before counting the pilot corpus.
Question-specific comparisons should not silently give one episode multiple
identities or duplicate its evidence across evaluation partitions.

## Open questions and proposed next discussion

| Concern | What remains undecided | When it becomes necessary |
| --- | --- | --- |
| Q01: usefulness | D013 settles the first objective; necessary versus helpful context and contrast handling still need query-specific examples | T01 meaning review, then T05 rubric |
| Q02: identity | Onset/end uncertainty, split/merge rules, overlaps and shared shocks | T01 critique, revise with T02 example |
| Q03/Q06: evidence | Minimum support by claim/purpose, conflict handling, unjudgeable versus irrelevant | T01/T02 evidence contract; T05 ranking/judgement policy |
| Q04/Q05: validity | Matched information budgets and judgements not defined by model features | Before structural comparisons; relevance rules before rankings |
| Q07: time | As-of versus retrospective mode, earlier-ordering rule, uncertain dates/restatements and contemporaneous response text | Before T05 freeze |
| Q08/Q09: usefulness | Diversity, negative/mixed cases, review effort and reader feedback | Source/corpus pilot and feasibility report |
| Q10: ambition | Bounded custom AI task and identity of `jev` | Later evidence-based design; not needed for these notes |

The original proposed objective was: **compare reported input-cost margin pressure
and pricing conditions, then inspect documented responses and stated reasoning**.
D013 now supplies the accepted materials/packaging/logistics-cost margin question,
with pricing and volume included where supported. Use that decision for the guide;
retain this earlier wording only as the proposal's reasoning. Later experimental
concerns remain deferred to their relevant checkpoints.
