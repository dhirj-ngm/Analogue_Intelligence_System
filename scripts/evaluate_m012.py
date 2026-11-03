"""Paired M011/M012 development checks on frozen queries and identical pools."""

from hashlib import sha256
import argparse
import json

from ais.pilot import ROOT
from ais.search import CaseSearch
from ais.historical import frozen_bytes

DIRECTORY = ROOT / "evaluation/search-m012"


def payload(row):
    return {
        k: v for k, v in row.items() if k in {"text", "cutoff", "before_period_end", "source_id"}
    }


def evaluate():
    freeze = json.loads((DIRECTORY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if path not in freeze["mutable_code"]:
            frozen_bytes(path, expected)
    inputs = json.loads((DIRECTORY / "queries.json").read_text())
    baseline = json.loads((DIRECTORY / "baseline.json").read_text())
    search = CaseSearch.load("m011")

    def paired(captured):
        p = captured["payload"]
        pool, excluded = search.candidate_pool(search.query(p))
        ids = [c["id"] for c in pool]
        if ids != captured["eligible_ids"] or excluded != captured["excluded"]:
            raise ValueError("Eligibility changed")
        observed = {}
        for name, method in [("old", "context_m010"), ("new", "context_m012")]:
            r = search.search(p, method=method)
            ranks = [{"id": c["id"], "score": c["score"]} for c in r["results"]]
            if r["eligible_count"] != len(ids) or r["excluded"] != excluded:
                raise ValueError("Method changed eligibility")
            if name == "old" and any(
                [
                    r["status"] != captured["status"],
                    ranks != captured["ranked"],
                    r["query_reading"] != captured["query_reading"],
                    r.get("clarification") != captured["clarification"],
                    {c["id"]: c.get("coverage") for c in r["results"]} != captured["coverage"],
                ]
            ):
                raise ValueError(f"M011 baseline no longer reproduces: {captured['id']}")
            observed[name] = {
                "ranked": ranks,
                "status": r["status"],
                "clarification": r.get("clarification"),
                "coverage": {c["id"]: c.get("coverage") for c in r["results"]},
                "query_reading": r["query_reading"],
                "pressure_matches": {c["id"]: c["pressure_matches"] for c in r["results"]},
                "named_matches": {
                    c["id"]: [
                        m["family"]
                        for m in c.get("pressure_matches", [])
                        if m.get("match_kind") == "named_input"
                    ]
                    for c in r["results"]
                },
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
        if row["id"] != captured["id"] or payload(row) != captured["payload"]:
            raise ValueError("Frozen query and captured baseline disagree")
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
            if ((actual["clarification"] or {}).get("kind") == "material_input") != row[
                "expect_material_clarification"
            ]:
                failures.append("clarification")
            for cid in row["related_only_cases"]:
                if not actual["coverage"].get(cid, {}).get("related_only"):
                    failures.append(f"related_only:{cid}")
            for cid in row["named_input_cases"]:
                if not actual.get("named_matches", {}).get(cid):
                    failures.append(f"named_input:{cid}")
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
        "historical_score_changes": [
            {"group": c["group"], "id": c["id"]}
            for c in historical
            if c["old"]["ranked"] != c["new"]["ranked"]
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
    for name in ("old", "new"):
        summary[name + "_counts"] = {
            "useful_target_queries": sum(
                bool(q["expected_useful_cases"]) for q in inputs["queries"]
            ),
            "useful_target_queries_found": sum(
                bool(q["expected_useful_cases"])
                and set(q["expected_useful_cases"]) <= set(ids(c, name))
                for q, c in zip(inputs["queries"], checks, strict=True)
            ),
            "expected_empty_queries": sum(q["expect_empty"] for q in inputs["queries"]),
            "expected_empty_left_empty": sum(
                q["expect_empty"] and not c[name]["ranked"]
                for q, c in zip(inputs["queries"], checks, strict=True)
            ),
            "queries_with_misleading_results": sum(
                any(f in {"unexpected_results", "forbidden_case"} for f in c[name]["failures"])
                for c in checks
            ),
            "required_clarifications": sum(
                q["expect_material_clarification"] for q in inputs["queries"]
            ),
            "required_clarifications_shown": sum(
                q["expect_material_clarification"]
                and (c[name]["clarification"] or {}).get("kind") == "material_input"
                for q, c in zip(inputs["queries"], checks, strict=True)
            ),
        }
    prior = json.loads((ROOT / "evaluation/collection-m011/results.json").read_text())
    ten = []
    for loss in baseline["ten_m011_target_rank_losses"]:
        h = next(c for c in historical if (c["group"], c["id"]) == (loss["group"], loss["id"]))
        before_expansion = next(
            c for c in prior["historical"] if (c["group"], c["id"]) == (loss["group"], loss["id"])
        )["old"]["ranked"]
        for target in loss["targets"]:

            def rank(rows):
                values = [r["id"] for r in rows]
                return values.index(target) + 1 if target in values else None

            ten.append(
                {
                    "group": loss["group"],
                    "id": loss["id"],
                    "text": h["payload"]["text"],
                    "target": target,
                    "pre_m011_rank": rank(before_expansion),
                    "m011_rank": rank(h["old"]["ranked"]),
                    "m012_rank": rank(h["new"]["ranked"]),
                    "m012_status": h["new"]["status"],
                    "m012_clarification": h["new"]["clarification"],
                }
            )
    summary["ten_m011_targets"] = ten
    labels = {}
    for path, group in [
        ("evaluation/search-m006/queries.json", "m006"),
        ("evaluation/collection-m007/checks.json", "m007"),
        ("evaluation/search-m009/queries.json", "m009"),
        ("evaluation/search-m010/queries.json", "m010"),
        ("evaluation/collection-m011/checks.json", "m011"),
    ]:
        for q in json.loads((ROOT / path).read_text())["queries"]:
            labels[group, q["id"]] = q.get("expected_useful_cases", [])
    summary["historical_target_regressions"] = []
    for h in historical:
        before, after = ids(h, "old"), ids(h, "new")
        for target in labels.get((h["group"], h["id"]), []):
            if target in before and (
                target not in after or after.index(target) > before.index(target)
            ):
                summary["historical_target_regressions"].append(
                    {
                        "group": h["group"],
                        "id": h["id"],
                        "target": target,
                        "old_rank": before.index(target) + 1,
                        "new_rank": after.index(target) + 1 if target in after else None,
                    }
                )
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
                ROOT / "scripts/evaluate_m012.py",
                ROOT / "src/ais/material_context.py",
                ROOT / "src/ais/language_context.py",
                ROOT / "src/ais/reader_context.py",
                ROOT / "src/ais/search.py",
                ROOT / "assets/app/reader.mjs",
                DIRECTORY / "queries.json",
                DIRECTORY / "baseline.json",
                DIRECTORY / "freeze.json",
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
    else:
        recorded = json.loads((DIRECTORY / "results.json").read_text())
        if {k: v for k, v in recorded.items() if k != "fingerprints"} != {
            k: v for k, v in result.items() if k != "fingerprints"
        }:
            raise ValueError("M012 observations differ from their frozen methods/cohort")
        for path, expected in recorded["fingerprints"].items():
            frozen_bytes(path, expected)
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
                        "historical_score_changes",
                        "new_set_rank_changes",
                        "ten_m011_targets",
                        "historical_target_regressions",
                    }
                },
                "new_rank_changes": len(summary["new_set_rank_changes"]),
                "historical_rank_changes": len(summary["historical_rank_changes"]),
                "historical_target_regressions": len(summary["historical_target_regressions"]),
            },
            indent=2,
        )
    )
    if result["summary"]["remaining_failures"]:
        raise SystemExit(1)
