"""Reproduce frozen M007 development checks on old and expanded collections."""

import argparse
from hashlib import sha256
import json

from ais.pilot import ROOT
from ais.search import CaseSearch

DIRECTORY = ROOT / "evaluation/collection-m007"


def legacy_probe(old, expanded):
    """Inspect existing query ranks without treating old coverage gaps as new labels."""
    rows = json.loads((ROOT / "evaluation/search-m006/queries.json").read_text())["queries"]
    changes, regressions, losses = [], [], []
    for row in rows:
        payload = {
            k: v
            for k, v in row.items()
            if k in {"text", "cutoff", "before_period_end", "source_id"}
        }
        pools = []
        observations = {}
        for name, search in [("old_collection", old), ("expanded", expanded)]:
            pool, _ = search.candidate_pool(search.query(payload))
            pools.append([c["id"] for c in pool])
            result = search.search(payload, method="context_m007")
            ids = [c["id"] for c in result["results"]]
            observations[name] = {
                "ranked_ids": ids,
                "status": result["status"],
                "useful_ranks": {
                    i: ids.index(i) + 1 if i in ids else None for i in row["expected_useful_cases"]
                },
            }
        if pools[0] != [i for i in pools[1] if i in old.by_id]:
            raise ValueError("Legacy probe changed eligibility of an existing case")
        before, after = observations["old_collection"], observations["expanded"]
        if before["ranked_ids"] != after["ranked_ids"]:
            changes.append(
                {
                    "id": row["id"],
                    "text": row["text"],
                    "legacy_expect_empty": row["expect_empty"],
                    **observations,
                }
            )
        if any(
            rank is not None and (after["useful_ranks"][i] or 6) > rank
            for i, rank in before["useful_ranks"].items()
        ):
            regressions.append(row["id"])
        if any(
            rank is not None and after["useful_ranks"][i] is None
            for i, rank in before["useful_ranks"].items()
        ):
            losses.append(row["id"])
    return {
        "queries": len(rows),
        "changed_rankings": changes,
        "target_rank_regressions": regressions,
        "target_retrieval_losses": losses,
        "note": "Development rank probe only. Legacy expected-empty labels described the old corpus; new coffee/declining-milk results require source inspection, not automatic false-positive grading. Partial matches need not cover every named input.",
    }


def evaluate():
    freeze = json.loads((DIRECTORY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if path not in freeze["mutable_code"]:
            if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen input changed: {path}")
    inputs = json.loads((DIRECTORY / "checks.json").read_text())
    baseline = json.loads((DIRECTORY / "baseline.json").read_text())
    old, expanded = CaseSearch.load("m006"), CaseSearch.load("m007")
    old_ids = set(old.by_id)
    checks = []
    for row, captured in zip(inputs["queries"], baseline["checks"], strict=True):
        payload = {k: row[k] for k in ("text", "cutoff")}
        methods = {}
        pools = {}
        for name, search, method in [
            ("original", old, "context_v1"),
            ("old_collection", old, "context_m007"),
            ("expanded", expanded, "context_m007"),
        ]:
            pool, excluded = search.candidate_pool(search.query(payload))
            eligible_ids = [c["id"] for c in pool]
            result = search.search(payload, method=method)
            ranked = [{"id": c["id"], "score": c["score"]} for c in result["results"]]
            if name == "original":
                actual = dict(
                    id=row["id"],
                    eligible_ids=eligible_ids,
                    excluded=excluded,
                    status=result["status"],
                    ranked=ranked,
                )
                if actual != captured:
                    raise ValueError(f"Original M006 output changed: {row['id']}")
            ids = [c["id"] for c in ranked]
            methods[name] = {
                "method": method,
                "eligible_ids": eligible_ids,
                "excluded": excluded,
                "ranked": ranked,
                "status": result["status"],
                "useful_ranks": {
                    i: ids.index(i) + 1 if i in ids else None for i in row["expected_useful_cases"]
                },
                "unexpected_candidates": bool(row["expect_empty"] and ids),
                "forbidden_returned": sorted(set(ids) & set(row.get("forbidden_cases", []))),
            }
            pools[name] = eligible_ids
        if pools["original"] != pools["old_collection"]:
            raise ValueError("Vocabulary changed eligibility")
        if pools["old_collection"] != [i for i in pools["expanded"] if i in old_ids]:
            raise ValueError("Expansion changed eligibility of an existing case")
        checks.append({**row, **methods})

    def found(c, name):
        return all(r is not None for r in c[name]["useful_ranks"].values())

    positives = [c for c in checks if not c["expect_empty"]]
    negatives = [c for c in checks if c["expect_empty"]]
    summary = {
        "queries": len(checks),
        "useful_queries": len(positives),
        "expected_empty_queries": len(negatives),
    }
    for name in ("original", "old_collection", "expanded"):
        summary[name] = {
            "useful_found_at_5": sum(found(c, name) for c in positives),
            "unexpected_candidate_queries": sum(
                c[name]["unexpected_candidates"] for c in negatives
            ),
            "forbidden_match_queries": sum(bool(c[name]["forbidden_returned"]) for c in checks),
        }
    summary.update(
        {
            "retrieval_improvements": [
                c["id"]
                for c in positives
                if not found(c, "old_collection") and found(c, "expanded")
            ],
            "retrieval_regressions": [
                c["id"]
                for c in positives
                if found(c, "old_collection") and not found(c, "expanded")
            ],
            "target_rank_regressions": [
                c["id"]
                for c in positives
                if any(
                    rank is not None and (c["expanded"]["useful_ranks"][i] or 6) > rank
                    for i, rank in c["old_collection"]["useful_ranks"].items()
                )
            ],
            "changed_rankings": [
                c["id"]
                for c in checks
                if [r["id"] for r in c["old_collection"]["ranked"]]
                != [r["id"] for r in c["expanded"]["ranked"]]
            ],
            "remaining_failures": [
                c["id"]
                for c in checks
                if (not c["expect_empty"] and not found(c, "expanded"))
                or c["expanded"]["unexpected_candidates"]
                or c["expanded"]["forbidden_returned"]
            ],
        }
    )
    comparisons = []
    for plan in inputs["comparisons"]:
        records = [expanded.details[i] for i in plan["ids"]]
        comparisons.append(
            {
                **plan,
                "records": [
                    {
                        k: c[k]
                        for k in (
                            "id",
                            "published",
                            "period",
                            "business_scope",
                            "metric",
                            "figures",
                            "comparison_limit",
                            "unknowns",
                        )
                    }
                    for c in records
                ],
            }
        )
    paths = [
        DIRECTORY / "checks.json",
        DIRECTORY / "freeze.json",
        ROOT / "data/collection/m007/cases.jsonl",
        *[
            ROOT / f"src/ais/{name}.py"
            for name in ("search", "context", "related", "vocabulary", "collection")
        ],
        ROOT / "scripts/check_collection_m007.py",
    ]
    return {
        "provenance": inputs["provenance"],
        "policy": inputs["comparison_policy"],
        "collections": {"old": old.catalog()["total"], "expanded": expanded.catalog()["total"]},
        "fingerprints": {
            str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths
        },
        "summary": summary,
        "checks": checks,
        "comparison_records": comparisons,
        "legacy_query_probe": legacy_probe(old, expanded),
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
        if recorded != result:
            raise ValueError("M007 observations differ; inspect before recording with --write")
    print(json.dumps(result["summary"], indent=2))
