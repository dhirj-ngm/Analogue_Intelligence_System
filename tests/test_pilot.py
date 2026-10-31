import copy
import unittest
from ais.pilot import ROOT, bm25, eligible, metrics, ranking_text, read_jsonl, validate


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.cases = read_jsonl(ROOT / "data/pilot/cases.jsonl")
        self.queries = read_jsonl(ROOT / "evaluation/pilot/queries.jsonl")
        self.judgements = read_jsonl(ROOT / "evaluation/pilot/judgements.jsonl")

    def test_publication_cutoff_not_reporting_end(self):
        c = copy.deepcopy(self.cases[0])
        c["publication_date"] = "2023-02-01"
        self.assertEqual(eligible(self.queries[0], c), (False, "after_cutoff"))

    def test_self_duplicate_unknown_and_future_period_exclusions(self):
        q = self.queries[0]
        self.assertEqual(eligible(q, self.cases[7])[1], "self")
        c = copy.deepcopy(self.cases[0])
        self.assertEqual(
            eligible(dict(q, exclude_groups=[c["duplicate_group"]]), c)[1],
            "duplicate_or_continuation",
        )
        c["publication_date"] = None
        self.assertEqual(eligible(q, c)[1], "unknown_publication_date")
        c["publication_date"] = q["cutoff"]
        c["period_end"] = q["before_period_end"]
        self.assertEqual(eligible(q, c)[1], "not_earlier_observation")

    def test_response_and_outcome_cannot_enter_text(self):
        c = copy.deepcopy(self.cases[0])
        before = ranking_text(c)
        c.update(
            response="SECRET RESPONSE", follow_up="FUTURE OUTCOME", rationale="LEAK", tags=["LEAK"]
        )
        self.assertEqual(ranking_text(c), before)

    def test_metrics_known_order_short_list_and_zero_gain(self):
        self.assertEqual(metrics(["a"], {"a": 3})["precision_at_5"], 0.2)
        self.assertEqual(metrics(["a"], {"a": 3})["ndcg_at_5"], 1)
        self.assertEqual(metrics(["a"], {"a": 0})["ndcg_at_5"], 0)
        self.assertLess(metrics(["b", "a"], {"a": 3, "b": 0})["ndcg_at_5"], 1)

    def test_bm25_term_match_and_empty(self):
        scores = bm25("packaging", ["packaging costs", "cyber disruption"])
        self.assertGreater(scores[0], scores[1])
        self.assertEqual(bm25("x", []), [])
        self.assertEqual(bm25("x", [""]), [0])

    def test_malformed_and_incomplete_judgements_rejected(self):
        with self.assertRaises(ValueError):
            validate(self.cases, self.queries, self.judgements[:-1])
        self.cases[0]["period_end"] = "2099-01-01"
        with self.assertRaises(ValueError):
            validate(self.cases, self.queries, self.judgements)

    def test_real_corpus_and_pair_coverage(self):
        validate(self.cases, self.queries, self.judgements)
        self.assertEqual(len(self.cases), 10)
        self.assertEqual(len(self.queries), 5)
        self.assertEqual(len(self.judgements), 33)


if __name__ == "__main__":
    unittest.main()
