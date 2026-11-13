# Rook Industries: course working file

## Session scope, Product School lab

This directory is coursework for Product School's "Codex for PMs"
certification. Everything in it is a fictional teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.codex-for-pms/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it); and, only if the student once said no to trusting this folder, change that one trust setting for this folder in Codex's settings file, keeping a copy of the file first.
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

### Products and customers

The user succeeds Dispatch PM Priya Raghunathan (left 21 August 2026). Rook sells per-active-responder subscriptions to independent masked responders and handlers; responders are not employees.

- **Dispatch:** flagship coordination product. Handlers use web; responders use phones. Incident → rank available responders → ping → taken assigns/engages; turned down or missed advances to the next responder.
- **Supply:** equipment requisitions, approvals, fulfillment and maintenance. Service intervals set schedules; field failures can advance them.
- Dispatch writes the **Responder Availability Record**; Supply reads it for maintenance scheduling during low callout load. Availability changes affect both products.
- Monthly release train; routing configuration and ping wait ship in releases, not handler settings.

### People to work with

- **Helen Achebe, Director of Product:** roadmap and commitments.
- **Marcus Oyelaran, Engineering Manager:** engineering, technical sounding board, rough data pulls.
- **Wen Li, Staff Engineer:** built routing; consult on ranking.
- **Ravi Menon, Data Analyst:** official weekly acceptance numbers.
- **Sofia Marino, Designer:** console, phone app, September interviews.
- **Nadia Hoffmann, Support Lead:** complaints, ticket breakdown; regular check-ins recommended.

### Vocabulary and measures

A **callout** requests incident attendance; a **ping** offers it to one responder. Outcomes: **taken**, **turned down**, **missed** (ping wait expired). **Acceptance rate** = taken / all pings, reported weekly. **Time-to-accept** = median seconds from sent to taken. **Coverage gap** = no available responder matches required capability tags, distinct from low acceptance.

**Routing priority** combines travel-time proximity, availability, capability match and recent acceptance history; turned-down/missed pings lower future ranking. **Handler:** responder readiness, availability, tags and gear. **Quartermaster:** stock and approvals. **Mutual aid/shared cover:** cross-city coverage, unsupported today.

### Where things stand

- **4.1, 16 June 2026:** travel-time proximity, bulk callouts, push reliability. Console/mobile stable per Priya; routing risky.
- **4.2, 12 August:** proximity weighted up against acceptance history; ping wait 90 → 60 seconds; persistent filters and three fixes.
- Priya reports falling acceptance. Nadia: tickets ~3× normal on 18 August; still elevated 26 August, two-thirds “phone never goes off,” one-third “gone before I could answer.” Recheck dated observations.
- Marcus questioned identical routing treatment for responders turning jobs down; unresolved. Separate routing/timeout effects. Priya's seasonality explanation and opposition to rollback are opinions; recovery unverified.
- Document routing with Wen; assess impact using Ravi's numbers, Nadia's tickets and Sofia's research.
- **Q3 roadmap, reviewed 30 June:** still names Priya. Availability Confidence (score beside stated availability): committed 4.2, absent from release notes; shipment unconfirmed. Priya reports deferred items; reconcile commitments with Helen. Supply approval chains: committed 4.3. Handler app/shared cover: Q4 explorations.

### Guardrails and sources

Never infer legal identities or assume identity mappings exist. Cover identities are not stored in production. Read Security Policy 4.1 before responder-record changes.

Sources: wiki [Company](https://app.notion.com/p/3eac8516f5018120af01caaedd4b0761), including product pages, glossary, directory, releases/comments and roadmap; `00-rook/company/notes/handoff-from-priya.docx` (21 August 2026). Treat source dates as snapshots.

- The handover omits Ravi; release comments distinguish Marcus's rough pulls from official weekly reporting.
- Priya's dismissal of filter complaints lacks a supporting impact assessment in these sources.
- Ask Priya for routing acceptance criteria, affected responder cohorts and rollback decision thresholds.

- A compounding loss of offers after missed/declined pings is a hypothesis to test, not an established explanation.
- The reviewed Company material does not identify Supply's owner; find that partner before availability changes.
- The cover note and reviews in `01-origin-story/extra-practice/` summarize existing sources; they are not independent evidence.

- Four September console-redesign interviews: 3/4 mention disappearing offers, 2/4 quiet or uneven work; readability and handler alerts are prominent.
- All 147 tickets are classified into 56 specific issues in `02-super-hearing/support-ticket-classification.md`; the dated comparison is in `support-tickets-before-after-12-august.md` alongside it.
- Before 12 August: 40 tickets/44 days; after: 105/26 days; release-day tickets: 2, separate. Daily filing rate rises 4.4x, while filing handlers rise from 11 to 12.
- After 12 August, 30 missing/reduced-offer tickets concern four responders; 14 disappearing-offer tickets concern ten. Together these are 44/105 tickets; follow-ups are not independent customers, and filing dates do not prove onset or cause.
- Only Captain Vantage overlaps the interviewed and ticketed responder samples. Kip describes The Gale overloaded while Meteor Mite is quiet; no equivalent overload complaint appears in the tickets.
- Halloran reports improved maintenance scheduling, yet two later tickets report busy-day bookings. The sources reveal different experiences; the interviews also mention the core offer problems, so they are not purely about console design.

- For remaining modules, use a Dispatch business-lead perspective: responder readiness, reliable incident assignment, customer trust and explicit decision evidence; keep business judgment distinct from verified facts.
- Module 3 audited all 1,696 pings and 1,319 incidents (29 June–6 September), retaining all 160 responder-week cells. Evidence, SQL, executive brief and technical handoff are in `03-rewind/`.
- Acceptance is 76.8% over six baseline weeks, 54.2% in the mixed release week and 72.7% in the final week. Missed share is 2.3% baseline versus 15.1% over three full post weeks.
- Farlight, Vesper, The Undertow and Meteor Mite receive 49 offers/week baseline, only three combined in the final week, with none taken in the last two weeks. Ashgrove/Halfmoon have milder declines; tickets alone did not identify the severe four.
- Incident demand falls 11.1% per week; the severe four's weekly offers fall 83.0%, while the other twelve's rise 24.3%. Eligibility/availability history, answer times and prior-year data are absent, so causation and readiness are unverified.
- Module 4 must trace timeout, missed-history effects, ranking and eligibility with Wen; validate concrete cases in the Module 3 analysis before selecting a fix or changing the shared availability record.

- Module 4 reproduced the mechanism with 16 passing tests against unchanged source; omitted device, clock and availability dependencies were controlled. Reports and evidence are in `04-x-ray-vision/`.
- A controlled 75-second response is taken with 90 seconds but missed with 60. Dispatch penalizes missed and explicitly declined outcomes equally (-0.12); taken adds 0.08. History still carries 0.25 ranking weight.
- A listed, available responder can go unoffered when someone above accepts first; history has no time-based recovery while retained. The unresolved aging TODO dates to 2019. This does not demonstrate an automatic unavailable-state change.
- Fixed-offer replay of all 1,696 outcomes drives the severe four's modeled scores to zero by the final week for initial scores 0, 0.5 and 1. Historical production scores and complete causal attribution remain unverified.
- Restoring 90 seconds does not reset damaged history. Reweighting reduced each miss's rank contribution from 0.048 to 0.030; distinguish that allocation change from the shorter-window trigger and old recovery-policy gap.
- Module 5 should design an explainable readiness/recovery flow, preserving Supply's availability contract. Capability is soft-ranked here; confirm a hard eligibility gate in the omitted adapter before any recovery rollout.

- Module 5 produced `05-super-speed/brief.md` and a self-contained `prototype.html`: Dispatch Ready Review across Kip's console, Mite's phone and operations review, using verified historical evidence and clearly simulated actions.
- The proposed policy is one appropriate offer within a two-hour review window, with a 90-second demo offer. These are design proposals, not approved production settings or guaranteed allocations.
- Readiness confirmation is scoped to the review. Five fit/maintenance checks gate authorization; expiry, changed fit and responder pause block or withdraw the opportunity. Missed and declined remain distinct, and historical outcomes and shared availability are unchanged.
- All 23 browser checks pass, including source-history reconciliation, unchanged historical scorecards, audit-note handling, blocked/expired paths, responder pause and a 390px mobile layout. Screenshots and validation are in the module's evidence folder.
- The prototype pairs acceptance with offers to the four affected responders and callout take rate. Numeric pilot targets, eligibility-adjusted measures, live Supply integration and operational rollout remain review gates rather than verified benefits.

- Module 6 created the repo-local `review-checklist` skill: owner, observable success measure, bounded current scope and problem-first framing, with exact source evidence for every judgment.
- A fresh manual review of all four Product briefs found one flag each: Bulk Callout has no owner; Routing Override Audit Log has no success measure; Approval Chains expands scope; Handler Phone App leads with a solution. Source snapshots and the complete baseline are in `06-sidekicks/`.
- Identifiable team/role ownership can pass; a missing baseline is a follow-up when a real measure exists. The source assigns Approval Chains to the Rook Supply team; do not infer Halloran's ownership from the course example.
- Skill structure validates and 18 state-integrity tests pass. The helper preserves the last complete baseline on missing/unknown sources, rejects fabricated excerpts and distinguishes source removal from issue resolution.
- Automation `rook-product-brief-review` is ACTIVE for Monday 08:00 app-local review in this chat; Chicago is the intended user zone, but the tool does not expose independent timezone confirmation. It reports meaningful changes and new access failures/recovery; unchanged successful reviews stay quiet. First scheduled execution remains unverified.
- All six module exercises now have deliverables. Course submission/certification requirements and production rollout remain separate from completing and saving the exercises.

- The Modules 3–6 handoff includes one original user prompt per module; retain those verbatim and do not duplicate them during later saves.
- The four brief-review flags identify decisions to resolve; passing the checklist is not authorization to build or launch the work.
- The weekly review is configured in the app. Its committed prompt and automation record document the workflow; cloning this repo alone does not create an active scheduled job.
