"""Behavioral tests for review-state integrity, not semantic brief grading."""
import copy
import importlib.util
import io
import json
import unittest
import uuid
from pathlib import Path

MODULE = Path(__file__).resolve().parent
ROOT = MODULE.parent
SPEC = importlib.util.spec_from_file_location("review_state", ROOT / ".agents/skills/review-checklist/scripts/review_state.py")
review_state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_state)
BASE = json.loads((MODULE / "reviews/manual-2026-11-12.json").read_text(encoding="utf-8"))

class ReviewStateTests(unittest.TestCase):
    def setUp(self):
        self.directory = MODULE / ".validation-temp/state-tests" / uuid.uuid4().hex
        self.directory.mkdir(parents=True)
        self.report = self.directory / "report.json"
        self.state = self.directory / "state.json"
        self.delta = self.directory / "delta.json"

    def run_report(self, report=None):
        self.report.write_text(json.dumps(report or BASE, ensure_ascii=False), encoding="utf-8")
        return review_state.apply_report(self.report, self.state, self.delta)

    def baseline(self):
        self.run_report()
        return self.state.read_bytes()

    def test_01_baseline_accounts_for_all_briefs_and_four_flags(self):
        result = self.run_report()
        self.assertEqual(result["status"], "baseline_created")
        self.assertEqual(result["brief_count"], 4)
        self.assertEqual(result["flag_count"], 4)
        self.assertEqual(len(result["new"]), 4)
        self.assertTrue(result["should_surface"])

    def test_02_unchanged_review_is_quiet(self):
        self.baseline()
        result = self.run_report()
        self.assertEqual(result["status"], "unchanged")
        self.assertFalse(result["should_surface"])

    def test_03_rephrased_reasons_do_not_create_false_alerts(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        for b in report["briefs"]:
            for check in b["checks"].values():
                check["reason"] += " Reviewer phrasing changed."
        self.assertFalse(self.run_report(report)["should_surface"])

    def test_04_unrelated_source_edit_does_not_repeat_the_same_flags(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        report["briefs"][0]["source_text"] += "\nAdministrative date updated.\n"
        self.assertEqual(self.run_report(report)["status"], "unchanged")

    def test_05_resolved_flag_is_visible_and_not_new(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        b = report["briefs"][0]
        b["source_text"] += "\nOwner: Dispatch PM.\n"
        b["checks"]["owner_named"] = {"status":"pass", "section":"Owner", "evidence":["Owner: Dispatch PM."], "reason":"Explicit role now assigned."}
        result = self.run_report(report)
        self.assertEqual(len(result["resolved"]), 1)
        self.assertEqual(len(result["new"]), 0)
        self.assertTrue(result["should_surface"])

    def test_06_new_issue_identity_is_reported(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        c = report["briefs"][0]["checks"]["scope_bounded"]
        c.update(status="flag", business_impact="Synthetic state-transition fixture.", next_action="Review the synthetic change.")
        result = self.run_report(report)
        self.assertEqual(len(result["new"]), 1)
        self.assertTrue(result["should_surface"])

    def test_07_changed_evidence_updates_existing_issue(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        c = report["briefs"][0]["checks"]["owner_named"]
        c["evidence"] = ["Flagging this for whoever picks it up next quarter."]
        result = self.run_report(report)
        self.assertEqual(len(result["changed"]), 1)
        self.assertEqual(len(result["new"]), 0)

    def test_08_incomplete_read_preserves_complete_baseline(self):
        old = self.baseline()
        report = copy.deepcopy(BASE)
        report["complete"] = False
        report["briefs"].pop()
        report["access_errors"] = ["One source unavailable."]
        result = self.run_report(report)
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["resolved"], [])
        self.assertEqual(old, self.state.read_bytes())

    def test_09_repeated_same_access_failure_is_quiet(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        report["complete"] = False
        report["briefs"].pop()
        report["access_errors"] = ["One source unavailable."]
        self.assertTrue(self.run_report(report)["should_surface"])
        self.assertFalse(self.run_report(report)["should_surface"])

    def test_10_access_restoration_is_visible(self):
        self.baseline()
        bad = copy.deepcopy(BASE)
        bad["complete"] = False
        bad["access_errors"] = ["Connector unavailable."]
        self.run_report(bad)
        restored = self.run_report()
        self.assertTrue(restored["access_restored"])
        self.assertTrue(restored["should_surface"])

    def test_11_explicit_source_removal_is_not_false_resolution(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        removed = report["briefs"].pop()
        report["expected_ids"].remove(removed["id"])
        result = self.run_report(report)
        self.assertEqual(len(result["removed_sources"]), 1)
        self.assertEqual(result["resolved"], [])

    def test_12_fabricated_quote_is_rejected_without_baseline_change(self):
        old = self.baseline()
        report = copy.deepcopy(BASE)
        report["briefs"][0]["checks"]["owner_named"]["evidence"] = ["This quote does not exist."]
        with self.assertRaises(ValueError):
            self.run_report(report)
        self.assertEqual(old, self.state.read_bytes())

    def test_13_duplicate_source_ids_are_rejected(self):
        self.baseline()
        report = copy.deepcopy(BASE)
        report["briefs"].append(copy.deepcopy(report["briefs"][0]))
        with self.assertRaises(ValueError):
            self.run_report(report)

    def test_14_empty_index_cannot_produce_an_all_clear(self):
        report = copy.deepcopy(BASE)
        report["expected_ids"], report["briefs"] = [], []
        with self.assertRaises(ValueError):
            self.run_report(report)
        self.assertFalse(self.state.exists())

    def test_15_unknown_judgment_preserves_baseline(self):
        old = self.baseline()
        report = copy.deepcopy(BASE)
        report["briefs"][0]["checks"]["owner_named"] = {"status":"unknown", "reason":"Cannot determine.", "evidence":[]}
        result = self.run_report(report)
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(old, self.state.read_bytes())

    def test_16_outside_artifact_path_is_rejected(self):
        with self.assertRaises(ValueError):
            review_state.artifact_path("../outside.json")

    def test_17_report_and_baseline_must_be_separate(self):
        self.report.write_text(json.dumps(BASE), encoding="utf-8")
        with self.assertRaises(ValueError):
            review_state.apply_report(self.report, self.report, self.delta)

    def test_18_missing_check_is_rejected(self):
        report = copy.deepcopy(BASE)
        del report["briefs"][0]["checks"]["success_measure"]
        with self.assertRaises(ValueError):
            self.run_report(report)

if __name__ == "__main__":
    log = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReviewStateTests)
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    output = {"tests_run":result.testsRun, "failures":len(result.failures), "errors":len(result.errors),
              "successful":result.wasSuccessful(), "log":log.getvalue(),
              "scope":"Review-state transitions and evidence integrity. Semantic checklist behavior was separately exercised on four freshly read wiki briefs."}
    (MODULE / "evidence").mkdir(exist_ok=True)
    (MODULE / "evidence/review-state-validation.json").write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(log.getvalue(),end="")
    print(json.dumps({k:output[k] for k in ["tests_run","failures","errors","successful"]}))
    raise SystemExit(0 if result.wasSuccessful() else 1)

