# Extra practice review

This exercise uses the repository's fictional Rook context. It does not describe the student's real employer. The one-page covering note is in the adjacent AGENTS.md; the root session restrictions remain in force.

## Prompt 1

> Read 01-origin-story/extra-practice/AGENTS.md, the root AGENTS.md and 00-rook/company/notes/handoff-from-priya.docx. What's contradictory or missing between the covering note and the handover? Distinguish contradictions from omissions and unverified assumptions. What should I ask my predecessor about?

### Findings

There is no established direct contradiction about what shipped. The consequential differences concern evidence, omitted context and unresolved intent.

| Issue | Difference between sources | Question for Priya |
| --- | --- | --- |
| Cause of declining acceptance | The handover favors seasonality and September recovery. The covering note treats both as unverified because routing and timeout changed together. | What historical comparisons support seasonality? What would disprove it? |
| Routing intent | Root context preserves Marcus's unresolved question about responders turning jobs down. The handover omits it. | What behavior was intended, and where are the decision and acceptance criteria? |
| Two complaint patterns | Root context records missing offers and expiring offers separately. The handover mentions general complaints without this breakdown. | Which cohorts lost offers? Did missed/declined pings affect their subsequent ranking? |
| Measurement ownership | The handover directs number requests to Marcus. The covering note names Ravi as the official reporting owner; root context distinguishes rough engineering pulls from weekly numbers. | Which reports informed your decisions, and what limitations do they have? |
| Deferred commitments | The handover says unnamed items slipped. Root context identifies Availability Confidence as committed to 4.2 but absent from release notes. That absence does not establish deferral. | What shipped, slipped or was promised? What is Helen expecting, and who owns it now? |
| Supply and security | The handover omits the shared availability dependency and responder-identity constraints preserved in root context. | What cross-product checks and security reviews have been completed? |
| Filter priority and rollback | Priya calls filter complaints cosmetic and discourages rollback without supplying an impact assessment or decision thresholds. | What impact evidence supports that priority, and what would justify a targeted change or rollback? |

## Prompt 2

> Based on 01-origin-story/extra-practice/AGENTS.md, the root AGENTS.md and the handover, what should I be worried about as the covering Dispatch PM? Rank the five most consequential risks. For each, distinguish evidence from uncertainty and give the next check that would change my decision.

### Findings

1. **Choosing a fix from an untested causal story.** Two release changes coincide with the reported decline. Historical seasonality and recovery are not established here. Ask Ravi for outcome trends split into taken, turned down and missed, with relevant historical comparisons and responder cohorts. Choose interventions after distinguishing the patterns.
2. **Missing persistent losses in access to callouts.** Dated support reports emphasize phones no longer receiving offers. Ranking also uses recent acceptance history. A compounding effect is plausible, not demonstrated. Trace offer exposure and ranking for affected responders with Wen and compare with Nadia's complaints.
3. **Accepting unintended routing behavior as policy.** Marcus raised a question about treatment of responders declining work; the sources do not resolve it. Compare Priya's intended behavior with Wen's implementation and concrete responder examples before approving another change.
4. **Inheriting commitments without ownership.** The roadmap still names Priya; the handover leaves deferred items unnamed. Availability Confidence's delivery status is unconfirmed. Reconcile shipment evidence, customer promises, owners and dates with Helen before making new commitments.
5. **Creating a Supply regression while fixing Dispatch.** Supply consumes Dispatch's availability record for maintenance scheduling. The sources establish the dependency, not an existing regression. Identify affected consumers and validate scheduling behavior before changing availability calculations or updates.

## First conversations

Ask Priya about original intent and decision thresholds; Ravi about reliable measures; Nadia about complaint cohorts; Wen about routing behavior; Helen about commitments. Include the Supply owner when evaluating availability changes; that person is not identified in the reviewed material.

## Evidence limits

The covering note is a summary, not independent corroboration. Root AGENTS.md summarizes the Company wiki; the handover is Priya's account dated 21 August 2026. No new ping-data analysis, code inspection or September recovery verification was performed for this practice. Original source pointers are in root AGENTS.md.
