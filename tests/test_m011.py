"""Evidence contracts and collection safeguards, not human relevance grades."""

from copy import deepcopy
from datetime import date, timedelta
from hashlib import sha256
import json
import unittest

from ais.collection import M011, load_collection, validate
from ais.context import read_pressure
from ais.pilot import ROOT, read_jsonl
from ais.search import CaseSearch
from ais.vocabulary import FAMILIES
from scripts.check_collection_m011 import evaluate


class GeographicCollectionTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load()
        self.records = {c["id"]: c for c in read_jsonl(M011)}

    def query(self, text, **extra):
        return self.search.search({"text": text, "cutoff": "2026-11-03", **extra})

    def test_existing_artifacts_and_method_modules_match_prefreeze_hashes(self):
        freeze = json.loads((ROOT / "evaluation/collection-m011/freeze.json").read_text())
        for path, expected in freeze["sha256"].items():
            if path not in freeze["mutable_code"]:
                self.assertEqual(sha256((ROOT / path).read_bytes()).hexdigest(), expected, path)
        self.assertEqual(self.search.catalog()["total"], 20)
        self.assertEqual(self.search.catalog()["companies"], 15)
        self.assertEqual(CaseSearch.load("m007").catalog()["total"], 17)

    def test_every_addition_retains_scope_source_dates_and_assistant_provenance(self):
        for c in self.records.values():
            self.assertFalse(c["human_reviewed"])
            self.assertEqual(c["review_status"], "assistant_source_checked; human_review_pending")
            self.assertTrue(c["geography"]["markets"])
            self.assertTrue(c["geography"]["scope_note"])
            self.assertTrue(c["business_scope"])
            self.assertTrue(c["comparison_limit"])
            self.assertTrue(c["unknowns"])
            for s in c["sources"]:
                self.assertFalse(s["document_retained"])
                self.assertRegex(s["inspected_document_sha256"], r"^[a-f0-9]{64}$")
                self.assertTrue(s["retention"]["terms_urls"])
                self.assertTrue(s["publication_evidence"]["locator"])
            result = self.query(c["pressure"]["value"])["results"]
            shown = next(r for r in result if r["id"] == c["id"])
            self.assertEqual(shown["geography"], c["geography"])
            self.assertEqual(shown["source"]["url"], c["sources"][0]["url"])

    def test_new_publication_cutoffs_reporting_end_and_self_exclusion(self):
        for cid, c in self.records.items():
            text = c["pressure"]["value"]
            previous = (date.fromisoformat(c["published"]) - timedelta(days=1)).isoformat()
            with self.subTest(case=cid):
                self.assertNotIn(
                    cid, [r["id"] for r in self.query(text, cutoff=previous)["results"]]
                )
                self.assertIn(
                    cid, [r["id"] for r in self.query(text, cutoff=c["published"])["results"]]
                )
                self.assertNotIn(
                    cid,
                    [
                        r["id"]
                        for r in self.query(text, before_period_end=c["period"]["end"])["results"]
                    ],
                )
                result = self.query(text, source_id=cid)
                self.assertNotIn(cid, [r["id"] for r in result["results"]])
                self.assertEqual(result["excluded"]["self"], 1)

    def test_new_continuation_is_not_counted_or_returned_twice(self):
        c = next(iter(self.records.values()))
        continuation = {**deepcopy(c), "id": "CONTINUING-REPORT"}
        with self.assertRaisesRegex(ValueError, "continuing situation"):
            validate(load_collection() + [continuation])
        flat = deepcopy(self.search.by_id[c["id"]])
        flat["id"] = continuation["id"]
        search = CaseSearch(
            self.search.cases + [flat], list(self.search.details.values()) + [continuation]
        )
        for source_id in (None, c["id"]):
            result = search.search(
                {"text": c["pressure"]["value"], "cutoff": "2026-11-03", "source_id": source_id}
            )
            self.assertEqual(result["excluded"]["duplicate_or_continuation"], 1)
            returned_group = {r["id"] for r in result["results"]} & {c["id"], continuation["id"]}
            self.assertEqual(len(returned_group), 1 if source_id is None else 0)

    def test_cost_estimate_forecast_and_margin_scopes_are_not_conflated(self):
        kao = self.records["KAO-CP-2022"]
        self.assertEqual((kao["metric"]["value"], kao["metric"]["unit"]), (-46, "JPY billion"))
        self.assertIn("not a reported operating loss", kao["margin_or_profit"]["value"])
        self.assertIn("2022-versus-2021", kao["metric"]["basis"])
        self.assertIn("Chemical", kao["metric"]["basis"])
        # The FY2023 energy forecast bar is not a FY2022 energy observation.
        self.assertNotIn(
            "energy", read_pressure(kao["pressure"]["value"], families=FAMILIES)["words"]
        )
        tiger = self.records["TIGER-2023-H1"]
        self.assertEqual(
            [(m["value"], m["unit"]) for m in tiger["figures"]],
            [(76, "ZAR million"), (12, "ZAR million"), (48, "ZAR million")],
        )
        self.assertIn("no reconciliation", tiger["unknowns"][0])
        self.assertTrue(all(m["value"] != 64 for m in tiger["figures"]))
        marico = self.records["MARICO-INDIA-2021-Q4"]
        self.assertEqual(marico["metric"]["value"], 17.6)
        self.assertIn("India", marico["metric"]["scope"])
        self.assertIn("market price", marico["figures"][0]["name"])
        self.assertIn("not Marico actual", marico["figures"][0]["basis"])

    def test_geography_actions_metrics_and_later_outcomes_cannot_rank(self):
        queries = ["oil packaging", "grain energy", "oil plastic", "milk costs fall"]

        def observations():
            return [
                [(c["id"], c["score"], c["coverage"]) for c in self.query(q)["results"]]
                for q in queries
            ]

        before = observations()
        for cid in self.records:
            c = self.search.details[cid]
            c["geography"] = {"label": "U.S. milk cocoa", "markets": ["U.S."]}
            c["business_scope"] = "Coffee milk cattle electricity"
            for f in ("response", "margin_or_profit", "other_drivers"):
                c[f]["value"] = "Coffee milk cocoa costs rose and caused recovery."
            c["metric"]["value"] = 999999
            self.search.by_id[cid]["company"] = "Coffee milk cocoa"
        self.assertEqual(observations(), before)

    def test_source_evidence_dates_still_gate_ranking_and_future_responses(self):
        cid = "MARICO-INDIA-2021-Q4"
        c = self.search.details[cid]
        c["pressure"]["evidence"]["public_date"] = "2027-01-01"
        self.assertNotIn(cid, [r["id"] for r in self.query("oil plastic")["results"]])
        c["pressure"]["evidence"]["public_date"] = c["published"]
        c["response"]["value"] = "LATER-PRIVATE-RESPONSE"
        c["response"]["evidence"]["public_date"] = "2027-01-01"
        result = self.query("oil plastic")
        shown = next(r for r in result["results"] if r["id"] == cid)
        self.assertFalse(shown["fields"]["response"]["available"])
        self.assertNotIn("LATER-PRIVATE-RESPONSE", str(result))

    def test_paired_observations_reproduce_including_misses_not_graded_away(self):
        result = evaluate()
        self.assertEqual(result["method"], "context_m010")
        self.assertEqual(result["collections"], {"old": 17, "expanded": 20})
        self.assertEqual(result["summary"]["historical_entries"], 186)
        self.assertEqual(result["summary"]["historical_target_retrieval_losses"], [])
        self.assertEqual(
            {r["id"] for r in result["summary"]["remaining_failures"]},
            {"copra-only", "paper-cardboard", "diesel-counterexample"},
        )
        for group in result["comparisons"]:
            for c in group["displayed_records"]:
                self.assertTrue(c["coverage"]["partial"])
                self.assertTrue(c["important_differences"])
                self.assertTrue(c["fields"]["response"]["evidence"])


if __name__ == "__main__":
    unittest.main()
