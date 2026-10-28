# Rook Dispatch cover note

Fictional course exercise. All root AGENTS.md session restrictions apply.

## Your remit

Cover the incoming Dispatch PM following Priya Raghunathan's departure on 21 August 2026. Diagnose the reported acceptance decline, clarify release commitments and coordinate decisions with Product and Engineering. Validate dated evidence before treating it as current.

## Product and customers

Rook sells subscriptions per active responder to independent masked responders and handlers. Responders are customers, not employees.

Dispatch ranks available responders for an incident, then offers a callout by phone. A taken ping assigns the incident; a turned-down or missed ping moves to the next responder. Handlers use the web console. Supply manages equipment and maintenance; it reads the availability record written by Dispatch.

## Measures and vocabulary

- Acceptance rate: taken pings divided by all pings; weekly headline measure.
- Time-to-accept: median seconds from sent to taken.
- Coverage gap: no available responder matches the required capability tags.
- Routing priority: travel-time proximity, availability, capability match and recent acceptance history. Missed/declined pings lower future ranking.

## Current decisions

Release 4.2 shipped 12 August: proximity gained weight and ping wait fell from 90 to 60 seconds. Priya reports declining acceptance. Nadia reported elevated complaints: missing offers and offers expiring too quickly. Seasonality is a hypothesis; September recovery is unverified.

Establish who lost offers, distinguish routing from timeout effects, and clarify whether the treatment of responders declining work was intentional. Document routing with Wen before proposing changes.

Availability Confidence was committed to 4.2 but is absent from release notes; shipment is unconfirmed. Reconcile deferred commitments and delivery ownership with Helen. Check Supply maintenance effects before changing availability.

## People

- Helen Achebe: Product director; roadmap and commitments.
- Marcus Oyelaran: Engineering manager; technical decisions and rough data pulls.
- Wen Li: Staff engineer; routing implementation.
- Ravi Menon: Analyst; official weekly reporting.
- Nadia Hoffmann: Support lead; complaints and ticket breakdown.
- Sofia Marino: Designer; console, phone app and interviews.
- Priya Raghunathan: predecessor; intended behavior and decision history.

## Sources and constraints

Start with the root AGENTS.md and `00-rook/company/notes/handoff-from-priya.docx` (21 August). Root context summarizes the Company wiki and release comments; roadmap status dates to 30 June. Ask for fresh numbers, explicit commitments and rollback criteria. Never infer responder legal identities; consult Security Policy 4.1 before responder-record changes.
