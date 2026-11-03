"""Paired collection development observations; no independent relevance claims."""

import argparse
from hashlib import sha256
import json

from ais.pilot import ROOT
from ais.search import CaseSearch

DIRECTORY = ROOT / "evaluation/collection-m011"
METHOD = "context_m010"


def payload(row):
    return {
        k: v for k, v in row.items() if k in {"text", "cutoff", "source_id", "before_period_end"}
    }


def observe(search, row):
    p = row.get("payload", payload(row))
    pool, excluded = search.candidate_pool(search.query(p))
    r = search.search(p, method=METHOD)
    return {
        "id": row["id"],
        "payload": p,
        "eligible_ids": [c["id"] for c in pool],
        "excluded": excluded,
        "status": r["status"],
        "ranked": [{"id": c["id"], "score": c["score"]} for c in r["results"]],
        "query_reading": r["query_reading"],
        "clarification": r.get("clarification"),
        "coverage": {c["id"]: c["coverage"] for c in r["results"]},
    }


def ranked(observation):
    return [c["id"] for c in observation["ranked"]]


def evaluate():
    freeze = json.loads((DIRECTORY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if (
            path not in freeze["mutable_code"]
            and sha256((ROOT / path).read_bytes()).hexdigest() != expected
        ):
            raise ValueError(f"Frozen M011 input changed: {path}")
    inputs = json.loads((DIRECTORY / "checks.json").read_text())
    if inputs["method"] != METHOD:
        raise ValueError("The frozen method must stay unchanged")
    baseline = json.loads((DIRECTORY / "baseline.json").read_text())
    old, expanded = CaseSearch.load("m007"), CaseSearch.load("m011")

    def paired(captured):
        before, after = observe(old, captured), observe(expanded, captured)
        if before != {k: v for k, v in captured.items() if k != "group"}:
            raise ValueError(f"Frozen M010/17-case output changed: {captured['id']}")
        if before["eligible_ids"] != [i for i in after["eligible_ids"] if i in old.by_id]:
            raise ValueError("Expansion changed eligibility of an existing case")
        return {
            "id": captured["id"],
            "payload": captured["payload"],
            "old": before,
            "expanded": after,
        }

    checks = []
    for row, captured in zip(inputs["queries"], baseline["queries"], strict=True):
        if row["id"] != captured["id"] or payload(row) != captured["payload"]:
            raise ValueError("Frozen checks/baseline disagree")
        check = paired(captured)
        for name in ("old", "expanded"):
            actual, wanted = check[name], row["expected_useful_cases"]
            ids = ranked(actual)
            actual["useful_ranks"] = {i: ids.index(i) + 1 if i in ids else None for i in wanted}
            actual["failures"] = []
            if not set(wanted) <= set(ids):
                actual["failures"].append("useful_case_missing")
            if row["expect_empty"] and ids:
                actual["failures"].append("unexpected_results")
            if set(ids) & set(row["forbidden_cases"]):
                actual["failures"].append("forbidden_case")
        checks.append({**row, **check})

    # Expectations from the earlier development sets are historical labels, not
    # new independent labels for newly collected evidence.
    legacy_labels = {}
    for group, path in [
        ("m006", "evaluation/search-m006/queries.json"),
        ("m007", "evaluation/collection-m007/checks.json"),
        ("m009", "evaluation/search-m009/queries.json"),
        ("m010", "evaluation/search-m010/queries.json"),
    ]:
        for row in json.loads((ROOT / path).read_text())["queries"]:
            legacy_labels[group, row["id"]] = row.get("expected_useful_cases", [])
    historical, rank_losses, retrieval_losses = [], [], []
    for captured in baseline["historical"]:
        c = {"group": captured["group"], **paired(captured)}
        targets = legacy_labels.get((c["group"], c["id"]), [])
        before, after = ranked(c["old"]), ranked(c["expanded"])
        c["prior_useful_targets"] = targets
        lost = [i for i in targets if i in before and i not in after]
        lower = [
            i
            for i in targets
            if i in before and (i not in after or after.index(i) > before.index(i))
        ]
        if lost:
            retrieval_losses.append({"group": c["group"], "id": c["id"], "targets": lost})
        if lower:
            rank_losses.append({"group": c["group"], "id": c["id"], "targets": lower})
        historical.append(c)

    def changed(rows):
        return [
            {
                "group": c.get("group"),
                "id": c["id"],
                "old": ranked(c["old"]),
                "expanded": ranked(c["expanded"]),
            }
            for c in rows
            if ranked(c["old"]) != ranked(c["expanded"])
        ]

    summary = {"queries": len(checks), "historical_entries": len(historical)}
    for name in ("old", "expanded"):
        positives = [c for c in checks if c["expected_useful_cases"]]
        negatives = [c for c in checks if c["expect_empty"]]
        summary[name] = {
            "useful_target_queries": len(positives),
            "all_useful_targets_at_5": sum(
                set(c["expected_useful_cases"]) <= set(ranked(c[name])) for c in positives
            ),
            "expected_empty_queries": len(negatives),
            "expected_empty_left_empty": sum(not c[name]["ranked"] for c in negatives),
            "queries_with_misleading_results": sum(
                any(f in {"unexpected_results", "forbidden_case"} for f in c[name]["failures"])
                for c in checks
            ),
        }
    summary.update(
        changed_rankings=changed(checks),
        remaining_failures=[
            {"id": c["id"], "failures": c["expanded"]["failures"]}
            for c in checks
            if c["expanded"]["failures"]
        ],
        historical_rank_changes=changed(historical),
        historical_target_rank_losses=rank_losses,
        historical_target_retrieval_losses=retrieval_losses,
    )
    comparisons = []
    p = {"text": "oil packaging grain energy", "cutoff": "2026-11-03"}
    results = {c["id"]: c for c in expanded.search(p, method=METHOD)["results"]}
    for plan in inputs["comparison_checks"]:
        if not set(plan["ids"]) <= results.keys():
            raise ValueError("Frozen comparison cases cannot be selected in app results")
        comparisons.append(
            {
                "payload": p,
                "requirements": plan["requirements"],
                "displayed_records": [results[i] for i in plan["ids"]],
            }
        )
    paths = [
        DIRECTORY / "checks.json",
        DIRECTORY / "baseline.json",
        DIRECTORY / "freeze.json",
        ROOT / "data/collection/m011/cases.jsonl",
        ROOT / "scripts/check_collection_m011.py",
        *[
            ROOT / f"src/ais/{n}.py"
            for n in (
                "search",
                "collection",
                "pilot",
                "context",
                "reader_context",
                "language_context",
                "related",
                "vocabulary",
                "historical",
            )
        ],
        *[ROOT / f"assets/app/{n}" for n in ("app.js", "index.html", "reader.mjs")],
    ]
    return {
        "provenance": inputs["provenance"],
        "method": METHOD,
        "collections": {"old": old.catalog()["total"], "expanded": expanded.catalog()["total"]},
        "fingerprints": {
            str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths
        },
        "summary": summary,
        "checks": checks,
        "comparisons": comparisons,
        "historical": historical,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    if args.write:
        (DIRECTORY / "results.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        )
    elif json.loads((DIRECTORY / "results.json").read_text()) != result:
        raise ValueError(
            "M011 observations/fingerprints changed; inspect before explicitly recording --write"
        )
    summary = result["summary"]
    print(
        json.dumps(
            {
                **{
                    k: v
                    for k, v in summary.items()
                    if k
                    not in {
                        "historical_rank_changes",
                        "changed_rankings",
                        "historical_target_rank_losses",
                    }
                },
                "changed_rankings_count": len(summary["changed_rankings"]),
                "historical_rank_changes_count": len(summary["historical_rank_changes"]),
                "historical_target_rank_losses_count": len(
                    summary["historical_target_rank_losses"]
                ),
            },
            indent=2,
        )
    )
    # Reproducing honest misses is success, not a relevance pass. Never suppress
    # observations or fail the build merely to force a case/search change.
