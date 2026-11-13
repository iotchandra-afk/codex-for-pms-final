# Submission evidence and reproduction

The [official assignment](assignment-brief.md) names four qualitative grading criteria and the required artifacts. [SUBMISSION.md](../SUBMISSION.md) maps each requirement to actual work; [final-report.html](../final-report.html) is the required final presentation.

## Verification records

- [Assignment/evidence audit](validation.json): 13 passing checks of required artifacts, original prompts, context preservation, quote provenance, ticket totals, metric reconciliation, original code hashes, actual skill runs and links.
- [Browser/print validation](report-validation.json): 16 checks of the actual final report, six verbatim prompt-result pairs, the embedded prototype journey, keyboard access, mobile/tablet overflow, embedded assets and print output.
- [Desktop capture](report-desktop.png) and [mobile capture](report-mobile.png): visually inspected for hierarchy, readability and clipping.
- [Printable report](final-report.pdf), [two-page AGENTS.md render](agents-print.pdf), and [one-page product brief render](brief-print.pdf). The original Markdown/HTML remain the authoritative editable artifacts.
- [Prompt-to-artifact map](prompt-artifact-map.json): the exact six selected user prompts, their source slots and the real artifacts paired with them. The presentation embeds the actual saved prototype unchanged and inlines its visual assets, so the story and demonstration work from one HTML file. Linked source documents still require the repo.

The existing module evidence separately records 10 metric checks, 16 controlled mechanism tests, 23 prototype browser tests and 18 review-state tests. Those are historical validation runs; the submission audit checks their records and unchanged sources without pretending to rerun all of them.

## Reproduce from the course root

```powershell
python -B submission/validate_submission.py
node submission/validate-report.cjs "<absolute path to an installed Playwright module>"
```

The browser harness uses headless Chromium or Microsoft Edge, blocks external resource requests, and keeps its profile and temporary files in this folder's ignored `.browser-temp/`. No account credentials or external service are needed for these checks. It does not submit the project to the LMS or change the recurring workflow.

The audit's baseline `859ca5b` is the earlier verified course wrap-up. It checks that original prompt wording and the session-scope block survived the hardening work. The current version of the revised skill is tied to its validation record by SHA-256.

The official brief requires **two actual skill runs and a schedule**. The two manual reviews are actual executions; the first future weekly trigger remains an operational follow-up. A supplied example output is not counted as an execution. Check counts and requirement coverage are not an instructor score.
