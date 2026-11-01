"""Paired M005 development evaluation on a frozen corpus and query set."""

import argparse
from hashlib import sha256
import json

from ais.pilot import ROOT
from ais.search import CaseSearch

DIRECTORY = ROOT / "evaluation/search-m005"


def evaluate():
    freeze = json.loads((DIRECTORY / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if path == "src/ais/search.py":
            continue  # The changed implementation is fingerprinted below.
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen evaluation input changed: {path}")
    inputs = json.loads((DIRECTORY / "queries.json").read_text())
    baseline = json.loads((DIRECTORY / "baseline.json").read_text())
    search = CaseSearch.load()
    checks = []
    for row, captured in zip(inputs["queries"], baseline["checks"], strict=True):
        payload = {
            k: v
            for k, v in row.items()
            if k in {"text", "cutoff", "before_period_end", "source_id"}
        }
        pool, excluded = search.candidate_pool(search.query(payload))
        ids = [c["id"] for c in pool]
        if ids != captured["eligible_ids"] or excluded != captured["excluded"]:
            raise ValueError(f"Eligible pool differs from frozen baseline: {row['id']}")
        methods = {}
        for name, method in [("old", "literal_v1"), ("new", "related_v1")]:
            result = search.search(payload, method=method)
            if result["eligible_count"] != len(ids) or result["excluded"] != excluded:
                raise ValueError("Method changed the eligible pool")
            ranked = [{"id": c["id"], "score": c["score"]} for c in result["results"]]
            if name == "old" and (
                ranked != captured["ranked"] or result["status"] != captured["status"]
            ):
                raise ValueError(
                    f"Literal method no longer reproduces captured M004 output: {row['id']}"
                )
            ranked_ids = [c["id"] for c in ranked]
            ranks = {
                case_id: ranked_ids.index(case_id) + 1 if case_id in ranked_ids else None
                for case_id in row["expected_useful_cases"]
            }
            methods[name] = {
                "method": method,
                "eligible_ids_sha256": sha256(json.dumps(ids).encode()).hexdigest(),
                "ranked": ranked,
                "useful_ranks": ranks,
                "status": result["status"],
                "matched_count": result["matched_count"],
                "unexpected_candidates": bool(row["expect_empty"] and ranked),
            }
        checks.append({**row, "eligible_ids": ids, "excluded": excluded, **methods})
    positive = [c for c in checks if not c["expect_empty"]]
    negative = [c for c in checks if c["expect_empty"]]

    def hits(check, method):
        return all(rank is not None for rank in check[method]["useful_ranks"].values())

    summary = {
        "queries": len(checks),
        "useful_case_queries": len(positive),
        "expected_empty_queries": len(negative),
        "old_useful_found_at_5": sum(hits(c, "old") for c in positive),
        "new_useful_found_at_5": sum(hits(c, "new") for c in positive),
        "old_unexpected_candidate_queries": sum(
            c["old"]["unexpected_candidates"] for c in negative
        ),
        "new_unexpected_candidate_queries": sum(
            c["new"]["unexpected_candidates"] for c in negative
        ),
        "retrieval_improvements": [
            c["id"] for c in positive if not hits(c, "old") and hits(c, "new")
        ],
        "retrieval_regressions": [
            c["id"] for c in positive if hits(c, "old") and not hits(c, "new")
        ],
        "rank_regressions": [
            c["id"]
            for c in positive
            if any(
                c["old"]["useful_ranks"][case] is not None
                and (c["new"]["useful_ranks"][case] or 6) > c["old"]["useful_ranks"][case]
                for case in c["expected_useful_cases"]
            )
        ],
        "false_positive_regressions": [
            c["id"]
            for c in negative
            if not c["old"]["unexpected_candidates"] and c["new"]["unexpected_candidates"]
        ],
        "false_positive_improvements": [
            c["id"]
            for c in negative
            if c["old"]["unexpected_candidates"] and not c["new"]["unexpected_candidates"]
        ],
    }
    fingerprints = {
        str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
        for path in [
            DIRECTORY / "queries.json",
            DIRECTORY / "freeze.json",
            DIRECTORY / "baseline.json",
            ROOT / "src/ais/search.py",
            ROOT / "src/ais/related.py",
        ]
    }
    return {
        "scope": "Assistant-authored development checks, selected with knowledge of M004 misses. Expected useful cases are not exhaustive relevance grades; no independent validation or causal claims.",
        "fingerprints": fingerprints,
        "summary": summary,
        "checks": checks,
    }


def report_text(report):
    s = report["summary"]
    lines = [
        "# M005 paired search checks",
        "",
        report["scope"],
        "",
        f"Across {s['useful_case_queries']} useful-case queries, expected cases appeared in the first five in {s['old_useful_found_at_5']} old / {s['new_useful_found_at_5']} new results.",
        f"Across {s['expected_empty_queries']} expected-empty queries, unexpected candidates appeared in {s['old_unexpected_candidate_queries']} old / {s['new_unexpected_candidate_queries']} new results.",
        "",
        "| Query ID | Expected useful case(s) | Old rank(s) | New rank(s) | Unexpected candidates old → new |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in report["checks"]:
        old = ", ".join(str(r) if r else "miss" for r in c["old"]["useful_ranks"].values()) or "—"
        new = ", ".join(str(r) if r else "miss" for r in c["new"]["useful_ranks"].values()) or "—"
        flags = (
            f"{c['old']['unexpected_candidates']} → {c['new']['unexpected_candidates']}"
            if c["expect_empty"]
            else "—"
        )
        lines.append(
            f"| {c['id']} | {', '.join(c['expected_useful_cases']) or 'expect empty'} | {old} | {new} | {flags} |"
        )
    lines += ["", "Changes (query IDs):"]
    for key in [
        "retrieval_improvements",
        "retrieval_regressions",
        "rank_regressions",
        "false_positive_regressions",
        "false_positive_improvements",
    ]:
        lines.append(f"- {key.replace('_', ' ')}: {', '.join(s[key]) or 'none'}")
    lines += [
        "",
        "Both methods use the same ordered eligible, deduplicated pool per query; IDs and matching pool hashes are recorded in results.json. The old method must reproduce every captured baseline rank and score. No cases or source records were added or changed.",
        "",
        "The old method uses literal BM25 on allowlisted challenge text plus a shared pressure-word gate. The new method uses the same BM25 formula on named families from pressure passages only. A fixed vocabulary joins related inputs; generic ingredient/commodity words do not rank a case. This changes both the vocabulary and scoring representation, not the eligibility rules. No responses, outcomes or business identity are used to build concepts.",
        "",
        "Remaining limits: related inputs are not identical materials. The vocabulary does not reliably understand industry, sales versus input costs, direction of change or mixed negation. Falling milk costs, booming milk sales and airline fuel can produce misleading candidates; oil paintings already misled the old method. The mixed-negation query can still lose a useful packaging match. Explicitly negative/unknown clauses remain excluded. The app displays its term links and cautions; this is not a general relevance model.",
        "",
        "Inputs and expected cases were frozen in commit cb1b37c before search changes, from M004 base bd2046f. The 33 queries were deliberately chosen development examples, not a held-out benchmark. Run `make search-check` to verify the freeze, reproduce the literal baseline, and compare the new results without network access. `PYTHONPATH=src python3 scripts/evaluate_search.py --write` records outputs. No model experiment was rerun.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write actual results and report")
    args = parser.parse_args()
    report = evaluate()
    if args.write:
        (DIRECTORY / "results.json").write_text(json.dumps(report, indent=2) + "\n")
        (DIRECTORY / "report.md").write_text(report_text(report))
    print(json.dumps(report["summary"], indent=2))
