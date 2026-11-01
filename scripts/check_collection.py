"""Reproduce the small collection checks without fetching sources or models."""

import argparse
from hashlib import sha256
import json

from ais.collection import COLLECTION, load_collection
from ais.pilot import ROOT
from ais.search import CaseSearch


def run():
    records = load_collection()
    search = CaseSearch.load()
    path = ROOT / "evaluation/collection/queries.json"
    inputs = json.loads(path.read_text())
    checks = []
    for query in inputs["queries"]:
        result = search.search(
            {"text": query["text"], "cutoff": inputs["cutoff"]}, method="literal_v1"
        )
        ids = [case["id"] for case in result["results"]]
        expected = query["useful_case"]
        checks.append(
            {
                **query,
                "ranked_ids": ids,
                "status": result["status"],
                "useful_case_rank": ids.index(expected) + 1 if expected in ids else None,
                "finding": "unsupported situation correctly left empty"
                if expected is None and not ids
                else "useful case retrieved"
                if expected in ids
                else "useful case missed",
            }
        )
    return {
        "query_inputs_sha256": sha256(path.read_bytes()).hexdigest(),
        "collection_sha256": sha256(COLLECTION.read_bytes()).hexdigest(),
        "additional_cases": len(records),
        "app_cases": search.catalog()["total"],
        "note": "Development observations only. Misses are reported, not converted to passing relevance judgements. Source access was checked manually; this command is offline.",
        "checks": checks,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write", action="store_true", help="Save observed rankings outside the frozen pilot"
    )
    args = parser.parse_args()
    report = json.dumps(run(), indent=2, ensure_ascii=False) + "\n"
    if args.write:
        (ROOT / "evaluation/collection/results.json").write_text(report)
    print(report, end="")
