# M001-T02 — One real source-to-case walkthrough

**Recorded:** 9 October 2026, Asia/Kolkata  
**Episode:** `EP-CL-APAC-2022Q4-001` — Colgate-Palmolive, Asia Pacific, Q4 2022  
**Guide/schema:** Guide 0.2 / `m001-t02-trial-0.1`  
**State:** Assistant-curated draft; author checks passed; human meaning review pending

## The case and why this source

Colgate's Asia Pacific division reports operating margin of 26.0% for Q4 2022,
with a year-over-year fall of 220 basis points. The issuer attributes the decline
primarily to materials and packaging inflation. It also identifies partial
offsets from pricing, programme savings, advertising and overhead changes, while
noting increased logistics costs. This is an attributed explanation, not an
identified causal effect or a single-driver decomposition.

The [official earnings release](https://investor.colgatepalmolive.com/news-releases/news-release-details/colgate-announces-4th-quarter-and-full-year-2022-results)
was published on 27 January 2023. Its divisional introduction explicitly compares
Q4 2022 with Q4 2021. Selecting this divisional case keeps the cost narrative and
margin measure in the same scope and period; group-wide annual gross margin and
other divisions are not substituted. The release was an existing project lead,
not a new firm/window sampling plan. One accessible document suffices for this
bounded trial; no second analogue or subsequent source was acquired.

## Open the evidence and follow the references

Canonical records are [the source manifest](../source_manifest.jsonl) and
[the episode dataset](../episodes.jsonl). Evidence text is stored once in the
episode; the tables here refer to those span IDs rather than reproduce quotations.

| Case element | Claim / evidence | Full-context locator and interpretation |
| --- | --- | --- |
| Cost pressure and reported relationship | CL-CL-APAC-001 / SP-CL-APAC-001, SP-CL-APAC-002 | Divisional Performance → Asia Pacific (15% of Company Sales) → second bullet. Preserve issuer attribution, primary contributor wording and partial offsets. |
| Reported margin effect | CL-CL-APAC-002 / SP-CL-APAC-005 | Fourth Quarter Operating Profit By Division → Asia Pacific row; read the column headings. Margin level and margin change are separate from the profit amount and profit growth columns. |
| Pricing response evidence | CL-CL-APAC-003 / SP-CL-APAC-003 | Same divisional bullet. Realized higher pricing is reported; no specific price announcement or effective date is established. |
| Savings response evidence | CL-CL-APAC-004 / SP-CL-APAC-004 | Same bullet. Programme-associated savings are reported; detailed operational interventions and timing remain unknown. |
| Other contributors / qualification | CL-CL-APAC-005 / SP-CL-APAC-002 | Inspect the complete second bullet, not this small offset excerpt alone. Its context hash and locator identify the full statement containing other contributors. |

Five excerpts retain 23 source words in total. They are intentionally short;
four are fragments of one mixed driver paragraph, not complete standalone
evidence paragraphs. The exact text, section, HTML element, inspected line,
normalized-context SHA-256 and character offsets are in each span. Offsets are
zero-based Unicode characters with exclusive ends after HTML entity decoding,
descendant-text concatenation and whitespace collapse. Case and punctuation are
unchanged. Line numbers supplement semantic locators and may move on refetch.
Open the linked release and inspect the complete paragraph/row for qualifications.

## Dates, identity and metrics

The observed interval is 1 October–31 December 2022; the comparator is the same
quarter of 2021. The release date is 27 January 2023, corroborated by its dateline,
date heading and JSON-LD metadata. The page's unrelated current quote/widget date
is excluded. Retrieval was `2026-10-08T23:56:50.033396+00:00`, measured from the
saved response body's filesystem timestamp. The manifest distinguishes a current
inspected page from an unchanged historical archive, which was not verified.

The actual pressure onset and end are unknown. This single observation/update
does not prove that Q4 was the entire episode, that the pressure ended, or that
it was independent of other firms' shocks. No named shared shock is inferred.
Pricing/savings effect statements concern Q4; their January publication date is
neither an announcement-event date nor an implementation-effective date.

| Metric | Value / unit | Definition, scope and basis |
| --- | --- | --- |
| Operating margin level | 26.0 percent | Divisional operating profit divided by divisional net sales; Q4 2022, Asia Pacific, issuer-reported unstarred row |
| Operating-margin change | −220 basis points | Reported change versus Q4 2021 in the same division; −2.2 percentage points, not −220 percent |

The figures are reported, not derived estimates. Table 5's segment data are
unaudited. The row is not labelled Base Business; do not silently describe this
segment measure as consolidated GAAP gross margin. Rounded table amounts need
not recreate a separately reported rounded change exactly. No numerical cost
contribution, exact price/volume decomposition or response-effect estimate is
manufactured.

## Responses, rationale and follow-up unknowns

Fourteen explicit missing-value objects distinguish checked-but-unreported,
unchecked and ambiguous evidence, and record the checked sections. Specific
pricing interventions, product/customer coverage, retailer constraints and
effective dates remain unknown. No absence is converted to weak pricing power,
no action, zero cost or a mismatch. Group-wide CEO remarks are not transferred
into a rationale for a divisional action. Later realized observations have not
been checked. The release's 2023 guidance is a forecast, not a recovery.

## Proposed investigation, comparison and information boundary

Proposed question: which earlier company situations help investigate
materials/packaging-cost operating-margin pressure with multiple reported
offsets? After challenge-based retrieval, inspect their documented responses,
stated rationale and differences in division, cost exposure, period and metric
basis. This is a question sketch, not a benchmark query or relevance grade.
There is no second case here and therefore no demonstrated analogue comparison.

Claims 001/002 are challenge-only candidates for a later representation;
claims 003–005 are display-only because they contain responses and offsets.
No ranking text is generated or frozen. Copying the full source driver paragraph
would import response information into similarity features. T05 must still
settle cutoff semantics, historical ordering, unknown-date eligibility,
self/duplicate exclusions and contemporaneous-response treatment. Neither this
case nor a partial comparison is automatically an eligible candidate.

## Actual access and retention checks

The release returned HTTP 200 on one direct HTTPS GET without authentication.
A web-tool open timed out despite the direct request succeeding; indexed search
access is distinguished from actual document access in the manifest.

The release footer links to [Colgate's Terms of Use](https://www.colgatepalmolive.com/en-us/legal-privacy-policy/terms-of-use).
That page returned HTTP 200 but serves a wrapper whose operative OneTrust notice
URL returned HTTP 404 (`curl` exit 22). Official-page indexed terms describe
personal/noncommercial use, reserved IP rights and copying/distribution
restrictions; that indexed text is not a verified current full notice. Full
retention and redistribution clearance therefore remain unresolved.

No full HTML/PDF is stored in the repository or claimed as a permitted archive.
Only local factual annotation, minimal attributed excerpts, locators and observed
hashes are retained; temporary inspection bodies are discarded after checks.
This does not assert an open licence or public redistribution permission.
Reproduction requires refetching the source, which may change or become unavailable.
This limitation affects archival/public reuse, rather than changing the case's
business meaning; Domain can inspect the public page directly.

## Guide findings and schema problems exposed

DOM-T01-01 is applied in guide §9: first-example linkage must be supported in
compatible scope/period, while partial leads and qualitative headwinds remain
allowed. The selected division supplies an attributed relationship and a margin
measure. DOM-T01-02 is applied in H1: action statement availability and effective
timing are distinct. Neither resolution is labelled human acceptance.

The real example prompted guide 0.2's further working clarifications: current
page hashes do not establish historical immutability; short excerpts need full
context locators and declared offsets; table headings/basis/rounding survive
serialization; and reported response effects do not reveal exact interventions.
JSONL uses nested evidence and worksheet sections to keep one canonical example.
The trial schema is reversible and not a final M002 storage choice. Domain should
assess whether the bounded observation/unknown onset and excerpt-context approach
make the case usable before Records freezes a curation version.

## Effort and actual verification

EFF-M001-T02-001 measures the observed working envelope from
`2026-10-08 23:56:25 UTC` to `2026-10-09 00:01:11 UTC`: **286 seconds / 4 minutes
46 seconds**, from the first recorded clock observation through the first passing
record checks. It includes source access investigation, guide revision,
annotation and checks, following initial repository reading. It excludes later
handoff/status writing and does not estimate active annotation-only time or
human review effort. Active curation-only time and human review time are unknown;
no human review was performed. This single assistant-assisted trial is not a
human curation-time benchmark or a ten-case effort projection.

Author checks used temporary standard-library inspections, with no network
calls during record validation: one source/episode; five exact excerpt/context
hash/offset matches; five claim references and action/update/metric references;
publication after reporting end; two reported units/definitions; −220 bp =
−2.2 pp; fourteen explicit unknowns; distinct challenge/display lineage; no
frozen ranking text, human-review claim or full-source repository cache.

An initial authoring assertion expected 24 excerpt words; recounting found 23
and corrected that expectation before records were written. A notice-inspection
attempt failed because the 404 response produced no file; the missing body is
recorded as a terms failure, not a successfully inspected notice. Subsequent
record checks passed. No application code, persistent utility or runtime was
introduced, so application unit tests/lint were not applicable. No retrieval,
evaluation, independent code review or human meaning review ran.

The [T02 handoff](../../docs/workflow/M001-T02-handoff.md) records final artifact
hashes, repository checks, limits and the exact next Domain checkpoint. Stop
here: T03 firm/window coverage has not started.
