# Prototype validation

Module 5 · 12 November 2026 · Fictional Rook Dispatch

**Result: 23 browser checks passed, 0 failed, 0 page/console errors, 0 external prototype page requests.** The exact results are in [prototype-validation.json](evidence/prototype-validation.json).

## Acceptance coverage

| Module 4 requirement | Implemented experience | Browser evidence |
| --- | --- | --- |
| Distinguish offers, taken, declined, missed and quiet periods | Verified Mite/Gale trend and seven-event history | Checks 01,19; historical events matched to Module 3 source |
| Make the quiet period actionable | Handler review entry and linked role workspaces | Checks 02–04,23 |
| Responder readiness without guaranteed allocation | Explicit acknowledgement, confirmation, scoped review and pause | Checks 04,06,21,22 |
| Keep missed distinct from refusal | Separate timeout, decline and withdrawn states | Checks 08,09,11,22 |
| Give actions scope and a receipt | Bounded review, note, audit entries, one demo offer | Checks 06,12,13,16 |
| Respect availability/capability/region/travel/maintenance | Five blocking checks; changed fit pauses or withdraws | Checks 03,05,10,11 |
| Pair acceptance with access and incident assignment | Historical 72.7% acceptance, three offers to the affected four and 94.5% callout take rate | Check 20; figures remain historical after demo actions |
| Preserve readiness/history boundaries | Immutable historical data and availability fixture | Checks 13,18,21,22 |
| Explain the controlled 75-second case | Visible 60-versus-90 comparison and live illustrative offer | Checks 07,14 |
| Deliver a working journey, not just a setting | Request → confirmation → review → offer → outcome → receipt | Checks 06–13 |
| Keyboard and mobile usability | Keyboard workspace tabs, 390px responsive layout, early mobile action | Checks 15,17,23 |

Checks establish prototype behavior. They do not validate real eligibility, actual Supply scheduling, live device delivery or production effectiveness.

## Visual inspection

Inspected the final renders at desktop and mobile sizes:

- [Handler desktop](evidence/handler-desktop.png)
- [Operations review](evidence/operations-review.png)
- [Responder live offer](evidence/responder-live.png)
- [Handler mobile](evidence/handler-mobile.png)

The mobile review entry is available before scrolling; all three workspaces fit a 390px viewport. The final layouts have no detected horizontal overflow or clipped controls. The mobile screenshot is a full-page capture, not an indication that every section fits on one phone screen.

## Iterations completed

The first 18 browser journeys passed. Review then added a paired service scorecard, early mobile review entry, and responder withdrawal/reconfirmation. Five further checks cover these changes; all 23 pass after the refinements.

A sandboxed headless-browser launch initially failed before any tests ran. Running the same harness with desktop process permission resolved that environment issue. The saved final evidence records the successful run.

The preview was separately verified to return HTTP 200 on localhost. The headless end-to-end checks use the exact standalone HTML file, which has inline styles/scripts and no remote dependencies.

## Rollout decisions still required

- Helen: approve scope, pilot policy and the proposed review/offer windows.
- Marcus/Wen: define recovery-state semantics and verify the hard eligibility gate, delivery/answer timing and rollout/rollback behavior.
- Supply owner: test the real shared availability contract and maintenance implications.
- Ravi: baseline eligibility-adjusted exposure and set numeric pilot/abort thresholds.
- Nadia/Sofia: validate wording, agency, operational workload and the handler/responder journey.

These are proposed assignments, not messages sent to colleagues. Prototype completion is separate from launch approval.

