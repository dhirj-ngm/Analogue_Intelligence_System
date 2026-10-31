"""Check that saved runs cover precisely the frozen candidate sets."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ais.pilot import ROOT, eligible, fingerprint, metrics, read_jsonl

cases = read_jsonl(ROOT / "data/pilot/cases.jsonl")
queries = read_jsonl(ROOT / "evaluation/pilot/queries.jsonl")
labels = read_jsonl(ROOT / "evaluation/pilot/judgements.jsonl")
results = json.loads((ROOT / "evaluation/pilot/baselines/rankings.json").read_text())
assert fingerprint() == json.loads((ROOT / "evaluation/pilot/freeze-manifest.json").read_text())
assert len(results) == 2 * len(queries)
assert len({(r["query_id"], r["method"]) for r in results}) == len(results)
for q in queries:
    expected = {c["id"] for c in cases if eligible(q, c)[0]}
    grades = {j["case_id"]: j["grade"] for j in labels if j["query_id"] == q["id"]}
    paired = [r for r in results if r["query_id"] == q["id"]]
    assert {r["method"] for r in paired} == {"bm25", "dense"}
    for r in paired:
        ids = [x["id"] for x in r["ranking"]]
        assert len(ids) == len(expected) and set(ids) == expected
        assert metrics(ids, grades) == r["metrics"]
print("Frozen hashes, both methods, all eligible candidates and saved metrics verified.")
