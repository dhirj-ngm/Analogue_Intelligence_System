"""Additional source-linked cases, separate from the frozen M001 pilot.

One canonical record holds each situation. The adapter exposes the existing
search interface; only its pressure description enters first-stage ranking.
"""

from copy import deepcopy
from datetime import date
from urllib.parse import urlsplit

from ais.pilot import ROOT, read_jsonl

COLLECTION = ROOT / "data/collection/cases.jsonl"
M007 = ROOT / "data/collection/m007/cases.jsonl"
M011 = ROOT / "data/collection/m011/cases.jsonl"
FIELDS = ("pressure", "margin_or_profit", "other_drivers", "response")


def validate(records):
    ids, groups = set(), set()
    for case in records:

        def require(condition, message):
            if not condition:
                raise ValueError(f"{case.get('id', 'unknown case')}: {message}")

        require(case["id"] not in ids, "duplicate ID")
        require(case["duplicate_group"] not in groups, "continuing situation counted twice")
        ids.add(case["id"])
        groups.add(case["duplicate_group"])
        start, end = case["period"]["start"], case["period"]["end"]
        for day in (start, end, case["published"], case["checked_on"]):
            require(date.fromisoformat(day).isoformat() == day, "invalid ISO date")
        require(start <= end <= case["published"], "invalid reporting/publication dates")
        require(case["company"] and case["business_scope"], "business scope missing")
        require(case["unknowns"] and case["episode_boundary"], "unknowns or boundary missing")
        require(case["human_reviewed"] is False, "human review has not occurred")
        require(
            case["review_status"] == "assistant_source_checked; human_review_pending",
            "review provenance missing",
        )
        sources = {s["url"]: s for s in case["sources"]}
        require(len(sources) == len(case["sources"]), "duplicate source URL")
        for source in sources.values():
            url = urlsplit(source["url"])
            require(
                url.scheme == "https" and url.hostname and not url.username and not url.password,
                "unsafe source URL",
            )
            require(
                source["access"]["method"] and source["access"]["checked_on"],
                "access check missing",
            )
            require(
                source["retention"] and source["publication_evidence"]["locator"],
                "source provenance missing",
            )
            require(source["document_retained"] is False, "source documents must remain external")
            require(
                case["published"] <= source["published"] <= case["checked_on"],
                "source date mismatch",
            )

        def evidence(item):
            ref = item["evidence"]
            require(ref["url"] in sources, "evidence source is undeclared")
            require(
                ref["public_date"] == sources[ref["url"]]["published"],
                "evidence publication mismatch",
            )
            require(
                ref["locator"] and ref["period_start"] == start and ref["period_end"] == end,
                "evidence scope mismatch",
            )

        for key in FIELDS:
            require(case[key]["value"] and case[key]["kind"], "field attribution missing")
            evidence(case[key])
        for metric in [case["metric"], *case["figures"]]:
            for key in ("name", "unit", "basis", "scope", "comparison", "kind"):
                require(bool(metric[key]), f"metric {key} missing")
            require(
                isinstance(metric["value"], (int, float)) and not isinstance(metric["value"], bool),
                "metric must be numeric",
            )
            require(
                metric["unit"]
                in {
                    "percent",
                    "USD million",
                    "basis points",
                    "USD per 100 lb",
                    "JPY billion",
                    "ZAR million",
                },
                "unsupported metric unit",
            )
            evidence(metric)
        for conflict in case["conflicts"]:
            require(
                conflict["value"] and len(conflict["sources"]) >= 2, "conflict needs both sources"
            )
            for ref in conflict["sources"]:
                evidence({"evidence": ref})
    return records


def load_collection(version="m011"):
    if version not in {"m006", "m007", "m011"}:
        raise ValueError("Unknown collection version.")
    records = read_jsonl(COLLECTION)
    if version in {"m007", "m011"}:
        records += read_jsonl(M007)
    if version == "m011":
        records += read_jsonl(M011)
    return validate(records)


def search_records(records):
    flat, details = [], []
    for record in records:
        case = deepcopy(record)
        ref = case["pressure"]["evidence"]
        flat.append(
            {
                "id": case["id"],
                "company": case["company"],
                "period_start": case["period"]["start"],
                "period_end": case["period"]["end"],
                "publication_date": case["published"],
                "source_url": ref["url"],
                "locator": ref["locator"],
                "challenge": case["pressure"]["value"],
                "duplicate_group": case["duplicate_group"],
                "limitations": case["episode_boundary"],
                "evidence_excerpt": case["excerpt"],
            }
        )
        details.append(case)
    return flat, details


if __name__ == "__main__":
    records = load_collection()
    print(f"Validated {len(records)} additional situations; source documents remain external.")
