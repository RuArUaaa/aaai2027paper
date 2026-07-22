# Fable 5 Review Disposition — Owner Decision A

```text
DECISION_EVENT = NEW_EXPERIMENT_SCOPE_REQUIRES_OWNER_AUTHORIZATION
OWNER_RESPONSE = A
DECISION_TIME = 2026-07-22T12:44:00+08:00
PAPER_DIRECTION = MEASUREMENT_AND_METHODOLOGY
ACTUAL_SKIP_ROUTE = D0_COMPLETE_INELIGIBLE_AS_PROPOSED
EXPERIMENT_AUTHORIZATION = NONE
MODEL_EXPERIMENT_CALLS_AUTHORIZED = 0
GPU_RUNS_AUTHORIZED = 0
NEW_AGENT_TRAJECTORIES_AUTHORIZED = 0
```

## Disposition

The five Fable 5 documents are retained as independent review inputs. They do
not override frozen C3/C6/C4 evidence or the main coordinator's scientific
judgment.

| Fable 5 proposal | Decision | Binding interpretation |
|---|---|---|
| Identifiability-first measurement/methodology paper | ACCEPT | This is the paper backbone. |
| Recommended title | ACCEPT | Use the title in `docs/AAAI27_ABSTRACT_SUBMISSION.md`. |
| Submit an abstract before the official deadline | ACCEPT | Manual author action; no assistant submission was authorized. |
| Three-framework audit as bounded evidence | ACCEPT_WITH_SCOPE | Only the frozen candidates, pinned commits, and located public artifacts are covered. |
| Exact response/tool reuse as a new mechanism | REJECT | It is ordinary cache/replay and has no mechanism-novelty claim. |
| HumanEvalFix exact reuse as a positive Q-rubric example | REJECT | It does not establish Q2/Q3 selective consumption or a strong C6 testbed. |
| Test outcome as a C3 directed verifier | REJECT | It is a naive outcome oracle; C3 remains `NEED_NEW_VERIFIER`. |
| Immediate Route C model run up to 2,000 calls | REJECTED_BY_D0 | The proposed native testbed is ineligible and the cap cannot fund the stated design. |
| CPU-only idea card, static feasibility gate, preregistration, and budget accounting | ACCEPT | This is the full authorization granted by owner response A. |
| “The project has never executed any live skip” | REJECT_AS_OVERBROAD | Frozen VRAA M4 executed 80 exact producer-node injection skips; it did not execute downstream/cascade skip or the proposed response/tool 2×2. |

## Authoritative scientific state

```text
C3 = NARROW_GAP; NEED_NEW_VERIFIER
C3_GATE_EFFECT = UNCHANGED
C6 = NARROW_GAP / CONDITIONAL_CLEAR_GAP; FAIL_MEASUREMENT
C6_STRONG_TESTBED = NOT_FOUND
C4 = HIGH_COLLISION; REJECTED
PRIMARY_PAPER_IDENTITY = MEASURE_BEFORE_YOU_REUSE
EXPERIMENT_AUTHORIZATION = NONE
```

The proposed actual-skip calibration was assessed as a separate measurement
evaluation and stopped at D0. Even a future materially different calibration
could not validate selective-consumption structure, establish a runtime
directed verifier, or rescue exact caching as a novel method.

## D0 outcome

The authorized static audit completed without model or GPU use and returned
`INELIGIBLE_AS_PROPOSED`:

- the native HumanEvalFix workflow has four LLM nodes, not the proposed
  two-stage single-agent loop;
- source and test text are serialized into every LLM prompt;
- no native interactive tool-result consumer supports the proposed tool-cache
  arm;
- 1,968 is a condition-cell count, not a model-call count;
- under the stated identity-only-hit, two-calls-per-cell assumptions, the
  optimistic unimplemented two-stage count is 3,280 model calls, and the native
  four-node no-hit count is 7,872;
- implementing the Fable 5 design would require a new harness.

See `experiments/actual_skip_calibration/d0_static_audit.md`. The proposed
calibration is stopped; it is not waiting for a larger budget.

## Authorized stage: completed D0 documentation only

Allowed:

- revise and package the abstract;
- write one bounded idea card;
- inspect existing HumanEvalFix source and already recorded artifacts;
- define a static semantic-eligibility gate;
- write a preregistration and auditable call-budget formula;
- run CPU-only documentation, parser, and structural checks.

Forbidden:

- any model or API call to a studied system;
- any GPU use or inference service;
- generation of a new agent trajectory;
- implementation or execution of cache/replay arms;
- repository mutations used as experimental treatments;
- presenting a test oracle as a directed reuse-damage certificate;
- changing frozen C3/C6/C4 results.

## Requirements for any materially different future testbed

The current route has no smoke stage. A materially different testbed would need
a new owner decision confirming all of the following:

1. a native cacheable invocation can remain byte-identical while a relevant
   environment state changes, without rewriting the prompt or candidate
   workflow to manufacture the condition;
2. cache identity, hidden state, validator input, and outcome oracle each have
   stable identities;
3. the exact model- and tool-call budget is derived from the real workflow;
4. the study is labeled a calibration baseline, not a C6 testbed or new cache;
5. stop rules and task IDs are frozen before any model call;
6. a separate numerical authorization is recorded.

Requirement 1 failed for the proposed HumanEvalFix route. The exact-reuse
branch is stopped and the paper remains a pure measurement/methodology paper.

## Files governed by this decision

- `docs/AAAI27_ABSTRACT_SUBMISSION.md` — authoritative submission text;
- `idea_cards/measure_before_reuse.md` — authoritative paper idea card;
- `experiments/actual_skip_calibration/preregistration.md` — design-only
  preregistration;
- `refine-logs/EXPERIMENT_PLAN.md` and `refine-logs/EXPERIMENT_TRACKER.md` —
  stage plan and tracker;
- `docs/FABLE5_*.md` — review inputs, not final authorization records.
