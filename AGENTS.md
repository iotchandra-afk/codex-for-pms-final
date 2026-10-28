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
