# Module 4 completed

Completed 12 November 2026 for the fictional Rook Dispatch coursework.

The supplied routing mechanism is validated against Module 3's observed metrics. Sixteen tests pass using the original source with controlled omitted adapters; five source hashes confirm no routing/configuration changes. Production incident-level attribution remains conditional on telemetry that the course extract does not contain.

## Deliverables

- [Executive decision brief](decision-brief.md): verified mechanism, intervention tradeoffs, proposed owners and recommendation.
- [Mechanism and evidence](routing-mechanism.md): source map, flow diagram, controlled cases, fixed-sequence replay, Module 3 crosswalk, Supply and capability boundaries.
- [Module 5 handoff](module-5-handoff.md): handler/responder recovery experience, acceptance criteria, metrics and rollout gates.
- [Validation harness](validate_mechanism.py): reproducible standard-library tests against actual source modules.
- [Machine-readable validation](evidence/mechanism-validation.json): 16 passed tests, logs, controlled-case outputs and source hashes.
- [Full fixed-sequence replay](evidence/fixed-sequence-replay.json): modeled per-event history and weekly snapshots under three initial-state assumptions, plus missed-neutral sensitivity.
- [Replay summary](evidence/replay-summary.json): baseline, transition and final modeled scores for the four affected responders.
- [Original prompt](prompts.md): preserved user instruction.

## Completion criteria

- [x] Inspect all five routing components and the changelog.
- [x] Distinguish what changed in 4.2 from the pre-existing scoring/recovery policy.
- [x] Reproduce a willing response becoming missed under the shorter window.
- [x] Verify equal treatment of missed/refused outcomes and asymmetric recovery credit.
- [x] Show how candidate inclusion can coexist with no offers and no score recovery.
- [x] Validate ranking-weight changes separately from timeout behavior.
- [x] Replay all 1,696 observed outcomes without inventing missing candidate or delivery records.
- [x] Separate modeled scores from historical production state and counterfactual service outcomes.
- [x] Check the readiness/Supply boundary and flag the unverified capability eligibility gate.
- [x] Produce a decision recommendation and actionable Module 5 design handoff.
- [x] Record the prompt and findings within the course repo.

## Reproduce

From the course root, using Python 3.11 or another compatible Python 3 installation:

```powershell
python -B 04-x-ray-vision/validate_mechanism.py
```

The harness uses only the standard library, makes no device or database calls, disables bytecode writes, and writes evidence under this module. It checks the original modules' hashes. No service change or external message has been sent.

The next module is the product brief and working prototype. Its purpose is to make the recovery experience real before engineering selects and rolls out a policy change.
