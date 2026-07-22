# Selective-Consumption Phenomenon and Testbed Qualification Protocol

Date: 2026-07-22

Status: **FROZEN BEFORE DEEP CANDIDATE SOURCE REVIEW AND BEFORE RESULTS**

This audit is a bounded, CPU-only qualification gate. It asks whether public,
real agent workflows already expose mechanically observable selective
consumption. It is not a C3/C6 model experiment, cache experiment, reuse
experiment, or mutation experiment.

## 1. Audit question

For a single producer artifact in an authentic agent workflow, does the native
framework do at least one of the following?

1. omit delivery to some downstream consumers;
2. deliver different typed projections to different downstream consumers; or
3. emit native access/read records that mechanically identify the subset each
   downstream consumer actually accessed?

The audit does **not** infer use from final natural-language output, apparent
semantic influence, attention, similarity, citation, or a judge's opinion.

## 2. Authorized and forbidden work

Authorized:

- read-only clones of public source repositories at frozen commits;
- existing public traces, event logs, example run artifacts, and committed test
  fixtures;
- static call-chain analysis and exact source locators;
- small CPU-only parsers and descriptive routing matrices;
- repository metadata, SHA-256 verification, and focused tests.

Forbidden:

- starting a candidate's model, inference server, GPU, or large container;
- creating a new agent trajectory, even with a local or replay model;
- modifying a candidate framework, its prompts, or its routing configuration to
  manufacture fan-out or sparsity;
- adding a reviewer, chooser, consumer, or access hook;
- performing mutation, cache, reuse, or invalidation experiments;
- substring, Jaccard, title/citation mention, embedding, attention, LLM
  self-report, LLM judge, or any other final-text usage proxy;
- changing C3/C6 historical raw results or frozen Route A+ evidence.

## 3. Frozen candidate universe

`candidate_universe.json` is part of this protocol commit. It contains every
candidate considered during pre-screening, the inclusion/exclusion reason,
frozen order, remote repository, frozen source commit for included candidates,
and expected source/trace locations.

Rules after this commit:

- exactly the three included candidates are audited in their frozen order;
- each framework is assigned to exactly one execution worker;
- no included candidate may be replaced after seeing a source result or Q level;
- no fourth candidate may be added;
- failure to locate the expected trace lowers evidence to `CODE_ONLY_CANDIDATE`;
  it does not authorize a substitute candidate;
- if later evidence shows that a candidate violated an inclusion criterion, it
  remains in results as `INELIGIBLE_AFTER_DEEP_REVIEW` with the reason.

## 4. Operational definitions

### 4.1 Producer artifact

A runtime object or serialized record created by a workflow node and made
available to downstream execution. It must have either:

- a native stable identity; or
- a deterministic identity derivable from a pinned public trace record without
  semantic inference (for example, a framework task/message/checkpoint ID or a
  SHA-256 over a canonically serialized record).

A researcher's post-hoc grouping of unrelated strings is not one artifact.

### 4.2 Downstream consumer

A real framework agent, node, handler, task invocation, reviewer, chooser, or
tool/workflow component whose input is assembled by the candidate runtime.
Telemetry sinks, serializers, UIs, and this audit's parser do not count as
scientific consumers unless they are themselves nodes in the authentic agent
workflow.

Repeated invocations of the same node type count as separate consumers only
when the public trace gives them distinct stable task/execution identities and
independent input records.

### 4.3 Framework-native delivery and projection

Evidence is framework-native only when the pinned runtime's ordinary execution
path constructs the delivery/projection and passes it to a consumer. An
application may select a supported routing primitive or typed input schema, but
the audit may not create a new projection. A field subset extracted only by the
audit parser is not framework-native.

### 4.4 Raw bypass

A raw bypass exists when the same consumer can obtain the complete unprojected
artifact through another ordinary runtime path. A Q2 claim must either show no
such path or enumerate and model every bypass. An undocumented possibility is
not treated as absent.

### 4.5 Public trace/event instance

An already-public, immutable or content-addressed runtime artifact that records
at least one concrete delivery, task input, message/event, checkpoint task, or
review/choice input. Documentation prose alone is not a trace. Committed
notebook output, JSON/JSONL/YAML event data, a repository test fixture captured
from the real runtime, or an official benchmark trajectory may qualify if its
provenance is explicit.

## 5. Evidence levels

### `CODE_ONLY_CANDIDATE`

The pinned source contains a potential native path, but no public runtime
instance demonstrates it. It cannot qualify a formal C6 experiment.

### `TRACE_CONFIRMED`

Requires all three:

1. pinned source commit;
2. exact source locator for the creation, route/projection, and consumer-input
   path; and
3. at least one existing public trace/event instance bound to the same mechanism.

The trace must expose exact structured fields. A screenshot or final response is
insufficient.

## 6. Exclusive Q levels

Each candidate receives exactly one highest level after evidence collection.

### Q0 — broadcast/full delivery

Every consumer receives the same complete artifact. No selective-consumption
structure is present.

### Q1 — selective non-delivery

The native framework does not deliver an artifact to some consumers. This proves
selective routing, primarily as non-delivery.

### Q2 — consumer-specific typed projection

The same producer artifact is natively transformed into different typed
projections and delivered to different consumers. The projections must be the
actual consumer inputs. A consumer must not also read the complete raw artifact,
unless all bypass access is explicitly represented in the evidence.

### Q3 — native field/record/read access log

The native execution mechanism emits field-level, record-level, or read-level
access records from which the subset actually accessed by every consumer can be
mechanically reconstructed. Each record must bind stable artifact identity and
consumer identity. A trace that merely records the producer output, with no
delivery/read binding, does not qualify.

### QX — invalid semantic proxy

The only available signal is substring, Jaccard, title/citation mention,
embedding, attention, self-report, LLM judge, or another final-text semantic
proxy. QX maps directly to `FAIL_MEASUREMENT` and cannot be promoted to Q1–Q3.

Q levels are structural, not scores. `TRACE_CONFIRMED` is an orthogonal evidence
axis; for example, `Q2 + CODE_ONLY_CANDIDATE` remains ineligible.

## 7. Source and trace evidence requirements

For each included candidate, collect exact locators for every applicable item:

1. artifact creation;
2. stable artifact identity assignment;
3. route/subscription/projection decision;
4. consumer input assembly;
5. raw bypass or proof-relevant access boundary;
6. access/delivery log creation;
7. trace serialization;
8. at least one public trace instance.

Each locator records repository, commit, path, symbol, start/end line, and a
short factual statement. Web documentation may explain an API but cannot replace
the pinned source locator.

Trace records additionally require URL or repository path, immutable commit or
content hash, media type, byte count where downloadable, and SHA-256 for every
locally archived audit copy.

## 8. Candidate record schema

Every candidate must have the following fields in the evidence/result pipeline:

1. framework/repository;
2. pinned commit;
3. publication or project source;
4. public trace/event-log source;
5. producer artifact;
6. artifact stable identity;
7. producer node;
8. downstream consumers;
9. complete input actually received by each consumer;
10. typed projection presence;
11. field/read access-log presence;
12. raw-artifact bypass status;
13. exact source locators;
14. minimum trace/event instance;
15. repeated-consumer count;
16. producer-artifact count;
17. consumer-edge count;
18. Q level;
19. evidence level;
20. from-scratch/outcome-oracle feasibility;
21. whether formal integration requires framework modification;
22. coarse integration cost (`LOW`, `MEDIUM`, `HIGH`, or `UNKNOWN`);
23. C6 relationship;
24. C3 directed-verifier relationship;
25. main limitations/evidence gaps.

`raw_locators.json` and `results.json` use `null` plus a reason when an item is
not mechanically recoverable. They do not guess.

## 9. Counting rules

- `producer_artifact_count`: distinct stable artifact identities in the public
  instances that meet the artifact definition.
- `consumer_edge_count`: distinct `(artifact_id, consumer_execution_id)`
  deliveries/accesses.
- `repeated_consumer_count`: distinct consumer executions for an artifact when
  at least two exist; otherwise zero.
- counts are per frozen, locally archived public instance and are not population
  estimates;
- duplicate SEND/DELIVER telemetry for one delivery is deduplicated by native
  message/task ID plus consumer ID;
- a parent list split into child records counts as one parent artifact only if a
  native parent ID/provenance relation binds every child projection;
- missing stable identity prevents Q3 and strong-testbed qualification, even if
  payload equality is visually obvious.

## 10. Analysis and tests

`analyse.py` may only parse frozen evidence and compute descriptive counts,
routing matrices, completeness flags, and deterministic hashes. It must not use
network access, execute candidate code, invoke a model, infer semantic use, or
emit the final scientific verdict.

`test_audit.py` must use synthetic fixtures derived from the audit's own schema,
write only to a temporary directory, and cover:

- exact delivery-edge counting and deduplication;
- parent/projection identity linkage;
- raw-bypass flags;
- evidence-completeness gates;
- QX contamination rejection;
- deterministic result serialization.

Raw `results.json` contains observed facts and deterministic completeness flags,
not Q labels, C6 qualification, novelty, or a candidate ranking.

## 11. Pre-registered decision rules

### 11.1 Strong C6 testbed

`C6_STRONG_TESTBED_QUALIFIED` requires one candidate with all of:

- Q2 or Q3;
- `TRACE_CONFIRMED`;
- stable producer-artifact identity;
- at least two real downstream consumers;
- independently reconstructable consumer inputs;
- no unmodelled raw bypass;
- no framework/prompt modification needed to expose the structure;
- a possible from-scratch or outcome oracle in principle;
- no final-text heuristic.

Qualification establishes only the testbed prerequisite, not that a C6 method
works. The only allowed next artifact would be a new idea card/preregistration;
no model or GPU experiment is authorized.

### 11.2 Weak routing

If the highest level is Q1:

```text
C6_STRONG = NOT_QUALIFIED
SELECTIVE_ROUTING_DIRECTION = POSSIBLE
```

Permissible framing is routing-aware compute placement, context non-delivery, or
weak selective invalidation. It must not be called receiver-conditioned
validity or query-relative artifact reuse.

### 11.3 No strong structure

If every candidate is Q0, Q1, QX, or `CODE_ONLY_CANDIDATE`:

```text
C6_STRONG_TESTBED = NOT_FOUND
```

No fourth candidate is added; C6 strong form does not restart; no model/GPU run
occurs. The verdict instead recommends a measurement/position paper or bounded
research-direction reset, then stops for owner review.

## 12. C3 directed-verifier boundary

Selective routing alone has no positive C3 implication. A candidate is marked
`C3_DIRECTED_VERIFIER_CANDIDATE` only if its native runtime certificate can, at
execution time and without a text heuristic, distinguish reuse-induced damage
from baseline task error.

The record must specify certificate input, output, execution time, whether it
runs on every attempt, expected cost, false-positive/negative modes, and the
causal reason it attributes damage to reuse rather than merely detecting task
failure. Otherwise the C3 field is `NOT_FOUND` for that candidate.

## 13. Artifact and commit order

1. protocol commit: this file plus `candidate_universe.json`, with no results;
2. evidence commit: `source_manifest.json`, `raw_locators.json`, `analyse.py`,
   `test_audit.py` (and immutable small public trace excerpts if licensing and
   size permit), with no final Q verdict;
3. raw-result commit: uninterpreted `results.json` only;
4. verdict commit: `framework_matrix.md`, `verdict.md`,
   `docs/selective_consumption_audit_decision.md`, and handoff update.

Before every commit: run the relevant focused tests, `git diff --check`, and
`git status --short`; stage only explicit audit paths. Pre-existing untracked
`.agents/`, `.claude/`, and `.codex/` directories remain untouched.

## 14. Mandatory stop events

Stop and send the owner a decision package when any of these first occurs:

- fewer than two candidates survive pre-screening;
- all frozen candidates end at Q0/Q1/QX or code-only;
- any candidate reaches trace-confirmed Q2/Q3;
- a genuine C3 directed-verifier candidate appears;
- evidence requires a model, GPU, framework modification, or large container;
- a more direct work covers current C6 novelty;
- load-bearing source and public trace evidence remain materially inconsistent.

