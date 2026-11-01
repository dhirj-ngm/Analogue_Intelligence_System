"""Frozen expectations, safety constraints and source-only pressure reading."""

from copy import deepcopy
from hashlib import sha256
import json
import unittest

from ais.context import read_pressure
from ais.pilot import ROOT
from ais.search import CaseSearch


class ContextSearchTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load(collection="m006")
        self.directory = ROOT / "evaluation/search-m006"
        self.queries = json.loads((self.directory / "queries.json").read_text())["queries"]

    def run_query(self, text, **extra):
        return self.search.search(
            {"text": text, "cutoff": "2026-11-01", **extra}, method="context_v1"
        )

    def test_all_frozen_expectations_and_explicitly_forbidden_cases(self):
        for row in self.queries:
            payload = {
                k: v
                for k, v in row.items()
                if k in {"text", "cutoff", "before_period_end", "source_id"}
            }
            with self.subTest(query=row["id"]):
                result = self.search.search(payload, method="context_v1")
                ids = [c["id"] for c in result["results"]]
                self.assertTrue(set(row["expected_useful_cases"]) <= set(ids))
                self.assertFalse(set(row.get("forbidden_cases", [])) & set(ids))
                if row["expect_empty"]:
                    self.assertEqual(result["status"], "insufficient_evidence")
                    self.assertEqual(ids, [])

    def test_mixed_negation_keeps_only_positive_input_and_records_what_was_ignored(self):
        row = next(r for r in self.queries if r["id"] == "not-but")
        profile = read_pressure(row["text"])
        self.assertEqual(profile["words"], {"packaging": {"packaging"}})
        self.assertEqual(profile["directions"], {"packaging": {"up"}})
        result = self.run_query(row["text"])
        self.assertEqual(result["query_reading"]["ignored"][0]["text"], "not milk")
        self.assertTrue(all("dairy" not in c["matching_pressure_terms"] for c in result["results"]))

    def test_topic_lists_do_not_claim_query_prices_rose(self):
        row = next(r for r in self.queries if r["id"] == "topic-only")
        result = self.run_query(row["text"])
        self.assertIn("direction not specified", result["query_reading"]["summary"])
        for match in result["results"][0]["pressure_matches"]:
            self.assertEqual(match["query_direction"], "unspecified")
            self.assertEqual(match["report_direction"], "up")

    def test_empty_context_results_explain_the_reason_without_widening_dates(self):
        for query_id, phrase in [
            ("falling-milk", "opposite direction"),
            ("milk-sales", "Sales or demand"),
            ("airline", "outside"),
            ("changed", "which way"),
        ]:
            row = next(r for r in self.queries if r["id"] == query_id)
            result = self.run_query(row["text"], cutoff="2026-11-01")
            self.assertEqual(result["empty_reason"], "context_not_supported")
            self.assertIn(phrase, result["message"])
            self.assertEqual(result["query"]["cutoff"], "2026-11-01")
            self.assertGreater(result["eligible_count"], 0)

    def test_direction_matching_supports_declining_sources_instead_of_banning_declining_queries(
        self,
    ):
        # Synthetic change in memory only; no real case or source is rewritten.
        self.search.details["GIS-2007"]["pressure"]["value"] = "Dairy and grain input costs fell."
        result = self.run_query("Milk costs are falling.")
        self.assertEqual([c["id"] for c in result["results"]], ["GIS-2007"])
        self.assertEqual(result["results"][0]["pressure_matches"][0]["report_direction"], "down")
        self.assertEqual(self.run_query("Milk costs are rising.")["results"], [])

    def test_opposite_direction_vetoes_partial_overlap_and_unknown_sources_are_not_filled_in(self):
        row = next(r for r in self.queries if r["id"] == "split-costs")
        result = self.run_query(row["text"])
        self.assertEqual([c["id"] for c in result["results"]], ["KC-2011"])
        self.assertGreater(result["context_filtered"]["opposite_direction"], 0)
        self.search.details["GIS-2007"]["pressure"]["value"] = "Dairy input costs changed."
        self.assertEqual(self.run_query("Milk costs")["results"], [])

    def test_contractions_comparatives_and_separate_causal_clauses(self):
        # Grammar regression probes; not added to the frozen evaluation counts.
        for text in ["Milk costs can't rise.", "Milk costs won't rise.", "Milk is less expensive."]:
            self.assertEqual(self.run_query(text)["results"], [])
        result = self.run_query("Milk sales fell because milk costs rose.")
        self.assertEqual(result["results"][0]["id"], "GIS-2007")
        self.assertTrue(
            all(m["query_direction"] == "up" for m in result["results"][0]["pressure_matches"])
        )

    def test_responses_outcomes_figures_and_case_identity_cannot_change_reading_or_scores(self):
        before = self.run_query("Milk costs rose.")
        for case in self.search.cases:
            case.update(
                company="Airline",
                challenge="milk costs fell",
                response="milk sales",
                follow_up="milk costs fell",
            )
        for detail in self.search.details.values():
            detail.update(company="Airline", business_scope="banking")
            for field in ["response", "margin_or_profit", "other_drivers"]:
                detail[field]["value"] = "Airline fuel costs fell; milk sales rose."
        after = self.run_query("Milk costs rose.")

        def ranking(result):
            return [(c["id"], c["score"], c["pressure_matches"]) for c in result["results"]]

        self.assertEqual(ranking(before), ranking(after))

    def test_dates_self_and_continuations_use_the_same_pool_for_both_methods(self):
        duplicate = dict(deepcopy(self.search.by_id["GIS-2007"]), id="GIS-CONTINUING")
        detail = dict(deepcopy(self.search.details["GIS-2007"]), id=duplicate["id"])
        search = CaseSearch(
            self.search.cases + [duplicate], list(self.search.details.values()) + [detail]
        )
        payload = dict(text="milk flour electricity", cutoff="2026-11-01", source_id="GIS-2007")
        old, new = [search.search(payload, method=m) for m in ["related_v1", "context_v1"]]
        self.assertEqual(old["excluded"], new["excluded"])
        self.assertEqual(old["eligible_count"], new["eligible_count"])
        self.assertEqual(new["excluded"]["self"], 1)
        self.assertEqual(new["excluded"]["duplicate_or_continuation"], 1)
        search.details["GIS-2007"]["pressure"]["evidence"]["public_date"] = "2027-01-01"
        for method in ["related_v1", "context_v1"]:
            with self.assertRaisesRegex(ValueError, "not public"):
                search.search(payload, method=method)

    def test_frozen_case_and_evaluation_bytes_and_recorded_method_results(self):
        freeze = json.loads((self.directory / "freeze.json").read_text())
        for path, expected in freeze["sha256"].items():
            if path != "src/ais/search.py":
                self.assertEqual(sha256((ROOT / path).read_bytes()).hexdigest(), expected, path)
        report = json.loads((self.directory / "results.json").read_text())
        for check in report["checks"]:
            payload = {
                k: v
                for k, v in check.items()
                if k in {"text", "cutoff", "before_period_end", "source_id"}
            }
            self.assertEqual(
                check["old"]["eligible_ids_sha256"], check["new"]["eligible_ids_sha256"]
            )
            for name, method in [("old", "related_v1"), ("new", "context_v1")]:
                result = self.search.search(payload, method=method)
                self.assertEqual(
                    [dict(id=c["id"], score=c["score"]) for c in result["results"]],
                    check[name]["ranked"],
                )
                self.assertEqual(result["query_reading"], check[name]["query_reading"])


if __name__ == "__main__":
    unittest.main()
