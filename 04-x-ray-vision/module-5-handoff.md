# Module 5 design handoff

Product direction: make readiness, missed offers and a return to routing understandable and actionable for handlers and independent responders.

This handoff is input to the next module's product brief and prototype. It does not implement a service change or predetermine an approved scoring policy.

## Problem and intended outcome

A willing responder can miss a short offer window, lose history points, move down future rankings and lose the very opportunities required to recover. Handlers can see a quiet phone without understanding whether readiness, eligibility, delivery or ranking is responsible.

Deliver an explainable route back for an eligible, ready responder while protecting prompt incident assignment and the quality of the capability match. Successful recovery means restored appropriate opportunity and reliable response, not a cosmetically higher acceptance ratio.

## Core scenario

Use Meteor Mite and Kip for the prototype, with The Gale as the same-area contrast. Keep actual Module 3 facts separate from illustrative UI state: Mite's post weeks contain 4, 2 and 1 offers; Gale's contain 17, 20 and 21. Historical eligibility, delivery times and production scores are unobserved. Any score or reason shown beyond verified data must be labeled simulated.

The handler needs a clear account of recent offers, missed versus declined outcomes, readiness status and what action can be requested. The responder needs a usable offer experience and a bounded way to confirm readiness or request review after a quiet stretch.

## Decisions for the brief

- What qualifies a responder for review: observed loss of offers plus explicit readiness and eligibility evidence.
- How missed differs from deliberate decline in the proposed policy.
- Whether window containment, a better response interaction or both are required.
- How retained score damage is addressed: approved recovery event, calibrated aging, supervised reset or bounded opportunity. Show tradeoffs rather than silently granting work.
- Which parts are visible to a handler, which belong to the responder, and what requires an operational review.

## Prototype acceptance criteria

1. Kip can inspect Mite's recent offer history and distinguish missed, declined, taken and no-offer periods.
2. A quiet period triggers an explainable review path; it does not automatically mark Mite unavailable.
3. A responder can confirm readiness or request review without claiming a guaranteed incident assignment.
4. Missed is not presented as proof of refusal; delivery/answer gaps are stated honestly.
5. A recovery action shows its scope, status and an audit event; it does not silently overwrite history or readiness.
6. Any proposed re-entry respects capability, urgency, region and travel-time constraints.
7. Headline acceptance is paired with responder opportunity and incident assignment measures.
8. The interface preserves the shared availability contract; Supply implications and the unverified hard capability gate are explicit engineering dependencies.
9. Include a 75-second controlled response example to explain the 90-versus-60 window effect, clearly marked illustrative.
10. The experience is a working handler/responder flow, not merely a switch that changes a timeout number.

## Validation and rollout gates

Before a service change: agree policy with Helen; review behavior and rollout with Marcus/Wen; establish hard eligibility and Supply integration; obtain timing/ranking telemetry; review customer explanation with Nadia/Sofia; define metrics and abort criteria with Ravi.

Track eligible opportunity and time since last offer alongside missed/declined mix, callout take rate and dispatch latency. The current extract cannot measure eligibility-adjusted exposure or median time-to-accept. Do not present a synthetic prototype scorecard as a verified production dashboard.

## Evidence

[Module 4 mechanism](routing-mechanism.md), [controlled tests](evidence/mechanism-validation.json), [Module 3 analysis](../03-rewind/metrics-analysis.md), and the director's existing [Module 5 request](../05-super-speed/director-request.txt).

