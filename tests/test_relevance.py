"""Synthetic labels test analysis arithmetic; none are human review evidence."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from ais.relevance import (
    analyze,
    check,
    digest,
    prepare,
    save,
    snapshot,
    validate_submission,
)


class RelevanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.packet = {
            "packet_id": "synthetic-only",
            "queries": [
                {"query_id": "Q1", "items": [{"item_id": "A"}, {"item_id": "B"}, {"item_id": "C"}]},
                {"query_id": "Q2", "items": [{"item_id": "D"}]},
            ],
        }
        self.private = {
            "queries": [
                {
                    "query_id": "Q1",
                    "items": {"A": "C1", "B": "C2", "C": "C3"},
                    "displayed": [{"id": "C1"}, {"id": "C2"}],
                },
                {"query_id": "Q2", "items": {"D": "C3"}, "displayed": []},
            ]
        }
        self.submission = {
            "packet_id": "synthetic-only",
            "reviewer_id": "TEST_ONLY",
            "attestation": {
                "human": True,
                "created_cases_or_rules": False,
                "seen_expected_answers": False,
                "used_ai_judgements": False,
            },
            "judgements": [],
            "queries": [],
        }
        for qid, item, label in [
            ("Q1", "A", "useful"),
            ("Q1", "B", "not_useful"),
            ("Q1", "C", "useful"),
            ("Q2", "D", "useful"),
        ]:
            self.submission["judgements"].append(
                {
                    "query_id": qid,
                    "item_id": item,
                    "usefulness": label,
                    "reason": "Synthetic fixture rationale, not a human judgement.",
                    "misleading": "yes" if label == "not_useful" else "no",
                    "misleading_reason": "Synthetic mismatch",
                    "source_access": "not_opened",
                    "source_note": "",
                }
            )
        self.submission["queries"] = [
            {
                "query_id": q,
                "coverage": "limited",
                "reason": "Synthetic coverage rationale.",
                "missing_cases": "Unverified suggestion",
            }
            for q in ("Q1", "Q2")
        ]

    def registered(self, submission, **changes):
        path = self.directory / (submission["reviewer_id"] + ".json")
        save(path, submission)
        entry = {
            "reviewer_id": submission["reviewer_id"],
            "type": "human",
            "identity_verified": True,
            "independence_confirmed": True,
            "created_cases_or_rules": False,
            "is_project_user": False,
            "verification_method": "SYNTHETIC TEST ONLY",
            "authorization_reference": "SYNTHETIC TEST ONLY",
            "receipt_reference": "SYNTHETIC TEST ONLY",
            "submission_sha256": digest(path),
            **changes,
        }
        return path, entry

    def test_real_packet_is_blinded_exhaustive_and_dates_are_preserved(self):
        packet, private = snapshot()
        self.assertEqual(private["collection_count"], 17)
        self.assertEqual(len(packet["queries"]), 10)
        self.assertEqual(sum(len(q["items"]) for q in packet["queries"]), 154)
        forbidden = {
            "score",
            "rank",
            "ranked",
            "displayed",
            "expected_useful_cases",
            "expected_answers",
            "case_id",
            "method_id",
            "pressure_matches",
            "query_reading",
            "sampling_stratum",
        }

        def keys(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden & value.keys())
                for item in value.values():
                    keys(item)
            elif isinstance(value, list):
                for item in value:
                    keys(item)

        keys(packet)
        for q, meta in zip(packet["queries"], private["queries"], strict=True):
            self.assertEqual(len(meta["eligible_ids"]), len(q["items"]))
            self.assertEqual(set(meta["items"].values()), set(meta["eligible_ids"]))
            for item in q["items"]:
                self.assertLessEqual(item["published"], q["cutoff"])
                self.assertLess(item["period"]["end"], q["before_period_end"])
                self.assertTrue(item["source"]["url"].startswith("https://"))
                for field in item["fields"].values():
                    if field["evidence"]:
                        self.assertLessEqual(field["evidence"]["public_date"], q["cutoff"])
            if q["query_id"] == "Q09":
                self.assertNotIn("SJM-COFFEE-2011", meta["eligible_ids"])
            if q["query_id"] == "Q10":
                self.assertNotIn("HSY-2025-Q1", meta["eligible_ids"])

    def test_packet_reproduces_refuses_overwrite_and_detects_tampering(self):
        packet, private = prepare(self.directory)
        self.assertEqual(check(self.directory), (packet, private))
        with self.assertRaisesRegex(ValueError, "already frozen"):
            prepare(self.directory)
        path = self.directory / "reviewer/packet.html"
        path.write_text(path.read_text() + "tamper")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            check(self.directory)

    def test_no_reviewers_means_no_human_results_or_zero_quality_claim(self):
        report = analyze(self.packet, self.private, [], {"reviewers": []})
        self.assertEqual(report["state"], "awaiting_independent_human_review")
        self.assertEqual(report["judged_pairs"], 0)
        self.assertEqual(report["reviews"], [])
        self.assertEqual(report["disagreement_status"], "not_measured")

    def test_self_attestation_ai_user_contributor_and_unverified_receipts_do_not_qualify(self):
        path, person = self.registered(self.submission)
        for change in [
            {"type": "ai"},
            {"identity_verified": False},
            {"created_cases_or_rules": True},
            {"is_project_user": True},
            {"receipt_reference": ""},
            {"submission_sha256": "wrong"},
        ]:
            with self.subTest(change=change):
                report = analyze(
                    self.packet, self.private, [path], {"reviewers": [{**person, **change}]}
                )
                self.assertEqual(report["independent_human_reviewers"], 0)
                self.assertEqual(len(report["excluded_submissions"]), 1)
        report = analyze(self.packet, self.private, [path], {"reviewers": []})
        self.assertEqual(report["reviews"], [])

    def test_synthetic_complete_arithmetic_includes_omissions_and_false_abstentions(self):
        path, person = self.registered(self.submission)
        report = analyze(self.packet, self.private, [path], {"reviewers": [person]})
        review = report["reviews"][0]
        q1, q2 = review["queries"]
        self.assertEqual(q1["measures"]["useful_share_of_displayed"], 0.5)
        self.assertEqual(q1["measures"]["within_eligible_pool_recall"], 0.5)
        self.assertEqual(q1["measures"]["useful_omitted_ids"], ["C3"])
        self.assertEqual(q1["displayed_misleading"], {"no": 1, "yes": 1})
        self.assertTrue(q2["measures"]["empty_result_with_useful_case"])
        self.assertIsNone(q2["measures"]["useful_share_of_displayed"])
        self.assertEqual(
            review["aggregate"], {"displayed_useful": 1, "displayed_total": 2, "useful_share": 0.5}
        )
        self.assertEqual(report["disagreement_status"], "not_measured")

    def test_partial_and_uncertain_are_not_silently_collapsed_or_extrapolated(self):
        self.submission["judgements"][0]["usefulness"] = "partly_useful"
        self.submission["judgements"][1]["usefulness"] = "unsure"
        self.submission["judgements"].pop()
        path, person = self.registered(self.submission)
        report = analyze(self.packet, self.private, [path], {"reviewers": [person]})
        review = report["reviews"][0]
        self.assertEqual(
            review["queries"][0]["displayed_labels"], {"partly_useful": 1, "unsure": 1}
        )
        self.assertEqual(review["queries"][0]["measures"]["useful_share_of_displayed"], 0)
        self.assertIsNone(review["queries"][1]["measures"])
        self.assertIsNone(review["aggregate"])

    def test_invalid_or_duplicate_labels_and_missing_reasons_are_rejected(self):
        mutations = [
            lambda s: s.update(packet_id="other"),
            lambda s: s["judgements"].append(s["judgements"][0]),
            lambda s: s["judgements"][0].update(reason=""),
            lambda s: s["judgements"][0].update(item_id="unknown"),
            lambda s: s["judgements"][0].update(misleading="unsure", misleading_reason=""),
            lambda s: s["judgements"][0].update(source_access="unavailable", source_note=""),
            lambda s: s["attestation"].update(used_ai_judgements=True),
            lambda s: s["judgements"][0].update(case_id="forged mapping"),
            lambda s: s["queries"][0].update(missing_cases={"wrong": "format"}),
        ]
        for mutation in mutations:
            bad = deepcopy(self.submission)
            mutation(bad)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_submission(bad, self.packet)

    def test_multiple_reviewers_keep_disagreements_and_original_reasons(self):
        second = deepcopy(self.submission)
        second["reviewer_id"] = "TEST_ONLY_2"
        second["judgements"][0].update(
            usefulness="unsure", reason="Different synthetic uncertainty"
        )
        pa, a = self.registered(self.submission)
        pb, b = self.registered(second)
        result = analyze(self.packet, self.private, [pa, pb], {"reviewers": [a, b]})
        self.assertEqual(result["disagreement_status"], "observed_on_shared_pairs")
        self.assertEqual(len(result["disagreements"]), 1)
        disagreement = result["disagreements"][0]
        self.assertEqual(disagreement["reviewers"]["TEST_ONLY_2"]["usefulness"], "unsure")
        self.assertEqual(
            disagreement["reviewers"]["TEST_ONLY_2"]["reason"], "Different synthetic uncertainty"
        )


if __name__ == "__main__":
    unittest.main()
