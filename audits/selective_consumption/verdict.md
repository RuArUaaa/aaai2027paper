# Selective-Consumption Phenomenon and Testbed Qualification Verdict

Date: 2026-07-22

Protocol commit: `74f9c1407735121837becb91169adddd4f94c16f`

Final uninterpreted raw-results commit: `356e9bd8ab5350e7163a23efeb5bc9d7e41ba5fb`

## Verdict

```text
AUDIT_STATUS = COMPLETE
AUTOGEN = Q1 + CODE_ONLY_CANDIDATE
LANGGRAPH = Q0 + CODE_ONLY_CANDIDATE
SWE_AGENT = Q1 + CODE_ONLY_CANDIDATE

C6_STRONG_TESTBED = NOT_FOUND
SELECTIVE_ROUTING_DIRECTION = POSSIBLE
C3_DIRECTED_VERIFIER_CANDIDATE = NOT_FOUND

PRIMARY_CANDIDATE = NONE_PENDING_OWNER_DECISION
EXPERIMENT_AUTHORIZATION = NONE
```

This triggers mandatory decision event 3: every frozen candidate ends at Q0,
Q1, or code-only. No fourth framework may be added inside this audit, and no
model/GPU/formal C3/C6 experiment may begin.

## Evidence boundary

All three pinned codebases contain relevant framework-native source paths. None
contains or links a qualifying public runtime artifact that binds the target
mechanism to stable producer-artifact and consumer-execution identities.
Accordingly:

- `machine_readable_trace_count = 0` for every candidate;
- trace-derived producer, consumer-edge, and repeated-consumer counts remain
  `null`;
- source/test topology counts are reported only as static facts;
- no final-text, substring, Jaccard, citation, embedding, attention, LLM
  self-report, or LLM-judge signal was used.

## Candidate judgments

### AutoGen — Q1 / CODE_ONLY_CANDIDATE

The audited handoff application registers three topic-isolated AI consumers.
One `UserTask` published to an agent-specific topic is delivered only to the
matching subscriber; the other two agents receive no envelope. The selected
handler receives the complete `UserTask`, so this is selective non-delivery,
not consumer-specific typed projection.

The runtime assigns a stable UUID `message_id`, but the public evidence cannot
bind it to a consumer delivery. `MessageEvent` omits the ID, and its publish
DELIVER event sets `receiver=None`. OTEL process spans could carry message ID,
payload, and consumer destination, but no exported public span instance was
found. The committed handoff history is outcome state, not a routing trace.

Therefore Q1 is supported by pinned source, while `TRACE_CONFIRMED` is not.

### LangGraph — Q0 / CODE_ONLY_CANDIDATE

LangGraph has native destination routing: a conditional branch can emit
`Send(node,arg)`, the runtime schedules only the named node, and `packet.arg`
becomes that task's actual input. That alone does not establish Q1: an
unselected graph node is not automatically a real downstream consumer of the
same artifact. The concrete two-consumer source fixture sends identical full
state to both retrievers and therefore supports Q0, not selective non-delivery.

The apparently stronger Q2 route fails the frozen requirements:

1. no public archived instance binds two different projections to one stable
   parent producer artifact and two concrete task IDs;
2. every task config receives a shared-channel `CONFIG_KEY_READ` closure;
3. the prebuilt tool path explicitly carries or hydrates full graph state; and
4. no read/access log records whether a consumer used that bypass.

Committed test expectations are useful source corroboration but use placeholder
IDs or contain no serialized task records. They are not an immutable runtime
trace. Without a frozen native graph containing both an actual recipient and an
actual nonrecipient for the same artifact, LangGraph remains Q0/code-only, not
Q1, Q2, or Q3.

### SWE-agent RetryAgent — Q1 / CODE_ONLY_CANDIDATE

A completed attempt creates one `ReviewSubmission` and sends it to the one
configured retry-loop type. Score Reviewer and Chooser are mutually exclusive,
not simultaneous downstream consumers of one artifact. Repeated Reviewer model
samples have no separate public execution identities and do not count as
distinct consumers.

The native optional Preselector path does, however, meet the code-level Q1
structure: the Preselector consumes eligible rendered submission records and
returns indices, after which the Chooser receives only the selected subset.
Unselected `ReviewSubmission` records are not delivered to the Chooser. This is
record-level non-delivery, not a typed projection.

The shipped public RetryAgent configuration does not enable the Preselector,
and no public RetryAgent trajectory demonstrates the optional path. The 22
tracked `.traj` files contain no `attempts`, `chooser`, `best_attempt_idx`, or
review path. Reviewer/Chooser messages are configurable text/Jinja renderings
rather than typed projections. The result is Q1/code-only, not Q2 or
`TRACE_CONFIRMED`.

## C6 effect

No candidate satisfies the conjunction required by
`C6_STRONG_TESTBED_QUALIFIED`:

- none reaches Q2 or Q3;
- none is `TRACE_CONFIRMED` for the relevant mechanism;
- no public instance supplies stable parent artifact identity plus two
  independently reconstructable consumer inputs; and
- LangGraph additionally has an unobserved raw-state bypass.

Therefore:

```text
C6_STRONG_TESTBED = NOT_FOUND
C6_STRONG_FORM_RESTART = NO
SELECTIVE_ROUTING_DIRECTION = POSSIBLE
```

AutoGen's topic path and SWE-agent's optional Preselector path can motivate weak
work on routing-aware compute placement, context/record non-delivery, or weak
selective invalidation. They cannot be described as receiver-conditioned
validity, query-relative artifact reuse, or different contracts for the same
artifact across receivers.

This audit does not reverse the existing C6 novelty label. It resolves the
testbed prerequisite negatively within the frozen candidate universe.

## C3 effect

No candidate provides a native runtime certificate that separates
reuse-induced damage from baseline task error:

- AutoGen certifies delivery, not correctness or causal damage;
- LangGraph records task input/result/error/checkpoint state, but an error may be
  an ordinary baseline failure and success may still hide semantic damage;
- SWE-agent's reviewer and chooser emit LLM-derived overall scores/choices and
  never observe a reuse intervention.

None has the required certificate input/output, causal attribution, bounded
cost, execution timing, and false-positive/negative semantics. Consequently:

```text
C3_DIRECTED_VERIFIER_CANDIDATE = NOT_FOUND
C3_CURRENT_STATUS = NARROW_GAP + NEED_NEW_VERIFIER
C3_GATE_EFFECT = UNCHANGED
```

Selective routing does not solve the C3 verifier problem.

## Authorized next step

No experiment is authorized. The recommended owner decision is to close the C6
strong-testbed search for this frozen universe and develop a bounded
measurement/position-paper direction around:

- the distinction between delivery, projection, and actual read evidence;
- stable producer/consumer identity requirements;
- raw-bypass accounting; and
- why public agent traces currently fail testbed qualification.

An alternative is a bounded research-direction reset outside the current C3/C6
strong formulations. Either route requires owner authorization and a new idea
card/preregistration before any experiment.

## Compliance counters

```text
MODEL_EXPERIMENT_CALLS = 0
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
LARGE_EXPERIMENTS = 0
CANDIDATE_FRAMEWORK_EXECUTIONS = 0
CANDIDATE_FRAMEWORK_MODIFICATIONS = 0
EXPERIMENT_AUTHORIZATION = NONE
```

## Strongest remaining risk

The audit is deliberately bounded to the frozen candidates, commits, and public
artifacts located for those sources. A qualifying externally hosted telemetry
export could exist outside the discovered official artifacts. That possibility
does not promote present evidence to `TRACE_CONFIRMED`, and this protocol does
not permit adding or substituting a candidate after seeing the result.
