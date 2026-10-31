"""Read-only reader search. Frozen pilot data and results are never rewritten."""

from collections import Counter
from copy import deepcopy
from datetime import date
import re
from urllib.parse import urlsplit

from ais.pilot import ROOT, bm25, eligible, ranking_text, read_jsonl, tokens

# These words alone do not establish a specific, supported pressure match.
FILLER = set(
    "a an and are as at be been being business by can case cases company companies "
    "cost costs could decline declined declining decrease decreased effect effects facing "
    "fell for from gross had has have higher how i in increase increased increases "
    "inflation input inputs is it its lower margin margins material materials may my "
    "of on operating or our pressure pressures profit profits reported reports reporting "
    "rose rising situation than that the their this to was we were what when which "
    "while with would year years".split()
)


def specific_terms(text):
    return set(tokens(text)) - FILLER


def pressure_terms(text):
    # Conservative handling of explicit unknown/negated clauses in curated records.
    clauses = re.split(r"[;.]", text)
    return specific_terms(
        " ".join(
            c for c in clauses if not re.search(r"\b(no|not|unknown|unestablished)\b", c, re.I)
        )
    )


def iso_date(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label} must be a date in YYYY-MM-DD format.")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{label} is not a valid calendar date.") from None
    return value


def safe_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Case evidence must have a public HTTPS source URL.")
    return value


class CaseSearch:
    def __init__(self, cases, structured):
        self.cases = deepcopy(cases)
        self.details = {c["id"]: deepcopy(c) for c in structured}
        self.by_id = {c["id"]: c for c in self.cases}
        if len(self.by_id) != len(cases) or len(self.details) != len(structured):
            raise ValueError("Case IDs must be unique.")
        if self.by_id.keys() != self.details.keys():
            raise ValueError("Structured and retrieval cases must have identical IDs.")
        for case in self.cases:
            detail = self.details[case["id"]]
            for key in ("period_start", "period_end"):
                iso_date(case[key], key)
            if case.get("publication_date"):
                iso_date(case["publication_date"], "Publication date")
            if case["period_start"] > case["period_end"]:
                raise ValueError("Case reporting period is reversed.")
            if case.get("publication_date") and case["publication_date"] < case["period_end"]:
                raise ValueError("Case publication precedes its reporting period end.")
            if (
                detail["company"] != case["company"]
                or detail["period"] != {"start": case["period_start"], "end": case["period_end"]}
                or detail["published"] != case.get("publication_date")
            ):
                raise ValueError("Case identity, period or publication metadata disagree.")
            safe_url(case["source_url"])
            if not ranking_text(case).strip() or not case.get("duplicate_group"):
                raise ValueError("Cases need challenge text and a duplicate/continuation group.")
            for key in ("pressure", "margin_or_profit", "other_drivers", "response"):
                evidence = detail[key]["evidence"]
                safe_url(evidence["url"])
                if not evidence["locator"]:
                    raise ValueError("A source locator is required for each field.")
                if evidence.get("public_date"):
                    iso_date(evidence["public_date"], "Evidence publication date")

    @classmethod
    def load(cls):
        return cls(
            read_jsonl(ROOT / "data/pilot/cases.jsonl"),
            read_jsonl(ROOT / "data/pilot/cases-structured-v2.jsonl"),
        )

    def catalog(self):
        return {
            "total": len(self.cases),
            "companies": len({c["company"] for c in self.cases}),
            "default_date": date.today().isoformat(),
            "cases": [
                {
                    "id": c["id"],
                    "company": c["company"],
                    "period_end": c["period_end"],
                    "published": c["publication_date"],
                    "challenge": ranking_text(c),
                }
                for c in self.cases
            ],
        }

    def query(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Search must be a JSON object.")
        text = payload.get("text")
        if not isinstance(text, str) or not 3 <= len(text.strip()) <= 2000:
            raise ValueError("Describe a situation using 3–2000 characters.")
        cutoff = iso_date(payload.get("cutoff"), "Publication cutoff")
        supplied_end = payload.get("before_period_end")
        before = iso_date(
            cutoff if supplied_end in (None, "") else supplied_end, "Situation period end"
        )
        if before > cutoff:
            raise ValueError("Situation period end cannot be after the publication cutoff.")
        source_id = payload.get("source_id")
        if source_id == "":
            source_id = None
        if source_id is not None and (
            not isinstance(source_id, str) or source_id not in self.by_id
        ):
            raise ValueError("Choose a known source case or leave it blank.")
        company = payload.get("company", "")
        if not isinstance(company, str) or len(company) > 100:
            raise ValueError("Company must be text of at most 100 characters.")
        query = {
            "text": text.strip(),
            "cutoff": cutoff,
            "before_period_end": before,
            "source_id": source_id,
            "exclude_groups": [],
            "company": company.strip(),
        }
        if source_id:
            source = self.by_id[source_id]
            # Query evidence itself must be public, not just its reporting period.
            if self.evidence_reason(source, cutoff):
                raise ValueError(
                    "The selected source case's challenge was not public by this cutoff."
                )
            query["before_period_end"] = min(before, source["period_end"])
            query["exclude_groups"] = [source["duplicate_group"]]
            query["company"] = source["company"]
        return query

    def evidence_reason(self, case, cutoff):
        detail = self.details[case["id"]]
        # Original ranking_text includes challenge/context; check all of its source fields.
        dates = [case.get("publication_date"), detail.get("published")]
        dates += [
            detail[key]["evidence"].get("public_date")
            for key in ("pressure", "margin_or_profit", "other_drivers")
        ]
        if any(not d for d in dates):
            return "unknown_challenge_date"
        if any(d > cutoff for d in dates):
            return "challenge_evidence_after_cutoff"
        return None

    def search(self, payload):
        query = self.query(payload)
        exclusions = Counter()
        candidates = []
        seen = set()
        for case in sorted(self.cases, key=lambda c: (c.get("publication_date") or "", c["id"])):
            ok, reason = eligible(query, case)
            reason = reason if not ok else self.evidence_reason(case, query["cutoff"])
            if reason:
                exclusions[reason] += 1
                continue
            if case["duplicate_group"] in seen:
                exclusions["duplicate_or_continuation"] += 1
                continue
            seen.add(case["duplicate_group"])
            candidates.append(case)
        # Reuse the baseline on the identical admissible, deduplicated pool.
        scores = bm25(query["text"], [ranking_text(c) for c in candidates])
        requested = pressure_terms(query["text"])
        matches = []
        for case, score in zip(candidates, scores):
            matched = sorted(
                requested & pressure_terms(self.details[case["id"]]["pressure"]["value"])
            )
            if score > 0 and matched:
                matches.append(self.present(case, query, score, matched))
        matches.sort(key=lambda c: (-c["score"], c["id"]))
        return {
            "status": "candidates" if matches else "insufficient_evidence",
            "message": (
                "Partial pressure matches — inspect the evidence and differences."
                if matches
                else "Insufficient evidence for a comparison in this corpus. "
                "No eligible case has a specific pressure-term match. "
                "Try naming a material, disruption or other pressure, or adjust the dates."
            ),
            "query": query,
            "eligible_count": len(candidates),
            "matched_count": len(matches),
            "excluded": dict(sorted(exclusions.items())),
            "results": matches[:5],
            "method": "BM25 on challenge text only; specific pressure-term overlap required. "
            "Scores are not confidence or probabilities. This lexical gate is not a relevance model.",
        }

    def present(self, case, query, score, matched):
        detail = self.details[case["id"]]
        fields = {}
        for key in ("pressure", "margin_or_profit", "other_drivers", "response"):
            field = detail[key]
            public = field["evidence"].get("public_date")
            visible = bool(public and public <= query["cutoff"])
            fields[key] = {
                "value": field["value"] if visible else "Not available by the selected cutoff.",
                "kind": field["kind"],
                "available": visible,
                "evidence": deepcopy(field["evidence"]) if visible else None,
            }
        differences = [detail["comparison_limit"], case["limitations"]]
        if query["company"]:
            same = query["company"].casefold() == case["company"].casefold()
            differences.append(
                "Earlier observation at the same company; scope and conditions may have changed."
                if same
                else f"Different company: {case['company']}. Exposures and constraints may differ."
            )
        differences.append(
            "Your situation's metric basis and business scope need separate verification."
        )
        return {
            "id": case["id"],
            "company": case["company"],
            "period": deepcopy(detail["period"]),
            "published": detail["published"],
            "score": round(float(score), 6),
            "matching_pressure_terms": matched,
            "unmatched_terms": sorted(specific_terms(query["text"]) - set(matched)),
            "fields": fields,
            "metric": deepcopy(detail["metric"]),
            "important_differences": list(dict.fromkeys(differences)),
            "unknowns": list(detail["unknowns"])
            + [
                "Action-level rationale and later outcomes are not established in these case records."
            ],
            "source": {
                "url": case["source_url"],
                "locator": case["locator"],
                "excerpt": case["evidence_excerpt"],
            },
            "review_status": detail["review_status"],
        }
