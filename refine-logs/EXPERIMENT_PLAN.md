# Experiment Plan

**Problem**: Computation-reuse claims in LLM agent workflows are often made
without native evidence that the relevant artifact was accessed, execution was
actually skipped, validation was economical, or an outcome difference was
caused by reuse.

**Method thesis**: Qualify the evidence before evaluating reuse: separate
delivery/access, actual skip, verifier cost, and outcome attribution, and
report only the strongest claim supported by native runtime records.

**Date**: 2026-07-22

**Current authorization**: design and CPU-only static audit; zero model calls,
zero GPU runs, zero new trajectories.

## Claim map

| Claim | Why it matters | Minimum convincing evidence | Linked blocks |
|---|---|---|---|
| C1. The evidence ladder prevents unsupported selective-consumption claims. | Final-text proxies cannot identify native delivery/read structure. | Frozen protocol; pinned source locators; CODE_ONLY/TRACE_CONFIRMED separation; parser tests; bounded wording. | B1, B3 |
| C2. Reuse economics must separate actual skips, verifier cost, and post-hoc attribution. | A nominal cache hit or successful final output does not establish net benefit or reuse-caused damage. | C3 v2.1 reanalysis; full-run cost denominator; task-native outcome oracle; actual execution bits; paired baseline labels kept post-hoc. | B2, B4 |

### Anti-claims to rule out

- The paper proposes a novel response or tool cache.
- A single-agent exact-replay study satisfies Q2/Q3 selective consumption.
- A task test suite is a runtime directed verifier for reuse damage.
- The three audited repositories establish an ecosystem-wide absence result.

## Paper storyline

Main paper must prove:

1. why final-text usage/equivalence proxies fail the identifiability test;
2. how the evidence ladder changes which claims are admissible;
3. what the bounded framework audit supports and does not support;
4. why verifier cost and attribution change the economics of reuse.

Appendix can support:

- complete source locator tables and manifests;
- C3 v2.1 correction details;
- a design-only actual-skip calibration protocol;
- a later controlled calibration only if separately authorized and completed.

Experiments intentionally cut:

- new C6 framework search beyond the frozen universe;
- semantic/text usage proxies;
- arbitrary-shell dependency tracking;
- SWE-bench-scale mutation campaigns;
- any mechanism comparison claiming exact caching as novel.

## Experiment blocks

### Block B1: Evidence-ladder application

- **Claim tested**: C1.
- **Why this block exists**: demonstrates that the rubric produces auditable,
  conservative classifications rather than retrospective semantic judgments.
- **Dataset / split / task**: frozen AutoGen, LangGraph, and SWE-agent source
  snapshots and located public artifacts.
- **Compared systems**: no performance comparison; compare admissible evidence
  types Q0–Q3/QX under one frozen rubric.
- **Metrics**: Q level, CODE_ONLY/TRACE_CONFIRMED, producer/consumer counts,
  raw bypass, trace instance count, locator coverage.
- **Setup details**: existing CPU-only parser and source manifests.
- **Success criterion**: every classification reconstructs from raw locators
  and frozen rules without text heuristics.
- **Failure interpretation**: unresolved locator conflict downgrades evidence;
  it never upgrades a candidate.
- **Table / figure target**: main-paper evidence ladder and three-framework
  result matrix.
- **Priority**: MUST-RUN; completed evidence, integration still required.

### Block B2: Verifier-aware economics

- **Claim tested**: C2.
- **Why this block exists**: separates nominal saving from validation cost and
  distinguishes outcome failure from reuse-attributable damage.
- **Dataset / split / task**: frozen C3 traces plus fixture-level focused tests.
- **Compared systems**: naive outcome verifier and hypothetical directed
  verifier as labeled conditional analyses.
- **Metrics**: skip fraction, verifier/full-run cost fraction, `rho_outcome`,
  post-hoc `rho_blame`, rescue, remaining error, net-saving sign.
- **Setup details**: v2 results preserved; v2.1 non-verdict correction applied.
- **Success criterion**: all quantities reproduce from the declared source
  inputs and no post-hoc variable is described as runtime executable.
- **Failure interpretation**: missing raw inputs restrict reproducibility to
  code paths, fixtures, and invariants.
- **Table / figure target**: main-paper conditional cost map.
- **Priority**: MUST-RUN; completed evidence, integration still required.

### Block B3: Static actual-skip eligibility audit

- **Claim tested**: whether B4 is a non-tautological evaluation of C2.
- **Why this block exists**: exact replay under state change is meaningful only
  if explicit invocation identity can remain fixed while native relevant state
  changes.
- **Dataset / split / task**: existing HumanEvalFix source, schemas, and recorded
  artifacts; no new execution.
- **Compared systems**: explicit invocation bytes versus separately identified
  environment state for each native workflow node.
- **Metrics**: eligible invocation count, stable identity coverage, actual-skip
  field availability, task-oracle availability, model/tool calls per arm.
- **Setup details**: read-only source audit and a call-budget derivation.
- **Success criterion**: at least one native invocation passes every D0
  qualification rule in the preregistration.
- **Failure interpretation**: stop B4 and keep the paper on the measurement
  route; do not manufacture an eligible path.
- **Table / figure target**: appendix qualification table or a concise no-go
  limitation.
- **Priority**: MUST-RUN before requesting any model calls; **completed with
  `INELIGIBLE_AS_PROPOSED`**. The native four-node workflow, full source/test
  prompts, missing tool-result consumer path, and undercounted call budget
  trigger the stop rule.

### Block B4: Outcome-grounded actual-skip calibration — cut after B3

- **Claim tested**: C2, in one bounded setting.
- **Why this block existed**: it would have provided an example of actual-skip
  and outcome measurement, not a positive Q2/Q3 selective-consumption example.
- **Dataset / split / task**: task IDs and state variable to be frozen only if
  B3 passes. HumanEvalFix has prior project exposure, so no split is called
  fresh or untouched.
- **Compared systems**: paired from-scratch, response replay, validated tool
  replay, and combined replay arms.
- **Metrics**: model/tool invocations actually skipped, full-run and validator
  cost, outcome agreement, false accepts, task success, post-hoc attribution.
- **Setup details**: defined in
  `experiments/actual_skip_calibration/preregistration.md`.
- **Success criterion**: the harness passes identity controls and yields
  interpretable paired measurements; positive net saving is not required.
- **Failure interpretation**: distinguish harness failure, eligibility failure,
  zero saving, and outcome disagreement.
- **Table / figure target**: optional main-paper calibration table; otherwise
  appendix or omitted.
- **Priority**: CUT for the proposed HumanEvalFix route. It is not blocked on
  compute; B3 found the testbed scientifically ineligible as written.

### Block B5: Failure and scope analysis

- **Claim tested**: anti-claims and boundary discipline.
- **Why this block exists**: prevents a measurement paper from drifting into a
  postmortem, ecosystem-wide claim, or ordinary-cache mechanism paper.
- **Dataset / split / task**: frozen negative dossier, Fable 5 review, and owner
  disposition.
- **Compared systems**: claimed evidence strength versus actually available
  evidence.
- **Metrics**: unsupported-claim count in the final claim/evidence matrix.
- **Setup details**: independent final review before submission.
- **Success criterion**: zero unsupported core claims.
- **Failure interpretation**: downgrade or delete the claim; do not add an
  experiment to rescue wording.
- **Table / figure target**: limitations and reproducibility sections.
- **Priority**: MUST-RUN during manuscript review.

## Run order and milestones

| Milestone | Goal | Runs | Decision gate | Cost | Risk |
|---|---|---|---|---|---|
| M0 | Package existing evidence | B1/B2 integration checks | All core numbers trace to frozen artifacts | CPU only; 0 model calls | Missing external raw files limit end-to-end reproduction |
| M1 | Decide whether calibration is scientifically expressible | B3 static audit | `INELIGIBLE_AS_PROPOSED` | CPU only; 0 model calls | Completed: native workflow fails the testbed condition |
| M2 | Freeze conditional execution | None for this route | STOPPED | 0 | A new harness would be a different testbed |
| M3 | Small smoke | None | STOPPED | 0 | No execution authorization |
| M4 | Pilot/confirmation | None | STOPPED | 0 | No execution authorization |
| M5 | Final claim audit | B5 | Zero unsupported core claims | CPU only | Deadline pressure encourages overclaiming |

## Compute and data budget

- Current model/API calls: 0 authorized, 0 executed in this stage.
- Current GPU-hours: 0 authorized, 0 executed.
- Current new trajectories: 0 authorized, 0 executed.
- D0 data preparation: read-only inspection of existing source and recorded
  artifacts.
- Future budget: none for the stopped HumanEvalFix route. The audit found 1,968
  was a condition-cell count. Under the stated identity-only-hit and
  two-calls-per-cell assumptions, the optimistic unimplemented two-stage count
  is 3,280 model calls; the native four-node design starts at 7,872 before hits.
- Human evaluation: none.
- Biggest bottleneck: identifying a native state change that preserves the
  complete explicit invocation while retaining an outcome oracle.

## Risks and mitigations

- **Risk: exact-replay experiment is tautological.**

  **Mitigation:** D0 hard stop if state changes always change invocation bytes,
  or if a hit requires a weakened key.

- **Risk: ordinary cache is presented as novelty.**

  **Mitigation:** cache mechanics are an explicit anti-claim; B4 is only a
  measurement calibration.

- **Risk: outcome oracle is mistaken for directed verification.**

  **Mitigation:** use post-hoc labels only for analysis and keep C3 unchanged.

- **Risk: audit scope is generalized to an ecosystem.**

  **Mitigation:** repeat frozen candidate, commit, and artifact boundaries in
  every result statement.

- **Risk: apparent held-out evidence is not independent.**

  **Mitigation:** label any HumanEvalFix partition a preregistered execution
  split; the full benchmark has prior project exposure.

- **Risk: abstract commits to an unfinished experiment.**

  **Mitigation:** abstract commits to the measurement protocol, not an executed
  empirical section.

## Final checklist

- [x] Main paper claims are limited to two linked claims.
- [x] Novel cache/reuse mechanism is explicitly not claimed.
- [x] Conditional calibration is separated from existing evidence.
- [x] Final-text proxies are excluded from native-use evidence.
- [x] Nice-to-have execution is separated from must-run evidence integration.
- [x] B3 static qualification completed and independently checked; proposed
  testbed stopped as ineligible.
- [ ] Manuscript claim/evidence matrix contains no unsupported core claim.
- [ ] Any future model calls have a separate written authorization.
