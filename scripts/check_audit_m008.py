"""Reproduce the small AI audit; never admit its labels as human judgements."""

from collections import Counter
from hashlib import sha256
import json

from ais.pilot import ROOT
from ais.relevance import STUDY, check as check_optional_packet
from ais.search import CaseSearch

DIRECTORY = ROOT / "evaluation/audit-m008"


def observe(selection, search):
    rows = []
    for row in selection["queries"]:
        payload = {k: row[k] for k in ("text", "cutoff", "before_period_end")}
        pool, excluded = search.candidate_pool(search.query(payload))
        result = search.search(payload, method=selection["method"])
        rows.append(
            {
                "id": row["id"],
                "payload": payload,
                "eligible_ids": [c["id"] for c in pool],
                "excluded": excluded,
                **{k: result[k] for k in ("status", "query_reading", "message")},
                "displayed": result["results"],
            }
        )
    return {"provenance": selection["provenance"], "queries": rows}


def validate_labels(snapshot, labels, sources, search):
    if labels.get("judge_type") != "AI" or labels.get("independent_human_validation") is not False:
        raise ValueError("AI judgements must not be presented as human validation")
    queries = {q["id"]: q for q in snapshot["queries"]}
    expected = {(q["id"], c["id"]) for q in queries.values() for c in q["displayed"]}
    displayed = labels["displayed_judgements"]
    actual = [(r["query_id"], r["case_id"]) for r in displayed]
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError("Displayed judgements are missing, duplicated or not displayed")
    if Counter(r["query_id"] for r in labels["query_assessments"]) != Counter(queries.keys()):
        raise ValueError("Every selected query needs exactly one assessment")
    checked = {r["case_id"]: r for r in sources["checks"]}
    if len(checked) != len(sources["checks"]):
        raise ValueError("Duplicate source check")
    for source in checked.values():
        if (
            source["record_source_url"] != search.by_id[source["case_id"]]["source_url"]
            or not source["verified_url"].startswith("https://")
            or not source["locator"]
            or not source["finding"]
        ):
            raise ValueError("Source check lacks locatable evidence")
    for row in [*displayed, *labels["other_assessments"]]:
        q = queries[row["query_id"]]
        if row["source_check"] != row["case_id"] or row["source_check"] not in checked:
            raise ValueError("Assessment needs its own source check")
        if (
            row["usefulness"]
            not in {"useful", "partly_useful", "not_useful", "unsure", "not_eligible"}
            or row["misleading_risk"] not in {"low", "possible", "high"}
            or not row["reason"].strip()
        ):
            raise ValueError("Assessment category or reason missing")
        if "role" in row:
            if (row["query_id"], row["case_id"]) in expected:
                raise ValueError("A displayed result is not an omission")
            eligible = row["case_id"] in q["eligible_ids"]
            if row["role"] == "date_excluded":
                if eligible or row["usefulness"] != "not_eligible":
                    raise ValueError("Date-excluded example must remain ineligible")
            elif (
                row["role"] not in {"important_omission", "correct_direction_exclusion"}
                or not eligible
            ):
                raise ValueError("An omitted candidate must be eligible")


def run():
    # The optional human packet's method, data and renderer remain byte-identical.
    check_optional_packet(STUDY)
    for manifest in ("freeze.json", "observations-sha256.json"):
        for path, expected in json.loads((DIRECTORY / manifest).read_text())["sha256"].items():
            if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen audit artifact changed: {path}")
    human = json.loads((STUDY / "analysis.json").read_text())
    if (
        human["state"] != "human_validation_deferred"
        or human["judged_pairs"] != 0
        or human["independent_human_reviewers"] != 0
        or human["reviews"]
    ):
        raise ValueError("Human review must remain deferred with zero judgements")
    if json.loads((STUDY / "reviewer-registry.json").read_text())["reviewers"]:
        raise ValueError("No human reviewer is admitted for this AI audit")
    selection = json.loads((DIRECTORY / "selection.json").read_text())
    search = CaseSearch.load(selection["collection"])
    snapshot = json.loads((DIRECTORY / "snapshot.json").read_text())
    if observe(selection, search) != snapshot:
        raise ValueError("Current search differs from the captured AI audit")
    labels = json.loads((DIRECTORY / "judgements.json").read_text())
    sources = json.loads((DIRECTORY / "source-checks.json").read_text())
    validate_labels(snapshot, labels, sources, search)
    return {
        "provenance": "AI development judgements; not independent human validation",
        "queries": len(snapshot["queries"]),
        "displayed_assessments": len(labels["displayed_judgements"]),
        "displayed_AI_labels": dict(
            Counter(r["usefulness"] for r in labels["displayed_judgements"])
        ),
        "other_assessments": len(labels["other_assessments"]),
        "source_checks": len(sources["checks"]),
        "human_validation": "deferred",
        "human_judgements": 0,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
