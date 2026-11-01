# M008 frozen relevance evaluation plan

Freeze before collecting judgements: commit the queries, this plan, plan.json and
hashes of the current seventeen-case collection, search dependencies and app.
No case, ranking, query or metric changes during this evaluation. Investigate
failures as proposed future work. Historical labels are never M008 answers.

Ten realistic prompts cover named inputs, falling costs, multiple simultaneous
pressures, an uncovered input, an outside business and two historical information
dates. Builder selected them with knowledge of the collection; they are not an
independent or representative query sample. There are no expected relevance
answers. Search runs the frozen current method, with its actual first-five limit,
publication/period checks and self/continuation exclusions.

## Independent review

One independent human reviewer is the minimum small study; two are preferable
for observing disagreements. They must not have created the cases or search rules,
must not be Builder/the user, and must not use AI-generated relevance labels.
Record prior exposure to project labels and exclude exposed/non-independent
submissions from human metrics. Confirm identity/independence through an authorized
human contact channel, not merely a checkbox in a downloaded form. A self-attestation
alone does not verify a human. No contacting a new person or using a paid service
without the specific user authorization required in this session.

Present every eligible case for each query, shuffled deterministically. Judging the
entire eligible pool permits within-collection omissions to be measured, including
queries where the app shows no results. Reviewer material contains query dates,
source-linked case evidence, scope, reported actions/figures, differences and
unknowns. It contains no ranking, score, match explanation, expected answer,
returned/not-returned flag, original case ID or historical evaluation link. The
coordinator's mapping and results are separate and must not be sent to reviewers.
Original documents remain external. The reviewer can inspect them, mark source
access failures and identify factual ambiguities without altering frozen records.

For every query/case pair ask:

- Is this a **useful**, **partly useful**, **not useful** or **unsure** comparison?
  Useful helps analyse the stated situation with explainable differences; partly
  useful covers a limited aspect or important contrast. A shared word alone is
  insufficient. Neither label asserts that a company action would work elsewhere.
- Why? Name the matching issue and important differences or evidence gaps.
- Would presenting this as a comparison mislead a reader: **yes**, **no**, **unsure**?
  Explain yes/unsure. This is separate from usefulness.
- Was an original source **opened**, **not opened** or **unavailable**? Explain
  unavailable. Record remaining uncertainty in the rationale.

For each query ask whether the supplied eligible collection is **adequate**,
**limited**, **none** or **unsure**, why, and what case/source may be missing.
Outside-collection suggestions remain reviewer suggestions, not verified new cases.
The form supports saving/restoring drafts and exporting partial responses.
Unjudged rows are missing data, never implicit negative judgements.

## Admission and analysis fixed in advance

Preserve raw human submissions separately, with packet hash and pseudonymous
reviewer ID. A local registry records human identity verification, independence,
authorization reference and authenticated response provenance. Do not put personal
contact details in Git. Registry records and channel receipts are coordinator
evidence, not something inferred by analysis from text. Check for altered query/
case IDs, duplicate responses, wrong packet hashes, missing rationales, invalid
categories, and lack of human/independence verification. Exclude ineligible
submissions explicitly; never relabel AI or synthetic tests as human responses.

Report each reviewer's judgements separately. For fully judged queries calculate:

- Count useful / partly useful / not useful / unsure among displayed results and
  misleading yes/no/unsure, with actual displayed and judged denominators.
- Strict useful share of displayed results = useful / displayed count; undefined
  when the app displays none. Report partial/unsure separately, without dropping
  them from the denominator or silently treating them as correct.
- Within-eligible-pool recall = displayed useful / all useful in that query's
  judged eligible pool. Undefined if there are no useful cases. This is not recall
  of history or a measurement of missing companies outside the collection.
- List useful omitted cases; flag an empty app result when any eligible case is
  judged useful. For empty results with no useful case distinguish uncertainty
  and partial usefulness; do not infer universal absence of a comparison.

For incomplete queries report observed labels and missing counts only; do not
estimate full-query precision/recall. For a complete reviewer give micro counts
across queries and useful share with its numerator/denominator. No population
claim, statistical significance or general quality improvement is inferred.
Keep reviewer rationales, query coverage notes and source problems alongside
counts. Report disagreements on shared judged pairs with original labels and
rationales; do not majority-vote away uncertainty. With one reviewer disagreement
is unmeasured, not zero. With no verified independent reviewer all human measures
are unavailable and M008 remains pending, regardless of code/test success.

No authorized independent reviewer/channel is currently established in the repo.
Prepare the complete blinded packet, invitation text, response format and analysis
code before asking the user for only the contact/access authorization needed.
