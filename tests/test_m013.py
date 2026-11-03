"""Final local prototype safeguards; AI development checks, not human validation."""

from copy import deepcopy
from hashlib import sha256
import json
import unittest

from ais.pilot import ROOT
from ais.search import CaseSearch
from ais import polymer_context as polymers
from scripts.evaluate_m013 import evaluate

M = "MARICO-INDIA-2021-Q4"
C = "COKE-2022"


class PrototypeTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load()

    def query(self, text, **options):
        return self.search.search({"text": text, "cutoff": "2026-11-03", **options})

    def all_cases(self, result):
        return result["results"] + result["additional_results"]

    def test_frozen_pairs_historical_queries_and_unchanged_case_files(self):
        result = evaluate()
        self.assertEqual(result["summary"]["queries"], 44)
        self.assertEqual(result["summary"]["historical_queries"], 275)
        self.assertEqual(result["summary"]["remaining_failures"], [])
        freeze = json.loads((ROOT / "evaluation/search-m013/freeze.json").read_text())
        for path, expected in freeze["sha256"].items():
            if path not in freeze["mutable_code"]:
                self.assertEqual(sha256((ROOT / path).read_bytes()).hexdigest(), expected, path)

    def test_exact_polymers_and_single_definition_mentions(self):
        for text, family, case in [
            ("HDPE", "hdpe", M),
            ("high density polyethylene", "hdpe", M),
            ("High-density polyethylene (HDPE) plastic", "hdpe", M),
            ("HDPE (high-density polyethylene)", "hdpe", M),
            ("PET", "pet", C),
            ("polyethylene terephthalate", "pet", C),
            ("PET resin (polyethylene terephthalate)", "pet", C),
        ]:
            q = text + " input costs rose."
            r = self.query(q)
            self.assertEqual([c["id"] for c in self.all_cases(r)], [case], q)
            c = r["results"][0]
            self.assertEqual(c["coverage"]["supported"], [family])
            self.assertEqual(c["coverage"]["names"][family], polymers.POLYMERS[family][0])
            self.assertEqual(c["pressure_matches"][0]["match_kind"], "named_input")
            self.assertEqual(polymers.profile(q, query=True)["concepts"], [family])

    def test_siblings_and_generic_plastic_do_not_establish_specific_polymer(self):
        for q in ["HDPE costs rise.", "PET costs rise."]:
            requested = polymers.profile(q, query=True)
            for source in [
                "LDPE resin costs rise.",
                "PVC costs rise.",
                "Plastic costs rise.",
                "Petrochemical packaging costs rise.",
                "Polypropylene costs rise.",
            ]:
                r = polymers.profile(source)
                self.assertEqual(polymers.compatible_matches(requested, r)[0], [], source)
                self.assertEqual(polymers.scores(requested, [r]), [0.0], source)
        for q, s in [
            ("HDPE costs rise.", "PET costs rise."),
            ("PET costs rise.", "HDPE costs rise."),
        ]:
            self.assertEqual(
                polymers.compatible_matches(polymers.profile(q, query=True), polymers.profile(s))[
                    0
                ],
                [],
            )
        for q in [
            "LDPE plastic costs rose.",
            "PVC resin costs rose.",
            "Polypropylene polymer costs rose.",
            "Pet food costs rose.",
            "PET scan costs rose.",
        ]:
            self.assertEqual(self.all_cases(self.query(q)), [], q)
        generic = {c["id"]: c for c in self.all_cases(self.query("Plastic costs rose."))}
        for case in [M, C]:
            self.assertEqual(generic[case]["coverage"]["supported"], ["resin"])
            self.assertTrue(
                any(
                    m["match_kind"] == "more_specific_source"
                    for m in generic[case]["pressure_matches"]
                )
            )

    def test_combined_materials_remain_partial_and_pvc_not_claimed(self):
        r = self.query("HDPE and PET costs rose.")
        self.assertEqual({c["id"] for c in self.all_cases(r)}, {M, C})
        for c in r["results"]:
            self.assertEqual(c["coverage"]["supported_count"], 1)
            self.assertEqual(c["coverage"]["identified_count"], 2)
            self.assertTrue(c["coverage"]["partial"])
        r = self.query("PVC and packaging costs rose.")
        for c in self.all_cases(r):
            self.assertIn("pvc", c["coverage"]["missing"])
            self.assertNotIn("pvc", c["coverage"]["supported"])

    def test_more_results_retain_order_uniqueness_partial_coverage_and_evidence(self):
        r = self.query("natural oil packaging grain energy")
        self.assertEqual(len(r["results"]), 5)
        all_results = self.all_cases(r)
        ids = [c["id"] for c in all_results]
        self.assertNotIn(M, ids[:5])
        self.assertIn(M, ids[5:])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), r["matched_count"])
        self.assertEqual(all_results, sorted(all_results, key=lambda c: (-c["score"], c["id"])))
        for c in all_results:
            self.assertTrue(c["coverage"]["partial"])
            self.assertLess(c["coverage"]["supported_count"], c["coverage"]["identified_count"])
            self.assertTrue(c["fields"]["pressure"]["evidence"]["locator"])
            self.assertTrue(c["source"]["url"].startswith("https://"))

    def test_additional_results_share_dates_self_and_continuation_checks(self):
        text = "natural oil packaging grain energy"
        r = self.query(text, cutoff="2021-04-29")
        self.assertNotIn(M, [c["id"] for c in self.all_cases(r)])
        r = self.query(text, source_id=M)
        self.assertNotIn(M, [c["id"] for c in self.all_cases(r)])
        r = self.query(text, before_period_end="2021-03-31")
        self.assertNotIn(M, [c["id"] for c in self.all_cases(r)])
        flat = {**deepcopy(self.search.by_id[M]), "id": "CONTINUING"}
        detail = {**deepcopy(self.search.details[M]), "id": "CONTINUING"}
        search = CaseSearch(
            self.search.cases + [flat], list(self.search.details.values()) + [detail]
        )
        r = search.search({"text": text, "cutoff": "2026-11-03", "source_id": M})
        self.assertFalse({M, "CONTINUING"} & {c["id"] for c in self.all_cases(r)})
        self.assertEqual(r["excluded"]["duplicate_or_continuation"], 1)
        self.search.details[M]["pressure"]["evidence"]["public_date"] = "2027-01-01"
        self.assertNotIn(M, [c["id"] for c in self.all_cases(self.query("HDPE"))])
        self.search.details[C]["response"]["value"] = "FUTURE-ACTION"
        self.search.details[C]["response"]["evidence"]["public_date"] = "2027-01-01"
        self.assertNotIn("FUTURE-ACTION", str(self.query("PET")))

    def test_rank_and_additional_results_ignore_all_non_pressure_fields(self):
        queries = ["HDPE", "PET", "natural oil packaging grain energy"]

        def observe():
            return [
                [
                    (c["id"], c["score"], c["coverage"], c["pressure_matches"])
                    for c in self.all_cases(self.query(q))
                ]
                for q in queries
            ]

        before = observe()
        for case in self.search.details.values():
            for field in ["response", "margin_or_profit", "other_drivers"]:
                case[field]["value"] = "HDPE PET prices rose; an action caused recovery."
            case["metric"]["value"] = 123456
            case["unknowns"] = ["HDPE PET"]
            case["business_scope"] = "HDPE PET"
            case["geography"] = {"label": "HDPE PET"}
            self.search.by_id[case["id"]]["company"] = "HDPE PET"
        self.assertEqual(observe(), before)


if __name__ == "__main__":
    unittest.main()
