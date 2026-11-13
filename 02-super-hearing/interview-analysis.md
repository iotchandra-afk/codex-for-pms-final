# Four customer interviews: classified findings

Read from the connected Research database on 12 November 2026 (Chicago date). These are the four supplied transcript excerpts, dated 2–5 September 2026; they are not four complete recordings or a representative customer survey.

**The service concern is a lost chance to respond, followed by uncertainty about whether Dispatch still considers the responder for work.** Console usability and Supply concerns remain material; complaint frequency alone does not establish business priority or causation.

## Counting method and coverage

One interview contributes at most one count to each theme, even if it repeats the issue. Themes overlap: counts must not be added as independent people or tickets. A checkmark means the supplied excerpt explicitly reports the issue; a dash means it was not raised in that excerpt, not that the participant never experiences it. The handler-alert theme combines awareness and identification problems; it does not imply the same requested feature in all three interviews.

| Interview | Date | Responder(s) | Source snapshot |
| --- | --- | --- | --- |
| [Aunt Dot](https://app.notion.com/p/3eac8516f50181a0bf04dd3b61063feb) | 2026-09-03 | Vesper | [Excerpt](evidence/interviews/aunt-dot.md) |
| [Mr. Ambrose](https://app.notion.com/p/3eac8516f50181499a11d78c4982adee) | 2026-09-02 | Captain Vantage | [Excerpt](evidence/interviews/ambrose.md) |
| [Halloran](https://app.notion.com/p/3eac8516f5018132add7d1b2e2aa6cb6) | 2026-09-05 | Sgt. Bulwark | [Excerpt](evidence/interviews/halloran.md) |
| [Kip](https://app.notion.com/p/3eac8516f501815f9b0bc8b80e97d20a) | 2026-09-04 | Meteor Mite and The Gale | [Excerpt](evidence/interviews/kip.md) |

## Theme matrix

| Specific issue | Dot | Ambrose | Halloran | Kip | Interviews | Representative exact line |
| --- | --- | --- | --- | --- | ---: | --- |
| Offer disappears before the responder can answer | ✓ | ✓ | ✓ | — | **3/4** | “by the time he's actually got a thumb on the screen — it's gone.” — Aunt Dot |
| Quiet stretches or unexplained differences in work | ✓ | — | — | ✓ | **2/4** | “there have been stretches, more than one, where the phone just sits there and sits there” — Aunt Dot |
| Text or status badges are hard to read at a glance | ✓ | ✓ | — | — | **2/4** | “the text is small enough that from a normal standing distance I sometimes can't tell if something's changed unless I lean right in” — Aunt Dot |
| Handler alerts are missing, easy to miss or hard to distinguish | ✓ | ✓ | — | ✓ | **3/4** | “maybe something that tells me too, not just him, when something's come in” — Aunt Dot |
| Saved filters reset without warning | — | ✓ | — | — | **1/4** | “Twice now it's reverted to the default view” — Mr. Ambrose |
| Capability-tag definitions are hard to reach | — | ✓ | — | — | **1/4** | “The capability tag legend. It sits in a drawer off the responder detail panel” — Mr. Ambrose |
| Console brightness makes night work uncomfortable | — | — | — | ✓ | **1/4** | “I just want an actual dark theme built in.” — Kip |
| Requisition approvals take too long | — | — | ✓ | — | **1/4** | “it sat waiting on a quartermaster signature for eleven days.” — Halloran |
| Urgent equipment requests share an ineffective priority queue | — | — | ✓ | — | **1/4** | “One queue, everything in it, doesn't matter if it's laces or plate.” — Halloran |
| Field-failure reports have no visible follow-up | — | — | ✓ | — | **1/4** | “I file a failure report and it goes into a void.” — Halloran |
| Equipment catalog search returns broad or irrelevant results | — | — | ✓ | — | **1/4** | “I typed "plate" the other week looking for the vest plate and got forty results, half of them unrelated” — Halloran |

The [coding record](evidence/interview-coding.json) retains a separate exact excerpt for every positive cell, so each count is independently checkable against the source snapshots.

## Five consequential business issues

1. **Willing responders lose live opportunities (3/4).** Prioritize delivery/answer timing and onward escalation evidence. Ambrose explicitly says this happened earlier in the year; September interviews alone cannot date onset to 12 August.
2. **Some responders go quiet while another is overloaded (2/4 for quiet/uneven work; 1/4 for the explicit overload contrast).** Kip describes Mite and The Gale in the same city and week. Verify offer exposure, availability and eligibility before interpreting this as a routing failure or unfair allocation.
3. **Urgent protective-equipment replacement waits in a routine queue (1/4).** Halloran reports an eleven-day approval wait and an ineffective priority flag. Severity can outweigh frequency; route this to the Supply owner separately from Dispatch recovery.
4. **Handler awareness breaks at the point of action (3/4).** Dot wants a handler notification, Ambrose wants live callouts harder to miss, and Kip wants distinguishable sounds. Validate these separate needs rather than turning them into one assumed feature request.
5. **Poor visibility undermines confidence in operational state.** Readability appears in 2/4; silent filter resets and absent failure-report feedback each in 1/4. These are distinct issues with different owners, not one additive prevalence estimate.

## Improvements and limits

Ambrose values the August filter-persistence improvement but reports subsequent resets. Halloran says maintenance scheduling has improved for Bulwark. Kip likes the side-by-side coverage cards. Preserve these positive observations when proposing changes.

These interviews were recruited for console-redesign research, and the interviewer's questions influence what gets discussed. Halloran repeatedly redirects to Supply; the late mention of a disappearing offer would be easy to overlook in a console-only summary. No transcript supplies measured answer times, historical routing scores, representative prevalence, financial loss or verified release attribution.

Read [the interview-versus-ticket comparison](interviews-vs-tickets.md) before prioritizing. Subsequent metrics and code findings belong to Modules 3 and 4; they are not retroactive facts established by these conversations.

