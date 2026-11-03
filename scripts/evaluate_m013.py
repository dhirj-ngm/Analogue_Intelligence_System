"""M012/M013 on identical eligible cases; first five and extra access stay separate."""

import argparse
from hashlib import sha256
import json

from ais.pilot import ROOT
from ais.search import CaseSearch

DIRECTORY = ROOT / "evaluation/search-m013"


def evaluate():
    freeze = json.loads((DIRECTORY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if path not in freeze["mutable_code"]:
            if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen M013 input changed: {path}")
    inputs = json.loads((DIRECTORY / "queries.json").read_text())
    baseline = json.loads((DIRECTORY / "baseline.json").read_text())
    search = CaseSearch.load("m011")

    def paired(row):
        p = row["payload"]
        pool, excluded = search.candidate_pool(search.query(p))
        eligible = [c["id"] for c in pool]
        if eligible != row["eligible_ids"] or excluded != row["excluded"]:
            raise ValueError("Eligible cases changed")
        observations = {}
        for key, method in [("old", "context_m012"), ("new", "context_m013")]:
            result = search.search(p, method=method)
            first = result["results"]
            all_results = first + result.get("additional_results", [])
            actual = {
                "status": result["status"],
                "ranked": [{"id": c["id"], "score": c["score"]} for c in first],
                "additional_ranked": [
                    {"id": c["id"], "score": c["score"]} for c in all_results[5:]
                ],
                "matched_count": result["matched_count"],
                "coverage": {c["id"]: c["coverage"] for c in all_results},
                "pressure_matches": {c["id"]: c["pressure_matches"] for c in all_results},
                "query_reading": result["query_reading"],
                "clarification": result.get("clarification"),
            }
            if result["excluded"] != excluded or result["eligible_count"] != len(eligible):
                raise ValueError("Method changed eligibility")
            if key == "old" and any(actual[k] != row[k] for k in actual if k in row):
                raise ValueError(f"M012 baseline changed: {row['id']}")
            observations[key] = actual
        return {
            "id": row["id"],
            "payload": p,
            "eligible_ids": eligible,
            "excluded": excluded,
            **observations,
        }

    def ids(row, method, extra=False):
        value = row[method]
        return [r["id"] for r in value["ranked"] + (value["additional_ranked"] if extra else [])]

    checks = []
    for query, captured in zip(inputs["queries"], baseline["queries"], strict=True):
        p = {
            k: v
            for k, v in query.items()
            if k in {"text", "cutoff", "before_period_end", "source_id"}
        }
        if query["id"] != captured["id"] or p != captured["payload"]:
            raise ValueError("Frozen inputs disagree")
        row = paired(captured)
        for method in ("old", "new"):
            first, all_ids = ids(row, method), ids(row, method, True)
            failures = []
            if not set(query["expected_first_five"]) <= set(first):
                failures.append("first_five_target_missing")
            if not set(query["expected_accessible"]) <= set(all_ids):
                failures.append("accessible_target_missing")
            if query["expect_empty"] and all_ids:
                failures.append("unexpected_results")
            if set(query["forbidden_cases"]) & set(all_ids):
                failures.append("forbidden_case")
            for cid in query["partial_cases"]:
                c = row[method]["coverage"].get(cid)
                if not c or not c["partial"] or c["supported_count"] >= c["identified_count"]:
                    failures.append(f"partial_coverage:{cid}")
            row[method]["failures"] = failures
        checks.append(row)
    historical = [{"group": r["group"], **paired(r)} for r in baseline["historical"]]
    summary = {"queries": len(checks), "historical_queries": len(historical)}
    for method in ("old", "new"):
        summary[method] = {
            "all_expectations_met": sum(not r[method]["failures"] for r in checks),
            "first_five_target_queries": sum(
                bool(q["expected_first_five"]) for q in inputs["queries"]
            ),
            "first_five_targets_found": sum(
                bool(q["expected_first_five"])
                and set(q["expected_first_five"]) <= set(ids(r, method))
                for q, r in zip(inputs["queries"], checks, strict=True)
            ),
            "accessible_target_queries": sum(
                bool(q["expected_accessible"]) for q in inputs["queries"]
            ),
            "accessible_targets_found": sum(
                bool(q["expected_accessible"])
                and set(q["expected_accessible"]) <= set(ids(r, method, True))
                for q, r in zip(inputs["queries"], checks, strict=True)
            ),
            "expected_empty_queries": sum(q["expect_empty"] for q in inputs["queries"]),
            "expected_empty_left_empty": sum(
                q["expect_empty"] and not ids(r, method, True)
                for q, r in zip(inputs["queries"], checks, strict=True)
            ),
            "misleading_result_queries": sum(
                any(f in {"unexpected_results", "forbidden_case"} for f in r[method]["failures"])
                for r in checks
            ),
        }
    summary["remaining_failures"] = [
        {"id": r["id"], "failures": r["new"]["failures"]} for r in checks if r["new"]["failures"]
    ]
    for name, rows in [("new_set", checks), ("historical", historical)]:
        summary[name + "_rank_changes"] = [
            {
                "id": r["id"],
                **({"group": r["group"]} if "group" in r else {}),
                "old": ids(r, "old"),
                "new": ids(r, "new"),
            }
            for r in rows
            if ids(r, "old") != ids(r, "new")
        ]
    labels = {}
    for group, path, field in [
        ("m006", "search-m006/queries.json", "expected_useful_cases"),
        ("m007", "collection-m007/checks.json", "expected_useful_cases"),
        ("m009", "search-m009/queries.json", "expected_useful_cases"),
        ("m010", "search-m010/queries.json", "expected_useful_cases"),
        ("m011", "collection-m011/checks.json", "expected_useful_cases"),
        ("m012", "search-m012/queries.json", "expected_useful_cases"),
    ]:
        for q in json.loads((ROOT / "evaluation" / path).read_text())["queries"]:
            labels[group, q["id"]] = q.get(field, [])
    summary["historical_target_regressions"] = []
    summary["historical_target_gains"] = []
    for r in historical:
        old, new = ids(r, "old"), ids(r, "new")
        for target in labels.get((r["group"], r["id"]), []):
            if target in old and (target not in new or new.index(target) > old.index(target)):
                summary["historical_target_regressions"].append(
                    {
                        "group": r["group"],
                        "id": r["id"],
                        "target": target,
                        "old_rank": old.index(target) + 1,
                        "new_rank": new.index(target) + 1 if target in new else None,
                        "accessible": target in ids(r, "new", True),
                    }
                )
            if target not in old and target in new:
                summary["historical_target_gains"].append(
                    {
                        "group": r["group"],
                        "id": r["id"],
                        "target": target,
                        "new_rank": new.index(target) + 1,
                    }
                )
    paths = [
        "src/ais/polymer_context.py",
        "src/ais/material_context.py",
        "src/ais/search.py",
        "src/ais/historical.py",
        "assets/app/app.js",
        "assets/app/index.html",
        "assets/app/reader.mjs",
        "scripts/evaluate_m012.py",
        "scripts/evaluate_m013.py",
        "evaluation/search-m013/queries.json",
        "evaluation/search-m013/baseline.json",
        "evaluation/search-m013/freeze.json",
    ]
    return dict(
        provenance=inputs["provenance"],
        summary=summary,
        checks=checks,
        historical=historical,
        fingerprints={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    path = DIRECTORY / "results.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    elif json.loads(path.read_text()) != result:
        raise ValueError("M013 results/fingerprints changed")
    print(
        json.dumps(
            {k: v for k, v in result["summary"].items() if not k.endswith("rank_changes")}, indent=2
        )
    )
    if result["summary"]["remaining_failures"]:
        raise SystemExit(1)
