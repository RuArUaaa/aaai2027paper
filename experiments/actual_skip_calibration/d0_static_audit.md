# D0 Static Feasibility Audit — HumanEvalFix Actual-Skip Calibration

```text
AUDIT_STATUS = COMPLETE
VERDICT = INELIGIBLE_AS_PROPOSED
SOURCE_REPOSITORY = /Users/zijian_nong/research/aaai2027
SOURCE_HEAD = ae77f91bb8baad5f77da1278abb1a20272660417
SOURCE_MODE = READ_ONLY
MODEL_CALLS = 0
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
EXPERIMENTAL_MUTATIONS = 0
DATE = 2026-07-22
```

## Audit question

Does the historical HumanEvalFix implementation natively support Fable 5's
proposed two-stage single-agent experiment with response-cache and validated
tool-result-cache arms, a relevant state change that preserves complete
explicit invocation identity, actual execution/skip records, and a paired task
oracle—without building a new workflow or rewriting prompts?

## Verdict

No. The available historical assets support a different four-LLM-node
workflow and a host-side sandbox certificate. They do not contain the proposed
two-stage single-agent tool loop or response/tool 2×2. For the proposed
source/test mutations, no qualifying hidden-state condition was located that
makes exact full-invocation replay non-tautological.

Building the proposed workflow would be a new harness, and making source/test
state invisible to the exact invocation key would weaken the meaning of
"exact full-invocation" reuse. Under the owner-approved D0 stop rules, the
calibration branch stops before implementation.

This verdict is specific to the proposed HumanEvalFix Route C design. It does
not claim that all outcome-grounded actual-skip studies are impossible.
Other possible native external states—such as library, sandbox, or runtime
version changes—were not systematically enumerated and remain out of scope.
They are not needed for this verdict because the missing native tool loop, full
source/test serialization, schema gap, and new-harness requirement are each
independent failures of the proposed design.

## Load-bearing source reconstruction

### 1. The real workflow has four LLM calls, not two stages

The tracked historical pipeline is:

```text
Planner -> Coder -> Reviewer -> Fixer -> host-side sandbox certificate
```

Load-bearing locators in the historical repository:

- `pipelines/task_b.py:125-151` constructs the shared system, source, and test
  prefix.
- `pipelines/task_b.py:155-172` executes Planner.
- `pipelines/task_b.py:174-192` executes Coder.
- `pipelines/task_b.py:194-212` executes Reviewer.
- `pipelines/task_b.py:214-225` executes Fixer.
- `pipelines/task_b.py:227-242` evaluates the final Fixer text in the host-side
  sandbox.

The TraceBuild variant inserts one host-side `Test` node between Coder and
Reviewer, but the model-call count remains four. The test node directly invokes
the certificate function rather than an agent tool:

- frozen source
  `runs/vraa/pilot/SOURCE_SNAPSHOT/pipelines/tracebuild_harness.py:199-217`;
- test execution at the same file's `:259-266`;
- Reviewer prompt at `:267-273` contains source, tests, plan, and patch, but not
  the Test node's runtime result.

Consequences:

- `read_file`, `run_tests`, `apply_patch`, and `list_dir` are not native agent
  tools in this workflow;
- the proposed validated tool-result-cache arm has no matching consumer path;
- a two-stage single-agent loop would have to be newly implemented.

### 2. Relevant source/test state is serialized into every LLM prompt

`task_b.py:132-151` constructs a shared prefix containing source and test text.
The four node inputs at `:155-225` each consume this prefix. Therefore a source
or test mutation changes the explicit invocation bytes for every native LLM
node that should observe the change.

The completed TraceBuild discovery independently found the same structural
property:

- 60 tasks × 2 benchmark-provided mutations = 120 clusters;
- static and runtime read-set saving both equal 0;
- static and runtime classifications differ on 0/120 clusters;
- exact early cutoff improves on 2/120 clusters;
- every LLM node receives both full source and test resources.

See historical
`runs/tracebuild_discovery/EXPERIMENT_AUDIT.json:48-60,68-98`.

Hence:

- a key containing the complete invocation correctly misses after relevant
  source/test mutation;
- a key that still hits must omit changed serialized input and is no longer an
  exact full-invocation key;
- a state change applied only after an unchanged producer call does not by
  itself create a producer counterfactual.

### 3. A task-native outcome oracle exists

The sandbox extracts code, executes it in a subprocess, blocks declared
dangerous operations, and applies a timeout. The historical validator audit
reports agreement with all 164 stored pass/fail labels:

- `pipelines/sandbox_exec.py:26-100`;
- `runs/phase0_validator/validator_feasibility.json:15-28`.

This is sufficient as a post-hoc outcome oracle. It is not a runtime directed
certificate that attributes failure to reuse, and its recorded latency is
diagnostic rather than submission-grade systems timing.

### 4. The project has already executed producer-node skips

Fable 5's claim that the project never executed any live skip is too broad.
The frozen VRAA M4 runner injected an exact `plan` or `patch` artifact and did
not call the corresponding producer node:

- `runs/vraa/pilot/SOURCE_SNAPSHOT/pipelines/tracebuild_harness.py:205-245`;
- `runs/vraa/pilot/SOURCE_SNAPSHOT/pipelines/vraa_pilot_cpu.py:148-195`.

Across 40 traces, the runner serialized 720 generation records over 200
workflows (`runs/vraa/pilot/MERGE_COMPLETE.json:1-14`). The two forced-reuse
workflows per trace skip one producer call each, yielding 80 artifact-injection
events: 40 plan and 40 patch skips.

The frozen event schema identifies these rows with
`node_type="artifact_injection"`, but it has no explicit `executed` boolean
(`tracebuild_harness.py:295-326`). A future actual-skip protocol would therefore
need a schema change even to meet the preregistered execution-bit requirement.

That experiment remains a scientific no-go. In all 40/40 traces, the changed
FULL producer output was byte-identical to the base producer output because the
changed state was applied only to the receiver suffix. The comparator therefore
did not create the required counterfactual:

- `runs/vraa/m4_result_review/REPORT.md:158-187`.

The accurate remaining gap is:

> The project has not executed a downstream/cascade-skip study or the proposed
> response-cache × tool-cache 2×2. It has executed exact producer-node skips,
> but the frozen comparator was non-discriminating.

## Call-budget reconstruction

Fable 5's `164 tasks × 4 arms × 3 conditions = 1,968` counts condition cells,
not model calls.

Even under the unimplemented two-stage assumption:

```text
no-hit calls = 164 × 4 × 3 × 2 = 3,936
```

Under a stated optimistic scenario—exactly two calls per cell, only the
identity condition hits, both stages hit in the two response-replay arms, and
the tool-only arm saves no model call:

```text
saved calls = 164 × 2 response arms × 2 stages = 656
executed calls = 3,936 - 656 = 3,280
```

If replay-source priming requires a separate two-call execution per task, the
total becomes 3,608. An interactive tool loop would be higher and cannot be
counted until its maximum rounds are specified.

Directly applying four arms and three conditions to the native four-LLM-node
workflow yields 7,872 calls before hits. Its existing injection seam skips only
one plan or patch producer per workflow and does not implement the proposed
dual response/tool cache.

Therefore, under the Fable 5 arm/condition layout and these explicitly stated
two-stage assumptions, the proposed 2,000-call cap cannot fund the full design.

## D0 decision table

| Requirement | Result | Evidence |
|---|---|---|
| Existing two-stage single-agent workflow | FAIL | Native workflow has four LLM nodes |
| Native response/tool 2×2 | FAIL | No interactive agent tools or tool-result consumer path |
| Relevant state change with identical complete invocation | FAIL_AS_PROPOSED | Source and tests are serialized into all LLM prompts |
| Actual producer skip evidence | PASS_HISTORICALLY | VRAA M4 has 80 injection events |
| Explicit execution/skip boolean | FAIL | Skip is encoded indirectly as `artifact_injection` |
| Stable task-native outcome oracle | PASS | 164/164 certificate agreement |
| ≤2,000-call full design | FAIL | optimistic two-stage lower bound is 3,280 calls |
| No new framework or prompt rewrite | FAIL | proposed two-stage allowlist requires a new harness |

```text
D0_VERDICT = INELIGIBLE_AS_PROPOSED
CALIBRATION_EXECUTION = STOPPED
C3_GATE_EFFECT = UNCHANGED
C6_GATE_EFFECT = UNCHANGED
PRIMARY_PAPER_ROUTE = PURE_MEASUREMENT_AND_METHODOLOGY
EXPERIMENT_AUTHORIZATION = NONE
```

## Source integrity note

The historical repository is intentionally read-only and was already dirty.
The tracked gate-input HEAD is the expected
`ae77f91bb8baad5f77da1278abb1a20272660417`. VRAA M4 lives in untracked
historical paths but carries a frozen 48-file source bundle with aggregate
SHA-256
`8d7e58e00679051d1676fa28f1affc4f1f9d09018460c42baaf215e2a134157b`.
Exact file hashes used here are recorded in `d0_source_manifest.json`.
Only the entries marked `tracked_at_source_head` are retrievable from a clean
historical clone. The trace and VRAA entries are external local artifacts; the
recorded hashes verify the inspected copies but do not make those files
available from Git alone.
