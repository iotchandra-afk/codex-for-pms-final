"""Audit actual assignment artifacts and evidence; never assign an instructor grade."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone
import collections
import hashlib
import importlib.util
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
BASELINE = "859ca5b"
results = []


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def check(name, fn):
    try:
        detail = fn()
        results.append({"name": name, "passed": True, "detail": detail})
    except Exception as error:
        results.append({"name": name, "passed": False, "error": str(error)})


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def git_text(path):
    return subprocess.run(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT,
                          capture_output=True, encoding="utf-8", check=True).stdout


def slots(text):
    return [s.strip() for s in re.split(r"^### \d+\.\s*$", text, flags=re.M)[1:] if s.strip()]


def required_artifacts():
    paths = ["AGENTS.md", "final-report.html", "05-super-speed/brief.md",
             "05-super-speed/prototype.html", ".agents/skills/review-checklist/SKILL.md",
             "02-super-hearing/interview-analysis.md", "02-super-hearing/interviews-vs-tickets.md",
             "03-rewind/evidence/pings.json", "04-x-ray-vision/routing-mechanism.md"]
    require(all((ROOT / p).is_file() for p in paths), "Required artifact missing")
    require((ROOT / "00-rook/company/notes/handoff-from-priya.docx").is_file(), "Original handover missing")
    return {"required_files": len(paths), "original_scenario": "present"}


def context_scope():
    old = git_text("AGENTS.md")
    now = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    require(old.split("\n---\n", 1)[0] == now.split("\n---\n", 1)[0], "Session scope changed")
    require(len(now.split()) <= 750, "Context exceeds the compact submission budget")
    archived = (ROOT / "01-origin-story/working-context-history.md").read_text(encoding="utf-8")
    require(old.split("## Working context", 1)[1].lstrip() in archived, "Prior context lost")
    return {"scope": "unchanged", "words": len(now.split()), "history": "preserved"}


def original_prompts():
    counts = {}
    for folder in sorted(ROOT.glob("0[1-6]-*")):
        rel = f"{folder.name}/prompts.md"
        old = slots(git_text(rel))
        current = slots((ROOT / rel).read_text(encoding="utf-8-sig"))
        require(current and current[:len(old)] == old, f"Original prompts changed: {rel}")
        require(len(current) == len(set(current)), f"Duplicate prompts: {rel}")
        counts[folder.name] = len(current)
    require(len(counts) == 6, "Six prompt libraries required")
    return counts


def interview_provenance():
    coding = load("02-super-hearing/evidence/interview-coding.json")
    sources = {s["key"]: (ROOT / "02-super-hearing" / s["snapshot"]).read_text(encoding="utf-8-sig")
               for s in coding["sources"]}
    require(len(sources) == coding["source_count"] == 4, "Interview coverage incomplete")
    positives = 0
    for theme in coding["themes"]:
        require(theme["denominator"] == 4 and theme["count"] == len(theme["evidence"]), "Theme count mismatch")
        for key, quote in theme["evidence"].items():
            require(quote in sources[key], f"Unsupported interview quote: {theme['id']}/{key}")
            positives += 1
    counts = {t["id"]: t["count"] for t in coding["themes"]}
    require(counts["offer_expires"] == 3 and counts["quiet_uneven"] == 2 and counts["handler_awareness"] == 3,
            "Headline interview counts changed")
    return {"interviews": 4, "themes": len(coding["themes"]), "positive_cells_with_exact_quotes": positives}


def ticket_classification():
    rows = load("02-super-hearing/evidence/support-tickets.json")
    by_id = {r["ticket_number"]: r for r in rows}
    require(len(rows) == len(by_id) == 147, "Incomplete or duplicate tickets")
    require(set(by_id) == set(range(3001, 3148)), "Ticket identity gap")
    classified, groups = [], 0
    text = (ROOT / "02-super-hearing/support-ticket-classification.md").read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        parts = line.split("|")
        if len(parts) > 4 and parts[2].strip().isdigit():
            count = int(parts[2].strip())
            ids = [int(i) for i in re.findall(r"#(\d{4})", parts[4])]
            require(count == len(ids), "Classification count differs from ticket list")
            quote = re.search(r"“(.*)”", parts[3]).group(1)
            representative = int(re.search(r"#(\d{4})", parts[3]).group(1))
            require(quote in by_id[representative]["body"], f"Unsupported quote #{representative}")
            classified.extend(ids)
            groups += 1
    require(groups == 56 and len(classified) == len(set(classified)) == 147, "Primary classifications do not reconcile")
    require(set(classified) == set(by_id), "Unclassified tickets")
    periods = collections.Counter("before" if r["filed_at"][:10] < "2026-08-12" else
                                  "after" if r["filed_at"][:10] > "2026-08-12" else "release_day" for r in rows)
    require(dict(periods) == {"before": 40, "release_day": 2, "after": 105}, "Filing-window counts differ")
    return {"tickets": 147, "specific_groups": groups, "periods": dict(periods), "representative_quotes_verified": groups}


def source_comparison():
    rows = load("02-super-hearing/evidence/support-tickets.json")
    interview_responders = {"Vesper", "Captain Vantage", "Sgt. Bulwark", "Meteor Mite", "The Gale"}
    overlap = interview_responders & {r["about_responder"] for r in rows}
    require(overlap == {"Captain Vantage"}, "Responder sample overlap differs")
    text = (ROOT / "02-super-hearing/interviews-vs-tickets.md").read_text(encoding="utf-8-sig")
    verified = 0
    for line in text.splitlines():
        if line.startswith("|") and "“" in line:
            quote = re.search(r"“(.*?)”", line).group(1)
            ids = [int(i) for i in re.findall(r"#(\d{4})", line)]
            require(any(quote in next(r["body"] for r in rows if r["ticket_number"] == i) for i in ids),
                    "Unsupported comparison quote: " + quote)
            verified += 1
    return {"overlapping_responders": sorted(overlap), "comparison_ticket_quotes_verified": verified}


def metric_reconciliation():
    pings = load("03-rewind/evidence/pings.json")
    callouts = load("03-rewind/evidence/callouts.json")
    grid = load("03-rewind/evidence/responder-weeks.json")
    require(len(pings) == 1696 and len(callouts) == 1319, "Raw row counts differ")
    require(len(grid) == len({(r["week_start"], r["responder"]) for r in grid}) == 160, "Roster-week grid incomplete")
    require(sum(r["pings"] for r in grid) == len(pings), "Grid does not reconcile to raw pings")
    require(all(r["pings"] == r["taken"] + r["turned_down"] + r["missed"] for r in grid), "Outcomes do not reconcile")
    zero = [r for r in grid if r["pings"] == 0]
    require(zero and all(r["acceptance_pct"] is None for r in zero), "Zero-offer acceptance must remain undefined")
    severe = {"Farlight", "Vesper", "The Undertow", "Meteor Mite"}
    baseline = [r for r in grid if r["responder"] in severe and r["week_start"] < "2026-08-10"]
    final = [r for r in grid if r["responder"] in severe and r["week_start"] == "2026-08-31"]
    require(sum(r["pings"] for r in baseline) / 6 == 49 and sum(r["pings"] for r in final) == 3,
            "Headline cohort numbers differ")
    return {"pings": len(pings), "callouts": len(callouts), "responder_weeks": len(grid), "baseline_offers_per_week": 49, "final_week_offers": 3}


def original_code():
    record = load("04-x-ray-vision/evidence/mechanism-validation.json")
    for name, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / "00-rook/code/dispatch-routing" / name).read_bytes()).hexdigest()
        require(actual == expected, "Routing source changed: " + name)
    return {"unchanged_source_files": len(record["source_sha256"])}


def recorded_validation():
    data = load("03-rewind/evidence/validation.json")
    require(len(data) == 10 and all(c["passed"] for c in data), "Metric check failure")
    outputs = {}
    for module, rel, count in [("mechanism", "04-x-ray-vision/evidence/mechanism-validation.json", 16),
                               ("prototype", "05-super-speed/evidence/prototype-validation.json", 23),
                               ("review_state", "06-sidekicks/evidence/review-state-validation.json", 18)]:
        data = load(rel)
        require(data["successful"] and data["tests_run"] == count, "Saved validation failure: " + module)
        outputs[module] = count
    outputs["metric_reconciliation"] = 10
    return {"saved_passing_checks": outputs, "note": "Historical records; this audit does not relabel them as fresh reruns."}


def actual_skill_runs():
    spec = importlib.util.spec_from_file_location("review_state_audit", ROOT / ".agents/skills/review-checklist/scripts/review_state.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    runs = [load("06-sidekicks/reviews/manual-2026-11-12.json"), load("06-sidekicks/reviews/manual-2-2026-11-12.json")]
    require(len({r["run_id"] for r in runs}) == 2, "Skill runs not distinct")
    for run in runs:
        helper.inspect(run)
        require(run["run_type"] == "manual" and run["complete"] and len(run["briefs"]) == 4, "Incomplete actual skill run")
    state = load("06-sidekicks/review-state.json")
    require(state["last_complete_run"] == runs[1]["run_id"], "Baseline does not reflect second complete run")
    delta = load("06-sidekicks/reviews/manual-2-2026-11-12-delta.json")
    require(delta["status"] == "unchanged" and not delta["should_surface"], "Expected quiet repeat review")
    return {"actual_manual_runs": 2, "judgments_per_run": 16, "future_scheduler_trigger": "not claimed"}


def skill_revision_and_schedule():
    validation = load("06-sidekicks/evidence/revised-skill-validation.json")
    actual = hashlib.sha256((ROOT / ".agents/skills/review-checklist/SKILL.md").read_bytes()).hexdigest()
    require(validation["successful"] and validation["skill_sha256"] == actual, "Revised skill differs from validated version")
    automation = load("06-sidekicks/automation.json")
    require(automation["status"] == automation["last_registration_verification"]["status"] == "ACTIVE", "Schedule not registered ACTIVE")
    require(automation["automation_id"] == "rook-product-brief-review", "Wrong automation identity")
    return {"skill_hash_matches": True, "schedule_registration": "ACTIVE", "timezone_and_first_trigger": "documented operational follow-ups"}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets, self.ids = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.targets.append(attrs[key])


def deliverable_links():
    parser = LinkParser()
    parser.feed((ROOT / "final-report.html").read_text(encoding="utf-8"))
    require(len(parser.ids) == len(set(parser.ids)), "Duplicate HTML anchors")
    targets = [(ROOT / "final-report.html", t) for t in parser.targets]
    for file in [ROOT / "SUBMISSION.md", ROOT / "COURSE-COMPLETION.md", ROOT / "AGENTS.md",
                 *ROOT.glob("0[1-6]-*/*.md")]:
        targets.extend((file, t) for t in re.findall(r"\]\(([^)]+)\)", file.read_text(encoding="utf-8-sig")))
    local = 0
    for file, target in targets:
        if "://" in target or target.startswith("data:"):
            continue
        if target.startswith("#"):
            if file.suffix == ".html":
                require(target[1:] in parser.ids, "Broken report anchor: " + target)
            continue
        path = (file.parent / target.split("#")[0]).resolve()
        require(path.is_relative_to(ROOT) and path.exists(), f"Missing/outside deliverable link: {file.name}: {target}")
        local += 1
    return {"local_targets_checked": local, "report_anchors": len(parser.ids)}


def assignment_and_limits():
    brief = (ROOT / "submission/assignment-brief.md").read_text(encoding="utf-8")
    report = (ROOT / "final-report.html").read_text(encoding="utf-8")
    for criterion in ("Application of Concepts", "Credibility & Reasoning", "Clarity", "Strategic Thinking"):
        require(criterion in brief and criterion.replace("&", "&amp;") in report or criterion in brief and criterion in report,
                "Rubric criterion absent: " + criterion)
    require("run twice" in brief and "final-report.html" in brief, "Actual requirement missing")
    require("No LMS submission has been made" in report, "Administrative status must be explicit")
    return {"rubric_criteria": 4, "source": "User-supplied official brief, corroborated in LMS", "grade": "Not assigned by this audit"}


for name, fn in [("Required artifacts", required_artifacts), ("Scope and compact context", context_scope),
                 ("Original prompt preservation", original_prompts), ("Interview counts and exact evidence", interview_provenance),
                 ("All ticket classifications and dated totals", ticket_classification), ("Cross-source comparison", source_comparison),
                 ("Zero-inclusive metric reconciliation", metric_reconciliation), ("Original routing hashes", original_code),
                 ("Saved validation records", recorded_validation), ("Two actual skill runs", actual_skill_runs),
                 ("Revised skill and schedule registration", skill_revision_and_schedule), ("Deliverable links", deliverable_links),
                 ("Official rubric and explicit limits", assignment_and_limits)]:
    check(name, fn)

output = {"reviewed_at": datetime.now(timezone.utc).isoformat(), "purpose": "Assignment artifact/evidence audit, not grading",
          "checks_run": len(results), "passed": sum(r["passed"] for r in results),
          "successful": all(r["passed"] for r in results), "checks": results,
          "separate_verification": {"report_browser_print": "submission/report-validation.json",
                                    "github": "Verify Public repo and matching local/remote commits after final save",
                                    "lms_submission": "Not performed", "instructor_score": "Not knowable in advance"}}
(ROOT / "submission/validation.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"checks_run": len(results), "passed": output["passed"], "successful": output["successful"],
                  "failures": [r for r in results if not r["passed"]]}, ensure_ascii=False))
raise SystemExit(0 if output["successful"] else 1)
