# Design-Only Preregistration — Outcome-Grounded Actual-Skip Calibration

```text
PREREG_STATUS = D0_COMPLETE_INELIGIBLE_AS_PROPOSED
OWNER_AUTHORIZATION = DESIGN_ONLY
EXPERIMENT_AUTHORIZATION = NONE
MODEL_CALL_BUDGET_AUTHORIZED = 0
GPU_BUDGET_AUTHORIZED = 0
NEW_TRAJECTORIES_AUTHORIZED = 0
DATE = 2026-07-22
```

## D0 disposition

The authorized static audit is complete. The proposed HumanEvalFix design is
`INELIGIBLE_AS_PROPOSED` because the historical implementation has four LLM
nodes rather than the proposed two-stage tool loop, serializes source and test
state into every LLM prompt, has no native response/tool-cache 2×2, and cannot
fit the claimed 2,000-call cap. See `d0_static_audit.md` and
`d0_source_manifest.json`.

Sections 5–11 are retained as the preregistered requirements that would have
governed a later run. They are inactive: D1–D4 are stopped, not authorized.

## 1. Scope and non-claims

This document defines a possible calibration of the paper's measurement
protocol. It does not authorize implementation or execution.

The calibration, if later approved, would measure exact-on-explicit-interface
replay. It would **not**:

- validate Q2/Q3 selective consumption;
- qualify a strong C6 testbed;
- provide a C3 directed verifier;
- introduce a novel cache or invalidation mechanism;
- use final-text similarity as evidence of access or correctness.

## 2. Primary qualification question

Does the unmodified candidate workflow expose at least one native invocation
for which:

1. the complete explicit invocation bytes are stable and hashable;
2. an outcome-relevant environment state can change without changing those
   bytes;
3. replay would skip real model or tool execution;
4. a paired from-scratch outcome oracle is available;
5. the condition is not manufactured by prompt rewriting or an artificial
   consumer?

This is the load-bearing D0 static gate. If the answer is no, the calibration
is stopped before implementation.

## 3. Definitions

- **Explicit invocation identity:** hash of model/tool identifier, serialized
  input bytes, tool schema and version, model version, decoding parameters, and
  any declared system configuration consumed by the invocation.
- **Environment identity:** separate hash of relevant repository files, tests,
  tool-visible state, and versioned external inputs. It is never silently
  folded into or omitted from the record.
- **Exact-on-explicit-interface hit:** explicit invocation identities match.
  This term makes no claim that the changed environment is semantically
  irrelevant.
- **Actual skip:** the underlying model or tool was not executed and the event
  log contains a stable replay-source identity plus `executed=false`.
- **Mutated-clean reference:** a from-scratch execution against the changed
  state, produced without replay.
- **Outcome agreement:** equality of task-native validator tuples between the
  replay arm and mutated-clean; final-text similarity is excluded.
- **False accept:** replay is admitted but outcome agreement with mutated-clean
  fails.
- **Verifier cost:** measured validation work divided by complete from-scratch
  run cost, `v = C_verifier / C_full`.

## 4. D0 static feasibility audit — completed

The D0 audit is read-only and CPU-only:

1. locate the existing HumanEvalFix workflow and all model/tool invocation
   assembly sites;
2. list every byte serialized into each invocation;
3. list repository/test/tool state available outside those bytes;
4. locate event serialization, execution flags, and task-native validator
   output;
5. determine whether a native state change can preserve explicit invocation
   identity while potentially changing the oracle;
6. derive calls per full run and calls per replay arm from code rather than
   from task-count arithmetic;
7. record the result as `ELIGIBLE`, `INELIGIBLE`, or `UNRESOLVED`.

No fixture mutation is executed in D0. No model is loaded or called.

### D0 stop rules

Set `INELIGIBLE` and stop if any condition holds:

- all relevant state is included in the explicit invocation bytes;
- replay can hit only by weakening an exact key;
- the native workflow does not record an actual execution/skip bit;
- a from-scratch outcome oracle cannot be paired by stable task identity;
- creating the condition requires changing prompts, adding a consumer, or
  building a new agent framework;
- evaluating it requires GPU, a large container/service, or a closed model as
  the only evidence source.

## 5. Conditional treatment design — stopped and not authorized

The following design becomes active only after a second written owner
authorization.

### Conditions

- `I`: identity state, used to audit deterministic replay and instrumentation.
- `H`: a native hidden-state change that preserves explicit invocation bytes
  and may alter the task-native oracle.

No `light` or `heavy` mutation category will be invented until D0 identifies a
native, mechanically defined state variable. If no such variable exists, the
study stops.

### Arms

- `A00`: full from-scratch execution; no replay.
- `A10`: exact-on-explicit-interface recorded model-response replay.
- `A01`: exact tool-result replay with the preregistered validator executed.
- `A11`: combined response and tool-result replay.

All arms must use the same task, environment identity, model/version,
temperature, prompts, tool versions, and outcome oracle. Any hidden difference
is a protocol violation.

### Controls

- Negative control: an identity or outcome-irrelevant state twin. The replay
  arm should agree with its from-scratch reference; disagreement diagnoses the
  harness.
- Positive instrumentation control: `A00` must report zero skipped model/tool
  invocations and reproduce its own event-count invariant.
- No oracle-admission arm is allowed; outcome labels cannot decide runtime
  reuse eligibility.

## 6. Outcomes

Primary descriptive endpoints:

1. actual model invocations skipped;
2. actual tool invocations skipped;
3. full-run cost and replay-arm cost on the same cost basis;
4. verifier cost fraction `C_verifier / C_full`;
5. outcome agreement with mutated-clean;
6. false-accept count and exact binomial interval;
7. task success for replay and mutated-clean;
8. paired post-hoc attribution categories: baseline error, reuse-induced
   damage, rescue, and remaining error.

`rho_blame` is analysis-only because it uses paired baseline labels after the
fact. It is never reported as a runtime certificate.

## 7. Analysis rules

- Unit of analysis: stable task identity; no within-task event is treated as an
  independent task.
- All task exclusions must be declared before observing arm outcomes.
- Report counts and intervals before averages.
- Report signed net saving; replay overhead may make it negative.
- Do not call an arm safe when zero failures are observed.
- Do not infer access or dependence from output text.
- Separate harness failure, cache ineligibility, and negative scientific
  result.
- All 164 HumanEvalFix tasks have prior project exposure. Any future split is a
  preregistered execution split, not a fresh or untouched benchmark split.

## 8. Conditional call accounting

The Fable 5 estimate is rejected because task-arm-condition cells are not model
calls. D0 must fill the following symbols from source:

```text
L_full = model calls in one complete from-scratch workflow
L_resp = model calls when the response-replay target is skipped
L_tool = model calls when only the tool result is replayed
L_both = model calls in the combined replay arm
L_prime = calls needed to create one replay source
R = preregistered retry allowance, default 0
N_s, N_p, N_c = smoke, pilot, and confirmation task counts
K = number of eligible state conditions

calls_per_task = L_prime + K * (L_full + L_resp + L_tool + L_both)
total_calls = (N_s + N_p + N_c) * calls_per_task + R
```

A future numerical request must show each term, distinguish tool executions
from model calls, and remain valid under the real loop/retry behavior. No
number in this section is currently authorized.

## 9. Conditional execution order

| Gate | Work | Current status | Authority required |
|---|---|---|---|
| D0 | Static source/schema eligibility and call accounting | COMPLETE: INELIGIBLE_AS_PROPOSED | Current owner decision A |
| D1 | Freeze task IDs, hashes, arms, and numerical budget | STOPPED | A different testbed would require a new decision |
| D2 | Small paired smoke | STOPPED | No execution authorization |
| D3 | Discovery/pilot | STOPPED | No execution authorization |
| D4 | Confirmation | STOPPED | No execution authorization |

No gate inherits unused calls from a later gate, and passing a gate does not
automatically authorize the next one.

## 10. Interpretation map

- D0 ineligible: **observed outcome**; pure measurement/methodology paper, no
  testbed claim, and no actual-skip execution under this preregistration.
- D0 eligible but smoke fails: document instrumentation qualification failure;
  no scientific reuse result.
- Nonzero skip with agreement: report a bounded exact-replay calibration, not
  a new method.
- Zero skip: exact eligibility is unproductive in the audited setting.
- False accepts: report the measured outcome boundary; do not attribute all
  task failures to reuse without paired baseline evidence.

## 11. Reproducibility requirements before D2

- pinned code commit and source manifest;
- stable task manifest and SHA-256 values;
- explicit invocation and environment identity schemas;
- raw event schema with `executed`, replay-source, cost, and oracle fields;
- CPU-only fixture tests for hit/miss, actual-skip accounting, cost signs, and
  post-hoc attribution categories;
- temporary test outputs only; no tracked fixture pollution;
- raw results committed separately from interpretation.
