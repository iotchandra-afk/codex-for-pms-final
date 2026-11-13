# Interviews versus support tickets

**Both sources report lost opportunities; interviews explain the lived experience, while tickets expose repeated failures across more workflows.** Neither source establishes cause, population prevalence or release attribution by itself.

## Comparable sources, different units

Four console-redesign transcript excerpts from 2–5 September are compared with all 147 tickets filed 29 June–7 September. Interview counts are people/conversations raising a theme out of four; ticket counts are primary issue assignments out of 147, including repeat reports. Themes overlap within interviews. Do not compare percentages as though these were equivalent samples.

The [interview matrix](interview-analysis.md) has an exact source excerpt for every positive cell. The [ticket classification](support-ticket-classification.md) assigns every ticket once across 56 issues; the [fresh full-body snapshot](evidence/support-tickets.json) permits verification. Source dates are filing/interview dates, not automatically incident onset.

## Loud in the interviews, comparatively rare in tickets

| Issue | Interviews | Tickets | What the difference tells the PM |
| --- | ---: | ---: | --- |
| Small text/status readability | 2/4 | 2 | In-context use exposes a persistent awareness cost that may not generate repeated tickets. |
| Handler-alert awareness or identification | 3/4 | 2 on identical sounds | The ticket pair covers sound discrimination; it does not capture all three interview requests. Dot wants handler notification, Ambrose wants live callouts harder to miss, Kip wants distinct sounds. |
| Dark theme/night brightness | 1/4, repeatedly emphasized by Kip | 4 | Repetition within one interview signals intensity for that participant, not additional customers. |
| One responder overloaded while another is quiet | 1/4 explicitly; quiet/uneven work in 2/4 | 0 primary overload reports | Tickets report lost offers, but do not show the other side of Kip's Mite/Gale comparison. Absence of an overload ticket is not evidence that overload never happens. |

“Mite thinks Mite's been forgotten. Gale's exhausted.” — [Kip](evidence/interviews/kip.md).

## Concentrated in tickets, absent from these interviews

These are specific ticket clusters, not a claim that each dominates the whole queue. All named clusters have 0/4 interview mentions in the supplied excerpts.

| Ticket issue | Count | Representative exact line | Ticket IDs |
| --- | ---: | --- | --- |
| Duplicate phone notifications | 3 | “The Longcast's phone went off a second time for a job he had already answered.” | #3007, #3016, #3040 |
| Filters fail to follow across computers | 2 | “The filters I save on one do not appear on the other.” | #3042, #3085 |
| Shared computer retains another handler's filters | 2 | “The console kept my filters, but it kept the ones from my colleague's shift, not mine.” | #3046, #3115 |
| No clear-all control for saved filters | 2 | “I cannot find a way to clear them all at once.” | #3066, #3076 |
| Screen-reader controls have no names | 2 | “Several buttons on the console are read out as "button" with no name” | #3039, #3137 |
| No shared handler handover notes | 2 | “there is nowhere in the console to leave a note for them.” | #3008, #3068 |
| Availability time zone unclear during travel | 2 | “the console seems to use my time zone, not the one she is in.” | #3050, #3116 |
| Equipment wrong size or wrong office | 4 across two issues | “Sgt. Falkirk's new gloves arrived in the wrong size.” | #3036, #3111, #3038, #3102 |
| Back orders or slipping repair returns | 4 across two issues | “The Undertow's spare mask has been on back order for a month.” | #3004, #3125, #3011, #3122 |
| Billing duplication | 2 | “Our invoice this month lists Halfmoon twice.” | #3023, #3075 |

The primary classification deliberately remains specific. The comparison does not combine every account, delivery or accessibility issue into an undifferentiated product defect.

## Shared problems and a genuine difference in experience

| Topic | Interviews | Tickets | Interpretation |
| --- | ---: | ---: | --- |
| Missing/reduced offers | 2/4 | 30 primary tickets | Both sources support investigation. The 30 reports concern four responders, not 30 independent customers. |
| Offer disappears before an answer | 3/4 | 15 | A shared service symptom. Ambrose says it happened earlier in the year; #3043 makes the same timing caveat. |
| Silent saved-filter reset | 1/4 | 4 | Ambrose values persistence but cannot fully trust it. Tickets also contain other filter failure modes absent from his account. |
| Slow approvals / ineffective urgency | 1/4 for each | 2 approval waits + 2 urgency reports | Halloran's protective-equipment example deserves escalation even though only one interview raises it. |
| Missing field-failure feedback | 1/4 | 2 | The reporting form can work while the feedback loop fails. |
| Broad catalog search | 1/4 | 2 | A shared Supply usability issue. |
| Maintenance scheduling | Halloran reports improvement | 2 busy-day booking complaints | These are different customers and snapshots, not mutually exclusive accounts or evidence either source is wrong. |

“It's gotten smarter about not booking maintenance into a week he's likely to be out” — [Halloran](evidence/interviews/halloran.md).

“The maintenance schedule booked Sgt. Falkirk's suit in for servicing on the day of the city marathon” — #3054, [ticket snapshot](evidence/support-tickets.json).

Only **Captain Vantage** overlaps the interviewed and ticketed responder samples. Do not infer that a complaint repeated across sources independently confirms the same responder or incident. Do not equate a good experience for Bulwark with resolved maintenance for Falkirk.

## Dated comparison and decision

Before 12 August there are 40 tickets over 44 days; after it, 105 over 26 days; two release-day tickets remain separate. The filing rate rises about 4.4 times. Of the 105 later tickets, 30 report missing/reduced offers and 14 disappearing offers: 44/105 without double counting. Repeated reports increase support load but do not establish 44 affected customers. See [the full dated comparison](support-tickets-before-after-12-august.md).

Prioritize appropriate access to callouts and the ability to answer them, while escalating urgent protective-equipment delays through Supply. Preserve a separate console-awareness workstream instead of dismissing it as cosmetic. Module 3 must test offer exposure and customer cohorts; Module 4 must test the mechanism. The two feedback sources alone cannot choose a routing change.

**Memorable line:** The tickets show repeated breakdowns; the interviews show what those breakdowns do to trust.
