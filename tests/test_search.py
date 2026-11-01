"""Deterministic reader safeguards; no model or external source access."""

from copy import deepcopy
import unittest

from ais.search import CaseSearch, SearchInputError


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load()
        self.query = {
            "text": "Packaging and logistics costs are increasing, putting pressure on margin.",
            "cutoff": "2023-01-27",
            "before_period_end": "2023-01-27",
        }

    def test_ranked_cases_have_pressure_evidence_scope_response_and_unknowns(self):
        result = self.search.search(self.query)
        self.assertEqual(result["status"], "candidates")
        self.assertTrue(result["results"])
        for case in result["results"]:
            self.assertTrue(case["matching_pressure_terms"])
            self.assertTrue(case["fields"]["pressure"]["evidence"]["locator"])
            self.assertTrue(case["fields"]["response"]["value"])
            self.assertTrue(case["metric"]["basis"])
            self.assertTrue(case["important_differences"])
            self.assertTrue(case["unknowns"])

    def test_publication_cutoff_is_inclusive_and_uses_publication_not_period(self):
        for cutoff, expected in [("2023-01-26", False), ("2023-01-27", True)]:
            result = self.search.search(dict(self.query, cutoff=cutoff, before_period_end=cutoff))
            self.assertEqual("CL-2022" in {c["id"] for c in result["results"]}, expected)
        self.assertNotIn("UL-2022", {c["id"] for c in result["results"]})

    def test_self_continuation_and_non_earlier_observations_are_excluded(self):
        duplicate = deepcopy(self.search.by_id["CL-2022"])
        duplicate["id"] = "CL-2022-UPDATE"
        detail = deepcopy(self.search.details["CL-2022"])
        detail["id"] = duplicate["id"]
        self.search = CaseSearch(
            self.search.cases + [duplicate], list(self.search.details.values()) + [detail]
        )
        result = self.search.search(dict(self.query, source_id="CL-2022"))
        self.assertNotIn("CL-2022", {c["id"] for c in result["results"]})
        self.assertNotIn(duplicate["id"], {c["id"] for c in result["results"]})
        self.assertEqual(result["query"]["before_period_end"], "2022-12-31")
        self.assertEqual(result["excluded"]["self"], 1)
        self.assertEqual(result["excluded"]["duplicate_or_continuation"], 1)

    def test_duplicate_candidates_are_collapsed_without_a_source_case(self):
        original = self.search.by_id["CL-2008"]
        duplicate = dict(deepcopy(original), id="CL-2008-UPDATE")
        detail = dict(deepcopy(self.search.details["CL-2008"]), id=duplicate["id"])
        search = CaseSearch(
            self.search.cases + [duplicate], list(self.search.details.values()) + [detail]
        )
        result = search.search(self.query)
        self.assertEqual(result["excluded"]["duplicate_or_continuation"], 1)
        self.assertNotIn(duplicate["id"], {c["id"] for c in result["results"]})

    def test_later_or_unknown_challenge_evidence_cannot_rank(self):
        self.search.details["CL-2022"]["pressure"]["evidence"]["public_date"] = "2023-02-01"
        self.search.details["CL-2008"]["other_drivers"]["evidence"]["public_date"] = None
        result = self.search.search(self.query)
        ids = {c["id"] for c in result["results"]}
        self.assertNotIn("CL-2022", ids)
        self.assertNotIn("CL-2008", ids)
        self.assertEqual(result["excluded"]["challenge_evidence_after_cutoff"], 1)
        self.assertEqual(result["excluded"]["unknown_challenge_date"], 1)

    def test_selected_query_case_must_also_have_public_evidence(self):
        with self.assertRaisesRegex(ValueError, "not public"):
            self.search.search(
                dict(
                    self.query,
                    cutoff="2022-12-31",
                    before_period_end="2022-12-31",
                    source_id="CL-2022",
                )
            )

    def test_response_outcome_rationale_and_display_limits_do_not_change_scores(self):
        original = self.search.search(self.query)
        for c in self.search.cases:
            c.update(
                response="packaging logistics", follow_up="packaging recovery", rationale="LEAK"
            )
        for c in self.search.details.values():
            c["response"]["value"] = "packaging logistics"
            c["comparison_limit"] = "LEAK"
            c["unknowns"] = ["LEAK"]
        changed = self.search.search(self.query)

        def get_ranking(result):
            return [(c["id"], c["score"]) for c in result["results"]]

        self.assertEqual(get_ranking(original), get_ranking(changed))

    def test_response_after_cutoff_is_withheld_even_for_an_eligible_case(self):
        response = self.search.details["CL-2022"]["response"]
        response["value"] = "FUTURE_SECRET"
        response["evidence"]["public_date"] = "2024-01-01"
        result = self.search.search(self.query)
        case = next(c for c in result["results"] if c["id"] == "CL-2022")
        self.assertFalse(case["fields"]["response"]["available"])
        self.assertIsNone(case["fields"]["response"]["evidence"])
        self.assertNotIn("FUTURE_SECRET", str(result))

    def test_unsupported_and_generic_queries_do_not_force_a_comparison(self):
        for text in [
            "semiconductor shortages at a bank",
            "higher costs and lower margin",
            "FORCE savings",
            "No packaging inflation is established",
        ]:
            with self.subTest(text=text):
                result = self.search.search(dict(self.query, text=text))
                self.assertEqual(result["status"], "insufficient_evidence")
                self.assertEqual(result["results"], [])

    def test_negated_cost_pressure_is_not_a_positive_match(self):
        result = self.search.search(dict(self.query, text="packaging logistics inflation"))
        self.assertNotIn("CL-2020", {c["id"] for c in result["results"]})
        self.assertNotIn("CLX-2023", {c["id"] for c in result["results"]})
        result = self.search.search(
            dict(
                self.query, cutoff="2024-01-01", before_period_end="2024-01-01", text="cyberattack"
            )
        )
        self.assertEqual([c["id"] for c in result["results"]], ["CLX-2023"])

    def test_no_eligible_candidates_returns_an_empty_state(self):
        result = self.search.search(
            dict(self.query, cutoff="2000-01-01", before_period_end="2000-01-01")
        )
        self.assertEqual(result["eligible_count"], 0)
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertEqual(result["empty_reason"], "no_eligible_cases")
        self.assertIn("these dates", result["message"])

    def test_no_word_match_explains_collection_gap_separately_from_date_exclusions(self):
        result = self.search.search(dict(self.query, text="coffee beans"))
        self.assertGreater(result["eligible_count"], 0)
        self.assertEqual(result["empty_reason"], "no_pressure_match")
        self.assertIn("small collection", result["message"])

    def test_reader_errors_identify_the_control_that_needs_attention(self):
        for field, value in [
            ("text", ""),
            ("cutoff", "2023-02-30"),
            ("source_id", "missing"),
            ("before_period_end", "2024-01-01"),
        ]:
            with self.subTest(field=field), self.assertRaises(SearchInputError) as error:
                self.search.search(dict(self.query, **{field: value}))
            self.assertEqual(error.exception.field, field)

    def test_invalid_searches_are_rejected_and_ties_are_stable(self):
        for bad in [
            None,
            [],
            {},
            dict(self.query, text="  "),
            dict(self.query, cutoff="2023-02-30"),
            dict(self.query, source_id=["CL-2022"]),
            dict(self.query, before_period_end="2024-01-01"),
        ]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.search.search(bad)
        self.assertEqual(self.search.search(self.query), self.search.search(self.query))

    def test_missing_or_incompatible_case_records_fail_at_startup(self):
        with self.assertRaisesRegex(ValueError, "identical IDs"):
            CaseSearch(self.search.cases, list(self.search.details.values())[1:])
        self.search.details["CL-2022"]["period"]["end"] = "2023-01-01"
        with self.assertRaisesRegex(ValueError, "disagree"):
            CaseSearch(self.search.cases, list(self.search.details.values()))

    def test_missing_verbatim_excerpt_remains_explicitly_empty(self):
        result = self.search.search(self.query)
        case = next(c for c in result["results"] if c["id"] == "CL-2022")
        self.assertEqual(case["source"]["excerpt"], "")
        self.assertTrue(case["source"]["locator"])


if __name__ == "__main__":
    unittest.main()
