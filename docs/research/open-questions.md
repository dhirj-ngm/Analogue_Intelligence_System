# Questions and experimental concerns

**Updated:** 9 October 2026  
**State:** User direction recorded in D012/D013; operational evaluation choices
remain open where listed below

Dheeraj has responded to Q01–Q11. Accepted direction and the delegated first
investigation are recorded in D012/D013 in [DECISIONS.md](../../DECISIONS.md).
The [Manager handoff](../workflow/manager-direction-handoff.md) separates each
answer from the remaining technical policy. Records/Domain should work from
those answers without treating conversational preferences as a complete
experimental protocol. Original concerns below are retained for their reasoning.

Product-first case learning, relevant clarifying questions, linked episode
updates, failures/mixed outcomes, labelled partial matches, later gap-driven AI
and checkpoint-based code review are established direction. Minimum evidence,
episode splits, date modes, independent judgements, information controls and
numeric thresholds remain operational questions. Ask only what the next task
requires; the user has delegated the first detailed FMCG scenario to Manager.

D014 subsequently authorizes the record repair and T01 guide work. The
[guide v0.1](../../data/annotation_guide.md) now supplies concrete proposals and
examples for Q02/Q03 review. Use its [checkpoint](../workflow/M001-T01-handoff.md)
for the next action; the old scope/startup agreement is no longer pending.

## Q01 — What makes a comparison useful?

Is the query investigating margin drivers, pricing responses, operational
constraints or another bounded question? The same case can have different
relevance for different objectives. Define the pilot objective and give examples
of useful and disqualifying evidence before assigning relevance grades.

## Q02 — Where does an episode begin and end?

Define how quarterly updates, continuing pressure, changing responses and shared
global shocks affect episode identity. Avoid counting passages as independent
cases. Record company, period, shock family and duplicate relationships.

## Q03 — Unknown evidence versus documented mismatch

How should absent context affect ranking and presentation? Missing pricing data
does not establish low pricing power. Missing mechanism evidence is not proof
of a different mechanism. Propose explicit unknowns and justified mismatch rules.

## Q04 — Better information versus better structure

A manually annotated structural method may receive information absent from a
raw-text baseline. Consider controls using raw text, normalized episode summaries,
summaries plus mechanism tags, and the same information plus directed relations.
The final experiment design and information budgets remain open.

## Q05 — Independent relevance judgements

If grades depend only on our feature tags, a tag-based scorer may succeed by
construction. Judge usefulness, evidence and material differences; fix rules
before results and blind reviewers to method where practical. Determine a second
human reviewer's availability and record disagreements or solo-review limits.
Model agreement alone is not independent domain validation.

## Q06 — Difficult negatives and insufficient evidence

Include similar wording with different pressures, similar pressures with different
constraints, partial evidence and queries without a strong analogue. Define how
the product reports an inadequate corpus. Avoid assuming every query has five
useful answers. Thresholds require evidence rather than arbitrary confidence.

## Q07 — Date rules and leakage

Define retrospective versus as-of-date investigation. Check publication cutoffs,
restatements, revised indicators, duplicate episodes and shared shock families.
Keep later outcomes out of the first similarity representation. A pretrained
generative model may know later events; constrain its claims to cited admissible
evidence and report the limitation instead of assuming time filtering removes
all knowledge contamination.

## Q08 — Curation effort and selection bias

Measure time per usable episode, missing fields, source access, review effort and
disagreement. Include unsuccessful, mixed and unresolved cases where supported;
a corpus of only recovery stories can mislead readers about response effectiveness.
Choose scale and schedule from measured effort and available hours.

## Q09 — Product usefulness and research claims

Which reader task will the demo support? How will evidence access, differences
and weak-match recognition be assessed? Ten episodes/five queries support a
pilot, not broad superiority. The structural hypothesis may fail while the
case-study workspace still provides useful evidence access.

## Q10 — Custom AI responsibility and tooling

Dheeraj intends a later custom AI component. Should it detect cost statements,
extract mechanisms, interpret hints or rerank candidates? What measured gap,
labels and held-out checks justify it? What exact tool or method is meant by
`jev`? Keep this unresolved instead of substituting a guessed architecture.

## Q11 — Review and process effort

Start with meaningful tests, static checks and an independent Codex review.
CodeRabbit is an optional additional reviewer when PR workflow and its findings
justify the overhead. Code, data/method and domain acceptance are distinct checks.
Keep the working documents proportional to useful decisions and artifacts.

## Recording a resolution

For a resolved question, add the answer, date, supporting evidence, decision ID
and affected specification. Preserve alternative reasoning. For a provisional
answer, state what observation would confirm or revise it. Do not turn a
discussion example into a real dataset record without source verification.
