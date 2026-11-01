"""Collection evidence contracts, real directional cases and ranking safeguards."""

from copy import deepcopy
from datetime import date, timedelta
from hashlib import sha256
import json
import unittest

from ais.collection import M007, load_collection, validate
from ais.pilot import ROOT, read_jsonl
from ais.search import CaseSearch
from ais.vocabulary import FAMILIES


class M007Tests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load()
        self.records = {c["id"]: c for c in read_jsonl(M007)}

    def query(self, text, **extra):
        return self.search.search({"text": text, "cutoff": "2026-11-01", **extra})

    def test_frozen_records_and_expectations_remain_identical(self):
        manifest = json.loads((ROOT / "evaluation/collection-m007/freeze.json").read_text())
        for path, expected in manifest["sha256"].items():
            if path not in manifest["mutable_code"]:
                self.assertEqual(sha256((ROOT / path).read_bytes()).hexdigest(), expected, path)

    def test_collection_has_distinct_groups_and_complete_source_contracts(self):
        self.assertEqual(len(load_collection()), 7)
        self.assertEqual(self.search.catalog()["total"], 17)
        self.assertEqual(self.search.catalog()["companies"], 12)
        for c in self.records.values():
            self.assertFalse(c["human_reviewed"])
            self.assertTrue(c["comparison_limit"])
            for s in c["sources"]:
                self.assertFalse(s["document_retained"])
                self.assertIn("sec.gov/Archives", s["url"])
                self.assertTrue(s["publication_evidence"]["url"])
        duplicate = deepcopy(load_collection())
        duplicate[-1]["duplicate_group"] = duplicate[0]["duplicate_group"]
        with self.assertRaisesRegex(ValueError, "continuing situation"):
            validate(duplicate)

    def test_new_materials_and_cost_decline_are_searchable_with_source_attribution(self):
        checks = json.loads((ROOT / "evaluation/collection-m007/checks.json").read_text())
        for family, aliases in checks["planned_vocabulary"].items():
            self.assertEqual(sorted(FAMILIES[family][1].split()), sorted(aliases))
        for query, expected in [
            ("Coffee input prices rose.", "SJM-COFFEE-2011"),
            ("Milk costs are falling.", "DF-2015"),
            ("Livestock input costs rose.", "TSN-BEEF-2024-Q1"),
            ("Aluminium costs rose.", "COKE-2022"),
        ]:
            result = self.query(query)
            with self.subTest(query=query):
                self.assertEqual(result["results"][0]["id"], expected)
                case = result["results"][0]
                self.assertTrue(case["pressure_matches"])
                self.assertEqual(
                    case["source"]["url"], self.records[expected]["pressure"]["evidence"]["url"]
                )
        self.assertEqual([c["id"] for c in self.query("Milk costs rise.")["results"]], ["GIS-2007"])
        self.assertEqual(self.query("Coffee costs fall.")["status"], "insufficient_evidence")
        for q in ("Cattle sales rose.", "Aluminum costs in steel smelting rose."):
            self.assertEqual(self.query(q)["results"], [])

    def test_publication_boundaries_and_self_exclusion_for_every_new_case(self):
        for case_id, c in self.records.items():
            text = c["pressure"]["value"]
            previous = (date.fromisoformat(c["published"]) - timedelta(days=1)).isoformat()
            with self.subTest(case=case_id):
                self.assertNotIn(
                    case_id, [r["id"] for r in self.query(text, cutoff=previous)["results"]]
                )
                self.assertIn(
                    case_id, [r["id"] for r in self.query(text, cutoff=c["published"])["results"]]
                )
                result = self.query(text, source_id=case_id)
                self.assertNotIn(case_id, [r["id"] for r in result["results"]])
                self.assertEqual(result["excluded"]["self"], 1)

    def test_new_case_continuation_and_reporting_end_exclusions(self):
        source = "TSN-BEEF-2024-Q1"
        self.search.by_id["SJM-COFFEE-2011"]["duplicate_group"] = self.records[source][
            "duplicate_group"
        ]
        result = self.query("coffee cattle", source_id=source)
        self.assertEqual(result["results"], [])
        self.assertEqual(result["excluded"]["duplicate_or_continuation"], 1)
        result = self.query("Cattle costs rose.", before_period_end="2023-12-30")
        self.assertEqual(result["results"], [])

    def test_metric_scopes_and_attribution_survive_adapter(self):
        dairy = self.query("milk costs fall")["results"][0]
        benchmark = dairy["figures"][0]
        self.assertEqual((benchmark["value"], benchmark["unit"]), (16.34, "USD per 100 lb"))
        self.assertIn("benchmark", benchmark["basis"].lower())
        self.assertIn("not", benchmark["basis"].lower())
        beef = self.query("cattle costs rise")["results"][0]
        self.assertEqual((beef["metric"]["value"], beef["metric"]["unit"]), (-206, "USD million"))
        self.assertIn("write-down", beef["fields"]["other_drivers"]["value"])
        for c in self.records.values():
            self.assertIn("issuer", c["response"]["kind"])
            self.assertTrue(c["metric"]["scope"])
            self.assertTrue(c["metric"]["comparison"])

    def test_responses_metrics_outcomes_and_identity_cannot_change_ranks(self):
        queries = ["coffee", "milk", "cattle", "aluminum", "packaging"]

        def rankings(text):
            result = self.query(text)
            return [(c["id"], c["score"], c["pressure_matches"]) for c in result["results"]]

        before = [rankings(q) for q in queries]
        for case_id in self.records:
            detail = self.search.details[case_id]
            for field in ("response", "margin_or_profit", "other_drivers"):
                detail[field]["value"] = (
                    "Milk coffee cattle aluminum costs rose; action caused profit."
                )
            detail["metric"]["value"] = 99999
            detail["business_scope"] = "Coffee milk aluminum cattle"
            self.search.by_id[case_id]["company"] = "Coffee Milk Aluminum Cattle"
        self.assertEqual(before, [rankings(q) for q in queries])


if __name__ == "__main__":
    unittest.main()
