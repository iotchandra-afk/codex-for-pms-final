# Module 6 completed

Completed 12 November 2026 for the fictional Rook coursework. The reusable skill, two actual source-backed manual reviews, complete baseline, active weekly workflow and root [final presentation](../final-report.html) are in place. The first future scheduled execution remains an operational follow-up; the official assignment requires two runs and a schedule.

The operating purpose is to catch weak commitments before they become delivery commitments: work without an accountable owner, an observable outcome, a release boundary or a demonstrated customer problem.

## Use the review

Invoke **$review-checklist** in this course folder, or ask: “Use $review-checklist to review the current Product briefs in Rook's wiki, show source evidence and compare with the last complete review.” The [skill](../.agents/skills/review-checklist/SKILL.md) also accepts selected local briefs; keep them inside this repo.

It reads the current source index and every current brief, then checks ownership, success measure, bounded scope and problem-first framing. It discovers new briefs on subsequent runs. An identifiable accountable team or role can satisfy ownership. A missing baseline remains a follow-up when the brief already identifies a real measure. Exploration ownership does not establish build staffing.

## First review: decisions to resolve

All four current briefs were read in full; the 16 judgments have exact supporting excerpts. There is one flag per brief.

| Brief | Decision gap | Recommended next action |
| --- | --- | --- |
| Bulk Callout | No accountable owner | Assign an owner or explicitly defer the commitment. |
| Requisition Approval Chains | A second approval grows into several workflows | Agree the first release boundary with the Supply owner. |
| Routing Override Audit Log | Logging features have no success measure | Define how support will establish that an override is traceable. |
| Handler Phone App | Opens with an app before establishing the problem | Lead with missed handler awareness and justify the proposed response. |

The [initial review](reviews/manual-2026-11-12.md) contains quotations, business consequences and follow-ups. The [full JSON report](reviews/manual-2026-11-12.json) retains every judgment and source text; [source snapshots](reviews/sources/) preserve the pages read. The source assigns Approval Chains to **the Rook Supply team**; a stakeholder's name in the supplied example is not evidence of ownership.

The [second actual review](reviews/manual-2-2026-11-12.md) reread all four current pages under the revised skill. All 16 checks were rejudged; the same four flags produced an unchanged, quiet delta. The two complete manual runs demonstrate the required repetition without claiming either was a scheduler trigger. [Revised-skill validation](evidence/revised-skill-validation.json) records the exact skill hash.

## Scheduled workflow

**Rook product brief review** is ACTIVE in this course chat, automation ID `rook-product-brief-review`. It is scheduled for **Mondays at 08:00 in the application's local time**. Chicago is the intended user timezone. The accepted API response does not independently expose the timezone or next-run timestamp; the first expected date is 16 November 2026 if the app uses Chicago time. No future execution is claimed.

The [scheduled prompt](scheduled-review-prompt.md) instructs the run to discover and reread the current wiki briefs, save a uniquely dated report and source snapshots, and use the [state helper](../.agents/skills/review-checklist/scripts/review_state.py). The [automation record](automation.json) records the active ID, recurrence interpretation, evidence and verification limits. Editing that record does not change the live schedule; change or stop the workflow through the app's automation controls.

Each complete run compares against [the last complete baseline](review-state.json). New or changed flags, resolutions, removed sources and access failure/recovery are surfaced. An unchanged successful review stays quiet. A removed page is not treated as a resolved issue. An incomplete review preserves the complete baseline, and repeated identical access failures do not repeat the same alert.

For local-folder work, keep the computer on, the app running, and the repo and wiki connection available. This follows the [official automation runtime guidance](https://learn.chatgpt.com/docs/automations?surface=app). The skill stays in the repo's `.agents/skills/` location described in the [official skill guidance](https://learn.chatgpt.com/docs/build-skills).

## Evidence and maintenance

- [Validation report](validation.md): structural validation, semantic review and state-transition coverage.
- [State tests](test_review_state.py): 18 passing checks; the runtime helper uses only Python's standard library.
- [Skill validation evidence](evidence/skill-validation.json) and [state validation evidence](evidence/review-state-validation.json).
- [Latest delta](reviews/latest-delta.json): machine-readable changes from the latest processed review.

Reproduce state tests from the course root with Python 3:

```powershell
python -B 06-sidekicks/test_review_state.py
```

Source review requires human/assistant judgment. The helper validates exact excerpt provenance and state transitions; passing it does not prove a judgment is correct. It does not edit wiki briefs or send messages. Keep any later review artifacts in this course folder.

The provided `scheduled-run-output.txt` remains an unchanged teaching example. The actual completed run is the manual review above. All six practical modules now have local deliverables; see [course completion](../COURSE-COMPLETION.md) for what remains outside the exercises.
