"""Validate Module 4 against the actual unmodified teaching-source modules.

Python standard library only. Device, clock and availability adapters are
controlled because their implementations are deliberately omitted from the repo.
No production configuration, routing source or source data is edited.
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import sys
import unittest
from contextlib import ExitStack
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
MODULE = Path(__file__).resolve().parent
ROOT = MODULE.parent
SOURCE = ROOT / "00-rook" / "code" / "dispatch-routing"
sys.path.insert(0, str(SOURCE))

import availability
import config
import history
import offer
import routing

RESULTS = {}
SOURCE_NAMES = ["config.py", "offer.py", "history.py", "routing.py", "availability.py"]
SOURCE_BEFORE = {n: hashlib.sha256((SOURCE / n).read_bytes()).hexdigest() for n in SOURCE_NAMES}


def responder(name, capabilities=("flight",)):
    return SimpleNamespace(name=name, capabilities=list(capabilities))


def callout(at=None):
    return SimpleNamespace(
        region="Example district",
        at=at or datetime(2026, 8, 13, 12, 0),
        location="Example incident",
        required_capabilities=["flight"],
    )


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def time(self):
        return self.now


def offer_with_clock(timeout, response_after):
    """A willing responder takes at response_after seconds, if still offered."""
    clock = FakeClock()
    r = responder("Example willing responder")
    c = callout()

    def poll(*_):
        if clock.now >= response_after:
            return offer.TAKEN
        clock.now += 1
        return None

    with ExitStack() as stack:
        stack.enter_context(patch.object(offer, "OFFER_TIMEOUT_SECONDS", timeout))
        stack.enter_context(patch.object(offer.time, "time", clock.time))
        push = stack.enter_context(patch.object(offer, "push_to_device"))
        withdraw = stack.enter_context(patch.object(offer, "withdraw_from_device"))
        stack.enter_context(patch.object(offer, "poll_device", side_effect=poll))
        result = offer.offer_to(r, c)
        return {"timeout": timeout, "response_after": response_after, "outcome": result,
                "elapsed": clock.now, "push_calls": push.call_count,
                "withdraw_calls": withdraw.call_count}


def observed_sequence_replay(initial_score, misses_penalized=True):
    """Fixed observed offers/outcomes, not a historical routing counterfactual."""
    pings = json.loads((ROOT / "03-rewind/evidence/pings.json").read_text(encoding="utf-8"))
    roster = json.loads((ROOT / "03-rewind/evidence/responders.json").read_text(encoding="utf-8"))
    people = {r["name"]: responder(r["name"]) for r in roster}
    history._scores.clear()
    history._scores.update({name: initial_score for name in people})
    weeks = [datetime(2026, 6, 29) + timedelta(weeks=i) for i in range(10)]
    ordered = sorted(pings, key=lambda p: (p["sent_at"], p["callout_number"], p["responder"]))
    snapshots, events = [], []
    index = 0
    counts = {"taken": 0, "turned down": 0, "missed": 0}
    for week in weeks:
        end = (week + timedelta(days=7)).isoformat()
        while index < len(ordered) and ordered[index]["sent_at"] < end:
            p = ordered[index]
            r = people[p["responder"]]
            before = history.recent_acceptance(r)
            counts[p["outcome"]] += 1
            if p["outcome"] == offer.TAKEN:
                history.record_accepted(r)
            elif p["outcome"] == offer.TURNED_DOWN or misses_penalized:
                history.record_declined(r)
            events.append({**p, "modeled_score_before": before,
                           "modeled_score_after": history.recent_acceptance(r)})
            index += 1
        snapshots.append({"week_start": week.date().isoformat(),
                          "scores": {name: history.recent_acceptance(r) for name, r in people.items()}})
    return {"assumed_initial_score": initial_score, "misses_penalized": misses_penalized,
            "counts": counts, "processed": index, "snapshots": snapshots, "events": events}


class MechanismTests(unittest.TestCase):
    def setUp(self):
        history._scores.clear()

    def tearDown(self):
        history._scores.clear()

    def test_01_same_willing_response_is_taken_at_90_but_missed_at_60(self):
        old = offer_with_clock(90, 75)
        new = offer_with_clock(60, 75)
        self.assertEqual(old["outcome"], offer.TAKEN)
        self.assertEqual(new["outcome"], offer.MISSED)
        self.assertEqual(old["withdraw_calls"], 0)
        self.assertEqual(new["withdraw_calls"], 1)
        RESULTS["controlled_75_second_response"] = {"90_seconds": old, "60_seconds": new}

    def test_02_deadline_is_strictly_before_60_seconds(self):
        before = offer_with_clock(60, 59)
        at = offer_with_clock(60, 60)
        self.assertEqual(before["outcome"], offer.TAKEN)
        self.assertEqual(at["outcome"], offer.MISSED)
        RESULTS["deadline_boundary"] = {"59_seconds": before, "60_seconds": at}

    def test_03_missed_and_explicit_refusal_have_identical_history_effect(self):
        results = {}
        for outcome in [offer.MISSED, offer.TURNED_DOWN]:
            r = responder(outcome)
            with patch.object(routing, "rank_for_callout", return_value=[r]), patch.object(
                offer, "offer_to", return_value=outcome
            ):
                self.assertIsNone(offer.dispatch(callout()))
            results[outcome] = history.recent_acceptance(r)
            self.assertAlmostEqual(results[outcome], 0.38)
        RESULTS["miss_vs_decline"] = results

    def test_04_acceptance_credit_and_early_stop(self):
        a, b = responder("First"), responder("Second")
        with patch.object(routing, "rank_for_callout", return_value=[a, b]), patch.object(
            offer, "offer_to", return_value=offer.TAKEN
        ) as send:
            self.assertIs(offer.dispatch(callout()), a)
        self.assertEqual(send.call_count, 1)
        self.assertAlmostEqual(history.recent_acceptance(a), 0.58)
        self.assertAlmostEqual(history.recent_acceptance(b), 0.5)

    def test_05_penalties_and_recovery_are_asymmetric_and_bounded(self):
        r = responder("Example")
        trace = [history.recent_acceptance(r)]
        for _ in range(5):
            history.record_declined(r)
            trace.append(history.recent_acceptance(r))
        self.assertEqual(history.recent_acceptance(r), 0)
        for _ in range(6):
            history.record_accepted(r)
        self.assertLess(history.recent_acceptance(r), history.NEUTRAL_SCORE)
        history.record_accepted(r)
        self.assertGreaterEqual(history.recent_acceptance(r), history.NEUTRAL_SCORE)
        for _ in range(100):
            history.record_accepted(r)
        self.assertEqual(history.recent_acceptance(r), 1)
        RESULTS["neutral_to_floor"] = trace
        RESULTS["acceptances_from_floor_to_at_least_neutral"] = 7

    def test_06_calendar_time_does_not_restore_history(self):
        r = responder("Quiet responder")
        history._set(r, 0.14)
        for date in [datetime(2026, 8, 13), datetime(2027, 8, 13)]:
            with patch.object(availability, "available_for", return_value=[r]), patch.object(
                availability, "travel_time_minutes", return_value=10
            ):
                self.assertEqual(routing.rank_for_callout(callout(date)), [r])
                self.assertAlmostEqual(history.recent_acceptance(r), 0.14)

    def test_07_one_miss_and_competitor_acceptance_reverse_priority(self):
        a, b = responder("Near responder"), responder("Far responder")
        minutes = {a.name: 10, b.name: 20}
        history._scores.update({a.name: 0.5, b.name: 0.9})
        with patch.object(availability, "available_for", return_value=[a, b]), patch.object(
            availability, "travel_time_minutes", side_effect=lambda r, _: minutes[r.name]
        ):
            scores_before = {r.name: routing.score(r, callout()) for r in [a, b]}
            self.assertEqual(routing.rank_for_callout(callout()), [a, b])
            with patch.object(offer, "offer_to", side_effect=lambda r, _: offer.MISSED if r is a else offer.TAKEN):
                self.assertIs(offer.dispatch(callout()), b)
            scores_after = {r.name: routing.score(r, callout()) for r in [a, b]}
            self.assertEqual(routing.rank_for_callout(callout()), [b, a])
            self.assertAlmostEqual(history.recent_acceptance(a), 0.38)
        RESULTS["priority_reversal"] = {"travel_minutes": minutes,
                                      "initial_history": {a.name: 0.5, b.name: 0.9},
                                      "score_before": scores_before, "score_after": scores_after,
                                      "near_history_after": 0.38,
                                      "far_history_after": 0.98,
                                      "note": "Both the near responder's penalties and the far responder's credits contribute."}

    def test_08_ranked_but_unoffered_remains_stuck_when_leader_keeps_accepting(self):
        a, b = responder("Low history"), responder("High history")
        history._scores.update({a.name: 0.26, b.name: 1.0})
        with patch.object(availability, "available_for", return_value=[a, b]), patch.object(
            availability, "travel_time_minutes", return_value=10
        ), patch.object(offer, "offer_to", return_value=offer.TAKEN) as send:
            for i in range(50):
                self.assertIs(offer.dispatch(callout(datetime(2026, 8, 13) + timedelta(days=i))), b)
                self.assertIn(a, routing.rank_for_callout(callout()))
            self.assertEqual(send.call_count, 50)
            self.assertTrue(all(c.args[0] is b for c in send.call_args_list))
            self.assertAlmostEqual(history.recent_acceptance(a), 0.26)
        RESULTS["ranked_without_offers"] = {"callouts": 50, "low_history_offers": 0,
                                           "low_history_score_start": 0.26,
                                           "low_history_score_end": 0.26}

    def test_09_reweighting_changes_priority_but_does_not_remove_history(self):
        a, b = responder("Near responder"), responder("Far responder")
        history._scores.update({a.name: 0.5, b.name: 0.9})
        with patch.object(availability, "available_for", return_value=[a, b]), patch.object(
            availability, "travel_time_minutes", side_effect=lambda r, _: 10 if r is a else 20
        ):
            new_order = [r.name for r in routing.rank_for_callout(callout())]
            with patch.object(routing, "WEIGHT_PROXIMITY", 0.45), patch.object(
                routing, "WEIGHT_RECENT_ACCEPTANCE", 0.40
            ):
                old_order = [r.name for r in routing.rank_for_callout(callout())]
            self.assertEqual(new_order, [a.name, b.name])
            self.assertEqual(old_order, [b.name, a.name])
            before = routing.score(a, callout())
            history.record_declined(a)
            after = routing.score(a, callout())
            self.assertAlmostEqual(before - after, 0.25 * 0.12)
        RESULTS["weight_sensitivity"] = {"pre_42_comment_values_order": old_order,
                                        "current_order": new_order,
                                        "current_score_cost_per_miss_before_floor": 0.03,
                                        "prior_weight_score_cost_per_miss_before_floor": 0.048}

    def test_10_zero_history_still_remains_on_supplied_candidate_list(self):
        a, b = responder("Zero"), responder("Other")
        history._set(a, 0)
        with patch.object(availability, "available_for", return_value=[a, b]), patch.object(
            availability, "travel_time_minutes", return_value=10
        ):
            self.assertEqual(set(r.name for r in routing.rank_for_callout(callout())), {a.name, b.name})

    def test_11_if_every_offer_is_missed_dispatch_exhausts_candidates(self):
        a, b = responder("One"), responder("Two")
        with patch.object(routing, "rank_for_callout", return_value=[a, b]), patch.object(
            offer, "offer_to", return_value=offer.MISSED
        ) as send:
            self.assertIsNone(offer.dispatch(callout()))
            self.assertEqual(send.call_count, 2)
            self.assertAlmostEqual(history.recent_acceptance(a), 0.38)
            self.assertAlmostEqual(history.recent_acceptance(b), 0.38)

    def test_12_provided_dispatch_does_not_write_readiness_or_supply_record(self):
        a = responder("Still marked available")
        a.available = True
        opaque_record = {"opaque_contract_fixture": ["must remain unchanged"]}
        before = copy.deepcopy(opaque_record)
        with patch.object(availability, "available_for", return_value=[a]), patch.object(
            availability, "travel_time_minutes", return_value=10
        ), patch.object(availability, "current_record", return_value=opaque_record) as record, patch.object(
            offer, "offer_to", return_value=offer.MISSED
        ):
            self.assertIsNone(offer.dispatch(callout()))
            self.assertTrue(a.available)
            record.assert_not_called()
        self.assertEqual(before, opaque_record)
        RESULTS["availability_boundary"] = {
            "supplied_dispatch_calls_current_record": False,
            "fixture_changed": False,
            "limit": "The real availability and Supply adapters are absent; this is not an end-to-end Supply contract test."}

    def test_13_capability_is_a_soft_score_in_this_component(self):
        near = responder("Near missing capability", capabilities=())
        far = responder("Far capable")
        with patch.object(availability, "available_for", return_value=[near, far]), patch.object(
            availability, "travel_time_minutes", side_effect=lambda r, _: 0 if r is near else 20
        ):
            self.assertEqual(routing.capability_score(near, callout()), 0)
            self.assertEqual(routing.rank_for_callout(callout())[0], near)
            with patch.object(offer, "offer_to", return_value=offer.TAKEN):
                self.assertIs(offer.dispatch(callout()), near)
        RESULTS["capability_boundary"] = {
            "fixture": "Available-for stub deliberately supplies an incapable candidate.",
            "observed": "This component ranks and offers that candidate; no hard capability gate here.",
            "limit": "Verify whether omitted upstream availability/eligibility code enforces full capability."}

    def test_14_fixed_observed_sequence_replay_is_complete(self):
        runs = {str(seed): observed_sequence_replay(seed) for seed in [0.0, 0.5, 1.0]}
        for seed, run in runs.items():
            self.assertEqual(run["processed"], 1696)
            self.assertEqual(run["counts"], {"taken": 1222, "turned down": 339, "missed": 135})
            self.assertEqual(len(run["snapshots"]), 10)
            self.assertTrue(all(0 <= s <= 1 for w in run["snapshots"] for s in w["scores"].values()))
        neutral = observed_sequence_replay(0.5, misses_penalized=False)
        RESULTS["fixed_sequence_replay"] = {"current_rule": runs, "misses_neutral_sensitivity": neutral,
            "limit": "Observed offers and outcomes held fixed. No missing candidate states are invented; this does not predict restored offers or avoided misses."}

    def test_15_hashes_confirm_source_unchanged(self):
        after = {n: hashlib.sha256((SOURCE / n).read_bytes()).hexdigest() for n in SOURCE_NAMES}
        self.assertEqual(SOURCE_BEFORE, after)

    def test_16_longer_timeout_does_not_reset_existing_low_history(self):
        a, b = responder("Low history"), responder("High history")
        history._scores.update({a.name: 0.26, b.name: 1.0})
        clock = FakeClock()
        with patch.object(availability, "available_for", return_value=[a, b]), patch.object(
            availability, "travel_time_minutes", return_value=10
        ), patch.object(offer, "OFFER_TIMEOUT_SECONDS", 90), patch.object(
            offer.time, "time", clock.time
        ), patch.object(offer, "push_to_device") as push, patch.object(
            offer, "poll_device", return_value=offer.TAKEN
        ), patch.object(offer, "withdraw_from_device"):
            self.assertIs(offer.dispatch(callout()), b)
            self.assertEqual(push.call_count, 1)
            self.assertIs(push.call_args.args[0], b)
            self.assertAlmostEqual(history.recent_acceptance(a), 0.26)
        RESULTS["timeout_restoration_limit"] = {
            "timeout": 90, "low_history_still_unoffered": True,
            "low_history_score": 0.26,
            "scope": "Controlled two-candidate case; restoring time alone does not reset existing history."}


if __name__ == "__main__":
    log = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MechanismTests)
    outcome = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    evidence = MODULE / "evidence"
    evidence.mkdir(exist_ok=True)
    replay = RESULTS.pop("fixed_sequence_replay", None)
    if replay is not None:
        (evidence / "fixed-sequence-replay.json").write_text(
            json.dumps(replay, indent=2) + "\n", encoding="utf-8")
    output = {"tests_run": outcome.testsRun, "failures": len(outcome.failures),
              "errors": len(outcome.errors), "successful": outcome.wasSuccessful(),
              "python": sys.version.split()[0], "source_sha256": SOURCE_BEFORE,
              "source_unchanged": SOURCE_BEFORE == {
                  n: hashlib.sha256((SOURCE / n).read_bytes()).hexdigest() for n in SOURCE_NAMES},
              "controlled_cases": RESULTS,
              "log": log.getvalue(),
              "scope": "Actual teaching source with mocked omitted adapters. Controlled mechanism validation, not deployed-system root-cause certification."}
    (evidence / "mechanism-validation.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(log.getvalue(), end="")
    print(json.dumps({k: output[k] for k in ["tests_run", "failures", "errors", "successful", "source_unchanged"]}))
    sys.exit(0 if outcome.wasSuccessful() else 1)

