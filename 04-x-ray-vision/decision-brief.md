# Dispatch needs a recovery path for missed offers

Executive decision brief · Module 4 · 12 November 2026  
Fictional Rook Industries; code and controlled tests, validated against Module 3.

**Decision recommendation:** approve design of a responder readiness and recovery flow. Evaluate response-window containment separately from correcting the history policy and restoring access for already affected customers. The investigation has progressed from an observed allocation problem to a reproducible mechanism in the supplied code.

## The failure path

The offer window fell from 90 to 60 seconds. A controlled responder answering after 75 seconds succeeds at 90 and is missed at 60. Dispatch then applies the same history penalty to a timeout as to an explicit refusal: minus 0.12. Taking a callout adds only 0.08.

History remains 25% of routing score. Lower ranking makes it more likely someone above the responder accepts first, ending the offer sequence. The lower-ranked responder receives no offer, earns no acceptance credit, and has no implemented time-based route back toward neutral while the score is retained.

**A responder can remain available and listed, yet become practically invisible.** Routing order determines actual opportunity because Dispatch stops at the first acceptance.

## Evidence connecting code to customer impact

Module 3 found Farlight, Vesper, The Undertow and Meteor Mite falling from 49 combined offers per week to three in the final week. The final two weeks contain no accepted callout for these four.

Replaying all 1,696 observed outcomes through the supplied history functions drives all four modeled scores to zero by the final week. Starting every score at 0, 0.5 or 1 produces the same end-baseline and final scores for these four. This is a fixed-offer replay, not a reconstruction of historical production scores or a forecast of restored offers.

Sixteen tests pass against the original modules with controlled device, time and availability adapters. A two-candidate example reverses priority after one missed offer and a competitor's acceptance. Another leaves a listed responder unoffered for 50 controlled callouts while the leader keeps accepting.

## Intervention discipline

| Option | Value | Limitation |
| --- | --- | --- |
| Review the 60-second window; test restoration or a better response experience | Can reduce new timeouts for willing responders | Does not reset existing low history; longer waits may delay onward escalation |
| Distinguish missed from explicitly declined | Stops treating ambiguous nonresponse as refusal | Existing score damage and access recovery still need a policy |
| Add controlled recovery with readiness confirmation and explanation | Gives affected customers a route back and makes decisions reviewable | Must respect capability, urgency, travel time and Supply contracts |
| Roll back proximity weighting | Reverses an allocation change | Does not cure missing score aging; increases history's weight from 0.25 to 0.40 |

**Owners to propose:** Helen approves the product policy; Marcus and Wen validate implementation and rollout; Ravi measures access and outcomes; Nadia and Sofia validate the handler/responder recovery experience.

Supply reads the shared availability record. The supplied dispatch path does not change it, so score decline is not evidence that responders were marked unavailable. Any new recovery feature must preserve its shape and agreed semantics.

**Confidence:** the code mechanism is reproduced. Missing delivery/answer logs, candidate snapshots, deployed-version evidence and historical scores prevent assigning every observed lost offer to this mechanism. Source hashes confirm no routing-source changes.

[Mechanism, evidence and limits](routing-mechanism.md) · [Module 5 design handoff](module-5-handoff.md)

