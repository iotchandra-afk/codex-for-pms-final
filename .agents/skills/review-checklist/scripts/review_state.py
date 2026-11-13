"""Validate review evidence and maintain a complete, low-noise baseline.
Semantic judgments are made by the review-checklist skill, not by this helper.
All inputs/outputs are confined to this repository's Module 6 artifacts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = ROOT / "06-sidekicks"
CRITERIA = ("owner_named", "success_measure", "scope_bounded", "problem_before_solution")

def artifact_path(value):
    path = (ROOT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    if not path.is_relative_to(ARTIFACTS.resolve()):
        raise ValueError("Review input/output must stay under 06-sidekicks.")
    if path.suffix.lower() != ".json":
        raise ValueError("Review artifacts must be JSON files.")
    return path

def normalized(text):
    return re.sub(r"\s+", " ", text).strip()

def atomic_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)

def inspect(report):
    required = ("run_id", "run_type", "reviewed_at", "complete", "expected_ids", "briefs")
    if any(k not in report for k in required):
        raise ValueError("Missing report metadata.")
    if report["run_type"] not in ("manual", "scheduled") or type(report["complete"]) is not bool:
        raise ValueError("Invalid run type or completeness.")
    if not isinstance(report["expected_ids"], list) or not report["expected_ids"]:
        raise ValueError("Empty or invalid source index cannot establish a clean review.")
    if len(set(report["expected_ids"])) != len(report["expected_ids"]):
        raise ValueError("Duplicate IDs in source index.")
    seen, flags, sources, unknown = set(), {}, {}, []
    for brief in report["briefs"]:
        for field in ("id", "title", "url", "source_text", "checks"):
            if field not in brief:
                raise ValueError("Missing brief field: " + field)
        identity = brief["id"]
        if identity in seen:
            raise ValueError("Duplicate brief ID: " + identity)
        seen.add(identity)
        text = brief["source_text"]
        if not isinstance(text, str) or not text.strip():
            raise ValueError("A reviewed brief needs actual source text.")
        if set(brief["checks"]) != set(CRITERIA):
            raise ValueError("Every brief needs exactly four check results.")
        sources[identity] = {"title": brief["title"], "url": brief["url"],
                            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
        for criterion in CRITERIA:
            check = brief["checks"][criterion]
            status = check.get("status")
            if status not in ("pass", "flag", "unknown"):
                raise ValueError("Invalid check status.")
            if not check.get("reason"):
                raise ValueError("Each judgment needs a reason.")
            excerpts = check.get("evidence", [])
            if status != "unknown" and (not excerpts or not check.get("section")):
                raise ValueError("Pass/flag needs quoted evidence and a section.")
            for quote in excerpts:
                if not isinstance(quote, str) or not normalized(quote) or normalized(quote) not in normalized(text):
                    raise ValueError("Excerpt not found in source: " + identity + "/" + criterion)
            if status == "unknown":
                unknown.append(identity + ":" + criterion)
            if status == "flag":
                if not check.get("business_impact") or not check.get("next_action"):
                    raise ValueError("Flag needs business impact and next action.")
                key = identity + ":" + criterion
                fingerprint = hashlib.sha256(json.dumps(
                    [criterion, sorted(normalized(q) for q in excerpts)], ensure_ascii=False
                ).encode("utf-8")).hexdigest()
                flags[key] = {"source_id": identity, "title": brief["title"], "url": brief["url"],
                              "criterion": criterion, "evidence": excerpts, "reason": check["reason"],
                              "business_impact": check["business_impact"], "next_action": check["next_action"],
                              "fingerprint": fingerprint}
    missing = sorted(set(report["expected_ids"]) - seen)
    unexpected = sorted(seen - set(report["expected_ids"]))
    complete = report["complete"] and not missing and not unexpected and not unknown and not report.get("access_errors")
    return complete, flags, sources, {"missing": missing, "unexpected": unexpected, "unknown": unknown,
                                     "access_errors": report.get("access_errors", [])}

def apply_report(report_path, state_path, delta_path):
    if len({report_path, state_path, delta_path}) != 3:
        raise ValueError("Report, baseline and delta must be separate files.")
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    complete, flags, sources, gaps = inspect(report)
    previous = json.loads(state_path.read_text(encoding="utf-8-sig")) if state_path.exists() else None
    previous_delta = json.loads(delta_path.read_text(encoding="utf-8-sig")) if delta_path.exists() else {}
    base = {"run_id": report["run_id"], "run_type": report["run_type"], "reviewed_at": report["reviewed_at"],
            "complete": complete, "brief_count": len(sources), "flag_count": len(flags)}
    if not complete:
        failure_fingerprint = hashlib.sha256(json.dumps(gaps, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        delta = {**base, "status": "incomplete",
                 "should_surface": previous_delta.get("failure_fingerprint") != failure_fingerprint,
                 "failure_fingerprint": failure_fingerprint, "baseline_preserved": True,
                 "new": [], "changed": [], "resolved": [], "removed_sources": [], "gaps": gaps}
        atomic_json(delta_path, delta)
        return delta
    old_flags = previous.get("flags", {}) if previous else {}
    old_sources = previous.get("sources", {}) if previous else {}
    removed = sorted(set(old_sources) - set(sources))
    new_keys = sorted(set(flags) - set(old_flags))
    changed_keys = sorted(k for k in set(flags) & set(old_flags) if flags[k]["fingerprint"] != old_flags[k]["fingerprint"])
    resolved_keys = sorted(k for k in set(old_flags) - set(flags) if old_flags[k]["source_id"] in sources)
    delta = {**base, "status": "baseline_created" if previous is None else
             "changed" if new_keys or changed_keys or resolved_keys or removed else "unchanged",
             "should_surface": bool(new_keys or changed_keys or resolved_keys or removed or previous_delta.get("status") == "incomplete"),
             "access_restored": previous_delta.get("status") == "incomplete",
             "baseline_preserved": False, "new": [flags[k] for k in new_keys],
             "changed": [flags[k] for k in changed_keys],
             "resolved": [old_flags[k] for k in resolved_keys],
             "removed_sources": [{"id": k, **old_sources[k]} for k in removed]}
    baseline = {"schema_version": 1, "last_complete_run": report["run_id"],
                "reviewed_at": report["reviewed_at"], "sources": sources, "flags": flags}
    atomic_json(state_path, baseline)
    atomic_json(delta_path, delta)
    return delta

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report")
    parser.add_argument("--state", default="06-sidekicks/review-state.json")
    parser.add_argument("--delta", default="06-sidekicks/reviews/latest-delta.json")
    args = parser.parse_args()
    try:
        delta = apply_report(artifact_path(args.report), artifact_path(args.state), artifact_path(args.delta))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, "Review state was not updated: " + str(exc) + "\n")
    print(json.dumps({"status": delta["status"], "briefs": delta["brief_count"], "flags": delta["flag_count"],
                      "should_surface": delta["should_surface"], "baseline_preserved": delta["baseline_preserved"]}))
    return 0 if delta["complete"] else 1

if __name__ == "__main__":
    raise SystemExit(main())

