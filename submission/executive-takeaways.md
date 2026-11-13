# Dispatch acceptance improved while four responders lost offers

Six-module executive review · 12 November 2026  
Rook Industries is a fictional Product School teaching scenario.

Acceptance rose from 54.2% in release week to 72.7% in the final week, approaching the 76.8% baseline. Over the same period, four responders nearly stopped receiving offers. Their combined offers fell from a baseline average of 49 per week to three in the final week.

**Recommendation:** keep the investigation open. Validate the proposed recovery process with engineering and customers. Before a production pilot, confirm responder eligibility, test Supply's maintenance integration and agree success measures and conditions for stopping the pilot.

## 1 · Origin Story: the handover left key claims unverified

Priya attributed the decline to seasonality and discouraged rollback without providing evidence of recovery or criteria for reconsidering the decision. Availability Confidence appeared on the roadmap, but its delivery status was unconfirmed. Supply also depended on Dispatch's availability record for maintenance scheduling.

**Action:** confirm what shipped, who owns outstanding commitments and what evidence would justify a change. Identify the Supply owner before changing shared availability data.

[Handover findings and questions](../01-origin-story/extra-practice/practice-review.md)

## 2 · Super Hearing: customers reported lost offers and difficulty answering

Four interviews and 147 support tickets described disappearing offers, quiet phones and uneven workloads. The daily ticket filing rate rose about 4.4 times after 12 August. Of 105 post-release tickets, 44 concerned missing, reduced or disappearing offers. Repeat reports contributed to that total; it does not represent 44 separate customers.

**Action:** investigate offer delivery and allocation alongside console usability. Use the interviews to understand the experience and the tickets to identify recurring problems. Neither source alone establishes the cause.

[Interview and ticket comparison](../02-super-hearing/interviews-vs-tickets.md)

## 3 · Rewind: the overall acceptance rate concealed large differences between responders

The analysis covered 1,696 pings, 1,319 incidents and all 160 responder-week records. Farlight, Vesper, The Undertow and Meteor Mite made up 25% of the roster but received only 1.8% of final-week offers, down from 28.4% during baseline. None took a callout in the final two weeks.

Weekly incident demand fell 11.1%, while their weekly offers fell 83.0% across the full post-release weeks. Demand alone does not explain the difference. Historical eligibility and availability records are missing, so the analysis cannot establish how many offers each responder should have received.

**Action:** report offers by responder, periods without offers and incident assignment outcomes alongside acceptance. Churn and revenue effects have not been measured.

[Analysis and supporting records](../03-rewind/decision-brief.md)

## 4 · X-Ray Vision: a missed offer can lower future priority without a timed recovery

In a controlled test, a responder answering after 75 seconds succeeds with a 90-second window and misses with 60 seconds. The supplied code subtracts 0.12 from history for both a missed offer and an explicit refusal; taking a callout adds 0.08. History contributes 25% of routing score and has no implemented time-based recovery while retained. A responder can remain available yet receive no offer because someone ranked above accepts first.

Sixteen controlled tests reproduced this behavior. Historical scores, eligibility and delivery logs are missing, so the tests cannot attribute every lost offer to it.

**Action:** review the response window, treatment of missed offers and recovery from low scores separately. Restoring 90 seconds would leave existing history unchanged.

[Code findings and possible changes](../04-x-ray-vision/decision-brief.md)

## 5 · Super Speed: the prototype shows how a responder could request review

Dispatch Ready Review lets a handler request review, a responder confirm readiness and operations check availability, capability, region, travel and maintenance. It proposes one suitable offer within a two-hour review window, using a 90-second demo offer. Expiry, changed circumstances or a responder pause can stop the process.

All 23 recorded browser checks passed. The review and offer windows are proposals. The prototype simulates the process; its effect on actual offers and incident assignment has not been tested.

**Action:** test the process with customers and engineering. Set numeric targets, check assignment delays and verify Supply integration before a production pilot.

[Product brief](../05-super-speed/brief.md) · [Prototype](../05-super-speed/prototype.html) · [Validation](../05-super-speed/validation.md)

## 6 · Sidekicks: repeated review found four unresolved brief problems

The review-checklist skill checks ownership, success measures, consistent scope and whether the problem is explained before the fix. Two manual reviews found the same four issues: Bulk Callout lacks an owner; Routing Override Audit Log lacks a success measure; Approval Chains expands scope; Handler Phone App proposes an app before establishing the problem.

The second run reported no changed issues. A weekly review is configured; its first future scheduled execution has not been verified.

**Action:** resolve the four decisions before committing delivery. Use later reviews to report changed findings and access failures while retaining the last complete review when sources cannot be read.

[Second review](../06-sidekicks/reviews/manual-2-2026-11-12.md) · [Review skill](../.agents/skills/review-checklist/SKILL.md)

## Proposed responsibilities

- **Helen / Product:** approve the pilot's scope, policy and stopping conditions; reconcile outstanding roadmap commitments.
- **Ravi / Data:** define offer measures that account for eligibility, assignment time and incident take rate; agree success and stop thresholds.
- **Marcus and Wen / Engineering:** confirm eligibility checks and deployed routing behavior; specify how scores recover and test the effect of response-window changes.
- **Supply owner, still to identify:** verify that the proposal preserves availability data and maintenance scheduling behavior.
- **Nadia and Sofia:** test whether handlers and responders understand the process and whether operations can manage the work it adds.
