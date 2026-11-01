"""Sentence bindings and abstentions, not an independent relevance benchmark."""

import unittest

from ais.language_context import query_profile
from ais.search import CaseSearch
from scripts.evaluate_m010 import evaluate


class SentenceTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load()

    def query(self, text, **extra):
        return self.search.search({"text": text, "cutoff": "2026-11-02", **extra})

    def test_frozen_pairs_and_old_method_reproduction(self):
        result = evaluate()
        self.assertEqual(result["summary"]["remaining_failures"], [])
        self.assertEqual(result["summary"]["historical_queries"], 130)
        self.assertEqual(result["summary"]["historical_rank_changes"], [])

    def test_opposite_denied_alternative_does_not_deny_positive_or_invent_it(self):
        for text in [
            "Milk costs rise not fall.",
            "Milk costs rise, not fall.",
            "Milk costs are not falling but rising.",
            "Milk costs are higher rather than lower.",
        ]:
            self.assertEqual(query_profile(text)["directions"], {"dairy": {"up"}}, text)
        for text in ["Milk costs did not fall.", "Milk costs are neither rising nor falling."]:
            self.assertEqual(self.query(text)["results"], [])

    def test_commas_bind_distinct_changes_but_keep_noun_lists_together(self):
        profile = query_profile("Milk and grain costs fell, energy and packaging costs rose.")
        self.assertEqual(
            profile["directions"],
            {"dairy": {"down"}, "grain": {"down"}, "energy": {"up"}, "packaging": {"up"}},
        )
        for text in [
            "Milk, wheat and electricity costs rise.",
            "Not only milk but also packaging costs are higher.",
        ]:
            self.assertTrue(all(v == {"up"} for v in query_profile(text)["directions"].values()))
        result = self.query("Milk costs fell, energy bills rose.")
        by_id = {c["id"]: c for c in result["results"]}
        self.assertEqual(by_id["DF-2015"]["coverage"]["missing"], ["energy"])
        self.assertEqual(by_id["KC-2011"]["coverage"]["missing"], ["dairy"])
        self.assertNotIn("GIS-2007", by_id)

    def test_ambiguous_directions_do_not_rank_an_invented_change(self):
        for text in [
            "Milk costs rise and fall.",
            "Milk costs fell last year but rise now.",
            "Milk costs rose in 2021 but fell in 2022.",
            "Milk costs fell, prices rose.",
            "Milk fell, energy rose.",
        ]:
            result = self.query(text)
            self.assertEqual(result["results"], [], text)
            self.assertEqual(result["clarification"]["kind"], "cost_direction", text)

    def test_reader_and_outside_supplier_customer_roles(self):
        for text in [
            "We are a food company, but our customers are airlines. Milk costs rise.",
            "An airline buys our dairy foods. Milk costs rise.",
            "Our company makes dairy foods. A bank funds our expansion. Milk costs rise.",
        ]:
            self.assertEqual(self.query(text)["results"][0]["id"], "GIS-2007", text)
        for text in [
            "We operate an airline for food customers. Fuel costs rise.",
            "We run a software company for airline customers. Milk input costs rise.",
            "Our supplier's costs rose but we run an airline. Fuel costs rise.",
        ]:
            self.assertEqual(self.query(text)["results"], [], text)
        for text in [
            "We are an airline supplier. Fuel costs rise.",
            "We use a logistics company to deliver food. Its fuel costs are rising.",
        ]:
            result = self.query(text)
            self.assertEqual(result["results"], [])
            self.assertEqual(result["clarification"]["kind"], "business_scope")

    def test_own_costs_purchase_prices_and_output_prices_are_distinct(self):
        for text in [
            "Our supplier's milk costs fell, but we pay more for milk.",
            "Our customers face higher energy costs, our milk costs rise.",
        ]:
            self.assertEqual(query_profile(text)["directions"], {"dairy": {"up"}})
        self.assertEqual(
            query_profile("Our supplier charges us lower milk prices.")["directions"],
            {"dairy": {"down"}},
        )
        for text in [
            "Our customers pay more for milk.",
            "We charge more for our milk products.",
            "Milk sales rise.",
        ]:
            self.assertEqual(self.query(text)["results"], [], text)

    def test_explicit_single_purchase_reference_and_unknown_input_do_not_conflict(self):
        result = self.query("We buy milk. It is getting cheaper.")
        self.assertEqual(result["results"][0]["id"], "DF-2015")
        result = self.query("Milk costs rise. Potato costs rise.")
        self.assertEqual(result["results"][0]["coverage"]["unrecognized"], ["potato"])
        self.assertTrue(result["partial_only"])
        # Post-freeze diagnostics: never carry a pronoun over an intervening
        # subject, or turn the reader's product identity into purchased inputs.
        for text in [
            "We buy milk. The supplier also sells cheese. It is getting cheaper.",
            "We are a milk cooperative. Feed and veterinary costs are rising.",
            "Milk costs climbed, electricity became cheaper.",
        ]:
            self.assertEqual(self.query(text)["results"], [], text)

    def test_pressure_only_scoring_even_with_ordinary_wording(self):
        text = "Milk costs rose, energy bills fell."

        def ranked():
            r = self.query(text)
            return [(c["id"], c["score"], c["coverage"]) for c in r["results"]]

        before = ranked()
        # Use a nonempty pressure query as well as the contradictory collection match.
        text = "Milk costs rise not fall."
        nonempty = ranked()
        for case in self.search.cases:
            detail = self.search.details[case["id"]]
            for field in ("response", "margin_or_profit", "other_drivers"):
                detail[field]["value"] = "Milk costs rose, energy costs fell. Caused recovery."
            case["company"] = "Milk energy airline"
            detail["business_scope"] = "Milk energy airline"
            detail["metric"]["value"] = 99999
        self.assertEqual(ranked(), nonempty)
        text = "Milk costs rose, energy bills fell."
        self.assertEqual(ranked(), before)


if __name__ == "__main__":
    unittest.main()
