"""Paired M008/M009 development checks on frozen queries and identical pools."""

from hashlib import sha256
import argparse
import json

from ais.pilot import ROOT
from ais.search import CaseSearch

DIRECTORY = ROOT / "evaluation/search-m009"


def payload(row):
    return {
        k: v for k, v in row.items() if k in {"text", "cutoff", "before_period_end", "source_id"}
    }


def evaluate():
    freeze = json.loads((DIRECTORY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if (
            path not in freeze["mutable"]
            and sha256((ROOT / path).read_bytes()).hexdigest() != expected
        ):
            raise ValueError(f"Frozen M009 input changed: {path}")
    inputs = json.loads((DIRECTORY / "queries.json").read_text())
    baseline = json.loads((DIRECTORY / "baseline.json").read_text())
    search = CaseSearch.load()

    def paired(captured):
        p = captured["payload"]
        pool, excluded = search.candidate_pool(search.query(p))
        ids = [c["id"] for c in pool]
        if ids != captured["eligible_ids"] or excluded != captured["excluded"]:
            raise ValueError("Eligibility changed")
        observed = {}
        for name, method in [("old", "context_m007"), ("new", "context_m009")]:
            r = search.search(p, method=method)
            ranks = [{"id": c["id"], "score": c["score"]} for c in r["results"]]
            if r["eligible_count"] != len(ids) or r["excluded"] != excluded:
                raise ValueError("Method changed eligibility")
            if name == "old" and any(
                [
                    r["status"] != captured["status"],
                    ranks != captured["ranked"],
                    r["query_reading"] != captured["query_reading"],
                ]
            ):
                raise ValueError(f"M008 baseline no longer reproduces: {captured['id']}")
            observed[name] = {
                "ranked": ranks,
                "status": r["status"],
                "clarification": r.get("clarification"),
                "coverage": {c["id"]: c.get("coverage") for c in r["results"]},
                "query_reading": r["query_reading"],
            }
        return {
            "id": captured["id"],
            "payload": p,
            "eligible_ids": ids,
            "excluded": excluded,
            **observed,
        }

    checks = []
    for row, captured in zip(inputs["queries"], baseline["queries"], strict=True):
        result = paired(captured)
        for name in ("old", "new"):
            actual = result[name]
            ids = [c["id"] for c in actual["ranked"]]
            failures = []
            if not set(row["expected_useful_cases"]) <= set(ids):
                failures.append("useful_case_missing")
            if row["expect_empty"] and ids:
                failures.append("unexpected_results")
            if set(row.get("forbidden_cases", [])) & set(ids):
                failures.append("forbidden_case")
            if bool(actual["clarification"]) != row["expect_clarification"]:
                failures.append("clarification")
            for cid, expected in row.get("coverage", {}).items():
                coverage = actual["coverage"].get(cid)
                if coverage is None or any(coverage[k] != v for k, v in expected.items()):
                    failures.append(f"coverage:{cid}")
            if row.get("unknown_coverage") and not any(
                c and c["unrecognized"] for c in actual["coverage"].values()
            ):
                failures.append("unknown_input_coverage")
            if row.get("unresolved_coverage") and not any(
                c and c["unresolved"] for c in actual["coverage"].values()
            ):
                failures.append("unresolved_input_coverage")
            actual["failures"] = failures
        checks.append(result)
    historical = [{"group": row["group"], **paired(row)} for row in baseline["historical"]]

    def ids(c, name):
        return [r["id"] for r in c[name]["ranked"]]

    summary = {
        "queries": len(checks),
        "old_queries_meeting_all_expectations": sum(not c["old"]["failures"] for c in checks),
        "new_queries_meeting_all_expectations": sum(not c["new"]["failures"] for c in checks),
        "remaining_failures": [
            {"id": c["id"], "failures": c["new"]["failures"]}
            for c in checks
            if c["new"]["failures"]
        ],
        "new_set_rank_changes": [c["id"] for c in checks if ids(c, "old") != ids(c, "new")],
        "nonempty_to_empty": [
            c["id"] for c in checks if c["old"]["ranked"] and not c["new"]["ranked"]
        ],
        "historical_queries": len(historical),
        "historical_rank_changes": [
            {"group": c["group"], "id": c["id"], "old": ids(c, "old"), "new": ids(c, "new")}
            for c in historical
            if ids(c, "old") != ids(c, "new")
        ],
    }
    summary["useful_case_retrieval_regressions"] = []
    summary["target_rank_regressions"] = []
    summary["useful_case_retrieval_gains"] = []
    for row, check in zip(inputs["queries"], checks, strict=True):
        old, new = ids(check, "old"), ids(check, "new")
        wanted = row["expected_useful_cases"]
        if wanted and set(wanted) <= set(old) and not set(wanted) <= set(new):
            summary["useful_case_retrieval_regressions"].append(row["id"])
        if wanted and not set(wanted) <= set(old) and set(wanted) <= set(new):
            summary["useful_case_retrieval_gains"].append(row["id"])
        if any(
            case in old and (case not in new or new.index(case) > old.index(case))
            for case in wanted
        ):
            summary["target_rank_regressions"].append(row["id"])
    return {
        "provenance": inputs["provenance"],
        "summary": summary,
        "fingerprints": {
            str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
            for p in [
                ROOT / "src/ais/historical.py",
                ROOT / "src/ais/relevance.py",
                ROOT / "assets/app/app.js",
                ROOT / "assets/app/index.html",
                ROOT / "assets/app/app.css",
                ROOT / "scripts/evaluate_m009.py",
                ROOT / "src/ais/reader_context.py",
                ROOT / "src/ais/search.py",
                ROOT / "assets/app/reader.mjs",
                DIRECTORY / "queries.json",
                DIRECTORY / "baseline.json",
            ]
        },
        "checks": checks,
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
        raise ValueError("M009 observations differ; inspect before explicitly recording --write")
    print(json.dumps(result["summary"], indent=2))
    if result["summary"]["remaining_failures"]:
        raise SystemExit(1)
