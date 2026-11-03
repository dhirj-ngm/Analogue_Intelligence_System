"""Protect provenance, eligibility and completeness of the small AI audit."""

from copy import deepcopy
import json
import unittest

from ais.search import CaseSearch
from scripts.check_audit_m008 import DIRECTORY, run, validate_labels


class AIAuditTests(unittest.TestCase):
    def setUp(self):
        self.search = CaseSearch.load("m007")
        self.snapshot = json.loads((DIRECTORY / "snapshot.json").read_text())
        self.labels = json.loads((DIRECTORY / "judgements.json").read_text())
        self.sources = json.loads((DIRECTORY / "source-checks.json").read_text())

    def test_snapshot_and_optional_packet_reproduce_with_human_validation_deferred(self):
        result = run()
        self.assertEqual(result["human_validation"], "deferred")
        self.assertEqual(result["human_judgements"], 0)
        self.assertEqual(result["displayed_assessments"], 10)

    def test_ai_cannot_be_relabelled_human_or_silently_drop_displayed_cases(self):
        for mutation in [
            lambda x: x.update(independent_human_validation=True),
            lambda x: x["displayed_judgements"].pop(),
            lambda x: x["displayed_judgements"].append(x["displayed_judgements"][0]),
        ]:
            bad = deepcopy(self.labels)
            mutation(bad)
            with self.assertRaises(ValueError):
                validate_labels(self.snapshot, bad, self.sources, self.search)

    def test_omissions_must_be_eligible_and_assessments_need_source_evidence(self):
        bad = deepcopy(self.labels)
        next(r for r in bad["other_assessments"] if r["role"] == "date_excluded")["role"] = (
            "important_omission"
        )
        with self.assertRaisesRegex(ValueError, "eligible"):
            validate_labels(self.snapshot, bad, self.sources, self.search)
        bad = deepcopy(self.sources)
        bad["checks"] = [c for c in bad["checks"] if c["case_id"] != "KC-2011"]
        with self.assertRaisesRegex(ValueError, "source check"):
            validate_labels(self.snapshot, self.labels, bad, self.search)


if __name__ == "__main__":
    unittest.main()
