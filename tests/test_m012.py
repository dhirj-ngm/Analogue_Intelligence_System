"""Material evidence, direction and ranking invariants; development checks only."""

from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from ais import material_context as materials
from ais.pilot import ROOT, bm25
from ais.historical import frozen_bytes
from ais.search import CaseSearch
from scripts.evaluate_m012 import evaluate


class MaterialTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load("m011")

    def query(self, text, **extra):
        return self.search.search(
            {"text": text, "cutoff": "2026-11-03", **extra}, method="context_m012"
        )

    def test_frozen_pairs_and_all_ten_m011_targets_are_reported(self):
        result = evaluate()
        self.assertEqual(result["summary"]["remaining_failures"], [])
        self.assertEqual(result["summary"]["historical_queries"], 211)
        self.assertEqual(len(result["summary"]["ten_m011_targets"]), 10)
        ambiguous = next(
            r for r in result["summary"]["ten_m011_targets"] if r["id"] == "food-scope"
        )
        self.assertIsNone(ambiguous["m012_rank"])
        self.assertEqual(ambiguous["m012_clarification"]["kind"], "material_input")
        freeze = json.loads((ROOT / "evaluation/search-m012/freeze.json").read_text())
        for path, expected in freeze["sha256"].items():
            if path not in freeze["mutable_code"]:
                frozen_bytes(path, expected)

    def test_fuel_result_is_related_cost_evidence_not_named_diesel(self):
        for q in ["Diesel fuel costs rose.", "Fuel input prices rose.", "Petrol costs rise."]:
            result = self.query(q)
            self.assertEqual([r["id"] for r in result["results"]], ["NES-WATERS-2011-H1"])
            c = result["results"][0]
            self.assertEqual(c["coverage"]["supported_count"], 0)
            self.assertEqual(c["coverage"]["related_count"], 1)
            self.assertTrue(c["coverage"]["partial"])
            self.assertFalse(c["pressure_matches"][0]["named_input_established"])
            self.assertIn("does not name", c["pressure_matches"][0]["explanation"])
        q = materials.profile("Diesel costs rise.", query=True)
        for source in [
            "Petrol costs rise.",
            "Petrochemical packaging costs rise.",
            "Edible oil costs rise.",
            "Transportation costs rise.",
        ]:
            p = materials.profile(source)
            self.assertEqual(materials.compatible_matches(q, p)[0], [], source)
            self.assertEqual(materials.scores(q, [p]), [0.0], source)

    def test_named_material_specificity_and_source_uses_are_not_invented(self):
        for q, expected in [
            ("Copra prices rose.", "MARICO-INDIA-2021-Q4"),
            ("Dried coconut kernel costs rose.", "MARICO-INDIA-2021-Q4"),
            ("Paper costs rise.", "KAO-CP-2022"),
            ("Cardboard costs rise.", "KAO-CP-2022"),
            ("Petrochemical packaging costs rise.", "KAO-CP-2022"),
        ]:
            c = self.query(q)["results"][0]
            self.assertEqual(c["id"], expected)
            self.assertEqual(c["pressure_matches"][0]["match_kind"], "named_input")
            if q.startswith("Dried"):
                self.assertFalse({"dried", "coconut", "kernel"} & set(c["unmatched_terms"]))
        for q in [
            "Palm oil costs rose.",
            "Coconut oil input costs rose.",
            "Crude oil input costs rose.",
        ]:
            self.assertEqual(self.query(q)["results"], [], q)
        self.assertEqual(
            [c["id"] for c in self.query("Cooking oil costs rose.")["results"]],
            ["MARICO-INDIA-2021-Q4"],
        )
        self.assertEqual([c["id"] for c in self.query("Pulp costs rose.")["results"]], ["KC-2011"])
        self.assertEqual(
            self.query("Pulp costs rose.")["results"][0]["coverage"]["supported_count"], 0
        )
        q = materials.profile("Edible oil costs rose.", query=True)
        self.assertEqual(
            materials.compatible_matches(
                q, materials.profile("Natural oils cost more; input prices rise.")
            )[0],
            [],
        )

    def test_definition_is_one_mention_and_shared_modifier_keeps_material_types(self):
        p = materials.profile("Copra (dried coconut kernel) costs rose.")
        self.assertEqual(p["concepts"], ["copra"])
        p = materials.profile(
            "Petrochemical raw-material and packaging costs rose; paper and cardboard costs rose."
        )
        self.assertEqual(
            set(p["words"]), {"petrochemical_raw", "petrochemical_packaging", "paper", "cardboard"}
        )
        self.assertNotIn("fuel", materials.index_concepts(p))
        self.assertNotIn("natural_oil", materials.index_concepts(p))

    def test_ambiguity_and_denied_or_opposed_material_directions_stay_cautious(self):
        r = self.query("Oil costs rise.")
        self.assertEqual(r["results"], [])
        self.assertEqual(r["clarification"]["kind"], "material_input")
        r = self.query("Oil and paper costs rise.")
        self.assertEqual([c["id"] for c in r["results"]], ["KAO-CP-2022"])
        self.assertTrue(r["results"][0]["coverage"]["partial"])
        for q in [
            "No oil or paper costs rose.",
            "No diesel or copra costs rose.",
            "Copra costs might rise.",
            "Paper costs fell.",
        ]:
            self.assertEqual(self.query(q)["results"], [], q)
        self.assertEqual(
            [c["id"] for c in self.query("Copra costs fell, paper costs rose.")["results"]],
            ["KAO-CP-2022"],
        )
        self.assertEqual(
            [c["id"] for c in self.query("Copra costs are rising not falling.")["results"]],
            ["MARICO-INDIA-2021-Q4"],
        )

    def test_newly_recognized_products_are_not_purchase_pressure(self):
        # Post-freeze adversarial probes; not added to frozen evaluation counts.
        for q in ["We sell copra at higher prices.", "We make paper.", "We sell cooking oil."]:
            self.assertEqual(self.query(q)["results"], [], q)
        r = self.query("We make cooking oil. Diesel costs rose.")
        self.assertEqual([c["id"] for c in r["results"]], ["NES-WATERS-2011-H1"])
        self.assertIn("cooking oil", r["query_reading"]["ignored"][0]["text"])
        self.assertEqual(self.query("We make software and paper. Fuel costs rose.")["results"], [])
        self.assertEqual(
            self.query("We buy copra. Its costs rose.")["results"][0]["id"], "MARICO-INDIA-2021-Q4"
        )

    def test_product_vs_packaging_use_does_not_erase_explicit_inputs(self):
        r = self.query(
            "We bottle drinks in plastic and aluminum containers. Packaging and road freight costs are higher together."
        )
        self.assertEqual(r["results"][0]["id"], "COKE-2022")
        r = self.query("We make cooking oil in India. Diesel costs rose.")
        self.assertEqual([c["id"] for c in r["results"]], ["NES-WATERS-2011-H1"])

    def test_compound_identity_and_typographic_variants_keep_material_meaning(self):
        for q in [
            "We sell copra, but we buy diesel.",
            "We make cooking oil, our diesel costs rose.",
        ]:
            self.assertEqual([c["id"] for c in self.query(q)["results"]], ["NES-WATERS-2011-H1"])
        for q, cid in [
            ("Dried-coconut kernels cost more; input prices rise.", "MARICO-INDIA-2021-Q4"),
            ("Cooking-oil costs rise.", "MARICO-INDIA-2021-Q4"),
            ("Rice-bran-oil costs rise.", "MARICO-INDIA-2021-Q4"),
        ]:
            self.assertEqual(self.query(q)["results"][0]["id"], cid)

    def test_scoring_uses_mentions_not_unused_link_count_and_prioritizes_names(self):
        q = materials.profile("Freight costs rise.", query=True)
        reports = [
            materials.profile("Oil-related distribution costs rise."),
            materials.profile("Transportation costs rise."),
        ]
        before = materials.scores(q, reports)
        with patch.dict(
            materials.BROADER_LINKS,
            {"oil_distribution": materials.BROADER_LINKS["oil_distribution"] | {"unused_type"}},
        ):
            self.assertEqual(materials.scores(q, reports), before)
        q = materials.profile("Natural oil costs rise.", query=True)
        exact, related = materials.scores(
            q,
            [
                materials.profile("Natural oil costs rise."),
                materials.profile("Rice bran oil costs rise."),
            ],
        )
        self.assertGreater(exact, related)
        # With no material links, this is the existing BM25 formula.
        q = materials.profile("Wheat energy costs rise.", query=True)
        reports = [materials.profile("Wheat costs rise."), materials.profile("Energy costs rise.")]
        self.assertEqual(
            materials.scores(q, reports),
            bm25(" ".join(q["concepts"]), [" ".join(r["concepts"]) for r in reports]),
        )

    def test_responses_identity_metrics_and_geography_cannot_create_material_evidence(self):
        queries = ["diesel", "copra", "paper", "petrochemical packaging", "rice bran oil"]

        def observe():
            return [
                [
                    (r["id"], r["score"], r["pressure_matches"], r["coverage"])
                    for r in self.query(q)["results"]
                ]
                for q in queries
            ]

        before = observe()
        for cid, c in self.search.details.items():
            for f in ("response", "margin_or_profit", "other_drivers"):
                c[f]["value"] = "Diesel, copra and paper costs rose; actions caused recovery."
            c["metric"]["value"] = 123456
            c["unknowns"] = ["Diesel copra paper"]
            c["business_scope"] = "Diesel copra paper"
            c["geography"] = {"label": "Diesel copra paper"}
            self.search.by_id[cid]["company"] = "Diesel copra paper"
        self.assertEqual(observe(), before)

    def test_evidence_dates_self_and_continuations_remain_shared(self):
        cid = "MARICO-INDIA-2021-Q4"
        self.assertEqual(self.query("copra", cutoff="2021-04-29")["results"], [])
        self.assertEqual(self.query("copra", cutoff="2021-04-30")["results"][0]["id"], cid)
        self.assertEqual(self.query("copra", source_id=cid)["results"], [])
        self.assertEqual(self.query("copra", before_period_end="2021-03-31")["results"], [])
        flat = {**deepcopy(self.search.by_id[cid]), "id": "CONTINUING"}
        detail = {**deepcopy(self.search.details[cid]), "id": "CONTINUING"}
        search = CaseSearch(
            self.search.cases + [flat], list(self.search.details.values()) + [detail]
        )
        r = search.search({"text": "copra", "cutoff": "2026-11-03", "source_id": cid})
        self.assertEqual(r["results"], [])
        self.assertEqual(r["excluded"]["duplicate_or_continuation"], 1)
        c = self.search.details[cid]
        c["pressure"]["evidence"]["public_date"] = "2027-01-01"
        self.assertEqual(self.query("copra")["results"], [])
        c["pressure"]["evidence"]["public_date"] = c["published"]
        c["response"]["value"] = "FUTURE-ACTION"
        c["response"]["evidence"]["public_date"] = "2027-01-01"
        self.assertNotIn("FUTURE-ACTION", str(self.query("copra")))


if __name__ == "__main__":
    unittest.main()
