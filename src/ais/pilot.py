"""Small, auditable historical retrieval pilot."""

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re
import time
import platform
import subprocess
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[2]
INPUTS = [
    "data/pilot/cases.jsonl",
    "evaluation/pilot/queries.jsonl",
    "evaluation/pilot/judgements.jsonl",
    "evaluation/pilot/protocol.md",
    "configs/pilot/baseline.json",
]


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def fingerprint():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS}


def eligible(query, case):
    if case["id"] == query.get("source_id"):
        return False, "self"
    if case["duplicate_group"] in query.get("exclude_groups", []):
        return False, "duplicate_or_continuation"
    if not case.get("publication_date"):
        return False, "unknown_publication_date"
    if date.fromisoformat(case["publication_date"]) > date.fromisoformat(query["cutoff"]):
        return False, "after_cutoff"
    if case["period_end"] >= query["before_period_end"]:
        return False, "not_earlier_observation"
    return True, "eligible"


def ranking_text(case):
    # Explicit allowlist: no response, metric, tags, rationale or later outcome.
    return case["challenge"]


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def bm25(query, documents, k1=1.2, b=0.75):
    if not documents:
        return []
    docs = [Counter(tokens(d)) for d in documents]
    avg = sum(sum(d.values()) for d in docs) / len(docs)
    scores = []
    for doc in docs:
        score = 0.0
        for term in set(tokens(query)):
            df = sum(term in d for d in docs)
            idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
            tf = doc[term]
            if tf:
                score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * sum(doc.values()) / avg))
        scores.append(score)
    return scores


def metrics(ranked_ids, grades, k=5):
    selected = [grades[i] for i in ranked_ids[:k]]

    def dcg(values):
        return sum((2**g - 1) / math.log2(i + 2) for i, g in enumerate(values))

    ideal = dcg(sorted(grades.values(), reverse=True)[:k])
    return {
        "precision_at_5": sum(g >= 2 for g in selected) / k,
        "ndcg_at_5": dcg(selected) / ideal if ideal else 0.0,
        "no_relevant_candidates": not any(g >= 2 for g in grades.values()),
    }


def validate(cases, queries, judgements):
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate case ID")
    for c in cases:
        if (
            not ranking_text(c).strip()
            or not c["source_url"].startswith("https://")
            or not c["locator"]
        ):
            raise ValueError("Missing evidence or challenge")
        if (
            not date.fromisoformat(c["period_start"])
            <= date.fromisoformat(c["period_end"])
            <= date.fromisoformat(c["publication_date"])
        ):
            raise ValueError("Invalid date ordering")
        if c["human_reviewed"]:
            raise ValueError("Pilot must not imply full human review")
        if not c["metric"]["unit"] or not c["metric"]["basis"]:
            raise ValueError("Missing metric definition")
    qids = [q["id"] for q in queries]
    if len(set(qids)) != len(qids):
        raise ValueError("Duplicate query ID")
    expected = {(q["id"], c["id"]) for q in queries for c in cases if eligible(q, c)[0]}
    actual = [(j["query_id"], j["case_id"]) for j in judgements]
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError("Judgement coverage differs from eligible pairs")
    for j in judgements:
        if j["grade"] not in range(4) or not j["rationale"]:
            raise ValueError("Invalid judgement")
    for q in queries:
        if q.get("source_id"):
            source = next(c for c in cases if c["id"] == q["source_id"])
            if source["publication_date"] > q["cutoff"]:
                raise ValueError("Query evidence after cutoff")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "freeze", "run", "search"])
    parser.add_argument("--text")
    parser.add_argument("--cutoff", default="2023-12-31")
    args = parser.parse_args()
    cases = read_jsonl(ROOT / INPUTS[0])
    queries = read_jsonl(ROOT / INPUTS[1])
    judgements = read_jsonl(ROOT / INPUTS[2])
    validate(cases, queries, judgements)
    frozen_path = ROOT / "evaluation/pilot/freeze-manifest.json"
    if args.command == "validate":
        print(
            f"Valid: {len(cases)} cases, {len(queries)} queries, {len(judgements)} eligible judgements"
        )
        return
    if args.command == "freeze":
        if frozen_path.exists():
            raise ValueError("Freeze already exists; create an explicit new benchmark version")
        frozen_path.write_text(json.dumps(fingerprint(), indent=2) + "\n")
        print("Inputs frozen before rankings")
        return
    if json.loads(frozen_path.read_text()) != fingerprint():
        raise ValueError("Frozen input mismatch")
    if args.command == "search":
        if not args.text:
            parser.error("--text required")
        query = dict(cutoff=args.cutoff, before_period_end=args.cutoff)
        candidates = [c for c in cases if eligible(query, c)[0]]
        scores = bm25(args.text, [ranking_text(c) for c in candidates])
        for c, score in sorted(zip(candidates, scores), key=lambda x: (-x[1], x[0]["id"]))[:5]:
            print(
                json.dumps(
                    dict(
                        case=c,
                        bm25_score=score,
                        warning="Uncalibrated candidate; inspect evidence and differences",
                    ),
                    ensure_ascii=False,
                )
            )
        return
    from sentence_transformers import SentenceTransformer

    config = json.loads((ROOT / INPUTS[4]).read_text())
    started = time.monotonic()
    model = SentenceTransformer(
        config["model"],
        revision=config["revision"],
        device="cpu",
        cache_folder=str(ROOT / "models"),
    )
    output = []
    eligibility = []
    for q in queries:
        candidates = []
        for c in cases:
            ok, reason = eligible(q, c)
            eligibility.append(dict(query_id=q["id"], case_id=c["id"], eligible=ok, reason=reason))
            if ok:
                candidates.append(c)
        docs = [ranking_text(c) for c in candidates]
        embeddings = model.encode(
            [q["text"]] + docs, normalize_embeddings=True, show_progress_bar=False
        )
        scores = dict(
            bm25=bm25(q["text"], docs, config["bm25_k1"], config["bm25_b"]),
            dense=(embeddings[1:] @ embeddings[0]).tolist(),
        )
        grades = {j["case_id"]: j["grade"] for j in judgements if j["query_id"] == q["id"]}
        for method, values in scores.items():
            ranked = sorted(zip(candidates, values), key=lambda x: (-x[1], x[0]["id"]))
            output.append(
                dict(
                    query_id=q["id"],
                    method=method,
                    ranking=[dict(id=c["id"], score=float(v)) for c, v in ranked],
                    metrics=metrics([c["id"] for c, _ in ranked], grades),
                )
            )
    out = ROOT / "evaluation/pilot/baselines"
    out.mkdir(exist_ok=True)
    (out / "rankings.json").write_text(json.dumps(output, indent=2) + "\n")
    (ROOT / "evaluation/pilot/eligibility.jsonl").write_text(
        "".join(json.dumps(x) + "\n" for x in eligibility)
    )
    (out / "run-manifest.json").write_text(
        json.dumps(
            dict(
                inputs=fingerprint(),
                config=config,
                elapsed_seconds=time.monotonic() - started,
                device="cpu",
                review="assistant; descriptive only",
                python=platform.python_version(),
                packages={
                    name: version(name)
                    for name in ["sentence-transformers", "torch", "transformers", "numpy"]
                },
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                git_base=subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
                git_dirty=bool(
                    subprocess.check_output(
                        ["git", "status", "--porcelain"], cwd=ROOT, text=True
                    ).strip()
                ),
            ),
            indent=2,
        )
        + "\n"
    )
    print(
        json.dumps([{k: r[k] for k in ["query_id", "method", "metrics"]} for r in output], indent=2)
    )


if __name__ == "__main__":
    main()
