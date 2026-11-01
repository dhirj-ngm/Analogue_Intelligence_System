"""Checks for evidence lineage and the reader's expanded corpus; no network."""

from copy import deepcopy
from datetime import date, timedelta
import json
import unittest

from ais.collection import load_collection, search_records, validate
from ais.pilot import ROOT, ranking_text
from ais.search import CaseSearch


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.records = load_collection()
        self.search = CaseSearch.load()

    def query(self, text, cutoff="2026-11-01", **extra):
        return self.search.search(dict(text=text, cutoff=cutoff, **extra))

    def test_batch_adds_distinct_companies_periods_and_costs_without_replacing_pilot(self):
        self.assertEqual(self.search.catalog()["total"], 13)
        self.assertEqual(self.search.catalog()["companies"], 8)
        self.assertEqual(len(self.records), 3)
        for case, query in zip(self.records, ["grains dairy energy", "oil distribution", "cocoa"]):
            self.assertEqual(self.query(query)["results"][0]["id"], case["id"])
            self.assertFalse(case["human_reviewed"])
            self.assertTrue(case["business_scope"])

    def test_all_new_cases_use_actual_publication_date_inclusively(self):
        for case in self.records:
            with self.subTest(case=case["id"]):
                text = case["pressure"]["value"]
                before = (date.fromisoformat(case["published"]) - timedelta(days=1)).isoformat()
                self.assertNotIn(case["id"], [c["id"] for c in self.query(text, before)["results"]])
                self.assertIn(
                    case["id"], [c["id"] for c in self.query(text, case["published"])["results"]]
                )
                result = self.query(text, case["published"], source_id=case["id"])
                self.assertNotIn(case["id"], [c["id"] for c in result["results"]])
                self.assertEqual(result["excluded"]["self"], 1)
                result = self.query(text, before_period_end=case["period"]["end"])
                self.assertNotIn(case["id"], [c["id"] for c in result["results"]])

    def test_continuing_reports_collapse_and_are_excluded_with_starting_case(self):
        original = self.search.by_id["HSY-2025-Q1"]
        duplicate = dict(deepcopy(original), id="HSY-CONTINUING")
        detail = dict(deepcopy(self.search.details[original["id"]]), id=duplicate["id"])
        search = CaseSearch(
            self.search.cases + [duplicate], list(self.search.details.values()) + [detail]
        )
        for source_id in (None, original["id"]):
            result = search.search(dict(text="cocoa", cutoff="2026-11-01", source_id=source_id))
            self.assertEqual(result["excluded"]["duplicate_or_continuation"], 1)
            self.assertNotIn(duplicate["id"], [c["id"] for c in result["results"]])
        duplicate_record = dict(deepcopy(self.records[-1]), id="HSY-CONTINUING")
        with self.assertRaisesRegex(ValueError, "continuing situation counted twice"):
            validate(self.records + [duplicate_record])

    def test_only_pressure_enters_new_case_rankings(self):
        flat, _ = search_records(self.records)
        for record, case in zip(self.records, flat):
            self.assertEqual(ranking_text(case), record["pressure"]["value"])
        before = [(c["id"], c["score"]) for c in self.query("cocoa energy")["results"]]
        for case in self.search.details.values():
            case["response"]["value"] = "cocoa energy"
            case["figures"] = []
            case["conflicts"] = []
            case["unknowns"] = ["cocoa energy"]
        after = [(c["id"], c["score"]) for c in self.query("cocoa energy")["results"]]
        self.assertEqual(before, after)
        self.assertEqual(self.query("lighter bottles")["status"], "insufficient_evidence")

    def test_units_basis_scope_and_source_conflict_survive_presentation(self):
        result = self.query("cocoa")["results"][0]
        self.assertEqual(result["metric"]["value"], 33.7)
        self.assertEqual(result["metric"]["scope"], "Global consolidated business")
        figures = result["figures"]
        self.assertEqual(
            [(m["value"], m["unit"]) for m in figures],
            [(41.2, "percent"), (1780, "basis points"), (1790, "basis points")],
        )
        self.assertIn("Non-GAAP", figures[0]["basis"])
        conflict = result["conflicts"][0]
        self.assertEqual(len(conflict["sources"]), 2)
        self.assertIn("unknown", conflict["value"])
        self.assertIn("not chosen or corrected", conflict["value"])
        for evidence in [m["evidence"] for m in figures] + conflict["sources"]:
            self.assertTrue(evidence["locator"])
            self.assertEqual(evidence["public_date"], "2025-05-01")

    def test_future_or_unknown_extra_evidence_is_withheld(self):
        detail = self.search.details["HSY-2025-Q1"]
        detail["figures"][0]["basis"] = "FUTURE_SECRET"
        detail["figures"][0]["evidence"]["public_date"] = "2027-01-01"
        detail["figures"][1]["evidence"]["public_date"] = None
        detail["conflicts"][0]["value"] = "FUTURE_SECRET"
        detail["conflicts"][0]["sources"][0]["public_date"] = "2027-01-01"
        result = self.query("cocoa")["results"][0]
        self.assertEqual(len(result["figures"]), 1)
        self.assertEqual(result["conflicts"], [])
        self.assertNotIn("FUTURE_SECRET", json.dumps(result))

    def test_primary_figure_requires_its_own_public_evidence(self):
        self.search.details["HSY-2025-Q1"]["metric"]["evidence"]["public_date"] = "2027-01-01"
        result = self.query("cocoa")
        self.assertEqual(result["results"], [])
        self.assertEqual(result["excluded"]["challenge_evidence_after_cutoff"], 1)

    def test_source_date_scope_and_metric_errors_are_rejected(self):
        for change, message in [
            (lambda c: c["metric"].update(unit="dollars?"), "unsupported metric unit"),
            (
                lambda c: c["pressure"]["evidence"].update(public_date="2027-01-01"),
                "publication mismatch",
            ),
            (lambda c: c["response"]["evidence"].update(period_end="2000-01-01"), "scope mismatch"),
            (lambda c: c["metric"].update(basis=""), "metric basis missing"),
            (
                lambda c: c["sources"][0].update(document_retained=True),
                "documents must remain external",
            ),
        ]:
            with self.subTest(message=message):
                records = deepcopy(self.records)
                change(records[0])
                with self.assertRaisesRegex(ValueError, message):
                    validate(records)

    def test_recorded_relevance_observations_are_reproducible_including_misses(self):
        inputs = json.loads((ROOT / "evaluation/collection/queries.json").read_text())
        observations = json.loads((ROOT / "evaluation/collection/results.json").read_text())
        for query, observation in zip(inputs["queries"], observations["checks"], strict=True):
            result = self.search.search(
                dict(text=query["text"], cutoff=inputs["cutoff"]), method="literal_v1"
            )
            self.assertEqual([c["id"] for c in result["results"]], observation["ranked_ids"])
        self.assertTrue(any(c["finding"] == "useful case missed" for c in observations["checks"]))


if __name__ == "__main__":
    unittest.main()
