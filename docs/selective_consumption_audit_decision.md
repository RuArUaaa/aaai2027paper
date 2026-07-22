# Selective-Consumption Audit Decision Package

```text
DECISION_EVENT = ALL_FROZEN_CANDIDATES_ARE_Q0_Q1_OR_CODE_ONLY
CURRENT_PHASE = SELECTIVE_CONSUMPTION_PHENOMENON_AND_TESTBED_QUALIFICATION_VERDICT
VERDICT = C6_STRONG_TESTBED_NOT_FOUND; C3_DIRECTED_VERIFIER_CANDIDATE_NOT_FOUND
```

## EVIDENCE

- AutoGen natively routes one complete `UserTask` only to matching topic
  subscribers, but no public OTEL/runtime trace binds its UUID message ID to a
  concrete consumer delivery. Its committed history is outcome state, not a
  routing trace.
- LangGraph natively routes `Send.arg` into a destination task, but a single
  destination does not establish a real nonrecipient consumer. Its concrete
  two-consumer fixture broadcasts identical full state; public expectations
  also lack concrete task IDs and parent/projection binding. Every task receives
  an unlogged shared-state read closure, and the prebuilt tool path exposes full
  state.
- SWE-agent's optional native Preselector consumes eligible submission records
  before a Chooser receives only the selected subset, establishing code-level
  Q1 non-delivery. Its shipped chooser config disables the Preselector, and all
  22 tracked `.traj` files lack RetryAgent/reviewer/chooser records.
- All three `machine_readable_trace_count` values are zero. Trace-derived
  producer-artifact, consumer-edge, and repeated-consumer counts remain `null`.
- The main coordinator independently checked at least two load-bearing source
  locators per framework and verified pinned commits/file SHA-256 values.
- No final-text semantic proxy was used. No candidate code, model, GPU,
  container, replay, or new trajectory was run.

## FRAMEWORK_RESULTS

```text
- candidate: Microsoft AutoGen
  q_level: Q1
  evidence_level: CODE_ONLY_CANDIDATE
  key_locator: python/packages/autogen-core/src/autogen_core/_single_threaded_agent_runtime.py:557-609
  main_limit: stable message_id exists in code but no public message-to-consumer delivery trace exists

- candidate: LangGraph
  q_level: Q0
  evidence_level: CODE_ONLY_CANDIDATE
  key_locator: libs/langgraph/tests/test_large_cases.py:3939-4168
  main_limit: concrete fan-out delivers identical full state; no real nonrecipient consumer or public parent-bound task trace; CONFIG_KEY_READ is unlogged

- candidate: SWE-agent RetryAgent
  q_level: Q1
  evidence_level: CODE_ONLY_CANDIDATE
  key_locator: sweagent/agent/reviewer.py:242-371
  main_limit: native Preselector subset route has no public RetryAgent trace and is disabled in the shipped configuration
```

```text
C3_IMPACT = UNCHANGED: NARROW_GAP + NEED_NEW_VERIFIER; no native runtime certificate attributes reuse-induced damage rather than baseline error
C6_IMPACT = STRONG TESTBED NOT FOUND; strong form must not restart; weak selective-routing direction remains possible through Q1 non-delivery only
```

## OPTIONS

### A. Close the strong C6 testbed search and pursue a measurement/position paper

Use the completed audit as the basis for a non-experimental contribution on the
distinction among delivery, typed projection, and actual read evidence; stable
identity; raw bypass; and public trace requirements. A later empirical extension
would require a separate idea card/preregistration and authorization.

### B. Close the current C3/C6 strong formulations and authorize a bounded direction reset

Return to the already documented landscape, define a new research question that
does not repackage ordinary cache/reuse/red-green work, and freeze a new protocol
before collecting experimental evidence. This is a new phase, not a fourth
candidate inside the completed audit.

## RECOMMENDATION

Choose **A**. It preserves the strongest new evidence from this round, avoids
manufacturing a testbed through configuration or instrumentation, and is the
only immediately supported direction that does not depend on a missing runtime
trace or verifier. Keep B as the fallback if the owner does not view the
measurement/testbed gap as publication-worthy.

```text
REQUESTED_AUTHORIZATION = Approve Option A for a bounded idea card/position-paper preregistration, or explicitly choose Option B. Do not authorize model/GPU/formal C3/C6 experiments at this checkpoint.

CURRENT_HEAD = d3ad56e5ea57c9ac719301de34f54b74bd169baf (verdict-package commit; this decision/handoff synchronization commit's parent)
WORKTREE_STATUS = verdict package committed; only pre-existing .agents/ .claude/ .codex/ were untracked before this synchronization edit and remain untouched
HANDOFF = docs/RESEARCHSTUDIO_HANDOFF.md
```

## Current authorization boundary

```text
PRIMARY_CANDIDATE = NONE_PENDING_OWNER_DECISION
BACKUP_CANDIDATE = SELECTIVE_CONSUMPTION_MEASUREMENT_POSITION_PAPER
EXPERIMENT_AUTHORIZATION = NONE
MODEL_EXPERIMENT_CALLS = 0
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
LARGE_EXPERIMENTS = 0
```
