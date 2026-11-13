# Module 3 completed

Completed 12 November 2026 for the fictional Rook Dispatch coursework.

The investigation verified the available metrics, challenged the aggregate recovery narrative and corrected the affected-responder priority list. It does not claim a proven implementation cause.

## Deliverables

- [Executive decision brief](decision-brief.md): decision recommendation, verified business impact, proposed owners and evidence limits.
- [Metrics analysis](metrics-analysis.md): all ten weeks, all sixteen responders, zero-inclusive offer matrix, customer-evidence reconciliation, exact-date sensitivity and Module 4 handoff.
- [Visual scorecard](metrics-trends.png): headline acceptance alongside exposure of the four affected responders.
- [Executed read-only SQL](queries.sql): extraction, grouping, joins and source-quality checks.
- [Evidence manifest](evidence/manifest.json): definitions, local-time semantics, comparison windows and limitations.
- [Validation results](evidence/validation.json): ten passed reconciliation/quality checks.
- [Original prompt](prompts.md): the user's Module 3 instruction, preserved verbatim.

The evidence folder also contains all 1,696 ping rows, 1,319 incident rows, the 16-responder roster, 160 responder-week cells and derived summaries. The complete datasets were paginated below the 1,000-row connector limit.

## Completion criteria

- [x] Retrieve and account for every available ping and incident.
- [x] Recompute weekly and pooled acceptance with explicit denominators.
- [x] Keep the mixed release week separate and test exact date cutoffs.
- [x] Retain zero-offer responder-weeks and examine every responder.
- [x] Compare responder exposure with incident demand and home-area context.
- [x] Reconcile SQL outputs with independent raw-record aggregation.
- [x] Triangulate interview and ticket leads, correcting the severe-cohort priority list.
- [x] Document evidence gaps and traceable questions for Module 4.
- [x] Save the original prompt, findings and visual evidence within the course repo.

## Reproduce the visual

From the course root in PowerShell:

```powershell
& '.\03-rewind\render-metrics.ps1'
```

This uses the Windows .NET charting library and the saved evidence files. No additional package install is needed.

The dataset ends on 6 September; findings refer to this historical scenario window. Module 4 is the next gate for validating the technical mechanism and choosing an intervention.
