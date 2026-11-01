"""Paired development evaluation on frozen queries and identical eligible cases."""

import argparse
from hashlib import sha256
import json

from ais.pilot import ROOT
from ais.search import CaseSearch


def evaluate(module="m006"):
    directory = ROOT / f"evaluation/search-{module}"
    old_method, new_method = (
        ("literal_v1", "related_v1") if module == "m005" else ("related_v1", "context_v1")
    )
    freeze = json.loads((directory / "freeze.json").read_text())
    for path, expected in freeze["sha256"].items():
        if path == "src/ais/search.py":
            continue  # The changed implementation is fingerprinted below.
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen evaluation input changed: {path}")
    inputs = json.loads((directory / "queries.json").read_text())
    baseline = json.loads((directory / "baseline.json").read_text())
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
        for name, method in [("old", old_method), ("new", new_method)]:
            result = search.search(payload, method=method)
            if result["eligible_count"] != len(ids) or result["excluded"] != excluded:
                raise ValueError("Method changed the eligible pool")
            ranked = [{"id": c["id"], "score": c["score"]} for c in result["results"]]
            if name == "old" and (
                ranked != captured["ranked"] or result["status"] != captured["status"]
            ):
                raise ValueError(f"Old method no longer reproduces captured baseline: {row['id']}")
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
                "forbidden_returned": sorted(set(ranked_ids) & set(row.get("forbidden_cases", []))),
                "query_reading": result.get("query_reading"),
                "context_filtered": result.get("context_filtered", {}),
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
        "old_forbidden_match_queries": sum(bool(c["old"]["forbidden_returned"]) for c in checks),
        "new_forbidden_match_queries": sum(bool(c["new"]["forbidden_returned"]) for c in checks),
        "top_result_changes": [
            c["id"]
            for c in checks
            if [r["id"] for r in c["old"]["ranked"][:1]]
            != [r["id"] for r in c["new"]["ranked"][:1]]
        ],
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
        "remaining_failures": [
            c["id"]
            for c in checks
            if (not c["expect_empty"] and not hits(c, "new"))
            or c["new"]["unexpected_candidates"]
            or c["new"]["forbidden_returned"]
        ],
    }
    fingerprints = {
        str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
        for path in [
            directory / "queries.json",
            directory / "freeze.json",
            directory / "baseline.json",
            ROOT / "src/ais/search.py",
            ROOT / "src/ais/related.py",
            ROOT / "src/ais/context.py",
        ]
    }
    return {
        "module": module,
        "scope": inputs["provenance"] + " No independent validation or causal claims.",
        "fingerprints": fingerprints,
        "summary": summary,
        "checks": checks,
    }


def report_text(report):
    s = report["summary"]
    lines = [
        f"# {report['module'].upper()} paired search checks",
        "",
        report["scope"],
        "",
        f"Across {s['useful_case_queries']} useful-case queries, expected cases appeared in the first five in {s['old_useful_found_at_5']} old / {s['new_useful_found_at_5']} new results.",
        f"Across {s['expected_empty_queries']} expected-empty queries, unexpected candidates appeared in {s['old_unexpected_candidate_queries']} old / {s['new_unexpected_candidate_queries']} new results.",
        f"Queries returning explicitly forbidden cases: {s['old_forbidden_match_queries']} old / {s['new_forbidden_match_queries']} new.",
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
        "top_result_changes",
        "remaining_failures",
    ]:
        lines.append(f"- {key.replace('_', ' ')}: {', '.join(s[key]) or 'none'}")
    lines += [
        "",
        "Both methods use the same ordered eligible, deduplicated pool per query; IDs and matching pool hashes are recorded in results.json. The old method must reproduce every captured baseline rank and score. No cases or source records were added or changed.",
        "",
        "M005 related_v1 is reproduced unchanged. M006 context_v1 retains its vocabulary and BM25 formula, reading only pressure passages. General clause rules separate inputs from sales/demand, identify rising/falling/unspecified directions, split contrast and independent assertions, remove denied/unknown statements, and recognize explicit non-consumer-goods business contexts. Product names in recognized business descriptions do not become input evidence. Opposite directions for any shared input veto a partial match on another input. Bare topic lists remain searches with unspecified direction; they are never labelled as increases in the query.",
        "",
        "Packaging investigation: M005 discarded the negated milk clause, leaving one packaging term. Compressed passage lengths then favour CL-2008 (one input family) over CL-2022 (packaging plus transport), through BM25 length normalization. A packaging-only query cannot justify preferring the latter case; CL-2022 stays useful at rank 3. M006 restores mixed-negation searches without forcing this case upward. The broader packaging/logistics query retains CL-2022 first. Scores and every rank are recorded; rank is not analogy quality.",
        "For the frozen mixed-clauses query, both methods give CL-2008 1.363102, CL-2015 1.056404, CL-2022 1.056404 and NES-WATERS-2011-H1 0.862371. CL-2015 and CL-2022 tie and are ordered by ID, not domain preference.",
        "",
        "Limits: this explicit grammar and industry vocabulary are incomplete. Complex attachment, omitted subjects, unlisted word senses/sectors, predictions and long-distance negation can still fail. Ignored statements and the interpreted direction are visible in the app. Related inputs are not identical materials; unknown source facts and action effects remain unknown. A passing development query does not validate general understanding or response effectiveness.",
        "Post-implementation diagnostics (diagnostics.json, excluded from frozen evaluation counts) still find safe but useful-case misses for unpunctuated 'rising not falling' and comma-linked opposite input changes. Mentioning a logistics supplier can also cause conservative industry rejection even when the business is a food maker. No frozen-query failures is not a claim of no remaining search failures.",
        "",
        "The 65 query texts, expectations and M005 baseline were frozen in 234fab0; b1f85a7 corrected one mixed-direction expectation before implementation to exclude a case with explicitly opposite dairy costs. No labels changed after method edits. These queries were chosen with knowledge of M005 failures and are not held-out or human judgements. `make search-check` reproduces M006; `make search-check-m005` reproduces historical M005 ranks without rewriting its files. `PYTHONPATH=src python3 scripts/evaluate_search.py --write` records M006 outputs. No case records or model experiment changed.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", choices=["m005", "m006"], default="m006")
    parser.add_argument("--write", action="store_true", help="Write actual results and report")
    args = parser.parse_args()
    if args.write and args.module == "m005":
        parser.error("Historical M005 outputs are frozen; run without --write.")
    directory = ROOT / f"evaluation/search-{args.module}"
    report = evaluate(args.module)
    if args.write:
        (directory / "results.json").write_text(json.dumps(report, indent=2) + "\n")
        (directory / "report.md").write_text(report_text(report))
    print(json.dumps(report["summary"], indent=2))
