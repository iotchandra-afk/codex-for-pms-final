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

### Business and people

The user succeeds Dispatch PM Priya Raghunathan (left 21 August 2026). Rook sells subscriptions per active responder; responders are customers, not employees. Dispatch coordinates callouts through handlers' web consoles and responders' phones. Supply handles equipment, approvals and maintenance; it reads Dispatch's Responder Availability Record. Preserve that shared contract.

Helen Achebe: Product commitments. Marcus Oyelaran: Engineering manager and rough data pulls. Wen Li: routing engineer. Ravi Menon: official metrics. Sofia Marino: design/research. Nadia Hoffmann: Support. Identify Supply's operational owner; an accountable Supply team in a brief does not identify that person.

### Vocabulary and verified findings

A callout is an incident request; a ping offers it to one responder. Taken assigns; turned down or missed advances. Acceptance = taken/all pings; zero-offer acceptance is undefined. Coverage gap means no eligible capability match. Time-to-accept means sent-to-taken seconds, unavailable in this extract.

4.2 (12 August) changed proximity/history weights and ping wait 90→60 seconds. Four interviews and 147 tickets report disappearing offers and quiet responders; interview and ticket denominators differ. Release-day tickets are separate; filing dates do not establish onset.

All 1,696 pings, 1,319 incidents and 160 responder-weeks were audited. Acceptance: 76.8% baseline, 54.2% mixed release week, 72.7% final week. Farlight, Vesper, The Undertow and Meteor Mite fall from 49 combined offers/week to three in the final week. Aggregate recovery conceals lost access.

Code tests reproduce missed and explicit decline both reducing history by 0.12; taken adds 0.08. History has no implemented aging while retained. Earlier acceptance can leave lower-ranked responders unoffered. A controlled 75-second answer succeeds at 90 seconds, misses at 60. Actual historical scores, eligibility, delivery timing and full causal attribution remain unknown.

### Decisions and navigation

[Module 1 history](01-origin-story/working-context-history.md) preserves Company/handover contradictions and commitments. Availability Confidence was committed to 4.2; shipment remains unconfirmed. Reconcile promises with Helen; seasonality is unverified.

[Module 2](02-super-hearing/README.md): counts, quotes and source disagreement. [Module 3](03-rewind/README.md): SQL/metrics. [Module 4](04-x-ray-vision/README.md): mechanism and handoff. [Module 5](05-super-speed/README.md): brief and simulated Ready Review. Its two-hour review and 90-second offer are proposals; readiness, eligibility, Supply checks and pilot thresholds require approval.

[Module 6](06-sidekicks/README.md): reusable owner/measure/scope/problem-first review. Team ownership can pass; missing baselines remain follow-ups. Preserve the last complete baseline on missing sources. Weekly app automation and two manual runs are separate evidence; cloning the repo does not create a schedule. [Submission](SUBMISSION.md) maps the official rubric and remaining administrative steps.

Never infer responder legal identities. Read Security Policy 4.1 before responder-record changes. Treat source dates as snapshots; summaries are not independent corroboration. Keep proposed decisions separate from verified facts.
