# Dispatch service access requires investigation

Executive decision brief · Module 3 · 12 November 2026  
Evidence covers 29 June–6 September 2026 in this fictional course scenario.

**Recommendation:** keep the 4.2 service investigation open and prioritize responder access to callouts. A recovering aggregate acceptance rate is insufficient evidence of service recovery.

## What the records establish

Acceptance is 76.8% across six baseline weeks, falls to 54.2% in release week, and reaches 72.7% in the final week. Meanwhile four responders receive just three offers combined in that final week, down from a baseline average of 49 offers per week. None takes a callout in either of the final two weeks.

| Responder | Baseline offers/week | Final-week offers | Final-week taken |
| --- | ---: | ---: | ---: |
| Farlight | 12.0 | 0 | 0 |
| Vesper | 13.8 | 1 | 0 |
| The Undertow | 12.0 | 1 | 0 |
| Meteor Mite | 11.2 | 1 | 0 |

These four constitute 25% of the roster but receive 1.8% of final-week offers, versus 28.4% of baseline offers. This is an exposure failure to investigate; their historical eligibility and availability cannot be verified from the available schema.

## Why this matters commercially and operationally

Dispatch sells dependable access to relevant callouts and reliable responder coordination. A headline that improves as struggling customers receive fewer offers is an incomplete operating measure. Lost opportunity and the risk of disengagement deserve attention; neither churn nor financial loss is measured here.

General demand does soften: incidents average 139.5 per week before release week and 124 afterward, an 11.1% reduction. But the four affected responders' offers fall 83.0% per week while the other twelve's rise 24.3%. Home-area demand falls only 1.4–14.3%; these areas are contextual demand proxies, not verified eligibility pools.

The ticket queue alone identified a different four: Farlight, The Undertow, Corporal Ashgrove and Halfmoon. The latter two decline moderately rather than approaching zero. Interviews supplied the missing leads: Aunt Dot described Vesper's quiet stretches, and Kip contrasted Meteor Mite with The Gale. Metrics therefore refine the escalation list rather than merely confirming the loudest complaints.

## Decisions and owners to propose

- **Helen / Product:** require responder-level access measures alongside aggregate acceptance before declaring recovery; keep urgent Supply concerns on their own escalation path.
- **Marcus and Wen / Engineering:** trace eligibility, ranking and the handling of missed pings for the four; investigate the shorter timeout and acceptance-history interaction in Module 4. A causal finding and rollout decision require that work.
- **Ravi / Data:** publish offers, outcomes, zero-offer weeks and time since last offer by responder, together with incident demand and callout take rate. Retrieve historical availability/eligibility and answer-time evidence.
- **Nadia and Sofia / customer evidence:** reconcile the affected responders' accounts, validate readiness with handlers, and distinguish notification visibility from allocation loss. These are proposed follow-ups; no messages have been sent.

**Release discipline:** the evidence supports urgent investigation and targeted validation. It does not yet justify a specific configuration change, establish that seasonality caused the pattern, or prove that the timeout caused the loss of offers.

[Full analysis and limitations](metrics-analysis.md) · [Executed queries](queries.sql) · [Evidence manifest](evidence/manifest.json)

