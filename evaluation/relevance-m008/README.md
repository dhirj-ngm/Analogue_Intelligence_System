# M008 independent relevance review

**Pending authorized human review.** No independent human judgements have been
collected. Builder and AI labels are not substitutes. The collection, method,
ten realistic prompts and [plan](plan.md) were frozen in `6362044`, before any
review. All seventeen cases and ranking code remain unchanged.

The blinded packet has **154 query–case pairs**: every eligible case per query,
shuffled. This supports measuring useful omissions inside the collection, not
recall of all history. The query sample is Builder-authored and case-informed;
independent reviewer labels would not make it a representative query benchmark.

## Review packet

Send only **reviewer/packet.html** to an authorized independent human, with
[invitation.txt](invitation.txt) filled with their agreed code and return channel.
The standalone form shows source-linked evidence, dates, scope, actions,
differences and unknowns, with the app's existing plain-language presentation.
It sends nothing. A reviewer can download/restore drafts and export partial or
complete JSON responses. Original reports remain external.

Do **not** send the repository, queries/plan files, coordinator snapshot, previous
evaluation labels or analysis: they can reveal sampling intent or actual result
membership. Scores, positions, match explanations, original case IDs and expected
answers are absent from the reviewer file. The coordinator snapshot separately
captures the app's actual displayed results and eligibility.

Initial repository and connected Drive searches found no existing review channel.
The user subsequently authorized email contact with a designated recipient (R01).
The invitation and frozen packet were sent on 1 November 2026, with Gmail readback
confirming the attachment. Human identity/independence and actual judgements remain
to be confirmed; the registry remains empty. Original delivery metadata is private.
No paid service or AI reviewer has been used. Contact authorization is distinct
from evidence of independent human judgement.

## Run and admit responses

```sh
make review-check       # Verify original inputs/packet and show current admission state
make review-browser     # Desktop/mobile form tests with disposable synthetic drafts
# Open evaluation/relevance-m008/reviewer/packet.html in a browser.
```

The packet is already generated and frozen. `PYTHONPATH=src python3 -m
ais.relevance prepare --directory /tmp/new-review-copy` reproduces a separate
copy; it refuses to overwrite an issued packet. `packet-manifest.json` hashes the
reviewer file, coordinator mapping and tooling. `freeze.json` hashes the original
collection/method/app and study inputs. Check failures require investigation,
not regeneration during judgement collection.

Keep exact received JSON in ignored `submissions/`, and identity/channel receipts
outside Git. The committed reviewer registry is empty. After specific contact
authorization and actual human receipt, create an ignored
`reviewer-registry.private.json` with a `reviewers` array. Each entry needs:

- Assigned `reviewer_id`, `type: "human"`, `identity_verified: true`,
  `independence_confirmed: true`, `created_cases_or_rules: false`, `is_project_user: false`.
- Nonempty `verification_method`, `authorization_reference`, `receipt_reference`
  grounded in the actual authorized human exchange, not inferred from form text.
- `submission_sha256` of the authenticated original response file.

These are coordinator assertions requiring evidence; software cannot verify human
identity from a checkbox. Reviewer declarations must also confirm independence,
no expected-answer exposure and no AI labels. Do not populate a registry with
test data. Authorize/verify any second reviewer separately; one reviewer cannot
measure inter-reviewer disagreement.

```sh
PYTHONPATH=src python3 -m ais.relevance analyze \
  --registry evaluation/relevance-m008/reviewer-registry.private.json \
  --submissions evaluation/relevance-m008/submissions
```

Review the output before using `--write`: it includes pseudonymous rationales and
source/coverage notes. Keep personal information private. Invalid provenance,
wrong packets, duplicate/unknown pairs, invalid categories and missing rationales
are excluded explicitly. Unjudged rows remain missing. Full-query measures require
all eligible pairs and the query coverage note; incomplete reviews are not
extrapolated. Usefulness, partial usefulness, uncertainty and misleading flags
remain separate. Complete queries expose useful omitted cases and false abstentions.
Disagreements retain both rationales; no forced consensus is inferred.

Current [analysis.json](analysis.json) and [report.md](report.md) contain the actual
pending state, not fabricated results. All new automated label fixtures live in
tests or disposable browser downloads, and never enter study submissions.
