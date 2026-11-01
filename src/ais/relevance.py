"""Frozen, blinded M008 packet and provenance-gated human relevance analysis."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from ais.pilot import ROOT
from ais.search import CaseSearch

STUDY = ROOT / "evaluation/relevance-m008"
REVIEW_ASSETS = ROOT / "assets/review"
LABELS = {"useful", "partly_useful", "not_useful", "unsure"}
MISLEADING = {"yes", "no", "unsure"}
ACCESS = {"opened", "not_opened", "unavailable"}
COVERAGE = {"adequate", "limited", "none", "unsure"}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def verify_inputs():
    freeze = json.loads((STUDY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if digest(ROOT / path) != expected:
            raise ValueError(f"Frozen M008 input changed: {path}")


def snapshot():
    verify_inputs()
    plan = json.loads((STUDY / "plan.json").read_text())
    queries = json.loads((STUDY / "queries.json").read_text())["queries"]
    search = CaseSearch.load(plan["collection"])
    blind, coordinator = [], []

    def order(value):
        return sha256((plan["ordering_seed"] + value).encode()).hexdigest()

    for row in sorted(queries, key=lambda q: order(q["id"])):
        payload = {k: row[k] for k in ("text", "cutoff", "before_period_end")}
        query = search.query(payload)
        candidates, excluded = search.candidate_pool(query)
        result = search.search(payload, method=plan["method"])
        items, mapping = [], {}
        for case in sorted(candidates, key=lambda c: order(row["id"] + c["id"])):
            item_id = "I" + order(row["id"] + case["id"])[:12]
            presented = search.present(case, query, 0, [])
            # Whitelist source evidence; do not send ranks, match explanations,
            # algorithm readings, case IDs or expected answers to the reviewer.
            evidence = {
                key: presented[key]
                for key in (
                    "company",
                    "period",
                    "published",
                    "fields",
                    "metric",
                    "figures",
                    "conflicts",
                    "important_differences",
                    "unknowns",
                    "source",
                )
            }
            evidence["business_scope"] = search.details[case["id"]].get(
                "business_scope", search.details[case["id"]]["metric"]["scope"]
            )
            evidence["source"]["locator"] = evidence["source"]["locator"].replace(
                "; detailed evidence in data/episodes.jsonl", ""
            )
            items.append({"item_id": item_id, **evidence})
            mapping[item_id] = case["id"]
        blind.append({"query_id": row["id"], **payload, "items": items})
        coordinator.append(
            {
                "query_id": row["id"],
                "eligible_ids": [c["id"] for c in candidates],
                "excluded": excluded,
                "items": mapping,
                "displayed": [{"id": c["id"], "score": c["score"]} for c in result["results"]],
                "status": result["status"],
            }
        )
    packet = {
        "study": plan["version"],
        "freeze_sha256": digest(STUDY / "freeze.json"),
        "queries": blind,
    }
    packet["packet_id"] = sha256(encoded(packet).encode()).hexdigest()
    private = {
        "packet_id": packet["packet_id"],
        "method": plan["method"],
        "collection_count": len(search.cases),
        "queries": coordinator,
    }
    return packet, private


def render(packet):
    template = (REVIEW_ASSETS / "packet.html").read_text()
    # Source text cannot escape the JSON script block or execute as HTML.
    payload = encoded(packet).replace("<", "\\u003c").replace("&", "\\u0026")
    reader = (ROOT / "assets/app/reader.mjs").read_text().replace("export ", "")
    review = "\n".join(
        line
        for line in (REVIEW_ASSETS / "review.mjs").read_text().splitlines()
        if not line.startswith("import ")
    )
    return (
        template.replace("__STYLE__", (REVIEW_ASSETS / "review.css").read_text())
        .replace("__DATA__", payload)
        .replace("__SCRIPT__", reader + "\n" + review.replace("export ", ""))
    )


def prepare(directory):
    if (directory / "packet-manifest.json").exists():
        raise ValueError(
            "Packet already frozen. Check it; do not overwrite an issued review packet."
        )
    packet, private = snapshot()
    reviewer = directory / "reviewer"
    reviewer.mkdir(parents=True, exist_ok=True)
    (reviewer / "packet.html").write_text(render(packet))
    save(directory / "coordinator/snapshot.json", private)
    files = ["reviewer/packet.html", "coordinator/snapshot.json"]
    manifest = {
        "packet_id": packet["packet_id"],
        "upstream_freeze_sha256": digest(STUDY / "freeze.json"),
        "artifacts": {p: digest(directory / p) for p in files},
        "tooling": {
            str(p.relative_to(ROOT)): digest(p)
            for p in [Path(__file__), *sorted(REVIEW_ASSETS.glob("*"))]
            if p.is_file()
        },
    }
    save(directory / "packet-manifest.json", manifest)
    return packet, private


def check(directory):
    packet, private = snapshot()
    manifest = json.loads((directory / "packet-manifest.json").read_text())
    if manifest["packet_id"] != packet["packet_id"] or manifest["upstream_freeze_sha256"] != digest(
        STUDY / "freeze.json"
    ):
        raise ValueError("Packet does not match frozen study")
    for path, expected in manifest["artifacts"].items():
        if digest(directory / path) != expected:
            raise ValueError(f"Frozen review artifact changed: {path}")
    for path, expected in manifest["tooling"].items():
        if digest(ROOT / path) != expected:
            raise ValueError(f"Review tooling changed since packet freeze: {path}")
    if json.loads((directory / "coordinator/snapshot.json").read_text()) != private:
        raise ValueError("Current search no longer reproduces the packet snapshot")
    if (directory / "reviewer/packet.html").read_text() != render(packet):
        raise ValueError("Reviewer material differs from the frozen evidence")
    return packet, private


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_submission(submission, packet):
    def fields(row, allowed):
        if not isinstance(row, dict) or set(row) - set(allowed):
            raise ValueError("unknown response fields or invalid row format")

    fields(submission, ("packet_id", "reviewer_id", "attestation", "judgements", "queries"))
    if submission.get("packet_id") != packet["packet_id"]:
        raise ValueError("wrong packet ID")
    attestation = submission.get("attestation", {})
    if not (
        attestation.get("human") is True
        and all(
            attestation.get(k) is False
            for k in ("created_cases_or_rules", "seen_expected_answers", "used_ai_judgements")
        )
    ):
        raise ValueError("human independence/blinding/no-AI attestation missing or ineligible")
    expected = {(q["query_id"], i["item_id"]) for q in packet["queries"] for i in q["items"]}
    valid_queries = {q["query_id"] for q in packet["queries"]}
    pairs, notes = {}, {}
    for row in submission.get("judgements", []):
        fields(
            row,
            (
                "query_id",
                "item_id",
                "usefulness",
                "reason",
                "misleading",
                "misleading_reason",
                "source_access",
                "source_note",
            ),
        )
        if any(
            not isinstance(row.get(k, ""), str)
            for k in ("reason", "misleading_reason", "source_note")
        ):
            raise ValueError("invalid case rationale text")
        key = (row.get("query_id"), row.get("item_id"))
        if key not in expected or key in pairs:
            raise ValueError("unknown or duplicate query/case response")
        pairs[key] = row
        values = [row.get(k) for k in ("usefulness", "misleading", "source_access")]
        if not any(values):
            if any(nonempty(row.get(k)) for k in ("reason", "misleading_reason", "source_note")):
                raise ValueError("notes without a completed case judgement")
            continue
        if (
            row.get("usefulness") not in LABELS
            or row.get("misleading") not in MISLEADING
            or row.get("source_access") not in ACCESS
        ):
            raise ValueError("invalid or incomplete case categories")
        if not nonempty(row.get("reason")):
            raise ValueError("case judgement needs a rationale")
        if row["misleading"] != "no" and not nonempty(row.get("misleading_reason")):
            raise ValueError("misleading/uncertain judgement needs an explanation")
        if row["source_access"] == "unavailable" and not nonempty(row.get("source_note")):
            raise ValueError("unavailable source needs a note")
    for row in submission.get("queries", []):
        fields(row, ("query_id", "coverage", "reason", "missing_cases"))
        if any(not isinstance(row.get(k, ""), str) for k in ("reason", "missing_cases")):
            raise ValueError("invalid query note text")
        key = row.get("query_id")
        if key not in valid_queries or key in notes:
            raise ValueError("unknown or duplicate query note")
        if row.get("coverage") and (
            row["coverage"] not in COVERAGE or not nonempty(row.get("reason"))
        ):
            raise ValueError("query coverage needs a valid category and rationale")
        notes[key] = row
    return {k: v for k, v in pairs.items() if v.get("usefulness")}, notes


def analyze(packet, private, submissions, registry):
    """Registry provenance is a coordinator assertion, not identity verification by code."""
    records = registry.get("reviewers", [])
    if len({r["reviewer_id"] for r in records}) != len(records):
        raise ValueError("duplicate reviewer registry entry")
    people = {r["reviewer_id"]: r for r in records}
    admitted, excluded, seen = [], [], set()
    for path in submissions:
        try:
            submission = json.loads(path.read_text())
            reviewer = submission.get("reviewer_id")
            person = people.get(reviewer, {})
            if not (
                person.get("type") == "human"
                and person.get("identity_verified") is True
                and person.get("independence_confirmed") is True
                and person.get("created_cases_or_rules") is False
                and person.get("is_project_user") is False
            ):
                raise ValueError("no verified, independent non-user human registry entry")
            if not all(
                nonempty(person.get(k))
                for k in ("verification_method", "authorization_reference", "receipt_reference")
            ):
                raise ValueError(
                    "human verification, authorization or response-channel evidence missing"
                )
            if person.get("submission_sha256") != digest(path):
                raise ValueError("response differs from authenticated submission receipt")
            if reviewer in seen:
                raise ValueError("duplicate submission for reviewer; no silent replacement")
            pairs, notes = validate_submission(submission, packet)
            admitted.append((reviewer, pairs, notes))
            seen.add(reviewer)
        except (ValueError, TypeError, KeyError, AttributeError) as error:
            excluded.append({"file": path.name, "reason": str(error)})
    by_query = {q["query_id"]: q for q in private["queries"]}
    reviews = []
    for reviewer, pairs, notes in admitted:
        queries = []
        for query in packet["queries"]:
            qid = query["query_id"]
            meta = by_query[qid]
            rows = {i: r for (q, i), r in pairs.items() if q == qid}
            displayed = {r["id"] for r in meta["displayed"]}
            returned = [r for i, r in rows.items() if meta["items"][i] in displayed]
            useful = {meta["items"][i] for i, r in rows.items() if r["usefulness"] == "useful"}
            complete = len(rows) == len(query["items"]) and bool(notes.get(qid, {}).get("coverage"))
            counts = Counter(r["usefulness"] for r in returned)
            measures = None
            if complete:
                measures = {
                    "useful_share_of_displayed": counts["useful"] / len(displayed)
                    if displayed
                    else None,
                    "within_eligible_pool_recall": len(useful & displayed) / len(useful)
                    if useful
                    else None,
                    "useful_omitted_ids": sorted(useful - displayed),
                    "empty_result_with_useful_case": bool(not displayed and useful),
                    "no_useful_in_judged_pool": not bool(useful),
                }
            queries.append(
                {
                    "query_id": qid,
                    "complete": complete,
                    "eligible_pairs": len(query["items"]),
                    "judged_pairs": len(rows),
                    "displayed_count": len(displayed),
                    "displayed_judged": len(returned),
                    "displayed_labels": dict(counts),
                    "displayed_misleading": dict(Counter(r["misleading"] for r in returned)),
                    "all_pool_labels": dict(Counter(r["usefulness"] for r in rows.values())),
                    "source_access": dict(Counter(r["source_access"] for r in rows.values())),
                    "measures": measures,
                    "query_note": notes.get(qid),
                    "judgements": [{"case_id": meta["items"][i], **r} for i, r in rows.items()],
                }
            )
        complete = all(q["complete"] for q in queries)
        denominator = sum(q["displayed_count"] for q in queries)
        numerator = sum(q["displayed_labels"].get("useful", 0) for q in queries)
        reviews.append(
            {
                "reviewer_id": reviewer,
                "complete": complete,
                "aggregate": {
                    "displayed_useful": numerator,
                    "displayed_total": denominator,
                    "useful_share": numerator / denominator if denominator else None,
                }
                if complete
                else None,
                "queries": queries,
            }
        )
    disagreements = []
    shared_pairs = 0
    for (a, pairs_a, _), (b, pairs_b, _) in combinations(admitted, 2):
        for key in sorted(pairs_a.keys() & pairs_b.keys()):
            shared_pairs += 1
            ra, rb = pairs_a[key], pairs_b[key]
            if (ra["usefulness"], ra["misleading"]) != (rb["usefulness"], rb["misleading"]):
                disagreements.append(
                    {
                        "query_id": key[0],
                        "case_id": by_query[key[0]]["items"][key[1]],
                        "reviewers": {a: ra, b: rb},
                    }
                )
    return {
        "packet_id": packet["packet_id"],
        "state": "independent_human_sample_complete"
        if any(r["complete"] for r in reviews)
        else "partial_independent_human_review"
        if reviews
        else "awaiting_independent_human_review",
        "independent_human_reviewers": len(reviews),
        "judged_pairs": sum(q["judged_pairs"] for r in reviews for q in r["queries"]),
        "reviews": reviews,
        "excluded_submissions": excluded,
        "shared_pair_comparisons": shared_pairs,
        "disagreement_status": "observed_on_shared_pairs" if shared_pairs else "not_measured",
        "disagreements": disagreements,
        "limits": "Small Builder-authored query sample. Human provenance requires authorized channel evidence, not self-attestation alone. No labels or metrics without verified independent human submissions. No claims about action effects, independent source validation or all historical cases.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "check", "analyze"])
    parser.add_argument("--directory", type=Path, default=STUDY)
    parser.add_argument("--registry", type=Path, default=STUDY / "reviewer-registry.json")
    parser.add_argument("--submissions", type=Path, default=STUDY / "submissions")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    packet, private = (
        prepare(args.directory) if args.command == "prepare" else check(args.directory)
    )
    if args.command == "analyze":
        result = analyze(
            packet,
            private,
            sorted(args.submissions.glob("*.json")),
            json.loads(args.registry.read_text()),
        )
        if args.write:
            save(args.directory / "analysis.json", result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(
            json.dumps(
                {
                    "packet_id": packet["packet_id"],
                    "queries": len(packet["queries"]),
                    "pairs": sum(len(q["items"]) for q in packet["queries"]),
                }
            )
        )


if __name__ == "__main__":
    main()
