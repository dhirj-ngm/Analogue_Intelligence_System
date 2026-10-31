"""Run the frozen v2 structured view without claiming full human-label metrics."""

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ais.pilot import bm25, eligible, read_jsonl  # noqa: E402

INPUTS = [
    "data/pilot/cases-structured-v2.jsonl",
    "evaluation/pilot/queries.jsonl",
    "evaluation/pilot/reader-judgements-v2.jsonl",
    "evaluation/pilot/protocol-v2.md",
    "configs/pilot/baseline.json",
]


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in INPUTS}


def challenge(case):
    return " ".join(case[key]["value"] for key in ("pressure", "margin_or_profit", "other_drivers"))


def main():
    cases = read_jsonl(ROOT / INPUTS[0])
    queries = read_jsonl(ROOT / INPUTS[1])
    grades = read_jsonl(ROOT / INPUTS[2])
    assert len(cases) == 10 and len(grades) == 5
    assert all(g["grade"] in range(4) and g["reason"] is None for g in grades)
    manifest = ROOT / "evaluation/pilot/freeze-manifest-v2.json"
    if not manifest.exists():
        manifest.write_text(json.dumps(hashes(), indent=2) + "\n")
    assert json.loads(manifest.read_text()) == hashes(), "v2 input freeze mismatch"
    import os

    os.environ["HF_HUB_OFFLINE"] = "1"
    from sentence_transformers import SentenceTransformer

    config = json.loads((ROOT / INPUTS[4]).read_text())
    model = SentenceTransformer(
        config["model"],
        revision=config["revision"],
        device="cpu",
        cache_folder=str(ROOT / "models"),
    )
    rankings = []
    for q in queries:
        candidates = []
        for case in cases:
            candidate = dict(
                id=case["id"],
                period_end=case["period"]["end"],
                publication_date=case["published"],
                duplicate_group=case["id"],
            )
            if eligible(q, candidate)[0]:
                candidates.append(case)
        docs = [challenge(case) for case in candidates]
        vectors = model.encode(
            [q["text"]] + docs, normalize_embeddings=True, show_progress_bar=False
        )
        methods = {
            "bm25": bm25(q["text"], docs, config["bm25_k1"], config["bm25_b"]),
            "dense": (vectors[1:] @ vectors[0]).tolist(),
        }
        for method, scores in methods.items():
            ranking = [
                case["id"]
                for case, score in sorted(
                    zip(candidates, scores), key=lambda x: (-x[1], x[0]["id"])
                )
            ]
            rankings.append(dict(query_id=q["id"], method=method, ranking=ranking))
    assert all(
        set(a["ranking"]) == set(b["ranking"]) for a, b in zip(rankings[::2], rankings[1::2])
    )
    out = ROOT / "evaluation/pilot/structured-review-ranks-v2.json"
    out.write_text(json.dumps(rankings, indent=2) + "\n")
    print("pair, BM25 position, dense position")
    for item in grades:
        pair = [r for r in rankings if r["query_id"] == item["query_id"]]
        print(item["pair"], *[r["ranking"].index(item["case_id"]) + 1 for r in pair])


if __name__ == "__main__":
    main()
