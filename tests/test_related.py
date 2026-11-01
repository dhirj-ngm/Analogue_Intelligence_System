"""Related-input search: source lineage, limits and paired reproducibility."""

from copy import deepcopy
from hashlib import sha256
import json
import unittest

from ais.pilot import ROOT
from ais.related import FAMILIES, analyze
from ais.search import CaseSearch


class RelatedSearchTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load(collection="m006")

    def query(self, text, **options):
        return self.search.search({"text": text, "cutoff": "2026-11-01", **options})

    def test_related_families_apply_to_terms_without_query_or_company_rules(self):
        for text, expected in [
            ("MILK wheat electricity", {"dairy", "grain", "energy"}),
            ("cacao chocolate", {"cocoa"}),
            ("diesel shipping plastic fibre", {"oil", "transport", "resin", "fibre"}),
            ("ingredient commodity cost margin", set()),
            ("General Mills Hershey Nestlé recovery savings", set()),
        ]:
            self.assertEqual(set(analyze(text)[0]), expected)
        aliases = [word for _, terms in FAMILIES.values() for word in terms.split()]
        self.assertEqual(len(aliases), len(set(aliases)))

    def test_three_m004_misses_retrieve_source_backed_cases_first(self):
        for text, case_id in [
            ("milk flour electricity", "GIS-2007"),
            ("chocolate ingredient inflation", "HSY-2025-Q1"),
            ("bottled-water freight and fuel", "NES-WATERS-2011-H1"),
        ]:
            with self.subTest(text=text):
                case = self.query(text)["results"][0]
                self.assertEqual(case["id"], case_id)
                self.assertTrue(
                    any(m["relationship"] == "related_terms" for m in case["pressure_matches"])
                )
                for match in case["pressure_matches"]:
                    self.assertTrue(all(word in text.lower() for word in match["query_terms"]))
                    self.assertTrue(
                        all(
                            word in case["fields"]["pressure"]["value"].lower()
                            for word in match["report_terms"]
                        )
                    )

    def test_negated_clauses_are_removed_before_expansion(self):
        for text in [
            "No milk input-cost pressure",
            "Chocolate cost pressure is unknown",
            "Fuel pressure is unestablished",
        ]:
            self.assertEqual(self.query(text)["results"], [])
        result = self.query("No milk input inflation; cocoa costs rising")
        self.assertEqual([c["id"] for c in result["results"]], ["HSY-2025-Q1"])
        self.assertEqual(result["results"][0]["matching_pressure_terms"], ["cocoa"])

    def test_generic_or_unsupported_words_do_not_create_concepts(self):
        for text in [
            "ingredient costs",
            "commodity inflation",
            "coffee beans",
            "steel costs",
            "lighter bottles",
        ]:
            self.assertEqual(self.query(text)["status"], "insufficient_evidence")

    def test_related_matches_cannot_cross_publication_period_or_self_limits(self):
        for text, case_id, before, day in [
            ("milk flour electricity", "GIS-2007", "2007-07-25", "2007-07-26"),
            ("oil freight", "NES-WATERS-2011-H1", "2011-08-09", "2011-08-10"),
            ("chocolate", "HSY-2025-Q1", "2025-04-30", "2025-05-01"),
        ]:
            self.assertNotIn(case_id, [c["id"] for c in self.query(text, cutoff=before)["results"]])
            self.assertIn(case_id, [c["id"] for c in self.query(text, cutoff=day)["results"]])
            self.assertNotIn(
                case_id, [c["id"] for c in self.query(text, source_id=case_id)["results"]]
            )
            end = self.search.by_id[case_id]["period_end"]
            self.assertNotIn(
                case_id, [c["id"] for c in self.query(text, before_period_end=end)["results"]]
            )

    def test_response_outcome_context_and_challenge_cannot_supply_new_concepts(self):
        payload = dict(text="chocolate", cutoff="2026-11-01")
        before = self.search.search(payload)
        for case in self.search.cases:
            case.update(challenge="chocolate", response="chocolate", follow_up="chocolate")
        for detail in self.search.details.values():
            for field in ["response", "margin_or_profit", "other_drivers"]:
                detail[field]["value"] = "chocolate"
            detail["comparison_limit"] = "chocolate"
            detail["unknowns"] = ["chocolate"]
        after = self.search.search(payload)
        self.assertEqual(
            [(c["id"], c["score"], c["pressure_matches"]) for c in before["results"]],
            [(c["id"], c["score"], c["pressure_matches"]) for c in after["results"]],
        )

    def test_methods_share_pool_when_duplicates_and_future_evidence_are_present(self):
        duplicate = dict(deepcopy(self.search.by_id["GIS-2007"]), id="GIS-CONTINUING")
        detail = dict(deepcopy(self.search.details["GIS-2007"]), id=duplicate["id"])
        search = CaseSearch(
            self.search.cases + [duplicate], list(self.search.details.values()) + [detail]
        )
        search.details["HSY-2025-Q1"]["pressure"]["evidence"]["public_date"] = "2027-01-01"
        old, new = [
            search.search(dict(text="milk cocoa grains", cutoff="2026-11-01"), method=method)
            for method in ["literal_v1", "related_v1"]
        ]
        self.assertEqual(old["eligible_count"], new["eligible_count"])
        self.assertEqual(old["excluded"], new["excluded"])
        self.assertEqual(new["excluded"]["duplicate_or_continuation"], 1)
        self.assertEqual(new["excluded"]["challenge_evidence_after_cutoff"], 1)
        self.assertNotIn(duplicate["id"], [c["id"] for c in new["results"]])

    def test_frozen_inputs_and_paired_observations_include_regressions(self):
        directory = ROOT / "evaluation/search-m005"
        freeze = json.loads((directory / "freeze.json").read_text())
        for path, expected in freeze["sha256"].items():
            if path != "src/ais/search.py":
                self.assertEqual(sha256((ROOT / path).read_bytes()).hexdigest(), expected, path)
        report = json.loads((directory / "results.json").read_text())
        self.assertTrue(report["summary"]["false_positive_regressions"])
        self.assertTrue(report["summary"]["rank_regressions"])
        for check in report["checks"]:
            payload = {
                k: v
                for k, v in check.items()
                if k in {"text", "cutoff", "before_period_end", "source_id"}
            }
            pool, exclusions = self.search.candidate_pool(self.search.query(payload))
            self.assertEqual([c["id"] for c in pool], check["eligible_ids"])
            self.assertEqual(exclusions, check["excluded"])
            self.assertEqual(
                check["old"]["eligible_ids_sha256"], check["new"]["eligible_ids_sha256"]
            )
            for name, method in [("old", "literal_v1"), ("new", "related_v1")]:
                result = self.search.search(payload, method=method)
                self.assertEqual(
                    [dict(id=c["id"], score=c["score"]) for c in result["results"]],
                    check[name]["ranked"],
                )


if __name__ == "__main__":
    unittest.main()
