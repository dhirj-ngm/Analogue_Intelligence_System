"""Reader roles, pressure coverage, clarification and existing evidence guards."""

import unittest

from ais.reader_context import query_profile
from ais.search import CaseSearch
from scripts.evaluate_m009 import evaluate


class ReaderContextTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load("m007")

    def run_query(self, text, **extra):
        return self.search.search({"text": text, "cutoff": "2026-11-02", **extra})

    def test_frozen_paired_expectations_and_historical_candidate_pools(self):
        result = evaluate()
        self.assertEqual(result["summary"]["remaining_failures"], [])
        self.assertEqual(result["summary"]["historical_queries"], 93)

    def test_partial_coverage_is_per_case_not_the_union_of_two_results(self):
        r = self.run_query("Milk costs fell while energy bills rose.")
        self.assertTrue(r["partial_only"])
        records = {c["id"]: c for c in r["results"]}
        self.assertEqual(records["DF-2015"]["coverage"]["supported"], ["dairy"])
        self.assertEqual(records["DF-2015"]["coverage"]["missing"], ["energy"])
        self.assertEqual(records["KC-2011"]["coverage"]["missing"], ["dairy"])
        self.assertNotIn("GIS-2007", records)

    def test_supplier_own_costs_and_outside_reader_are_not_turned_into_fmcg_pressure(self):
        r = self.run_query(
            "We make dairy foods. Our airline supplier's fuel costs are rising. Milk costs fall."
        )
        self.assertEqual([c["id"] for c in r["results"]], ["DF-2015"])
        self.assertTrue(r["query_reading"]["ignored"])
        for q in [
            "We operate an airline. Our food supplier faces higher milk costs.",
            "We are a logistics supplier. Fuel costs rise.",
        ]:
            self.assertEqual(self.run_query(q)["results"], [])

    def test_additional_role_and_negated_industry_diagnostics(self):
        # Additional probes, not added retroactively to frozen evaluation counts.
        for q in [
            "We are not an airline. Milk costs fall.",
            "An airline supplies our food factory with packaging. Packaging costs rise.",
            "An airline counts our food plant as a customer. Packaging costs rise.",
            "We bottle water. Our supplier is a logistics company. Freight costs rise.",
        ]:
            self.assertTrue(self.run_query(q)["results"])
        self.assertIsNone(query_profile("We are not an airline. Milk costs fall.")["blocked"])
        self.assertTrue(
            self.run_query(
                "We bottle water. Our logistics supplier charges us higher freight rates."
            )["results"]
        )

        self.assertTrue(
            self.run_query("We bottle water. Our logistics supplier is raising delivery prices.")[
                "results"
            ]
        )

    def test_clarification_does_not_infer_cattle_or_use_beef_output_fields(self):
        r = self.run_query("Our beef plant buys live animals. Beef raw-material costs rise.")
        self.assertEqual(r["results"], [])
        self.assertEqual(r["clarification"]["kind"], "live_animal_input")
        self.assertIn("Beef selling prices", r["clarification"]["message"])
        for q in ["Our beef sales rise.", "Beef selling prices rise.", "Cattle sales rise."]:
            r = self.run_query(q)
            self.assertIsNone(r["clarification"])
            self.assertEqual(r["results"], [])
        r = self.run_query("Cattle input costs rise.")
        self.assertEqual(r["results"][0]["id"], "TSN-BEEF-2024-Q1")

    def test_unknown_names_and_instructional_context_do_not_claim_full_coverage(self):
        for q in ["Milk and potato costs rise.", "Potato and milk costs rise."]:
            c = self.run_query(q)["results"][0]["coverage"]
            self.assertEqual(c["unrecognized"], ["potato"])
            self.assertTrue(c["partial"])
        r = self.run_query(
            "Our milk costs fell. I want a dairy example that separates input prices from price cuts and profit changes."
        )
        self.assertFalse(r["results"][0]["coverage"]["partial"])

    def test_responses_later_outcomes_and_business_identity_cannot_change_rank_or_coverage(self):
        query = "We bottle water. Our supplier serves airlines. Freight and fuel costs rise."

        def observed():
            r = self.run_query(query)
            return [(c["id"], c["score"], c["coverage"]) for c in r["results"]]

        before = observed()
        for c in self.search.cases:
            d = self.search.details[c["id"]]
            for k in ("response", "margin_or_profit", "other_drivers"):
                d[k]["value"] = "Airline fuel, cattle, milk and energy costs caused recovery."
            d["metric"]["value"] = 98765
            d["business_scope"] = "Airline company"
            c["company"] = "Airline company"
        self.assertEqual(observed(), before)

    def test_date_self_continuation_and_future_response_guards(self):
        text = "We bottle water. Our supplier serves airlines. Freight and fuel costs rise."
        self.assertEqual(self.run_query(text, cutoff="2011-08-09")["results"], [])
        self.assertEqual(
            self.run_query(text, cutoff="2011-08-10")["results"][0]["id"], "NES-WATERS-2011-H1"
        )
        result = self.run_query(text, source_id="NES-WATERS-2011-H1")
        self.assertEqual(result["excluded"]["self"], 1)
        self.assertEqual(result["results"], [])
        original_group = self.search.by_id["CL-2008"]["duplicate_group"]
        self.search.by_id["CL-2008"]["duplicate_group"] = self.search.by_id["NES-WATERS-2011-H1"][
            "duplicate_group"
        ]
        self.assertEqual(
            self.run_query(text, source_id="NES-WATERS-2011-H1")["excluded"][
                "duplicate_or_continuation"
            ],
            1,
        )
        self.search.by_id["CL-2008"]["duplicate_group"] = original_group
        self.search.details["NES-WATERS-2011-H1"]["response"]["evidence"]["public_date"] = (
            "2027-01-01"
        )
        self.assertFalse(self.run_query(text)["results"][0]["fields"]["response"]["available"])
